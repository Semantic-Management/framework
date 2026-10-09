# Works With: Frameworks and Technologies

SMF is designed to plug gaps. It can run **together** with your existing frameworks, **separately** from them, or as **individual functions** inside them.

## Frameworks and disciplines

| Framework | How SMF fits |
| --- | --- |
| **DAMA / data governance programs** | Authority and Modeling run inside existing stewardship and glossary processes; SMF adds perspectives, answer rules and Metric Contracts |
| **Data mesh / data product models** | Perspective ownership aligns with domain ownership; SMF supplies the cross-area answer rules |
| **MDM** | MDM manages the records; SMF manages what the entity means from each perspective |
| **Model Risk Management** | SMF confirms that model outputs are labeled and used with the right meaning |
| **AI governance (ISO/IEC 42001, NIST AI RMF)** | Assurance supplies evidence that AI tools interpret business meaning correctly. See [ai-governance-evidence.md](ai-governance-evidence.md) |
| **ITSM / ITIL** | Definition changes and meaning failures flow into existing change and incident processes |
| **TOGAF / enterprise architecture** | Modeling and Implementation feed information architecture |
| **COBIT** | Ownership, approvals and checks serve as control evidence over meaning |

## Technologies: implementation choices, not competitors

| Technology | SMF practices it can implement |
| --- | --- |
| Data catalogs and business glossaries (including Unity Catalog OSS and Amundsen) | Discovery, Modeling, Authority; hosting Metric Contracts |
| Semantic layers, metric stores and metric catalogs (e.g., dbt MetricFlow) | Measurement, Implementation, Resolution. One place computes (the catalog); one place agrees (the Metric Contract) |
| BI semantic models (e.g., Power BI) | Implementation |
| Knowledge graphs and ontologies | Modeling, Resolution |
| Open metadata (Egeria) | Modeling, Authority, Implementation |
| Data contracts (ODCS / ODPS) | The datasets beneath Metric Contracts; an ODCS data contract can link each field to the business definition it supports, and SMF contracts link back to the data contracts they're built on. See [contracts-in-context.md](contracts-in-context.md) |
| Interchange formats (Apache Ossie) | Exchange; the portable model carries the executable calculation and AI hints, an Ossie metric can point at the Metric Contract that governs it, and the contract records the Ossie model as one of its implementations. See [contracts-in-context.md](contracts-in-context.md) |
| Lineage (OpenLineage / Marquez) | Implementation and claim traces |
| AI tracing (e.g., Monocle) and AI assistant instructions | Resolution and Assurance for AI consumers |
| Governance platforms | Workflow for approvals, conflicts and change notes |

An all-open-source reference setup is described in [patterns/open-source-stack.md](patterns/open-source-stack.md).

How all of these connect, drawn once, is the [metamodel](metamodel.md). The connections that are missing in a given organization are its [gaps](gaps.md).

## What SMF adds

Meaning that depends on context is established work, not an SMF invention. Domain-driven design's bounded contexts, SBVR, Business Semantics Management and Egeria's context-specific glossary terms all handle it. See the [landscape research](research/landscape.md).

SMF's contribution is applying that idea to business metrics and AI answers:

- **Perspectives with named owners**, plus approved and not-approved uses, for each legitimate meaning of a metric
- **Ask when context can't decide:** expected behavior for people and AI, not a guess
- **Comparability:** what can and can't be compared or combined
- **Checks** that people and AI actually used the intended meaning
