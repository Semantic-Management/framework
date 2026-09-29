# The Missing Discipline: Managing Meaning

## Every important thing has a discipline, except meaning

| Discipline | Thing being managed | Typical signature artifact |
| --- | --- | --- |
| ITSM / ITIL | IT services | Service catalog |
| DAMA / Data Governance | Data | Data policies, stewardship assignments |
| TOGAF | Enterprise architecture | Architecture models |
| COBIT | IT governance and control | Control objectives |
| MDM | Master entities and records | Golden record |
| Model Risk Management | Analytical models | Model inventory, validation report |
| AI Governance | AI systems | AI risk assessment |
| **Semantic Management (SMF)** | **Business meaning** | **Semantic Contracts** (Metric Contract, Definition Contract) |

## Why now

Business meaning used to be managed informally. Experienced analysts knew which "revenue" a report used and quietly corrected for it. That stops working when:

- the same metric is rebuilt in five tools, each with its own logic;
- leaders from different parts of the business use the same words for different things;
- AI assistants answer business questions directly, with no analyst in between to catch the mismatch.

Analytics and AI are now the foundation for decisions. The meaning underneath them needs its own lifecycle, its own owners and its own checks.

## Where SMF hands off to its neighbors

SMF does not take over any existing discipline. It manages the part each one leaves open.

| Discipline | Manages | SMF manages the part it leaves open |
| --- | --- | --- |
| DAMA / Data Governance | Data: quality, stewardship, access | What the data *means*, and which meaning applies where |
| MDM | The Customer *records* | What "Customer" *means* from each perspective |
| Model Risk Management | The analytical model | Whether a model's output means what the report or decision assumes |
| AI Governance | The AI system: risk, safety, accountability | Whether the AI *interpreted* business meaning correctly |
| ITSM / ITIL | IT services | Changes to meaning, and failures of meaning, flowing into existing change and incident processes |
| TOGAF | Architecture | How meaning is realized across systems |
| COBIT | IT control objectives | Evidence of control over meaning: ownership, approvals, checks |

These lines are drawn from practice and are open to challenge. See [CONTRIBUTING.md](../CONTRIBUTING.md).

## What SMF is and isn't

**SMF is:**
- a discipline and an operating model;
- technology-independent;
- adoptable one practice at a time;
- designed to work with other frameworks, together or separately.

**SMF is not:**
- a catalog;
- a semantic layer;
- a metric store;
- a knowledge graph or ontology;
- a governance platform.

Those are **implementation technologies** for SMF practices. See [works-with.md](works-with.md).
