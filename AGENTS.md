# AGENTS.md: Repository Instructions

## Mission
Develop the **Semantic Management Framework (SMF)**: the discipline and open operating model for managing **business meaning** across people, data, analytics and AI. It is a peer to ITSM, DAMA, TOGAF, COBIT, MDM, model risk management and AI governance.

## Audience first
The primary audience is **business and analytics leaders**. Framework documents (`docs/`, `README.md`) must stay in plain business language. Technical material (schemas, YAML, CLI, identifiers) belongs in `reference/`. If a framework page needs a technical detail, link to `reference/` rather than inlining it.

Exception: files in `docs/research/` and `docs/patterns/` may name fields and schema identifiers when quoting a source or describing a technical pattern, and must be labeled non-normative.

## Canonical ideas (do not dilute)
- **Two things can be true.** A term can legitimately mean different things to different parts of the business. Each legitimate meaning is a **perspective** with an owner.
- **Context selects the perspective. When context can't, ask.**
- **The five answers:** use it · use the replacement · ask · flag the conflict · not governed. Guessing is never an answer.
- **Meaning is separate from measurement.** Classification rules (what counts) belong to meaning.
- **Semantic Contracts** are the signature artifacts: the **Metric Contract** (numbers) and the **Definition Contract** (terms). Human one-pager first, machine form second. They include perspective and comparability.
- **Contracts in context:** data contracts (ODCS) describe datasets; metric catalogs compute; SMF contracts agree on meaning. "One place computes, one place agrees." Never position SMF contracts as replacing data contracts or metric catalogs.
- **Vocabulary:** term, concept, perspective, context, Metric Contract. Do not introduce "domain" as a core term.
- **Flagship example:** Gross Margin with product, service and consolidated perspectives.

## Structure
- Nine practices, each adoptable on its own, with small / mid-size / enterprise forms.
- A lifecycle of meaning (define → authority → resolve → measure → implement → exchange → consume → assure → evolve). It describes what happens to a meaning; it is not a required sequence.
- SMF works **with** other frameworks: together, separately, or as individual functions.
- Catalogs, semantic layers, metric stores, knowledge graphs, ontologies and governance platforms are **implementation technologies**, never competitors.

## Rules
1. Keep practices independently adoptable.
2. Do not copy structure or text from other frameworks; interoperate with them.
3. Name no proprietary products as requirements; examples must be labeled as examples.
4. Label non-normative content (examples, patterns, research).
5. Evidence before novelty: claims of contribution must point to `docs/research/`.
6. Never add invented practitioner anecdotes; keep "Practitioner notes" placeholders for the framework owner.
7. After changing `reference/`, run:
   `python reference/tools/smf.py validate reference/examples/gross-margin --strict` and
   `python reference/tools/smf.py test reference/examples/gross-margin`.

## Reading order
README.md → docs/discipline.md → docs/principles.md → docs/vocabulary.md → docs/lifecycle.md → docs/practices.md → docs/metric-contract.md → docs/examples/gross-margin.md → docs/works-with.md → docs/research/ → reference/README.md
