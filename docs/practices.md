# The Nine Practices

Each practice is a capability an organization can adopt **on its own**, combine with others, or run inside a framework it already has. None requires another.

For each practice:
- **Why it matters:** the problem it solves.
- **What "done" looks like:** at three sizes.
- **Works with:** the frameworks and tools it plugs into.

| # | Practice | The question it answers |
| --- | --- | --- |
| 1 | [Semantic Discovery](#1-semantic-discovery) | What meanings, definitions and conflicts already exist? |
| 2 | [Semantic Modeling](#2-semantic-modeling) | How do we write down concepts and their perspectives? |
| 3 | [Semantic Authority](#3-semantic-authority) | Who decides what a term means, and in what scope? |
| 4 | [Semantic Resolution](#4-semantic-resolution) | Which perspective applies here, and what should people and AI do when it's unclear? |
| 5 | [Measurement Management](#5-measurement-management) | How is each number calculated, and who signs off? |
| 6 | [Semantic Implementation](#6-semantic-implementation) | Where is each definition built, and does it match? |
| 7 | [Semantic Interchange](#7-semantic-interchange-optional) *(optional)* | How does meaning move between systems intact? |
| 8 | [Semantic Assurance](#8-semantic-assurance) | Did the report or AI use the right meaning? Can we back up the number? |
| 9 | [Semantic Lifecycle Management](#9-semantic-lifecycle-management) | How do definitions change without breaking things or history? |

---

## 1. Semantic Discovery

**Why it matters:** You can't manage meaning you can't see. Most organizations don't know how many versions of "gross margin" they run.

**What it involves:**
- Collect definitions from reports, spreadsheets, semantic layers and people.
- Find the same term used with different meanings, and different terms used for the same meaning.
- Find "shadow" metrics built outside any agreed definition.
- Prioritize the few terms that cause the most confusion.

| Small | Mid-size | Enterprise |
| --- | --- | --- |
| A one-page list of the 10 most-argued terms | An inventory of priority metrics and where each lives | Ongoing harvesting from catalogs and BI tools; a tracked backlog |

**Works with:** data catalogs, BI tool inventories, governance program intake.

---

## 2. Semantic Modeling

**Why it matters:** Meaning needs a stable name that isn't just a label, so it survives renames, reorganizations and new tools.

**What it involves:**
- Record each **concept** and its **perspectives**.
- Record terms and aliases ("GM" = gross margin).
- Record classification rules, such as what makes a customer "active".
- Capture terms that aren't numbers in a **[Definition Contract](../templates/definition-contract.md)**.
- Record relationships, e.g., service gross margin is a perspective of gross margin.

| Small | Mid-size | Enterprise |
| --- | --- | --- |
| A shared doc or spreadsheet | A glossary with perspectives | A glossary, catalog or knowledge graph with stable IDs |

**Works with:** business glossaries, catalogs, Egeria, knowledge graphs, SKOS, ISO/IEC 11179 registries.

---

## 3. Semantic Authority

**Why it matters:** "Two things can be true" only works if each truth has an owner. Without owners, disagreements become permanent arguments.

**What it involves:**
- Name an owner for each concept and perspective.
- Name an enterprise default where one is needed, for specific contexts such as board reporting (often Finance's consolidated view). It is not a fallback for other questions.
- Decide conflicts. The four outcomes:
  - **merge:** they're the same;
  - **keep both as perspectives:** both are legitimate;
  - **record broader/narrower:** one contains the other;
  - **declare an open conflict:** with an owner and a date.

| Small | Mid-size | Enterprise |
| --- | --- | --- |
| The owner signs off on each definition | Named owners per perspective; a monthly decision slot | Delegated business-area owners; central forum only for cross-functional conflicts |

**Works with:** existing data stewardship and governance councils, data mesh domain ownership (a data mesh concept). Detail: [semantic-authority.md](semantic-authority.md).

---

## 4. Semantic Resolution

**Why it matters:** This is where confusion becomes visible or stays hidden. It covers every time a person, report or AI tool uses a term.

**What it involves:**
- Write **answer rules**: which perspective applies in which context.
- Apply the [five answers](vocabulary.md#the-five-answers): use it, use the replacement, ask, flag the conflict, not governed.
- Give people and AI the constraints that come with the answer: exclusions, time rules, what can't be compared.

**The rule:** *Context selects the perspective. When context can't, ask.*

| Small | Mid-size | Enterprise |
| --- | --- | --- |
| A table of terms, contexts and perspectives shared with the team and the AI assistant | Answer rules for all priority terms, built into report descriptions and AI prompts | Answer rules served to semantic layers and AI agents |

**Works with:** semantic layers, AI assistant instructions and context, the AI context that ODCS data contracts and Apache Ossie models can carry.

---

## 5. Measurement Management

**Why it matters:** Most "which number is right?" arguments are really about undocumented differences in calculation.

**What it involves:**
- A **[Metric Contract](metric-contract.md)** for each perspective that matters. Each contract covers:
  - what's included and excluded;
  - the time rules;
  - the owner;
  - where it's approved for use;
  - **comparability**: what it can and can't be compared or combined with.
- Approval and versioning of those contracts.

| Small | Mid-size | Enterprise |
| --- | --- | --- |
| One-page Metric Contracts for 5–10 key metrics | Contracts for all executive metrics, with sign-off | Contracts linked to semantic layer definitions and certification |

**Works with:** dbt MetricFlow and other semantic layers, BI measures, metric stores, Apache Ossie metrics, ODCS data contracts.

---

## 6. Semantic Implementation

**Why it matters:** A signed definition is only useful if the reports actually calculate it that way.

**What it involves:**
- Record where each Metric Contract is built (BI model, semantic layer, SQL, spreadsheet).
- Track whether each build matches the contract.
- Flag builds that don't match any contract.

| Small | Mid-size | Enterprise |
| --- | --- | --- |
| A "where is this calculated?" column on the contract | Inventory of builds per contract, with match status | Automated links from semantic layer and lineage tools |

**Works with:** semantic layers, BI tools, dbt, OpenLineage, Egeria semantic assignment.

---

## 7. Semantic Interchange (optional)

**Why it matters:** When meaning moves between platforms, perspectives and owners are often lost.

**What it involves:**
- Export and import definitions.
- Record how well mappings match: equivalent, broader, narrower, approximate.
- Note what doesn't survive the move.

| Small | Mid-size | Enterprise |
| --- | --- | --- |
| Usually not needed | During platform migrations | Ongoing across multiple semantic platforms |

**Works with:** Apache Ossie, SKOS, ODCS/ODPS, vendor semantic model formats.

---

## 8. Semantic Assurance

**Why it matters:** Good definitions don't guarantee correct use, especially by AI.

**What it involves:**
- **Checks:** questions with expected answers. For example, "In a leadership meeting, 'gross margin' should trigger *ask*."
- Run checks against reports and AI assistants before and after changes.
- **Claim traces** for consequential numbers: which contract, which build, which data.

| Small | Mid-size | Enterprise |
| --- | --- | --- |
| 20 test questions asked of the AI assistant each month | Checks run on every definition change | Automated checks in release pipelines; traces for board and regulatory numbers |

**Works with:** AI evaluation practices, NIST AI RMF and ISO/IEC 42001 evidence, existing incident and change processes, OpenLineage. See [ai-governance-evidence.md](ai-governance-evidence.md).

---

## 9. Semantic Lifecycle Management

**Why it matters:** Businesses change what they mean: new cost allocations, reorganizations, acquisitions. Without care, history becomes unreadable and reports quietly break.

**What it involves:**
- Version and date definitions.
- Name replacements for retired terms.
- Handle splits and merges.
- Keep "what did this mean in 2025?" answerable.

| Small | Mid-size | Enterprise |
| --- | --- | --- |
| A change note and effective date on each contract | Versioned contracts; change notices to report owners | Registration statuses, impact analysis, links to change management |

**Works with:** existing change management, Git versioning, ISO/IEC 11179 registration statuses.
