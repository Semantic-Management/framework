# Changelog

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
