# SMF Reference Specification v0.1

**Status:** Draft. Breaking changes are expected before v1.0.
**Type:** Normative for document shape and resolution states; the reference resolver in `tools/` is non-normative.

**Audience:** technical teams implementing SMF practices in tools and AI systems. You do not need this to adopt SMF; the framework in `docs/` is written for business and analytics leaders.

This reference gives SMF artifacts (concepts, perspectives, Metric Contracts, answer rules, checks) a common file format so tools, agents and tests can exchange them.

## 1. Documents

Every SMF document is a YAML (or JSON) object with two required envelope fields:

```yaml
smf: "0.1"        # spec version
kind: Concept     # document kind
```

A file may contain several documents separated by `---`.

| Kind | Purpose | Module | Schema |
| --- | --- | --- | --- |
| `Concept` | Stable identity for a business meaning | Core / Modeling | [concept](schemas/concept.schema.json) |
| `Term` | Label that maps to a concept | Core / Modeling | [term](schemas/term.schema.json) |
| `Perspective` | A legitimate, owned meaning of a concept (e.g., Service Gross Margin) | Core | [perspective](schemas/perspective.schema.json) |
| `Context` | The situation of a question; selects the perspective | Core | [context](schemas/context.schema.json) |
| `Ownership` | Owner and scope for a subject | Core / Authority | [ownership](schemas/ownership.schema.json) |
| `ClassificationRule` | What counts as an instance of a concept | Authority / Modeling | [classification-rule](schemas/classification-rule.schema.json) |
| `Conflict` | Declared, unresolved disagreement | Authority | [conflict](schemas/conflict.schema.json) |
| `ResolutionRule` | Default and contextual resolution for a term | Resolution | [resolution-rule](schemas/resolution-rule.schema.json) |
| `ResolutionResult` | Output of resolving a term in context | Resolution | [resolution-result](schemas/resolution-result.schema.json) |
| `MetricContract` | Governed measurement for one perspective, including comparability | Measurement | [metric-contract](schemas/metric-contract.schema.json) |
| `Binding` | Link from contract/concept to an implementation | Implementation | [binding](schemas/binding.schema.json) |
| `TestCase` | Expected behavior for a consumer or implementation | Assurance | [test-case](schemas/test-case.schema.json) |
| `ClaimTrace` | Trace for a specific quantitative claim | Assurance | [claim-trace](schemas/claim-trace.schema.json) |

Schemas use JSON Schema draft 2020-12. Schema IDs are URNs (`urn:semantic-management-framework:0.1:schema:<name>`) until a permanent home exists.

### Semantic Contracts in machine form

- A **Metric Contract** is the `MetricContract` document (plus `Binding` documents for where it's implemented). Field names align with those commonly used for metric contracts: expression (`formula`), `grain`, `valid_dimensions`, `filters`, `time_semantics`, `additivity`, `owner`, certification (`certified_for`), `version`. SMF adds `perspective`, approved uses, `comparability` and `built_on` (links to data contracts).
- A **Definition Contract** is a set of documents: `Concept`, its `Perspective`s, `Term`s, `Ownership`, any `ClassificationRule`s and the `ResolutionRule` for the term.
- To link from an ODCS data contract to an SMF contract, use ODCS `authoritativeDefinitions` with type `businessDefinition`. In the other direction, a `MetricContract` lists the data contracts it is built on in `built_on`. For the business-level picture, see [docs/contracts-in-context.md](../../docs/contracts-in-context.md).
- A `Perspective` may set `broader_than` (a list of perspective references) when it contains other perspectives, as Consolidated Gross Margin contains Product and Service. It records containment only. Comparability stays on the `MetricContract`.

#### Linking an ODCS data contract to an SMF contract (illustrative)

```yaml
# Inside an ODCS data contract
properties:
  - name: landed_cost_of_goods
    authoritativeDefinitions:
      - type: businessDefinition
        url: https://example.org/semantic/metric-contracts/product-gross-margin
```

#### Overlap with ODCS 3.2 `context` and `semanticType`

ODCS 3.2 added an AI `context` block and a `semanticType` tag (column, measure, dimension) to data contracts. They describe **one dataset**. SMF documents describe meaning **across** datasets: perspectives, owners, comparability and the five resolution states. Use both, and do not duplicate one inside the other.

Sources:
- ODCS v3.2 schema (`authoritativeDefinitions`): https://bitol-io.github.io/open-data-contract-standard/v3.2.0/schema/
- ODCS v3.2 / ODPS v1.1 release notes (AI `context`, `semanticType`): https://www.entropy-data.com/news/2026-09-08-odcs-3-2-odps-1-1

## 2. Identifiers

- Pattern: lowercase, dot-namespaced, at least two segments: `concept.customer`, `finance.net_revenue`.
- Version pin: `id@vN`, e.g. `finance.net_revenue@v3`.
- IDs are never derived from labels alone and never reused for a different meaning.
- A document may reference an ID defined elsewhere (another repo, a catalog). Validators warn about undefined references unless run in strict mode.

## 3. Resolution states (the five answers)

Plain-language names used in the framework docs are shown in brackets.

A `ResolutionResult` has exactly one `state`:

| State | Required fields |
| --- | --- |
| `RESOLVED` [use it] | `concept`, `basis` |
| `RESOLVED_VIA_REPLACEMENT` [use the replacement] | `concept`, `replaces` |
| `NEEDS_CLARIFICATION` [ask] | `options` (2 or more) |
| `CONFLICT` [flag the conflict] | `conflict_ref` or `conflict_owner` |
| `UNGOVERNED` [not governed] | none |

Consumers that claim SMF conformance **must not** present a guess as `RESOLVED`.

## 4. Reference resolution algorithm

Implementations may resolve however they like, as long as their results match the states. The reference algorithm (`reference/tools/smf.py resolve`) is:

1. **No rule for the term** (after checking aliases) → `UNGOVERNED`.
2. **Rule is deprecated** → `RESOLVED_VIA_REPLACEMENT` to `deprecated.replacement`.
3. **Contextual clauses:** a clause matches when every key in `when` equals the context value.
   - The most specific match (most keys) wins.
   - Equally specific matches with different outcomes → `CONFLICT`.
   - A clause either resolves (`resolve_to`) or returns a state (`NEEDS_CLARIFICATION`, `CONFLICT`, `UNGOVERNED`).
4. **No clause matches** → apply `default`.
5. **Resolved concept is superseded or retired with `replaced_by`** → `RESOLVED_VIA_REPLACEMENT`.
6. Attach the `perspective` of the selected metric contract, `constraints` from the metric contract (exclusions, valid dimensions, time semantics, grain) and `trust` (registration status, certification).

## 5. Conformance levels (draft)

| Level | A conforming implementation… |
| --- | --- |
| **Reader** | Parses and validates SMF documents |
| **Resolver** | Produces valid `ResolutionResult` documents using the five states |
| **Consumer** | Honors all five states: proceeds, discloses replacement, asks, discloses conflict, discloses ungoverned |
| **Tested consumer** | Publishes passing results for a declared set of `TestCase` documents |

## 6. Relationship to other specs

SMF does not redefine what other open specs already carry. See [docs/works-with.md](../../docs/works-with.md).

- Dataset-level contracts, AI `context` blocks and field synonyms: **ODCS / ODPS (Bitol)**
- Portable semantic models and metric expressions: **Apache Ossie**
- Lineage and run provenance: **OpenLineage**; `ClaimTrace.provenance` can point to an OpenLineage run
- Glossary and metadata type system: **Egeria**
- Concept mapping relations: **SKOS**
- Registration statuses: **ISO/IEC 11179-6**

## 7. Try it

```bash
pip install -r reference/tools/requirements.txt
python reference/tools/smf.py validate reference/examples/gross-margin --strict
python reference/tools/smf.py resolve reference/examples/gross-margin --term "gross margin" --context audience=leadership
python reference/tools/smf.py test reference/examples/gross-margin
```

## 8. Open questions

- Should `ResolutionRule` support ordered precedence in addition to specificity?
- Should `Context` support ranges (effective periods) natively?
- Should resolution states be proposed upstream as an ODCS extension and an OpenLineage facet?
