# Works With: Frameworks and Technologies

SMF is designed to plug gaps. It can run **together** with your existing frameworks, **separately** from them, or as **individual functions** inside them.

## Frameworks and disciplines

| Framework | How SMF fits |
| --- | --- |
| **DAMA / data governance programs** | Authority and Modeling run inside existing stewardship and glossary processes; SMF adds perspectives, answer rules and Metric Contracts |
| **Data mesh / data product models** | Perspective ownership aligns with domain ownership; SMF supplies the cross-domain answer rules |
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
| Data contracts (ODCS / ODPS) | The datasets beneath Metric Contracts; link both ways via ODCS `authoritativeDefinitions`. See [contracts-in-context.md](contracts-in-context.md) |
| Interchange formats (Apache Ossie) | Interchange of metric definitions |
| Lineage (OpenLineage / Marquez) | Implementation and claim traces |
| AI tracing (e.g., Monocle) and AI assistant instructions | Resolution and Assurance for AI consumers |
| Governance platforms | Workflow for approvals, conflicts and change notes |

An all-open-source reference setup is described in [patterns/open-source-stack.md](patterns/open-source-stack.md).

## What SMF adds that these don't

- **Perspectives:** two things can be true, each with an owner
- **The answer rule:** context selects the perspective; when it can't, ask
- **Comparability:** what can and can't be compared or combined
- **Checks** that people and AI actually used the intended meaning
