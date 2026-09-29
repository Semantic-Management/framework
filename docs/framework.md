# Semantic Management Framework: Overview

**Status:** v0.4 working draft

## Definitions

> **Semantic Management** is the discipline of intentionally managing organizational meaning across its lifecycle, from definition and authority through contextual resolution, measurement, implementation, exchange, consumption, assurance and evolution.

> **The Semantic Management Framework (SMF)** is a technology-independent operating model of principles, practices, roles, artifacts and lifecycle activities for managing organizational meaning across people, data, analytics and AI.

## The core question

> How does an organization intentionally manage business meaning, from definition and authority through measurement, implementation, machine interpretation and evidence?

## The operating model at a glance

| Component | What it is | Where |
| --- | --- | --- |
| **Discipline** | Why meaning needs its own discipline, and how it hands off to ITSM, DAMA, MDM, model risk and AI governance | [discipline.md](discipline.md) |
| **Principles** | Led by *two things can be true* and *context selects the perspective; when it can't, ask* | [principles.md](principles.md) |
| **Vocabulary** | Term, concept, perspective, context, Metric Contract, the five answers | [vocabulary.md](vocabulary.md) |
| **Lifecycle** | Define → authority → resolve → measure → implement → exchange → consume → assure → evolve | [lifecycle.md](lifecycle.md) |
| **Practices** | Nine capabilities, each adoptable on its own | [practices.md](practices.md) |
| **Roles and artifacts** | Who does what; the Metric Contract and supporting records | [roles-and-artifacts.md](roles-and-artifacts.md) |
| **Semantic Contracts** | Metric Contract (numbers) and Definition Contract (terms) | [metric-contract.md](metric-contract.md), [contracts-in-context.md](contracts-in-context.md) |
| **Adoption** | Small, mid-size and enterprise starting points | [getting-started.md](getting-started.md) |
| **Works with** | Frameworks and technologies SMF plugs into | [works-with.md](works-with.md) |

## How the pieces fit

```text
            Two things can be true
                     │
Term ──► Concept ──► Perspectives (each with an owner)
                          │
                          ├──► Metric Contract (how it's measured, what it can be compared with)
                          │
Context ──────────────────┴──► Answer: use it · use the replacement · ask · flag the conflict · not governed
                                         │
                               People · reports · AI assistants
                                         │
                                 Checks and claim traces
```

## Design commitments

- **Technology-independent.** Catalogs, semantic layers, metric stores, knowledge graphs, ontologies and governance platforms are ways to implement SMF, not competitors.
- **Framework-friendly.** SMF works together with other frameworks, separately from them, or as individual functions inside them.
- **Any size.** Every practice scales from small teams to enterprises; a few, like Interchange, are usually only needed at larger scale.
- **Adopt in pieces.** No practice requires another, a fixed sequence or a central system.
- **Business-first.** The framework is written for business and analytics leaders. Technical material lives in [reference/](../reference/README.md).

## Non-goals

SMF does not:
- catalog every noun;
- impose a single enterprise ontology;
- centralize every decision about meaning;
- replace existing tools or frameworks;
- eliminate legitimate differences between parts of the business;
- require a runtime service or a product.

## Success condition

An organization can answer, with increasing reliability:

> What does this mean, from which perspective, who owns it, how is it measured and built, did the person or AI use it correctly, and can we back up the number?
