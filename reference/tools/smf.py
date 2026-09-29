#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Alexander Nykolaiszyn and Semantic Management Framework contributors
"""Semantic Management Framework (SMF) reference CLI, spec v0.1.

Commands
  validate <path>                         Schema-validate SMF YAML files and check references
  resolve  <path> --term T [--context k=v ...]
                                          Resolve a term in context using the reference algorithm
  test     <path> [--results FILE]        Run TestCase documents. Term-based cases run against the
                                          reference resolver. Prompt-based cases need a consumer's
                                          results file (YAML mapping test id -> ResolutionResult).
  import-csv <csv> [--out FILE]           Convert a starter resolution table (CSV) into SMF YAML

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
ID_KINDS = {"Concept", "Context", "Perspective", "ClassificationRule", "MetricContract", "ResolutionRule",
            "Conflict", "TestCase", "ClaimTrace"}


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


def load_docs(path: Path):
    files = [path] if path.is_file() else sorted(
        p for p in path.rglob("*") if p.suffix in (".yaml", ".yml"))
    docs = []
    for f in files:
        with f.open(encoding="utf-8") as fh:
            for i, doc in enumerate(yaml.safe_load_all(fh)):
                if doc is None:
                    continue
                docs.append((f, i, _to_jsonable(doc)))
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
def refs_in(d):
    """Yield (field, ref) pairs for reference checks."""
    k = d.get("kind")
    get = d.get
    if k == "Term":
        yield "maps_to", get("maps_to")
        if get("context"):
            yield "context", get("context")
    elif k == "Concept":
        for r in get("relationships", []) or []:
            yield "relationships.object", r["object"]
        if get("replaced_by"):
            yield "replaced_by", get("replaced_by")
    elif k == "Ownership":
        yield "subject", get("subject")
    elif k == "ClassificationRule":
        yield "concept_ref", get("concept_ref")
    elif k == "Perspective":
        yield "concept_ref", get("concept_ref")
    elif k == "MetricContract":
        yield "measures.concept_ref", get("measures", {}).get("concept_ref")
        if get("perspective"):
            yield "perspective", get("perspective")
        comp = get("comparability") or {}
        for f in ("comparable_with", "not_comparable_with"):
            for r in comp.get(f, []) or []:
                yield f"comparability.{f}", r
        for r in get("classification_rules", []) or []:
            yield "classification_rules", r
        if get("variant_of"):
            yield "variant_of", get("variant_of")
    elif k == "Binding":
        yield "subject", get("subject")
    elif k == "ResolutionRule":
        dflt = get("default", {})
        for f in ("concept", "measurement"):
            if dflt.get(f):
                yield f"default.{f}", dflt[f]
        for o in dflt.get("options", []) or []:
            yield "default.options", o
        for c in get("contextual", []) or []:
            for f, v in (c.get("resolve_to") or {}).items():
                yield f"contextual.resolve_to.{f}", v
            for o in c.get("options", []) or []:
                yield "contextual.options", o
            if c.get("conflict_ref"):
                yield "contextual.conflict_ref", c["conflict_ref"]
        if get("deprecated"):
            yield "deprecated.replacement", get("deprecated")["replacement"]
    elif k == "Conflict":
        for c in get("candidates", []):
            yield "candidates", c
    elif k == "TestCase":
        e = get("expected", {})
        for f in ("concept", "measurement", "perspective"):
            if e.get(f):
                yield f"expected.{f}", e[f]
        for f in ("options", "must_not"):
            for o in e.get(f, []) or []:
                yield f"expected.{f}", o
    elif k == "ClaimTrace":
        yield "measurement", get("measurement")
        if get("concept"):
            yield "concept", get("concept")


def cmd_validate(args) -> int:
    docs = load_docs(Path(args.path))
    if not docs:
        print(f"No SMF YAML documents found under {args.path}")
        return 1
    schemas = load_schemas()
    errors, warnings = [], []
    seen = {}
    for f, i, d in docs:
        where = f"{f.relative_to(Path.cwd()) if f.is_relative_to(Path.cwd()) else f} #{i + 1}"
        if not isinstance(d, dict) or "kind" not in d:
            errors.append(f"{where}: missing 'kind'")
            continue
        kind = d["kind"]
        if kind not in schemas:
            errors.append(f"{where}: unknown kind '{kind}'")
            continue
        for e in sorted(schemas[kind].iter_errors(d), key=lambda e: list(e.path)):
            loc = "/".join(str(p) for p in e.path) or "(root)"
            errors.append(f"{where} [{kind}] {loc}: {e.message}")
        if kind in ID_KINDS and "id" in d:
            if d["id"] in seen:
                errors.append(f"{where}: duplicate id '{d['id']}' (first seen in {seen[d['id']]})")
            seen[d["id"]] = where
    idx = Index(docs)
    for f, i, d in docs:
        if not isinstance(d, dict):
            continue
        where = f"{f.name} #{i + 1}"
        for field, ref in refs_in(d):
            if ref and base_id(ref) not in idx.by_id:
                msg = f"{where} [{d.get('kind')}] {field}: '{ref}' is not defined in this set"
                (errors if args.strict else warnings).append(msg)
        if d.get("kind") == "ResolutionRule" and d["term"].strip().lower() not in idx.terms:
            warnings.append(f"{where} [ResolutionRule] term '{d['term']}' has no Term document")
    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    kinds = {}
    for _, _, d in docs:
        if isinstance(d, dict):
            kinds[d.get("kind")] = kinds.get(d.get("kind"), 0) + 1
    summary = ", ".join(f"{v} {k}" for k, v in sorted(kinds.items(), key=lambda kv: str(kv[0])))
    status = "FAILED" if errors else "OK"
    print(f"\n{status}: {len(docs)} documents ({summary}); {len(errors)} errors, {len(warnings)} warnings")
    return 1 if errors else 0


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


def _matches(when: dict, context: dict) -> bool:
    return all(str(context.get(k)) == str(v) for k, v in when.items())


def resolve(idx: Index, term: str, context: dict) -> dict:
    """Reference resolution algorithm (see spec/README.md §4)."""
    q = {"term": term, "context": context}
    rules = idx.rules.get(term.strip().lower(), [])
    if not rules:
        # Alias support: a Term that maps to a concept whose preferred term has a rule.
        for tdoc in idx.terms.get(term.strip().lower(), []):
            for other_term, tdocs in idx.terms.items():
                if other_term in idx.rules and any(d["maps_to"] == tdoc["maps_to"] for d in tdocs):
                    rules = idx.rules[other_term]
                    break
            if rules:
                break
    if not rules:
        return {"smf": SPEC_VERSION, "kind": "ResolutionResult", "query": q, "state": "UNGOVERNED"}
    rule = rules[0]
    basis = rule["id"]

    def finish(concept=None, measurement=None, state="RESOLVED", replaces=None):
        concept = concept or (idx.concept_for(measurement) if measurement else None)
        # Superseded concepts resolve to their replacement.
        cdoc = idx.by_id.get(base_id(concept)) if concept else None
        if state == "RESOLVED" and cdoc and cdoc.get("status") in ("superseded", "retired") and cdoc.get("replaced_by"):
            replaces, concept, state = concept, cdoc["replaced_by"], "RESOLVED_VIA_REPLACEMENT"
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
    idx = Index(load_docs(Path(args.path)))
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
    return problems


def cmd_test(args) -> int:
    idx = Index(load_docs(Path(args.path)))
    external = {}
    if args.results:
        with open(args.results, encoding="utf-8") as fh:
            external = _to_jsonable(yaml.safe_load(fh) or {})
    cases = [d for _, _, d in idx.docs if isinstance(d, dict) and d.get("kind") == "TestCase"]
    passed = failed = skipped = 0
    for c in cases:
        if c["id"] in external:
            actual, source = external[c["id"]], "consumer"
        elif c["input"].get("term"):
            actual, source = resolve(idx, c["input"]["term"], c["input"].get("context") or {}), "reference"
        else:
            skipped += 1
            print(f"SKIP  {c['id']:<34} prompt-based; supply consumer output with --results")
            continue
        probs = compare(c["expected"], actual)
        if probs:
            failed += 1
            print(f"FAIL  {c['id']:<34} [{source}] " + "; ".join(probs))
        else:
            passed += 1
            print(f"PASS  {c['id']:<34} [{source}] {actual.get('state')}")
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
        if r.get("concept") and r["concept"] not in concepts:
            concepts[r["concept"]] = r
    for cid, r in concepts.items():
        doc = {"smf": SPEC_VERSION, "kind": "Concept", "id": cid,
               "name": cid.split(".", 1)[-1].replace("_", " ").title(),
               "definition": r.get("definition") or "TODO: add definition", "status": "candidate"}
        out.append(doc)
        if r.get("owner"):
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
    r = sub.add_parser("resolve", help="resolve a term in context")
    r.add_argument("path")
    r.add_argument("--term", required=True)
    r.add_argument("--context", nargs="*", default=[], help="key=value pairs")
    t = sub.add_parser("test", help="run TestCase documents")
    t.add_argument("path")
    t.add_argument("--results", help="YAML mapping test id -> ResolutionResult from the consumer under test")
    c = sub.add_parser("import-csv", help="convert a starter resolution table")
    c.add_argument("csv")
    c.add_argument("--out")
    args = p.parse_args(argv)
    return {"validate": cmd_validate, "resolve": cmd_resolve, "test": cmd_test,
            "import-csv": cmd_import_csv}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
