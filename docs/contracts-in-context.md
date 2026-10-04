# Contracts in Context

"Contract" already means something in the data world. This page shows how SMF's contracts fit alongside data contracts, metric catalogs and semantic layers without competing with them.

## Three layers, three promises

| Layer | Contract | Promise between | Answers | Where it usually lives |
| --- | --- | --- | --- | --- |
| **Data** | **Data Contract** | Data producer → data consumer | Is this dataset shaped, fresh and good enough to use? | ODCS / ODPS (Bitol), data platforms |
| **Number** | **Metric Contract** (SMF) | Metric owner → the business | What does this number mean, from which perspective, where may it be used, what can it be compared with? | Metric catalogs, semantic layers, glossaries, or a shared document |
| **Term** | **Definition Contract** (SMF) | Meaning owner → the business | What does "Customer" or "Active Customer" mean, from which perspective, and who decides? | Glossaries, catalogs, or a shared document |

**Semantic Contract** is the umbrella name for SMF's two contracts. Most people will only ever say "Metric Contract" or "Definition Contract."

```text
Semantic Contract
├── Metric Contract       numbers: Gross Margin, Revenue, Churn
└── Definition Contract   terms: Customer, Active Customer, Region
```

**None of the three does another's job.**
- A data contract never says what gross margin means.
- A Metric Contract never promises that a dataset is fresh.
- A Definition Contract never says how a number is calculated.

## Working with data contracts (ODCS)

Data contracts describe datasets. SMF contracts describe the business meaning built on top of them. They link in both directions:

- **From the data contract to meaning.** An ODCS data contract can link each field to the business definition it supports. A column can point to the SMF contract that gives it business meaning.
- **From meaning to the data.** A Metric Contract lists the data contracts it's built on.

For example, the landed cost column in a sales data contract can link to the Product Gross Margin Metric Contract. Technical details and an example are in the [reference](../reference/spec/README.md).

**One overlap to be clear about:** newer versions of ODCS let a data contract carry AI guidance and tag what each field is (a column, a measure or a dimension). These describe **one dataset**. SMF handles meaning **across** datasets: perspectives, owners, comparability, and when to ask "which one?". Use both. Don't duplicate one inside the other.

## Working with metric catalogs and semantic layers

Metric catalogs, metric stores and semantic layers (for example dbt MetricFlow, Unity Catalog metric views, Cube, LookML or a BI semantic model) hold the **executable** definition of a metric. The Metric Contract holds the **agreement**.

> **One place computes. One place agrees.**

| | Metric catalog / semantic layer | Metric Contract |
| --- | --- | --- |
| Purpose | Calculate the number consistently | Agree what the number means and how it may be used |
| Formula | The executable logic | The formula in plain words, plus a pointer to the executable version |
| Usually has | Name, description, owner, certification, dimensions | All of that, plus perspective, approved and not-approved uses, comparability |
| Source of truth for | *How* it's computed | *What* it means and *who* decides |

**How to avoid conflict:**
- **Don't maintain the formula in two places as competing authorities.** The contract describes it and points to the catalog entry that implements it.
- **Host the contract in the catalog** when the catalog supports extra metadata. SMF doesn't need its own tool.
- **Let Assurance check for drift.** If the catalog's logic stops matching the contract, that's a finding to fix, not a second truth.
- **Add only what's missing.** Where a catalog already records owner and certification, the contract adds perspective, approved uses and comparability.

## Common field names

"Metric contract" is already used generically in the analytics community. SMF uses the common fields so practitioners recognize it, and adds its own:

| Common fields (widely used) | Added by SMF |
| --- | --- |
| Expression (formula) | Concept and **perspective** |
| Grain | Plain-words meaning |
| Allowed dimensions | **Approved for / not approved for** |
| Filters, inclusions, exclusions | **Comparable / not comparable with** |
| Time semantics | Owner accountability and sign-off |
| Additivity | Link to data contracts and implementations |
| Owner, certification, version | Change note and effective date |

SMF does not claim to have invented the metric contract. Its contribution is making **perspective, approved use and comparability** part of it. See the [landscape research](research/landscape.md) for the prior art.

## Sources
- ODCS and ODPS sources: see the [reference](../reference/spec/README.md).
- Generic use of "metric contract": https://weaveos.com/glossary/metric-contract ; https://datalakehousehub.com/blog/metric-contracts-code-multi-agent/
