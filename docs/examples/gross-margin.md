# Example: Gross Margin, Three Perspectives

**Type:** Non-normative

**Fictional company:** Lakeview Supply & Service sells appliances (**products**) and installs and maintains them (**services**). The situation is common in businesses of every size.

---

## The problem

At the quarterly leadership meeting:

- The **Product Line Lead** says gross margin is 34%.
- The **Services Lead** says gross margin is 22%.
- The **Controller's** board deck says 31%.

All three are correct. They are describing three different things with the same two words.

Then the CEO asks the new AI assistant, "What was our gross margin last quarter?" It answers "34%", from the product dashboard, with complete confidence.

## Why it happens

| | Product GM | Service GM | Consolidated GM |
| --- | --- | --- | --- |
| Formula shape | (Revenue − cost) ÷ revenue | (Revenue − cost) ÷ revenue | (Revenue − cost) ÷ revenue |
| What "cost" means | Landed cost of goods: materials, freight-in, duties | Technician labor, subcontractors, parts used | Total cost of revenue as reported |
| Owner | Product Line Lead | Services Lead | Controller |

The formulas look alike, which is exactly why nobody questions the difference. **Similar formulas can hide different meanings.**

## Applying SMF, practice by practice

**Discovery.** List every place "gross margin" is calculated. There are three legitimate versions and one spreadsheet that averages product and service margin together (a shadow metric).

**Modeling.** Record one concept, *Gross Margin*, with three perspectives: Product, Service, Consolidated. Record "GM" and "gross margin %" as aliases.

**Authority.**
- Each perspective gets its owner.
- The Controller's consolidated view is the enterprise default for board and external reporting only. Anywhere else the answer rule decides, or asks.
- Record the relationship as **broader/narrower**. Consolidated is broader: it covers all revenue and all cost of revenue. Product and Service are narrower, operational perspectives. Consolidated is computed from totals, not averaged and not a simple sum of the two margins. Its cost definition can differ (for example reserves or freight treatment), so the three won't reconcile by arithmetic. The Controller owns the reconciliation.
- The averaged spreadsheet is retired. Averaging the two perspectives has no agreed meaning.

**Measurement.** Write a [Metric Contract](../metric-contract.md) for each perspective. None of the three is comparable with another as a margin, and each contract says so. None may be averaged. The consolidated contract adds that the Controller owns the reconciliation.

**Resolution.** Write the answer rule:

| Context | Answer |
| --- | --- |
| Product review | Use Product Gross Margin |
| Services review | Use Service Gross Margin |
| Board deck, external reporting | Use Consolidated Gross Margin |
| Leadership meeting, or no context | **Ask:** "Which gross margin: consolidated, product, or service?" |

**Implementation.** Link each contract to where it's built: the finance model, the product dashboard, the services workbook.

**Assurance.** Add checks, and run them before relying on any AI assistant:
- "What was our gross margin?" asked in a leadership context **must be answered with a question**.
- "Gross margin" in a services review must use Service GM, never Product GM.

**Lifecycle.** Next fiscal year, freight-out moves into product cost. Product GM becomes v2 with an effective date, and last year's numbers stay readable under v1.

## The result

- In the next meeting, each leader's number is labeled with its perspective. The discussion moves to *why* service margin is lower, not *whose number is right*.
- The AI assistant asks "Which gross margin: consolidated, product, or service?" instead of guessing.
- Nobody averages the two perspectives anymore.

## Try it with the reference tools

This example is also available in machine-readable form, with runnable checks, in [reference/examples/gross-margin](../../reference/examples/gross-margin/README.md).
