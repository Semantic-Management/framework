# Roles and Artifacts

## Roles

Roles are responsibilities, not job titles. In a small business, one person may hold all of them. Many already exist under other names, such as data steward, BI lead or finance analyst.

| Role | Responsibility | Often held by |
| --- | --- | --- |
| **Meaning owner** | Accountable for what a concept or perspective means within a scope | Business leader for that area (e.g., Services Lead) |
| **Metric owner** | Approves a Metric Contract and its changes | Same person as the meaning owner, or Finance for financial metrics |
| **Steward** | Writes and maintains definitions, answer rules and checks | Analyst, data steward, finance analyst |
| **Enterprise authority** | Sets enterprise defaults and decides cross-functional conflicts | Controller, CDAO, or a small forum |
| **Builder** | Implements definitions in reports, semantic layers and AI tools | BI developer, analytics engineer |
| **Consumer owner** | Accountable for how a report suite or AI assistant uses meaning | Report owner, AI product owner |
| **Checker** | Runs checks and keeps evidence | Analyst, QA, AI governance team |

## Artifacts

| Artifact | What it is | Practice |
| --- | --- | --- |
| **Metric Contract** | Signature artifact (Semantic Contract for numbers): the agreed definition of one number for one perspective | Measurement Management |
| **Definition Contract** | Semantic Contract for business terms: meaning, perspectives, classification rules, owners | Modeling, Authority |
| Answer rule | Which perspective applies in which context, and when to ask | Resolution |
| Conflict record | A declared, owned, undecided disagreement | Authority |
| Build record | Where a contract is implemented, and whether it matches | Implementation |
| Check | A question with an expected answer, and its results | Assurance |
| Claim trace | The record that backs up a specific reported number | Assurance |
| Change note | What changed, why, and from when | Lifecycle Management |

Templates: [templates/](../templates/). Machine-readable forms: [reference/spec](../reference/spec/README.md).
