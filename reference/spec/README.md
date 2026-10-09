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

A folder of SMF documents may hold other files. The reference CLI reads a file as SMF only when at least one of its documents carries the `smf:` key or names an SMF `kind`; any other YAML or JSON file (a CI workflow, a tool's configuration, a data contract in another standard) is skipped and counted, and folders whose name starts with a dot are not walked. A document that names an SMF `kind` and omits `smf:` is an error, never a skip. See [where the files live](../README.md#where-the-files-live).

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
- Every row of the [one-page Metric Contract](../../templates/metric-contract.md) has a field. Beyond those above: `plain_words` ("In plain words"), `inclusions` and `exclusions` ("Includes / excludes"), `certified_for` and `not_certified_for` ("Approved for" / "Not approved for"), `effective_from`, `change_note`, and `sign_off {by, date}`. "Maintained by" is `Ownership.steward`. `Concept` carries `plain_words`, `change_note` and `sign_off` for the [Definition Contract](../../templates/definition-contract.md). All are optional.
- A **Definition Contract** is a set of documents: `Concept`, its `Perspective`s, `Term`s, `Ownership`, any `ClassificationRule`s and the `ResolutionRule` for the term.
- To link from an ODCS data contract to an SMF contract, use ODCS `authoritativeDefinitions` with type `businessDefinition`. In the other direction, a `MetricContract` lists the data contracts it is built on in `built_on`. For the business-level picture, see [docs/contracts-in-context.md](../../docs/contracts-in-context.md).
- A `Binding` names one implementation of a contract (`implementation.platform` and `ref`). It may carry an `id` so a `ClaimTrace` can name it. Two optional fields support Assurance: `implementation.derived_from` records the implementation a converter generated this one from, and `expression_snapshot` keeps the executable logic (or its SHA-256 digest) as it was when `conformance_status` was last assessed, so a tool can report drift instead of a reviewer re-reading the formula.
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

#### Field mapping: Apache Ossie metric and `MetricContract` (non-normative)

Apache Ossie is a draft interchange format (spec `0.2.0.dev0`; one model per document, no bundle or cross-model references). Its `metrics` entries carry `name`, `expression` (SQL per dialect), `description`, `datatype`, `ai_context` and `custom_extensions`. The table shows how each lines up with a `MetricContract`.

| Ossie metric field | `MetricContract` field | Note |
| --- | --- | --- |
| `name` | `id` / `name` | Ossie names are unique within one model only. SMF ids are namespaced and stable across models; record the Ossie name in a `Binding`, not as the SMF id |
| `expression.dialects[].expression` | `formula` | Ossie holds executable SQL; `formula` is the plain-words calculation that points at it. Ossie is "where it computes"; the contract is "where it agrees" |
| `description` | `name`, `measures.concept_ref` | Free text in Ossie; a concept reference in SMF |
| `datatype` | — | Not carried by SMF; stays in the implementation |
| `ai_context.synonyms` | `Term` documents | Ossie synonyms are per metric per model; SMF terms resolve per context with a `ResolutionRule` and the five states |
| `ai_context.instructions`, `ai_context.examples` | `ResolutionRule`, `TestCase` | Model-specific hints versus governed answer rules and checks that can be run |
| `custom_extensions[]` (`vendor_name`, JSON `data`) | — | The slot for a pointer back to the SMF contract; see the example below |
| — | `perspective` | Ossie has no perspective; two meanings of one metric are two unrelated metric names |
| — | `grain`, `valid_dimensions`, `filters`, `exclusions`, `time_semantics`, `additivity` | Implicit in the Ossie SQL and relationships; explicit and reviewable in SMF |
| — | `owner`, `certified_for`, `status`, `effective_from`, `version` | Ossie carries no ownership, approval, status or change history |
| — | `comparability` | Not representable in Ossie |
| — | `built_on` | Ossie datasets have a `source`; they do not reference data contracts |

Ossie model- and dataset-level `ai_context` also overlaps with ODCS 3.2 `context`: both are hints for one artifact. SMF is the cross-artifact layer for both.

#### Linking an Apache Ossie metric to an SMF contract (illustrative)

Ossie has no equivalent of ODCS `authoritativeDefinitions`; use a `custom_extensions` entry. The `vendor_name` and the keys inside `data` are a convention proposed here, not part of the Ossie spec.

```yaml
# Inside an Apache Ossie semantic model document
metrics:
  - name: product_gross_margin
    expression:
      dialects:
        - dialect: ANSI_SQL
          expression: (SUM(order_lines.product_revenue) - SUM(order_lines.landed_cost_of_goods)) / SUM(order_lines.product_revenue)
    description: Product Gross Margin (product perspective; see the SMF contract for approved uses and comparability)
    ai_context:
      instructions: "Governed by SMF contract product.gross_margin@v1. Not comparable with services.gross_margin."
    custom_extensions:
      - vendor_name: SMF
        data: '{"metric_contract": "product.gross_margin@v1", "perspective": "perspective.gross_margin.product"}'
```

In the other direction, a `Binding` records the Ossie model and metric as one implementation of the contract, alongside any BI measure or semantic-layer metric:

```yaml
smf: "0.1"
kind: Binding
subject: product.gross_margin@v1
implementation: { platform: ossie, ref: "sales_analytics/metrics/product_gross_margin" }
expression_snapshot:
  text: (SUM(order_lines.product_revenue) - SUM(order_lines.landed_cost_of_goods)) / SUM(order_lines.product_revenue)
  sha256: eb9475197f844c6cbf36b26528111818268eab92596a2f3fab3d149152768a9b
  captured_on: 2026-10-08
conformance_status: untested
```

Because Ossie is a hub format, the same contract will often have one Ossie binding and several bindings that a converter produced from it. Record that with `derived_from` so Assurance can test the hub once and treat the spokes as generated:

```yaml
smf: "0.1"
kind: Binding
subject: product.gross_margin@v1
implementation:
  platform: snowflake
  ref: "ANALYTICS.SEMANTIC.SALES_ANALYTICS / PRODUCT_GROSS_MARGIN"
  derived_from: { platform: ossie, ref: "sales_analytics/metrics/product_gross_margin" }
conformance_status: untested
```

Assurance then treats drift between the Ossie `expression` and the snapshot on its binding as a finding, as it does for any other binding. Whether the Ossie `expression` still matches the contract's plain-words `formula` remains a reviewer's call; the snapshot makes the drift check mechanical, not the judgement.

Sources:
- Apache Ossie core specification (`0.2.0.dev0`, draft): https://github.com/apache/ossie/blob/main/core-spec/spec.md

### Relationships across standards

The framework's [metamodel](../../docs/metamodel.md) draws the connections between data contracts, SMF documents, implementations and decisions. This table gives the field that records each connection. Where two standards record the same connection from opposite ends, both rows are listed; they must agree, and neither restates the other.

| Connection (plain name) | From | To | Field that records it | Owning spec |
| --- | --- | --- | --- | --- |
| built on | `MetricContract` | data contract | `MetricContract.built_on[]` | SMF |
| points to its business definition (same connection, other end) | ODCS field | `MetricContract` | `properties[].authoritativeDefinitions[]` with `type: businessDefinition` | ODCS 3.x |
| has | `Concept` | `Perspective` | `Perspective.concept_ref` | SMF |
| contains | `Perspective` | `Perspective` | `Perspective.broader_than[]` | SMF |
| measured by | `Perspective` | `MetricContract` | `MetricContract.perspective` (and `MetricContract.measures.concept_ref` to the concept) | SMF |
| what counts | `Concept` | `ClassificationRule` | `ClassificationRule.concept_ref`; `MetricContract.classification_rules[]` | SMF |
| comparable / not comparable with | `MetricContract` | `MetricContract` | `comparability.comparable_with[]`, `comparability.not_comparable_with[]`, `comparability.can_be_combined` | SMF |
| implemented in | `MetricContract` (or `Concept`) | implementation | `Binding.subject` → `Binding.implementation {platform, ref}` | SMF |
| generated into | implementation | implementation | `Binding.implementation.derived_from {platform, ref}` | SMF |
| as it was when last checked | `Binding` | expression | `Binding.expression_snapshot {text?, sha256, captured_on}`; `Binding.conformance_status` | SMF |
| points to its contract (same connection, other end) | Ossie metric | `MetricContract` | `metrics[].custom_extensions[]` with `vendor_name: SMF`, `data: {"metric_contract": "id@vN", ...}` (convention, not part of the Ossie spec) | Apache Ossie |
| selects | context | `ResolutionRule` clause | `ResolutionRule.contextual[].when` matched against the query `context`; `Context.conditions` names the contexts | SMF |
| applies to | `ResolutionRule` | `Concept` / `MetricContract` | `default` and `contextual[].resolve_to {concept, measurement}` | SMF |
| one of five answers | `ResolutionRule` | consumer | `ResolutionResult.state` with `basis`, `options`, `conflict_ref`, `replaces` | SMF |
| owned by | `Concept` / `Perspective` / `MetricContract` | person or role | `Ownership.subject` → `owner`, `steward`, `scope`; `Perspective.owner`; `MetricContract.owner`; approval in `sign_off {by, date}` on `MetricContract` and `Concept` | SMF |
| undecided | term | candidates | `Conflict.candidates[]`, `owner`, `target_date`; `ResolutionRule.contextual[].conflict_ref` | SMF |
| replaced by | `Concept` / term | `Concept` / `MetricContract` | `Concept.replaced_by`; `ResolutionRule.deprecated.replacement` | SMF |
| backed by | `ClaimTrace` | `MetricContract` version | `ClaimTrace.measurement` (`id@vN`), `ClaimTrace.concept` | SMF |
| computed by | `ClaimTrace` | implementation and run | `ClaimTrace.execution {binding, query_hash, executed_at}`, `sources[]`. `execution.binding` is a `Binding` id, or `<platform>:<ref>` matching a `Binding` in the set | SMF |
| run lineage (same connection, other end) | `ClaimTrace` | lineage run | `ClaimTrace.provenance {format: openlineage, ref}` | OpenLineage |
| tests | `TestCase` | consumer or resolver | `TestCase.input` / `expected`; consumer results keyed by test id | SMF |

The plain-language [gap catalogue](../../docs/gaps.md) lists what it means when one of these connections is missing. Most gaps can be found from the documents alone with the fields above; drift needs the implementation's current expression, and "check never run" needs a results file.

## 2. Identifiers

- Pattern: lowercase, dot-namespaced, at least two segments: `concept.customer`, `finance.net_revenue`.
- Version pin: `id@vN`, e.g. `finance.net_revenue@v3`.
- IDs are never derived from labels alone and never reused for a different meaning.
- A document may reference an ID defined elsewhere (another repo, a catalog). Validators warn about undefined references unless run in strict mode.
- A `ClaimTrace` names the build record that computed it in `execution.binding`, either by the `Binding`'s `id` or as `<platform>:<ref>`. A name that matches no `Binding` in the set is a warning, and an error in strict mode. A name that matches only build records of a different Metric Contract than the claim's `measurement` is an error.
- A reference must point at the right kind of document: a metric field names a `MetricContract`, a concept field names a `Concept`, a perspective field names a `Perspective`. A reference to a document of the wrong kind is an error, in strict mode or not.
- A term has at most one `ResolutionRule`, and one `Term` per context. A second rule for the same term, or two `Term` documents for the same term and context that map to different concepts, is a validation error. A resolver that finds more than one rule for a term returns `CONFLICT` rather than choosing one.

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

1. **No rule for the term** (after checking aliases) → `UNGOVERNED`. An alias is a `Term` that maps to a concept whose preferred term has a rule. Candidates are tried preferred terms first, then alphabetically, never in file order, and rules for deprecated terms are skipped.
2. **Rule is deprecated** → `RESOLVED_VIA_REPLACEMENT` to `deprecated.replacement`.
3. **Contextual clauses:** a clause matches when every key in `when` equals the context value. Values are compared as text and are case-sensitive; a YAML boolean compares as `true` or `false`. Context keys are free-form: the adopter chooses them (for example `business_area` or `audience`).
   - The most specific match (most keys) wins.
   - Equally specific matches with different outcomes → `CONFLICT`.
   - A clause either resolves (`resolve_to`) or returns a state (`NEEDS_CLARIFICATION`, `CONFLICT`, `UNGOVERNED`).
4. **No clause matches** → apply `default`.
5. **Resolved concept is superseded or retired with `replaced_by`** → `RESOLVED_VIA_REPLACEMENT`. If the replacement is itself superseded, follow the chain to the current concept.
6. Attach the `perspective` of the selected metric contract, `constraints` from the metric contract (exclusions, valid dimensions, time semantics, grain) and `trust` (registration status, certification).

## 5. Conformance levels (draft)

| Level | A conforming implementation… |
| --- | --- |
| **Reader** | Parses and validates SMF documents |
| **Resolver** | Produces valid `ResolutionResult` documents using the five states |
| **Consumer** | Honors all five states: proceeds, discloses replacement, asks, discloses conflict, discloses ungoverned |
| **Tested consumer** | Publishes passing results for a declared set of `TestCase` documents |

How `smf.py test` checks a consumer's results file (a mapping of test id to `ResolutionResult`):

- The file may only contain ids that match a `TestCase`; an unknown id is an error, so a misspelled id can never hide a failing case.
- Each result must be a valid `ResolutionResult`.
- `state` must match. `concept`, `measurement` and `perspective` must match when the case names them, and `options` must be the same set.
- A result must not use anything listed in `must_not`.
- Each name in `must_apply` must appear in the result's `constraints.exclusions`, which is where a result reports the exclusions of its Metric Contract.

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

`validate` and `test` print text by default. Add `--format json` for one JSON object with the same errors, warnings and counts, for use by other tools.

## 8. Open questions

- Should `ResolutionRule` support ordered precedence in addition to specificity?
- Should `Context` support ranges (effective periods) natively?
- Should resolution states be proposed upstream as an ODCS extension and an OpenLineage facet?
- Should Apache Ossie carry a native pointer to a governing definition (the equivalent of ODCS `authoritativeDefinitions`) instead of the `custom_extensions` convention above?
