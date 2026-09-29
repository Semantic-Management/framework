# Changelog

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
