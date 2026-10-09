# Changelog

## Unreleased

Proposed in #36, #37 and #39. Spec changes are additive: every new field is optional and existing documents validate unchanged.

### Added (reference tools and spec)
- `smf.py`: only SMF documents are read. A YAML or JSON file with no SMF document in it (a CI workflow, a tool's configuration, a data contract in another standard) is skipped and counted in the summary line, and folders whose name starts with a dot are not walked. A file that cannot be parsed is an error only when it has a top-level `smf:` line. A document that names an SMF `kind` and omits `smf:` is still an error. SMF documents can now sit at the root of a repository or beside the data contracts they are built on. (#36)
- `smf.py validate` and `test`: `--format json` prints one JSON object with the errors, warnings and counts. (#36)
- `reference/README.md`: "Where the files live", with a recommended layout. (#36)
- `metric-contract.schema.json`: optional `plain_words`, `inclusions`, `not_certified_for`, `change_note` and `sign_off {by, date}`, so every row of the one-page Metric Contract has a field. `concept.schema.json`: optional `plain_words`, `change_note` and `sign_off`, for the Definition Contract. The spec says "Maintained by" is `Ownership.steward`. (#37)
- Gross margin example: Service Gross Margin now carries its plain-words line, what it includes, what it is not approved for and its effective date, taken from `docs/metric-contract.md`. (#37)
- `binding.schema.json`: optional `id`. A duplicate is an error. (#39)
- `smf.py validate`: a claim's `execution.binding` must name a build record in the set, by `Binding` id or as `<platform>:<ref>`. No match is a warning, and an error in strict mode; a match that belongs to a different Metric Contract than the claim's is an error. Both examples validate unchanged. (#39)

### Changed (reference tools)
- `smf.py validate`: a missing path and an empty folder now end with the same summary line as any other failure.

### Added
- `docs/metamodel.md`: a model of the models. The four columns (data, meaning, analytics and AI, decision), a diagram of how data contracts, SMF documents, implementations and decisions connect, a table of every connection with the standard that records it, and the two ways to read it (audit trail of a decision; operating picture).
- `docs/gaps.md`: the gap catalogue. Thirty-odd named "connection that should exist and does not" cases, each with how it shows up, the practice that owns closing it, and a weight. Stated uses: work list, observed maturity reading, tool rendering rules, AI governance evidence.
- `reference/spec/README.md` "Relationships across standards": the field that records each connection in the metamodel, including the two recorded from the other end in ODCS (`authoritativeDefinitions`) and Apache Ossie (`custom_extensions`) and the OpenLineage run reference.
- Roadmap: the maturity model is now described as derived from closed gaps; a metamodel workbench (reads other standards' files, writes only SMF documents and patches, keeps no catalog of its own) is listed under Later.

## v0.5.0 (2026-10-08): Apache Ossie alignment and a contributor backlog

Minor bump because the spec gains two optional `Binding` fields. Existing documents validate unchanged. v0.4.8 and v0.4.9 were merged without tags; this release includes them.

### Added
- Contributor backlog: fourteen scoped issues, each one deliverable, under the labels `example`, `crosswalk`, `interop`, `prior-art` and `boundary-case`; `CONTRIBUTING.md` "Where to start" points at them.
- `docs/contracts-in-context.md`: "Working with interchange formats (Apache Ossie)", the Ossie counterpart to the ODCS section: what each side carries, two-way linking, the `ai_context` overlap, and what Ossie leaves out by design.
- `reference/spec/README.md`: non-normative field mapping between an Ossie metric and `MetricContract`, a linking convention (Ossie `custom_extensions` with `vendor_name: SMF` pointing at the contract; an SMF `Binding` with `platform: ossie` pointing back), and the spec source.
- `docs/research/landscape.md` and `bibliography.md`: findings sourced from the Ossie core spec (`0.2.0.dev0`, draft).
- Northwind example: an `untested` Ossie binding for Net Revenue, with an `expression_snapshot`.
- `binding.schema.json`: optional `implementation.derived_from` (the implementation a converter generated this one from) and `expression_snapshot` (the executable logic, or its SHA-256, as it was when conformance was last assessed). Both additive; existing bindings validate unchanged. `platform` now documents recommended values.
- Spec open question and roadmap: ask Apache Ossie for a native pointer to a governing definition, as ODCS has.

### Changed
- `docs/works-with.md`: the Ossie row now says how the two link, matching the ODCS row.

## v0.4.9 (2026-10-04): Code of conduct contact

### Changed
- `CODE_OF_CONDUCT.md`: concerns are reported through GitHub private reporting, replacing the placeholder contact.

## v0.4.8 (2026-10-04): Review fixes

### Fixed (reference tools and spec)
- `smf.py validate`: a second `ResolutionRule` for the same term, or two `Term` documents for the same term and context that map to different concepts, is now an error. The resolver returns `CONFLICT` instead of picking one by file order.
- `smf.py validate`: references must point at the right kind of document (a metric field must name a Metric Contract, and so on). `owner_ref` is now checked. Schema-invalid documents and YAML syntax errors are reported instead of crashing the validator.
- `smf.py resolve`: aliases are tried preferred-term first, never in file order, and rules for deprecated terms are skipped. A replacement that is itself superseded is followed to the current concept. A YAML boolean in a `when` clause now matches `--context key=true`.
- `smf.py test` and `resolve` stop with an error on a missing or empty path or on invalid documents.
- `smf.py test --results`: an id that matches no `TestCase` is an error, each result must be a valid `ResolutionResult`, and `must_apply` is now checked against the result's `constraints.exclusions`. The two sample results files are now full results.
- `smf.py import-csv`: a concept's definition and owner are now taken from the term's default row when that row names no concept. The shipped template round-trips.
- `smf.py` loads `.json` documents in folders, as the spec says it may.
- `resolution-rule.schema.json`: a `default` with `state: NEEDS_CLARIFICATION` now requires `options`, as `contextual` clauses already did.
- `requirements.txt`: added `rfc3339-validator` so `date-time` values are checked; `validate` warns if it is missing.
- `check-links.py`: skips code spans, and checks links with titles, reference-style links, HTML `href` and repeated-heading anchors.
- `site/build.py`: nested lists keep their levels. The home page no longer shows an edit link that 404s.

### Changed
- The context key in the starter answer table and both reference examples is now `business_area`, not `domain`, to match the vocabulary. Context keys are free-form; the spec now says so.
- Gross margin example: an `audience: external` context, answer rule and check resolve external reporting to the consolidated view, as the example page already said. The gross margin check count is now 7 passed, 0 failed, 1 skipped.
- `docs/metric-contract.md`: the Service Gross Margin example now matches its machine form (excludes, approved for).
- `docs/semantic-authority.md`: status is v0.4, seven objects, the seven roles from the vocabulary, the conflict outcomes from the practices page, and plain language in place of identifier blocks.
- `.github/workflows/validate.yml` now also runs the link check and `mkdocs build --strict`, and runs the checks on Python 3.9 and 3.12, matching the "Python 3.9+" claim in `smf.py`. `CONTRIBUTING.md`, the pull request template, `AGENTS.md` and `CLAUDE.md` list the same checks.
- `GOVERNANCE.md`: the spec version field is `smf:`, and the spec is in `reference/spec/`.

### Added
- `templates/answer-table.md`: a plain-language answer table template. `resolution-table.csv` stays as the file technical teams load into tools.
- Spec: rules for one answer rule per term, right-kind references, text matching of context values, and how `test` checks results.
- README repository map, `LICENSING.md` and `NOTICE` cover `site/`, `mkdocs.yml` and `prompts/`; `prompts/bootstrap-repo.md` is linked from `CONTRIBUTING.md`.

## v0.4.7 (2026-09-29): Website

### Added
- A browsable website built with MkDocs Material and published to GitHub Pages: `mkdocs.yml`, `site/` (home page, styles, build script, requirements) and `.github/workflows/pages.yml`.
- `.github/ISSUE_TEMPLATE/config.yml`: a "Questions and ideas → Discussions" link on the new-issue page.
- `site/build.py` assembles the website source so every relative link that works on GitHub also works on the site, and adjusts GitHub-style lists so they render the same.

### Changed
- `reference/tools/check-links.py`: skips `site/` and the website build folders.
- `docs/roles-and-artifacts.md` and `reference/README.md`: two folder links now point to a page (or to GitHub) so they work on the website.
- Home page browser-tab title no longer repeats the site name.

## v0.4.6 (2026-09-29): Wrap-up

### Changed
- `docs/semantic-authority.md`: the sample API block moved to `reference/examples/semantic-authority-examples.md` ("Sample API shape (optional)"), replaced by one plain sentence and a link.
- `docs/roadmap.md`: v0.4 through v0.4.5 summarized as one "Done" line; "this version" wording removed.
- `CLAUDE.md`: shortened. It defers to `AGENTS.md`, lists the local check commands and states the branch-and-pull-request workflow.

### Added
- `reference/tools/check-links.py`: checks that relative Markdown links and heading anchors resolve.

## v0.4.5 (2026-09-29): Plain language

### Changed
- `docs/semantic-authority.md`: the ten YAML examples moved to `reference/examples/semantic-authority-examples.md` and replaced with plain-language sentences and links. "Domain" replaced with "business area" where it was SMF's own term ("domain layer" is now "business-area layer"). The five technical state names replaced with the plain answers from the vocabulary.
- `docs/ai-governance-evidence.md`: schema names replaced with plain terms (ownership records, conflict records, context definitions, checks, claim traces).
- `docs/research-agenda.md`: "domain/context" reworded to "business area or context".
- Every non-normative page now carries the same `**Type:** Non-normative` line under its title, on its own line.
- `AGENTS.md`: added an exception under "Audience first" allowing `docs/research/` and `docs/patterns/` to name fields and schema identifiers when quoting a source or describing a technical pattern, provided they are labeled non-normative.

### Added
- `reference/examples/semantic-authority-examples.md`: illustrative YAML for each Semantic Authority object, with headings that match the practice page.

## v0.4.4 (2026-09-29): Consistency fixes

### Changed
- **Enterprise default** now applies only in the contexts an answer rule names (for example board and external reporting). It is not a fallback for company-wide questions; when context doesn't match a rule, ask. Wording aligned in vocabulary, practices, Semantic Authority, the Definition Contract template and the examples.
- **Consolidated Gross Margin** is recorded as broader than Product and Service. It is computed from totals, may define cost differently, and is reconciled by the Controller. None of the three is comparable with another as a margin. Updated in the gross margin example and its Metric Contracts.
- **Perspective is reframed as applied prior art**, not an SMF invention. "What SMF adds" in `works-with.md` now credits DDD, SBVR, Business Semantics Management and Egeria and links to the landscape research. The Apache Ossie row in `metric-contract.md` corrected to match the research.
- ODCS technical detail (linking example and field names) moved from `docs/` to `reference/spec/README.md`. Framework pages now describe it in plain language.
- "Proof" replaced with "evidence" in the framework's core question. "Domain" replaced with "business area" where it was SMF's own term.
- Non-normative type labels added to the gross margin example, research agenda and bibliography. Duplicate status line removed from the landscape research.
- Framework overview no longer says every practice has three size forms; a few, like Interchange, are usually only needed at larger scale.

### Added
- Vocabulary entries for the seven roles, Build record and Change note.
- Optional `broader_than` field on the Perspective schema, checked as a reference by the validator, and set on the consolidated perspective in the gross margin example.
- `not_comparable_with` on the consolidated Metric Contract in the gross margin example.

## v0.4.3 (2026-09-29)
- Repository moved to github.com/Semantic-Management/framework; links added to README and CONTRIBUTING.
- CI job renamed to `checks`.

## v0.4.2 (2026-09-28): Licensing

### Added
- `LICENSE` (Apache-2.0, for `reference/`), `LICENSE-docs` (CC BY 4.0, for the framework, docs and templates), `NOTICE`, and `LICENSING.md` explaining which applies where.
- SPDX identifiers on reference code, schemas and examples.

### Removed
- `LICENSE-TODO.md`.

## v0.4.1 (2026-09-28): Contracts in context

### Added
- `docs/contracts-in-context.md`: how SMF contracts sit alongside data contracts (ODCS) and metric catalogs; "one place computes, one place agrees"; ODCS `authoritativeDefinitions` linking example.
- **Semantic Contract** as the umbrella term; **Definition Contract** for business terms that aren't numbers, with a one-page template.
- `additivity` and `built_on` fields on Metric Contracts (template and reference schema).

### Changed
- Metric Contract template reorganized around commonly used field names (expression, grain, filters, time semantics, allowed dimensions, additivity, owner, certification, version), plus SMF's additions (perspective, approved uses, comparability).

## v0.4 (2026-09-28): Semantic Management, business-first

### Changed
- Name returned to **Semantic Management Framework (SMF)**, positioned as the missing discipline for business meaning alongside ITSM, DAMA, TOGAF, COBIT, MDM, model risk management and AI governance.
- README and framework docs rewritten for business and analytics leaders.
- Headline principle: **Two things can be true**, with **Context selects the perspective; when it can't, ask**.
- Flagship example changed from revenue to **gross margin** (product, service and consolidated perspectives).
- Practices rewritten in plain language with small / mid-size / enterprise forms.
- Resolution states presented as **the five answers**: use it, use the replacement, ask, flag the conflict, not governed.
- All technical material moved to `reference/` (spec, schemas, examples, CLI renamed `smf.py`; envelope field `smf:`).

### Added
- `docs/discipline.md` (peer disciplines and hand-offs), `docs/vocabulary.md` (term, concept, **perspective**, context, Metric Contract), `docs/lifecycle.md`, `docs/metric-contract.md`, `docs/roles-and-artifacts.md`, `docs/getting-started.md`, `docs/works-with.md`, `docs/examples/gross-margin.md`.
- **Perspective** as a core term and a reference document kind; `perspective` and `comparability` on Metric Contracts.
- One-page Metric Contract template.
- Machine-readable gross margin example with checks; alias support in the reference resolver.

### Removed
- "Open Semantic Contracts" naming and contract-first framing (v0.3).
- `core.md`, `terminology.md`, `quickstart.md`, `builds-on.md` (replaced by vocabulary, getting-started and works-with).

## v0.3
- Open project files; machine-readable spec and CLI; LF AI & Data research.

## v0.2
- Practices made independently adoptable; five resolution states; classification rules assigned to meaning.

## v0.1
- Initial starter.
