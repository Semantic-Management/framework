# Gap Catalogue: Connections That Should Exist

**Type:** Non-normative

The [metamodel](metamodel.md) shows the connections between data contracts, SMF documents, implementations and decisions. A gap is a connection that should exist and does not: a contract with no owner, a build with no contract behind it, a claim resting on a build nobody has tested.

Gaps are the work list. They are also the honest measure of how far Semantic Management has been adopted, because each one belongs to a practice, and a practice is in place when its gaps are closed for the terms that matter.

This catalogue names the gaps so tools can find them and people can talk about them. It does not say every gap must be closed. **Govern in proportion:** close the gaps on the terms where confusion, reuse, AI use, regulatory exposure or executive visibility make it matter, and leave the rest open on purpose.

## How to read a gap

| | |
| --- | --- |
| **Name** | What is missing, in plain words |
| **Looks like** | How it shows up in the organization |
| **Practice** | Which SMF practice owns closing it |
| **Weight** | How much it matters when the term matters: **critical** (a wrong number or a guess is likely), **high** (a dispute or a silent change is likely), **medium** (inconvenient, not dangerous) |

## Meaning

| Name | Looks like | Practice | Weight |
| --- | --- | --- | --- |
| **Term with no concept** | A word people use in reports and questions that nobody has written down. Everything built on it is a guess | Discovery, Modeling | high |
| **Concept with no owner** | A definition exists but nobody can approve a change to it | Authority | critical |
| **Perspective with no owner** | "Service gross margin" exists as a label but nobody is accountable for what it means | Authority | critical |
| **Two meanings, one label, no decision** | The same term is used two ways and nobody has said whether they are the same, both legitimate, one inside the other, or an open conflict | Authority | critical |
| **Conflict past its date** | A disagreement was declared with an owner and a target date, and the date has passed | Authority, Lifecycle | high |
| **Retired term with no replacement** | Something was deprecated but the thing to use instead is not named | Lifecycle | high |
| **Concept with no classification rule** | A term like "active customer" where what counts has never been written down, so every build decides for itself | Modeling, Authority | high |

## Resolution

| Name | Looks like | Practice | Weight |
| --- | --- | --- | --- |
| **Several perspectives, no answer rule** | A concept has two or more legitimate meanings and nothing says which applies where. Every consumer picks one silently | Resolution | critical |
| **Answer rule with no "ask"** | The rule names a perspective for some contexts and falls back to a default for everything else, so an unlisted situation gets a guess instead of a question | Resolution | critical |
| **Context nobody defined** | Answer rules refer to a situation ("board", "leadership meeting") that is not written down anywhere, so tools cannot recognize it | Resolution | medium |
| **Enterprise default used as a fallback** | The default meant for board and external reporting is being served to every unmatched question | Resolution, Authority | high |

## Measurement

| Name | Looks like | Practice | Weight |
| --- | --- | --- | --- |
| **Perspective with no Metric Contract** | A legitimate meaning of a number, with an owner, but no agreed definition of how it is measured | Measurement | high |
| **Metric Contract with no owner or sign-off** | A definition exists but nobody has approved it | Measurement, Authority | critical |
| **Metric Contract with no approved uses** | The number is defined but it is not written down where it may and may not be used, so it ends up in the board deck | Measurement | high |
| **Contract pair with no comparability statement** | Two contracts measure the same concept and neither says whether they may be compared or combined. Someone will average them | Measurement | critical |
| **Metric Contract with no data contracts beneath it** | The number is defined but it is not recorded what datasets it stands on, so a change upstream is a surprise | Measurement | medium |
| **Metric Contract with no version or effective date** | The definition has changed and last year's numbers can no longer be read under the definition that produced them | Lifecycle | high |

## Implementation

| Name | Looks like | Practice | Weight |
| --- | --- | --- | --- |
| **Metric Contract with no build record** | The agreement exists; nobody has recorded where it is actually calculated | Implementation | high |
| **Build with no contract (shadow metric)** | A measure in a BI model, a semantic layer or an interchange model that no contract governs | Discovery, Implementation | high |
| **Build never tested** | A build record exists but its conformance has never been assessed | Implementation, Assurance | high |
| **Build with no snapshot** | The build was assessed, but the calculation as it was at that moment was not kept, so drift can only be noticed by chance | Implementation | medium |
| **Build has drifted** | The calculation in the tool no longer matches the snapshot on its build record | Implementation, Assurance | critical |
| **Generated build with no source** | A semantic-layer or BI measure was produced from an interchange model, but the build record does not say so, so it gets tested as if it were hand-built | Implementation | medium |
| **Interchange model with no pointer back** | An Ossie metric, a semantic layer metric, a data product or a data contract field is governed by a contract but does not say so in its own file, so a tool reading only that file cannot find the agreement | Interchange | medium |

## Consumption and assurance

| Name | Looks like | Practice | Weight |
| --- | --- | --- | --- |
| **Consumer with no checks** | A report suite or AI assistant uses governed terms and nobody has written a single question with an expected answer | Assurance | critical |
| **"Ask" case never tested** | The answer rule says a situation should trigger a question, and no check confirms the consumer actually asks | Assurance | critical |
| **Check never run** | Checks exist; there are no results, or the results predate the last definition change | Assurance | high |
| **Consumer that guessed** | A check expected "ask" and the consumer answered with a number | Assurance | critical |
| **Claim with no contract version** | A number in a board deck or a filing that cannot be traced to the agreement that defined it | Assurance | critical |
| **Claim on an untested or drifted build** | The number is traced to a build whose conformance is untested, non-conformant or stale | Assurance | critical |
| **Claim with no verification** | The trace exists but nobody has confirmed the number by re-execution or reconciliation | Assurance | high |

## Lifecycle

| Name | Looks like | Practice | Weight |
| --- | --- | --- | --- |
| **Change with no note** | A definition's version went up and nothing says what changed, why, or from when | Lifecycle | high |
| **Superseded definition still in use** | A build or a claim still points at a retired version with no replacement recorded | Lifecycle, Implementation | high |

## Using the catalogue

- **As a work list.** Run it over the terms that matter and sort by weight. The critical gaps on executive metrics are the first quarter's work.
- **As a maturity reading.** A practice is in place for a term when its gaps are closed for that term. Counting closed gaps per practice, over the governed terms, gives a maturity picture that is observed rather than self-assessed. This is the basis for the maturity model on the [roadmap](roadmap.md).
- **As tool behavior.** A tool that renders the metamodel can show each gap as a missing connection on the card it belongs to. Most gaps are mechanical to find from the documents alone; a few (drift, checks never run) need the tool to read the implementation or the results.
- **As AI governance evidence.** The assurance gaps map directly onto the Measure and Manage functions in [ai-governance-evidence.md](ai-governance-evidence.md).

Names and weights here are a first cut from practice. Challenge them, add missing gaps, and bring cases where a gap was harmless or a closed gap still produced a wrong number. See [CONTRIBUTING.md](../CONTRIBUTING.md).
