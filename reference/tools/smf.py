#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Alexander Nykolaiszyn and Semantic Management Framework contributors
"""Semantic Management Framework (SMF) reference CLI, spec v0.1.

Commands
  validate <path> [--strict] [--format json]
                                          Schema-validate SMF YAML files and check references
  resolve  <path> --term T [--context k=v ...]
                                          Resolve a term in context using the reference algorithm
  test     <path> [--results FILE]        Run TestCase documents. Term-based cases run against the
                                          reference resolver. Prompt-based cases need a consumer's
                                          results file (YAML mapping test id -> ResolutionResult).
  import-csv <csv> [--out FILE]           Convert a starter resolution table (CSV) into SMF YAML

Only SMF documents are read. A file under <path> whose documents carry neither the `smf:` envelope
key nor an SMF `kind` (a CI workflow, a tool's configuration, a data contract in another standard)
is skipped and counted. Folders whose name starts with a dot are not walked.

Requires: Python 3.9+, PyYAML, jsonschema  (pip install -r reference/tools/requirements.txt)
This is a reference implementation for trying the spec, not a production service.
"""
from __future__ import annotations

import argparse
import csv
import datetime as _dt
import json
import sys
from pathlib import Path

try:
    import yaml
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError:  # pragma: no cover
    sys.exit("Missing dependencies. Run: pip install -r reference/tools/requirements.txt")

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_DIR = ROOT / "spec" / "schemas"
SPEC_VERSION = "0.1"
STATES = ["RESOLVED", "RESOLVED_VIA_REPLACEMENT", "NEEDS_CLARIFICATION", "CONFLICT", "UNGOVERNED"]

KIND_TO_SCHEMA = {
    "Concept": "concept",
    "Term": "term",
    "Context": "context",
    "Ownership": "ownership",
    "ClassificationRule": "classification-rule",
    "MetricContract": "metric-contract",
    "Binding": "binding",
    "ResolutionRule": "resolution-rule",
    "ResolutionResult": "resolution-result",
    "Conflict": "conflict",
    "Perspective": "perspective",
    "TestCase": "test-case",
    "ClaimTrace": "claim-trace",
}
# Binding is identified only when it carries the optional `id`.
ID_KINDS = {"Concept", "Context", "Perspective", "ClassificationRule", "MetricContract", "ResolutionRule",
            "Conflict", "TestCase", "ClaimTrace", "Binding"}


# --------------------------------------------------------------------------- loading
def _to_jsonable(obj):
    """YAML parses bare dates into date objects; schemas expect strings."""
    if isinstance(obj, dict):
        return {k: _to_jsonable(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_to_jsonable(v) for v in obj]
    if isinstance(obj, (_dt.date, _dt.datetime)):
        return obj.isoformat()
    return obj


def _looks_like_smf(doc) -> bool:
    """An SMF document carries the `smf:` envelope key. One that names an SMF kind and forgot the
    key still counts, so it is reported as an error and never skipped."""
    return isinstance(doc, dict) and ("smf" in doc or doc.get("kind") in KIND_TO_SCHEMA)


def _files_under(path: Path):
    """YAML and JSON files under path, in a stable order, leaving out folders whose name starts
    with a dot (.git, .github, .venv). A file given directly is always read."""
    if path.is_file():
        return [path]
    return sorted(p for p in path.rglob("*")
                  if p.is_file() and p.suffix in (".yaml", ".yml", ".json")
                  and not any(part.startswith(".") for part in p.relative_to(path).parts[:-1]))


def load_docs(path: Path, errors: list | None = None, skipped: list | None = None):
    """Load every SMF document under path. YAML syntax errors are appended to `errors` when a
    list is given; otherwise they stop the program with a clear message.

    A file with no SMF document in it belongs to something else (a workflow, a configuration file,
    a data contract in another standard): it is left out and appended to `skipped` when a list is
    given. A file with at least one SMF document is read whole, so a malformed document that sits
    beside valid ones is still reported."""
    docs = []
    for f in _files_under(path):
        try:
            with f.open(encoding="utf-8") as fh:
                found = [(f, i, _to_jsonable(doc)) for i, doc in enumerate(yaml.safe_load_all(fh))
                         if doc is not None]
        except yaml.YAMLError as e:
            msg = f"{f}: cannot parse: {str(e).splitlines()[0] if str(e) else type(e).__name__}"
            if errors is None:
                sys.exit(f"ERROR {msg}")
            errors.append(msg)
            continue
        if found and not path.is_file() and not any(_looks_like_smf(d) for _, _, d in found):
            if skipped is not None:
                skipped.append(f)
            continue
        docs.extend(found)
    return docs


def load_checked(path: Path):
    """Load a document set for `resolve` and `test`. Stops when the path has no documents or any
    document fails its schema, so a typo in a path or a malformed file can never read as a pass."""
    if not path.exists():
        sys.exit(f"ERROR path not found: {path}")
    docs = load_docs(path)
    if not docs:
        sys.exit(f"ERROR no SMF documents found under {path}")
    schemas = load_schemas()
    problems = _schema_problems(docs, schemas)
    if problems:
        for msg in problems:
            print(f"ERROR {msg}", file=sys.stderr)
        sys.exit("Fix the errors above first (run: smf.py validate <path>).")
    return docs


def load_schemas():
    schemas = {}
    for kind, name in KIND_TO_SCHEMA.items():
        with (SCHEMA_DIR / f"{name}.schema.json").open(encoding="utf-8") as fh:
            schemas[kind] = Draft202012Validator(json.load(fh), format_checker=FormatChecker())
    return schemas


def base_id(ref: str) -> str:
    return ref.split("@", 1)[0]


# --------------------------------------------------------------------------- index
class Index:
    def __init__(self, docs):
        self.by_id = {}
        self.terms = {}
        self.rules = {}
        self.docs = docs
        for _, _, d in docs:
            if not isinstance(d, dict):
                continue
            kind = d.get("kind")
            if kind in ID_KINDS and "id" in d:
                self.by_id[d["id"]] = d
            if kind == "Term":
                self.terms.setdefault(d["term"].strip().lower(), []).append(d)
            if kind == "ResolutionRule":
                self.rules.setdefault(d["term"].strip().lower(), []).append(d)

    def kind_of(self, ref):
        d = self.by_id.get(base_id(ref))
        return d.get("kind") if d else None

    def concept_for(self, ref):
        """Return the concept ID for a concept or metric reference."""
        d = self.by_id.get(base_id(ref))
        if not d:
            return None
        if d["kind"] == "Concept":
            return d["id"]
        if d["kind"] == "MetricContract":
            return d["measures"]["concept_ref"]
        return None


# --------------------------------------------------------------------------- validate
CONCEPT = {"Concept"}
MEASURE = {"MetricContract"}
CONCEPT_OR_MEASURE = {"Concept", "MetricContract"}


def refs_in(d):
    """Yield (field, ref, kinds) triples for reference checks. `kinds` is the set of document
    kinds the field may point at, or None when any identified document is acceptable."""
    k = d.get("kind")
    get = d.get
    if k == "Term":
        yield "maps_to", get("maps_to"), CONCEPT
        if get("context"):
            yield "context", get("context"), {"Context"}
    elif k == "Concept":
        for r in get("relationships", []) or []:
            yield "relationships.object", r["object"], CONCEPT
        if get("replaced_by"):
            yield "replaced_by", get("replaced_by"), CONCEPT
    elif k == "Ownership":
        yield "subject", get("subject"), None
    elif k == "ClassificationRule":
        yield "concept_ref", get("concept_ref"), CONCEPT
    elif k == "Perspective":
        yield "concept_ref", get("concept_ref"), CONCEPT
        for r in get("broader_than", []) or []:
            yield "broader_than", r, {"Perspective"}
    elif k == "MetricContract":
        yield "measures.concept_ref", get("measures", {}).get("concept_ref"), CONCEPT
        if get("perspective"):
            yield "perspective", get("perspective"), {"Perspective"}
        comp = get("comparability") or {}
        for f in ("comparable_with", "not_comparable_with"):
            for r in comp.get(f, []) or []:
                yield f"comparability.{f}", r, MEASURE
        for r in get("classification_rules", []) or []:
            yield "classification_rules", r, {"ClassificationRule"}
        if get("variant_of"):
            yield "variant_of", get("variant_of"), MEASURE
    elif k == "Binding":
        yield "subject", get("subject"), None
    elif k == "ResolutionRule":
        if get("owner_ref"):
            yield "owner_ref", get("owner_ref"), None
        dflt = get("default", {})
        if dflt.get("concept"):
            yield "default.concept", dflt["concept"], CONCEPT
        if dflt.get("measurement"):
            yield "default.measurement", dflt["measurement"], MEASURE
        for o in dflt.get("options", []) or []:
            yield "default.options", o, CONCEPT_OR_MEASURE
        for c in get("contextual", []) or []:
            rt = c.get("resolve_to") or {}
            if rt.get("concept"):
                yield "contextual.resolve_to.concept", rt["concept"], CONCEPT
            if rt.get("measurement"):
                yield "contextual.resolve_to.measurement", rt["measurement"], MEASURE
            for o in c.get("options", []) or []:
                yield "contextual.options", o, CONCEPT_OR_MEASURE
            if c.get("conflict_ref"):
                yield "contextual.conflict_ref", c["conflict_ref"], {"Conflict"}
        if get("deprecated"):
            yield "deprecated.replacement", get("deprecated")["replacement"], CONCEPT_OR_MEASURE
    elif k == "Conflict":
        for c in get("candidates", []):
            yield "candidates", c, {"Concept", "MetricContract", "Perspective"}
    elif k == "TestCase":
        e = get("expected", {})
        if e.get("concept"):
            yield "expected.concept", e["concept"], CONCEPT
        if e.get("measurement"):
            yield "expected.measurement", e["measurement"], MEASURE
        if e.get("perspective"):
            yield "expected.perspective", e["perspective"], {"Perspective"}
        for f in ("options", "must_not"):
            for o in e.get(f, []) or []:
                yield f"expected.{f}", o, CONCEPT_OR_MEASURE
    elif k == "ClaimTrace":
        yield "measurement", get("measurement"), MEASURE
        if get("concept"):
            yield "concept", get("concept"), CONCEPT


def _schema_problems(docs, schemas):
    """Return schema error messages for every document (missing kind, unknown kind, schema errors)."""
    out = []
    for f, i, d in docs:
        where = _where(f, i)
        if not isinstance(d, dict) or "kind" not in d:
            out.append(f"{where}: missing 'kind'")
        elif d["kind"] not in schemas:
            out.append(f"{where}: unknown kind '{d['kind']}'")
        else:
            for e in sorted(schemas[d["kind"]].iter_errors(d), key=lambda e: list(e.path)):
                loc = "/".join(str(p) for p in e.path) or "(root)"
                out.append(f"{where} [{d['kind']}] {loc}: {e.message}")
    return out


def _where(f, i):
    try:
        shown = f.relative_to(Path.cwd())
    except ValueError:
        shown = f
    return f"{shown} #{i + 1}"


def _binding_names(d) -> set:
    """The names a ClaimTrace may use for a Binding: its id, and '<platform>:<ref>'."""
    impl = d.get("implementation") or {}
    names = {f"{impl.get('platform')}:{impl.get('ref')}"}
    if d.get("id"):
        names.add(d["id"])
    return names


def _report_validate(args, path, docs, skipped, errors, warnings) -> int:
    """Print the outcome of `validate` as text or, with --format json, as one JSON object."""
    kinds = {}
    for _, _, d in docs:
        if isinstance(d, dict):
            kinds[str(d.get("kind"))] = kinds.get(str(d.get("kind")), 0) + 1
    status = "FAILED" if errors else "OK"
    if getattr(args, "format", "text") == "json":
        print(json.dumps({"command": "validate", "path": str(path), "strict": bool(args.strict),
                          "status": status, "documents": len(docs), "kinds": dict(sorted(kinds.items())),
                          "skipped_files": [str(f) for f in skipped],
                          "errors": errors, "warnings": warnings}, indent=2))
        return 1 if errors else 0
    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    summary = ", ".join(f"{v} {k}" for k, v in sorted(kinds.items()))
    note = f"; skipped {len(skipped)} file(s) that are not SMF documents" if skipped else ""
    print(f"\n{status}: {len(docs)} documents ({summary}); {len(errors)} errors, {len(warnings)} warnings{note}")
    return 1 if errors else 0


def cmd_validate(args) -> int:
    errors, warnings, skipped = [], [], []
    if not Path(args.path).exists():
        errors.append(f"path not found: {args.path}")
        return _report_validate(args, args.path, [], skipped, errors, warnings)
    docs = load_docs(Path(args.path), errors, skipped)
    if not docs and not errors:
        note = f" ({len(skipped)} file(s) skipped: not SMF documents)" if skipped else ""
        errors.append(f"no SMF documents found under {args.path}{note}")
        return _report_validate(args, args.path, [], skipped, errors, warnings)
    schemas = load_schemas()
    if "date-time" not in FormatChecker().checkers:
        warnings.append("the 'date-time' format is not being checked; install rfc3339-validator "
                        "(pip install -r reference/tools/requirements.txt)")
    # Documents that fail their schema are reported and then left out of the reference checks,
    # so one malformed file never hides (or crashes) the checks on the rest.
    errors.extend(_schema_problems(docs, schemas))
    valid = [(f, i, d) for f, i, d in docs
             if isinstance(d, dict) and d.get("kind") in schemas
             and not any(True for _ in schemas[d["kind"]].iter_errors(d))]
    seen = {}
    for f, i, d in valid:
        if d["kind"] in ID_KINDS and "id" in d:
            where = _where(f, i)
            if d["id"] in seen:
                errors.append(f"{where}: duplicate id '{d['id']}' (first seen in {seen[d['id']]})")
            seen[d["id"]] = where
    idx = Index(valid)
    rule_files = {}
    term_groups = {}
    for f, i, d in valid:
        if d["kind"] == "ResolutionRule":
            rule_files.setdefault(d["term"].strip().lower(), []).append((d["id"], f.name))
        if d["kind"] == "Term":
            key = (d["term"].strip().lower(), d.get("context"))
            term_groups.setdefault(key, []).append((d["maps_to"], f.name))
    for term, items in sorted(rule_files.items()):
        if len(items) > 1:
            listed = ", ".join(f"{rid} ({fn})" for rid, fn in items)
            errors.append(f"term '{term}' has more than one ResolutionRule: {listed}")
    for (term, ctx), items in sorted(term_groups.items(), key=lambda kv: (kv[0][0], str(kv[0][1]))):
        if len(items) > 1:
            where_ctx = f" in context {ctx}" if ctx else ""
            targets = {m for m, _ in items}
            listed = ", ".join(f"{m} ({fn})" for m, fn in items)
            if len(targets) > 1:
                errors.append(f"term '{term}'{where_ctx} maps to more than one concept: {listed}")
            else:
                warnings.append(f"term '{term}'{where_ctx} is defined more than once: {listed}")
    for f, i, d in valid:
        where = f"{f.name} #{i + 1}"
        for field, ref, kinds in refs_in(d):
            if not ref:
                continue
            actual = idx.kind_of(ref)
            if base_id(ref) not in idx.by_id:
                msg = f"{where} [{d.get('kind')}] {field}: '{ref}' is not defined in this set"
                (errors if args.strict else warnings).append(msg)
            elif kinds and actual not in kinds:
                want = " or ".join(sorted(kinds))
                errors.append(f"{where} [{d.get('kind')}] {field}: '{ref}' is a {actual}, but a {want} is required")
        if d.get("kind") == "ResolutionRule" and d["term"].strip().lower() not in idx.terms:
            warnings.append(f"{where} [ResolutionRule] term '{d['term']}' has no Term document")
    # A claim names the build record that computed it, by Binding id or as '<platform>:<ref>'.
    bindings = [d for _, _, d in valid if d["kind"] == "Binding"]
    for f, i, d in valid:
        named = (d.get("execution") or {}).get("binding") if d["kind"] == "ClaimTrace" else None
        if not named:
            continue
        where = f"{f.name} #{i + 1}"
        matches = [b for b in bindings if named in _binding_names(b)]
        if not matches:
            msg = (f"{where} [ClaimTrace] execution.binding: '{named}' matches no Binding in this set "
                   f"(use a Binding id or '<platform>:<ref>')")
            (errors if args.strict else warnings).append(msg)
        elif not any(base_id(b["subject"]) == base_id(d["measurement"])
                     or idx.kind_of(b["subject"]) != "MetricContract" for b in matches):
            # A build recorded against a concept (not a contract) cannot contradict the claim.
            subjects = ", ".join(sorted({b["subject"] for b in matches}))
            errors.append(f"{where} [ClaimTrace] execution.binding: '{named}' is a build of {subjects}, "
                          f"but the claim is backed by {d['measurement']}")
    return _report_validate(args, args.path, docs, skipped, errors, warnings)


# --------------------------------------------------------------------------- resolve
def _trust(idx: Index, concept, measurement):
    t = {}
    c = idx.by_id.get(base_id(concept)) if concept else None
    if c and c.get("status"):
        t["registration_status"] = c["status"]
    m = idx.by_id.get(base_id(measurement)) if measurement else None
    if m and m.get("certified_for"):
        t["certified_for"] = m["certified_for"]
    return t


def _constraints(idx: Index, measurement):
    m = idx.by_id.get(base_id(measurement)) if measurement else None
    if not m:
        return None
    c = {k: m[k] for k in ("exclusions", "valid_dimensions", "time_semantics", "grain") if m.get(k)}
    return c or None


def _text(v) -> str:
    """Context values are compared as text. YAML booleans become 'true' / 'false' so that a rule
    written `is_board: true` matches `--context is_board=true`. Comparison is case-sensitive."""
    if isinstance(v, bool):
        return "true" if v else "false"
    return str(v)


def _matches(when: dict, context: dict) -> bool:
    return all(k in context and _text(context[k]) == _text(v) for k, v in when.items())


def _rules_for(idx: Index, term: str):
    """Return the ResolutionRule documents for a term, following aliases.

    An alias is a Term that maps to a concept whose preferred term has a rule. Candidates are taken
    in a fixed order (preferred terms first, then alphabetical), never in file order, and rules for
    deprecated terms are skipped so a plain alias is never reported as a deprecated term.
    """
    key = term.strip().lower()
    if key in idx.rules:
        return idx.rules[key]
    concepts = {base_id(d["maps_to"]) for d in idx.terms.get(key, [])}
    if not concepts:
        return []
    cands = []
    for other, tdocs in idx.terms.items():
        if other == key or other not in idx.rules:
            continue
        if any(r.get("deprecated") for r in idx.rules[other]):
            continue
        live = [d for d in tdocs if not d.get("deprecated") and base_id(d["maps_to"]) in concepts]
        if live:
            cands.append((not any(d.get("preferred") for d in live), other))
    return idx.rules[min(cands)[1]] if cands else []


def resolve(idx: Index, term: str, context: dict) -> dict:
    """Reference resolution algorithm (see spec/README.md §4)."""
    q = {"term": term, "context": context}
    rules = _rules_for(idx, term)
    if not rules:
        return {"smf": SPEC_VERSION, "kind": "ResolutionResult", "query": q, "state": "UNGOVERNED"}
    if len(rules) > 1:
        # Two answer rules for one term is a governance fault. Never pick one by file order.
        ids = sorted(r["id"] for r in rules)
        return {"smf": SPEC_VERSION, "kind": "ResolutionResult", "query": q, "state": "CONFLICT",
                "basis": ids[0],
                "conflict_owner": f"unassigned (more than one answer rule for this term: {', '.join(ids)})"}
    rule = rules[0]
    basis = rule["id"]

    def finish(concept=None, measurement=None, state="RESOLVED", replaces=None):
        concept = concept or (idx.concept_for(measurement) if measurement else None)
        # Superseded concepts resolve to their replacement.
        # (and follow the chain when a replacement is itself superseded).
        cdoc = idx.by_id.get(base_id(concept)) if concept else None
        seen_ids = set()
        while (state in ("RESOLVED", "RESOLVED_VIA_REPLACEMENT") and cdoc
               and cdoc.get("status") in ("superseded", "retired") and cdoc.get("replaced_by")
               and cdoc["id"] not in seen_ids):
            seen_ids.add(cdoc["id"])
            replaces = replaces or concept
            concept, state = cdoc["replaced_by"], "RESOLVED_VIA_REPLACEMENT"
            cdoc = idx.by_id.get(base_id(concept))
        r = {"smf": SPEC_VERSION, "kind": "ResolutionResult", "query": q, "state": state,
             "concept": concept, "basis": basis}
        if measurement:
            r["measurement"] = measurement
            mdoc = idx.by_id.get(base_id(measurement)) or {}
            if mdoc.get("perspective"):
                r["perspective"] = mdoc["perspective"]
        if replaces:
            r["replaces"] = replaces
        cons = _constraints(idx, measurement)
        if cons:
            r["constraints"] = cons
        trust = _trust(idx, concept, measurement)
        if trust:
            r["trust"] = trust
        return r

    # 1. Deprecated terms resolve to their governed replacement.
    if rule.get("deprecated"):
        rep = rule["deprecated"]["replacement"]
        kind = idx.kind_of(rep)
        if kind == "MetricContract":
            return finish(measurement=rep, state="RESOLVED_VIA_REPLACEMENT", replaces=term)
        return finish(concept=rep, state="RESOLVED_VIA_REPLACEMENT", replaces=term)

    # 2. Contextual clauses: the most specific match wins; a tie with different outcomes is a CONFLICT.
    matched = [c for c in rule.get("contextual", []) or [] if _matches(c["when"], context)]
    if matched:
        best = max(len(c["when"]) for c in matched)
        top = [c for c in matched if len(c["when"]) == best]
        outcomes = {json.dumps({k: v for k, v in c.items() if k not in ("when", "prompt")}, sort_keys=True) for c in top}
        if len(outcomes) > 1:
            return {"smf": SPEC_VERSION, "kind": "ResolutionResult", "query": q, "state": "CONFLICT",
                    "basis": basis, "conflict_owner": "unassigned (equally specific rules disagree)"}
        c = top[0]
        if "resolve_to" in c:
            rt = c["resolve_to"]
            return finish(concept=rt.get("concept"), measurement=rt.get("measurement"))
        state = c["state"]
        r = {"smf": SPEC_VERSION, "kind": "ResolutionResult", "query": q, "state": state, "basis": basis}
        if state == "NEEDS_CLARIFICATION":
            r["options"] = c["options"]
        if state == "CONFLICT":
            ref = c.get("conflict_ref")
            if ref:
                r["conflict_ref"] = ref
                owner = (idx.by_id.get(ref) or {}).get("owner")
                if owner:
                    r["conflict_owner"] = owner
            else:
                r["conflict_owner"] = "unassigned"
        return r

    # 3. Default.
    d = rule["default"]
    if d.get("state"):
        r = {"smf": SPEC_VERSION, "kind": "ResolutionResult", "query": q, "state": d["state"], "basis": basis}
        if d.get("options"):
            r["options"] = d["options"]
        return r
    return finish(concept=d.get("concept"), measurement=d.get("measurement"))


def parse_context(pairs):
    ctx = {}
    for p in pairs or []:
        if "=" not in p:
            sys.exit(f"Bad --context '{p}'. Use key=value.")
        k, v = p.split("=", 1)
        ctx[k.strip()] = v.strip()
    return ctx


def cmd_resolve(args) -> int:
    idx = Index(load_checked(Path(args.path)))
    result = resolve(idx, args.term, parse_context(args.context))
    errs = list(load_schemas()["ResolutionResult"].iter_errors(result))
    print(yaml.safe_dump(result, sort_keys=False).rstrip())
    if errs:
        print(f"\n# WARNING: result does not validate: {errs[0].message}", file=sys.stderr)
        return 1
    return 0


# --------------------------------------------------------------------------- test
def compare(expected: dict, actual: dict):
    problems = []
    if actual.get("state") != expected["state"]:
        problems.append(f"state {actual.get('state')} != expected {expected['state']}")
    for f in ("concept", "measurement", "perspective"):
        if expected.get(f) and base_id(actual.get(f) or "") != base_id(expected[f]):
            problems.append(f"{f} {actual.get(f)} != expected {expected[f]}")
    if expected.get("options"):
        if set(map(base_id, actual.get("options") or [])) != set(map(base_id, expected["options"])):
            problems.append(f"options {actual.get('options')} != expected {expected['options']}")
    for bad in expected.get("must_not", []) or []:
        if base_id(actual.get("measurement") or "") == base_id(bad) or base_id(actual.get("concept") or "") == base_id(bad):
            problems.append(f"used forbidden {bad}")
    # must_apply names exclusions from the metric contract that the answer must carry.
    applied = {str(x) for x in ((actual.get("constraints") or {}).get("exclusions") or [])}
    for need in expected.get("must_apply", []) or []:
        if need not in applied:
            problems.append(f"constraint '{need}' not applied (constraints.exclusions: {sorted(applied) or 'none'})")
    return problems


def cmd_test(args) -> int:
    as_json = getattr(args, "format", "text") == "json"
    report = []

    def say(line):
        if not as_json:
            print(line)

    idx = Index(load_checked(Path(args.path)))
    external = {}
    if args.results:
        try:
            with open(args.results, encoding="utf-8") as fh:
                external = _to_jsonable(yaml.safe_load(fh) or {})
        except (OSError, yaml.YAMLError) as e:
            print(f"ERROR cannot read results file {args.results}: {e}")
            return 1
        if not isinstance(external, dict):
            print(f"ERROR {args.results}: expected a mapping of test id to ResolutionResult")
            return 1
    cases = [d for _, _, d in idx.docs if isinstance(d, dict) and d.get("kind") == "TestCase"]
    if not cases:
        print(f"ERROR no TestCase documents found under {args.path}")
        return 1
    unknown = sorted(set(external) - {c["id"] for c in cases})
    if unknown:
        print(f"ERROR {args.results}: ids that match no TestCase: {', '.join(map(str, unknown))}")
        return 1
    result_schema = load_schemas()["ResolutionResult"]
    passed = failed = skipped = 0
    for c in cases:
        if c["id"] in external:
            actual, source = external[c["id"]], "consumer"
            bad = sorted(result_schema.iter_errors(actual), key=lambda e: list(e.path)) if isinstance(actual, dict) else None
            if bad is None or bad:
                failed += 1
                why = "not a mapping" if bad is None else bad[0].message
                say(f"FAIL  {c['id']:<34} [{source}] result is not a valid ResolutionResult: {why}")
                report.append({"id": c["id"], "outcome": "failed", "source": source,
                               "problems": [f"result is not a valid ResolutionResult: {why}"]})
                continue
        elif c["input"].get("term"):
            actual, source = resolve(idx, c["input"]["term"], c["input"].get("context") or {}), "reference"
        else:
            skipped += 1
            say(f"SKIP  {c['id']:<34} prompt-based; supply consumer output with --results")
            report.append({"id": c["id"], "outcome": "skipped", "source": None,
                           "problems": ["prompt-based; supply consumer output with --results"]})
            continue
        probs = compare(c["expected"], actual)
        if probs:
            failed += 1
            say(f"FAIL  {c['id']:<34} [{source}] " + "; ".join(probs))
        else:
            passed += 1
            say(f"PASS  {c['id']:<34} [{source}] {actual.get('state')}")
        report.append({"id": c["id"], "outcome": "failed" if probs else "passed", "source": source,
                       "state": actual.get("state"), "problems": probs})
    if as_json:
        print(json.dumps({"command": "test", "path": str(args.path), "results": args.results,
                          "passed": passed, "failed": failed, "skipped": skipped, "cases": report}, indent=2))
    else:
        print(f"\n{passed} passed, {failed} failed, {skipped} skipped")
    return 1 if failed else 0


# --------------------------------------------------------------------------- import-csv
def _slug(s: str) -> str:
    out = "".join(ch if ch.isalnum() else "_" for ch in s.strip().lower())
    while "__" in out:
        out = out.replace("__", "_")
    return out.strip("_")


def cmd_import_csv(args) -> int:
    """CSV columns: term, context_key, context_value, concept, measurement, state, options, definition, owner.
    Rows with an empty context_key define the term's default. options are separated by '|'."""
    rows = list(csv.DictReader(open(args.csv, encoding="utf-8")))
    by_term, concepts, out = {}, {}, []
    for r in rows:
        term = r["term"].strip()
        if not term:
            continue
        by_term.setdefault(term, []).append(r)
    # A concept's definition and owner can sit on any row for it. A term's default row may carry
    # them even when it names no concept itself; they then belong to the term's main concept.
    for term, trs in by_term.items():
        default_rows = [r for r in trs if not r.get("context_key")]
        main = next((r["concept"] for r in default_rows if r.get("concept")), None) \
            or next((r["concept"] for r in trs if r.get("concept")), None)
        for r in default_rows + [x for x in trs if x not in default_rows]:
            cid = r.get("concept") or (main if not r.get("context_key") else None)
            if not cid:
                continue
            slot = concepts.setdefault(cid, {"definition": "", "owner": ""})
            slot["definition"] = slot["definition"] or (r.get("definition") or "").strip()
            slot["owner"] = slot["owner"] or (r.get("owner") or "").strip()
    for cid, r in concepts.items():
        doc = {"smf": SPEC_VERSION, "kind": "Concept", "id": cid,
               "name": cid.split(".", 1)[-1].replace("_", " ").title(),
               "definition": r["definition"] or "TODO: add definition", "status": "candidate"}
        out.append(doc)
        if r["owner"]:
            out.append({"smf": SPEC_VERSION, "kind": "Ownership", "subject": cid, "owner": r["owner"],
                        "scope": {"layer": "enterprise"}})
    for term, trs in by_term.items():
        default_rows = [r for r in trs if not r.get("context_key")]
        if not default_rows:
            sys.exit(f"Term '{term}' has no default row (empty context_key).")
        dr = default_rows[0]
        first = dr.get("concept") or next((r["concept"] for r in trs if r.get("concept")), None)
        out.append({"smf": SPEC_VERSION, "kind": "Term", "term": term, "maps_to": first or f"concept.{_slug(term)}"})

        def outcome(r):
            if r.get("state"):
                o = {"state": r["state"]}
                if r.get("options"):
                    o["options"] = [x.strip() for x in r["options"].split("|") if x.strip()]
                return o
            rt = {k: r[k] for k in ("concept", "measurement") if r.get(k)}
            return {"resolve_to": rt}

        dflt = outcome(dr)
        rule = {"smf": SPEC_VERSION, "kind": "ResolutionRule", "id": f"rule.term.{_slug(term)}", "term": term,
                "default": dflt.get("resolve_to") or {k: v for k, v in dflt.items()}}
        ctx = []
        for r in trs:
            if r.get("context_key"):
                c = {"when": {r["context_key"]: r["context_value"]}}
                c.update(outcome(r))
                ctx.append(c)
        if ctx:
            rule["contextual"] = ctx
        out.append(rule)
    text = yaml.safe_dump_all(out, sort_keys=False)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
        print(f"Wrote {len(out)} documents to {args.out}")
    else:
        print(text)
    return 0


# --------------------------------------------------------------------------- main
def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="smf", description="Semantic Management Framework reference CLI (spec v0.1)")
    sub = p.add_subparsers(dest="cmd", required=True)
    v = sub.add_parser("validate", help="validate SMF YAML")
    v.add_argument("path")
    v.add_argument("--strict", action="store_true", help="treat undefined references as errors")
    v.add_argument("--format", choices=["text", "json"], default="text", help="output format")
    r = sub.add_parser("resolve", help="resolve a term in context")
    r.add_argument("path")
    r.add_argument("--term", required=True)
    r.add_argument("--context", nargs="*", default=[], help="key=value pairs")
    t = sub.add_parser("test", help="run TestCase documents")
    t.add_argument("path")
    t.add_argument("--results", help="YAML mapping test id -> ResolutionResult from the consumer under test")
    t.add_argument("--format", choices=["text", "json"], default="text", help="output format")
    c = sub.add_parser("import-csv", help="convert a starter resolution table")
    c.add_argument("csv")
    c.add_argument("--out")
    args = p.parse_args(argv)
    return {"validate": cmd_validate, "resolve": cmd_resolve, "test": cmd_test,
            "import-csv": cmd_import_csv}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
