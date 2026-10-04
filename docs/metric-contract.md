# The Metric Contract

The Metric Contract is SMF's signature artifact, the way the golden record is MDM's and the validation report is model risk management's.

It is an **agreement about what a number means**, written for the person who owns the number first and for tools second.

The Metric Contract is one of two **Semantic Contracts**. Its sibling, the **Definition Contract**, covers business terms that aren't numbers, such as Customer or Region ([template](../templates/definition-contract.md)). For how both fit alongside data contracts and metric catalogs, see [contracts-in-context.md](contracts-in-context.md).

## What it answers

1. **What concept does it measure, and from which perspective?** e.g., Gross Margin, service perspective
2. **How is it calculated?** In plain words first, then the formula
3. **What's in, what's out?** Inclusions and exclusions
4. **Which time rules apply?** Fiscal or calendar; which date counts
5. **Who owns it?** Accountable owner and who maintains it
6. **Where may it be used?** e.g., services reviews, staffing decisions, not board reporting
7. **What can it be compared or combined with?** And what it must not be
8. **What is it built on, and where is it implemented?** Data contracts underneath; metric catalogs, semantic layers, reports or spreadsheets on top
9. **Which version is this, and since when?**

The template is in [templates/metric-contract.md](../templates/metric-contract.md).

## Example: Service Gross Margin (one page)

| | |
| --- | --- |
| **Concept / perspective** | Gross Margin · **Service** perspective |
| **In plain words** | Of every dollar we bill for installation and maintenance, how much is left after paying for the labor, subcontractors and parts it took to deliver |
| **Formula** | (Service revenue − (technician labor + subcontractor cost + parts used)) ÷ service revenue |
| **Includes** | Installation and maintenance work orders |
| **Excludes** | Product sales |
| **Grain** | One completed work order |
| **Time rules** | Fiscal month; counted when the work order is completed |
| **Additivity** | Non-additive (a ratio). Recompute from totals; never sum or average margins |
| **Owner** | Services Lead (maintained by Finance Analyst) |
| **Approved for** | Services reviews and staffing decisions |
| **Not approved for** | Board or external reporting (use Consolidated Gross Margin) |
| **Comparability** | **Not comparable with Product Gross Margin.** Cost is labor-based, not goods-based. Do not average the two. Compare over time within services |
| **Built on** | Work order and job-costing data contracts |
| **Implemented in** | Services KPI workbook, GM tab |
| **Version** | v1, effective 2026-01-01 |

## How it plays with other tools

The Metric Contract doesn't replace any tool. It is the agreement those tools implement.

One rule keeps this clean: **one place computes, one place agrees.** The metric catalog or semantic layer computes; the contract records the agreement and points to it.

| Tool or standard | Relationship |
| --- | --- |
| Semantic layers (dbt MetricFlow, others) | The executable version of the contract; the contract records which build implements it |
| BI measures (e.g., Power BI) | Same: an implementation, linked from the contract |
| Metric stores | Can host the contract's calculation; the contract adds perspective, ownership, approved uses and comparability |
| Apache Ossie | Portable format for metric definitions; the contract carries the ownership, approval and trust information Ossie leaves out, plus perspective and comparability |
| ODCS / ODPS data contracts | Describe the datasets the metric is built on; the Metric Contract describes the business number on top |
| Catalogs and glossaries | Can store and display contracts |

A machine-readable form of the Metric Contract, with a schema, is available in the [reference](../reference/spec/README.md) for teams that want to automate.

## Common mistakes the contract prevents

- Two leaders using the same term for different perspectives, and not realizing it
- Averaging metrics that can't be combined
- AI tools picking a perspective without saying which
- A definition changing silently, so last year's numbers no longer compare
