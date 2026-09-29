# Vocabulary

SMF uses a small set of plain words. Engineers will find the matching technical names in the [reference](../reference/README.md).

## The core five

| Word | Meaning | Gross margin example |
| --- | --- | --- |
| **Term** | The words people and tools use | "gross margin", "GM", "gross margin %" |
| **Concept** | The umbrella business idea a term points to | Gross Margin |
| **Perspective** | A legitimate, owned meaning of a concept. Two things can be true | Product · Service · Consolidated |
| **Context** | The situation of a question: who's asking, where, for what | Product review, services review, board deck, leadership meeting |
| **Metric Contract** | The agreed definition of a number for one perspective: what it measures, how it's calculated, what's included, who owns it, where it may be used, what it can be compared with | Product Gross Margin contract |

**Semantic Contract** is the umbrella for SMF's two contracts: the **Metric Contract** for numbers, and the **Definition Contract** for business terms that aren't numbers (Customer, Active Customer, Region). See [contracts-in-context.md](contracts-in-context.md) for how they sit alongside data contracts and metric catalogs.

**How they connect:**

```text
Term "gross margin"
   └─ points to → Concept: Gross Margin
                     ├─ Perspective: Product       → Metric Contract: Product Gross Margin
                     ├─ Perspective: Service       → Metric Contract: Service Gross Margin
                     └─ Perspective: Consolidated  → Metric Contract: Consolidated Gross Margin
Context (e.g., services review) → selects the Service perspective
Context (e.g., leadership meeting) → can't select → ask "which gross margin?"
```

## The five answers

Whenever a person or tool asks "what does this term mean here?", there are exactly five valid answers:

| Answer | When | What to do |
| --- | --- | --- |
| **Use it** | One perspective clearly applies | Proceed, and name the perspective |
| **Use the replacement** | The term or definition was retired | Use the named replacement, and say so |
| **Ask** | Several perspectives apply and context doesn't decide | Ask which one, showing the options |
| **Flag the conflict** | Owners disagree and nothing is decided yet | Don't choose; say who owns the decision |
| **Not governed** | Nobody has defined this term | Don't present an answer as official |

Guessing is never one of the answers.

## Other words

| Word | Meaning |
| --- | --- |
| **Definition Contract** | The agreed meaning of a business term, with its perspectives, classification rules and owners (template: [definition-contract.md](../templates/definition-contract.md)) |
| **Data Contract** | Not an SMF artifact: a promise about a dataset (e.g., ODCS). SMF contracts link to data contracts |
| **Owner** | The person accountable for a concept, perspective or Metric Contract within a scope |
| **Enterprise default** | The perspective used when a question is enterprise-wide, if one has been set (often Finance's consolidated view) |
| **Classification rule** | What counts as an instance, e.g., what makes a customer "active". Part of meaning, not measurement |
| **Comparability** | Whether two metrics can be compared or combined. Part of every Metric Contract |
| **Answer rule** | The written rule for which perspective a term resolves to in which context |
| **Conflict** | A declared, owned disagreement that hasn't been decided yet |
| **Check** | A test that a report or AI tool used the intended meaning |
| **Claim trace** | The record that backs up a specific reported number |

## Words SMF avoids

| Avoided | Why |
| --- | --- |
| "Single source of truth" | Conflicts with *two things can be true* |
| "Domain" as a core term | Overloaded (data mesh, org units, DNS). Perspective is used instead |
| "Proof" of numbers | A trace shows how a number was produced; it doesn't guarantee the data is right |
