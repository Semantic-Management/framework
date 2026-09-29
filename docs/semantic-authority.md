# Semantic Authority (Practice 3)

**Status:** v0.2 working draft (detail for Practice 3)
**Type:** Practice detail, adoptable on its own
**Purpose:** Define how an organization establishes, scopes and resolves authoritative business meaning

> This is the most detailed practice page. Sections with YAML examples are illustrations for technical teams; the practice itself needs only named owners, written perspectives and recorded decisions.

---

## 1. Summary

**Semantic Authority is the practice for deciding what business meaning is authoritative in a given organizational context.**

Its core questions are:

> **What does this concept mean here?**
> **Which concept does this term refer to?**
> **Who has authority over that meaning?**
> **In what context does a different meaning legitimately apply?**
> **How is ambiguity resolved?**

Semantic Authority governs things such as:

- concepts;
- entities;
- terminology;
- aliases;
- context;
- ownership;
- relationships;
- authority scope;
- classification rules;
- resolution rules.

It does **not** need to become a universal ontology, master-data platform, runtime semantic layer, or replacement for a catalog.

It is **not a required hub**. Other practices reference its outputs by stable ID when it exists, and use local references when it does not.

---

## 2. Relationship to the shared core and other practices

- The [vocabulary](vocabulary.md) defines term, concept, perspective, context and the five answers. Semantic Authority **uses** that vocabulary; it does not own it.
- Semantic Modeling (Practice 2) **represents** meaning; Semantic Authority **approves** it.
- Semantic Resolution (Practice 4) **applies** authority decisions at the moment of use.
- Measurement Management (Practice 5) **references** approved concepts and classification rules; it does not redefine them.

---

## 3. Ways to implement

An organization may implement this practice using:

- an existing catalog;
- a lightweight registry;
- a knowledge graph;
- Git-managed files;
- Apache Ossie-compatible semantic metadata;
- custom APIs;
- an existing data governance council and glossary.

The practice should not force new infrastructure.

---

## 4. Core scope

Semantic Authority owns the governance model for:

### Concepts

Abstract business meanings:

```text
Revenue
Customer
Product
Region
Order
Churn
Active Customer
```

### Entities

Things with identity:

```text
Customer entity
Product entity
Order entity
Employee entity
Facility entity
```

### Terms and aliases

Words people use:

```text
client
customer
account
subscriber
```

### Context

Meaning may depend on:

- domain;
- business unit;
- geography;
- audience;
- process;
- regulatory regime;
- application;
- time/effective period.

### Ownership

Who is accountable for authoritative meaning.

### Classification rules

Membership criteria that decide what counts as an instance of a concept (e.g., what makes a customer "Active"). These belong to meaning, not measurement.

### Resolution

How a consumer chooses among multiple legitimate meanings.

### Relationships

How concepts relate:

```text
is_a
part_of
associated_with
variant_of
deprecated_by
maps_to
```

---

## 5. What Semantic Authority does not own

Semantic Authority should not automatically absorb:

- metric formulas;
- KPI computation;
- analytical query execution;
- implementation conformance;
- data quality;
- master-data record management;
- access control;
- PII classification;
- generic technical lineage;
- AI testing;
- runtime claim provenance.

Measurement belongs to Measurement Management. Conformance belongs to Implementation and Assurance. AI testing and claim tracing belong to Assurance.

---

## 6. Primary objects

A minimal practice needs six objects. Concept, Term and Context are defined in the [vocabulary](vocabulary.md). Machine-readable versions are in the [reference](../reference/spec/README.md).

### 6.1 Concept

A stable identity for a business meaning.

```yaml
id: concept.customer
name: Customer
definition: >
  A party with an established commercial relationship
  with the organization.
```

### 6.2 Entity

A concept with identity/key semantics.

```yaml
id: entity.customer
concept_ref: concept.customer
identity_description: >
  Canonical organizational customer identity.
```

Semantic Authority does not need to own the actual MDM records.

### 6.3 Term

A label or alias used by people/systems.

```yaml
term: client
maps_to: concept.customer
context: sales
```

### 6.4 Context

A named condition under which meaning or resolution may differ.

```yaml
id: context.external_reporting
```

### 6.5 Authority Assignment

Who can establish or approve meaning within a scope.

```yaml
subject: concept.customer
authority:
  owner: Customer Operations
  steward: Data Governance
scope:
  domain: enterprise
```

### 6.6 Resolution Rule

How ambiguity is resolved.

```yaml
term: customer

default: concept.customer

contextual:
  - when:
      domain: support
    resolve_to: concept.support_account
```

### 6.7 Classification Rule

What counts as an instance of a concept.

```yaml
id: rule.active_customer.enterprise
concept_ref: concept.active_customer
criteria: >
  At least one paid order in the trailing 365 days,
  as of the evaluation date.
```

---

## 7. Two things can be true: authority is scoped, not global

A major principle:

> **Authoritative does not always mean globally singular.**

An organization may legitimately hold several **perspectives** on one concept, each with its own owner:

```text
Gross Margin
├── Product perspective       (owner: Product Line Lead)
├── Service perspective       (owner: Services Lead)
└── Consolidated perspective  (owner: Controller; enterprise default)
```

The same applies to entities such as Customer (commercial, billing, support, legal counterparty).

The practice should express:

- enterprise defaults for named contexts;
- domain-specific meanings;
- explicit relationships;
- resolution rules.

This is better than forcing every domain into one overloaded object.

---

## 8. Canonical identity vs. local meaning

Example:

```text
Term: "Region"

Enterprise reporting context:
concept.sales_region

Finance context:
concept.legal_reporting_region

Operations context:
concept.service_region
```

Semantic Authority should make these differences explicit.

It should not simply choose one and label the others "wrong."

---

## 9. Ownership model

Suggested roles:

### Accountable owner

Has authority to approve semantic meaning.

### Steward

Maintains definitions, mappings, aliases and resolution metadata.

### Technical custodian

Maintains implementation metadata where relevant.

### Consumer

Uses the meaning but does not control it.

Authority can be scoped by:

- enterprise;
- domain;
- geography;
- business process;
- effective period.

These roles can map onto existing data-governance roles (owner, steward, custodian) rather than create new ones.

---

## 10. Resolution

Resolution is one of the practice's most important outputs. It is applied at the moment of use by the Semantic Resolution practice.

Given:

```text
term + context
```

return one of the [five answers](vocabulary.md#the-five-answers): `RESOLVED`, `RESOLVED_VIA_REPLACEMENT`, `NEEDS_CLARIFICATION`, `CONFLICT` or `UNGOVERNED`.

Possible result:

```yaml
query:
  term: revenue
  context:
    audience: executive

result:
  state: RESOLVED
  concept: concept.revenue
  basis: rule.revenue.exec_default
```

If two meanings are equally valid and no rule exists:

```text
NEEDS_CLARIFICATION
```

The practice should prefer explicit ambiguity over silent guessing.

---

## 11. Relationship to Measurement Management

Measurement references meaning; it does not redefine it.

```text
Semantic Authority
concept.revenue
      │
      ▼
Measurement Management
finance.net_revenue
finance.gross_revenue
operations.operational_revenue
```

Semantic Authority defines the concept identity, context and classification rules.

Measurement Management defines how that concept is measured.

```yaml
metric:
  id: finance.net_revenue
  measures:
    concept_ref: concept.revenue
```

A measurement contract does not redefine Revenue as a concept.

---

## 12. The boundary test

Ask:

> **Is this about what something means, or how it is measured?**

And for membership:

> **Does it change which things count (meaning), or how they are counted (measurement)?**

| Question | Owning practice |
| --- | --- |
| What is a Customer? | Semantic Authority |
| Is "client" a synonym for Customer? | Semantic Authority |
| Which Region concept applies to Finance? | Semantic Authority (rule) / Resolution (applied) |
| Who owns the Product concept? | Semantic Authority |
| What counts as an Active Customer? | Semantic Authority (classification rule) |
| How many Active Customers did we have? | Measurement Management |
| What is Net Revenue? | Measurement Management, as a contract referencing Revenue |
| Which exclusions apply to Net Revenue? | Measurement Management |
| Which Power BI measure implements Net Revenue? | Semantic Implementation |
| Does that measure still conform? | Semantic Implementation (status) / Assurance (test) |
| Can the AI answer Net Revenue questions? | Semantic Assurance |
| Can this $39.8M answer be traced? | Semantic Assurance (claim tracing) |

This table is the practical scope guardrail.

---

## 13. Semantic objects vs. metric contracts

Avoid using one overloaded "semantic contract" object for everything.

### Semantic Authority object

Defines:

```text
meaning
identity
context
relationships
ownership
classification rules
resolution
```

### Metric contract (Measurement Management)

Defines:

```text
measurement
formula/components
grain
dimensions
filters/exclusions
time semantics
variants
certification
```

The linkage is by stable reference.

---

## 14. Effective dating

Meaning can change.

Example:

```text
Customer definition v2
effective 2027-01-01
```

Historical meaning should remain accessible.

Effective dates are especially important for:

- reorganizations;
- regulatory definitions;
- acquisitions;
- domain migrations;
- renamed or split concepts.

Detailed versioning practice is the Semantic Lifecycle Management practice.

---

## 15. Semantic mapping

Systems may implement local concepts.

Example:

```text
CRM "Account"
ERP "Sold-To"
Support "Organization"
        │
        ▼
concept.customer
```

Semantic Authority may record and approve mappings:

```yaml
source:
  system: crm
  object: Account

maps_to:
  concept: concept.customer

mapping_type: contextual
```

It should not automatically claim perfect equivalence.

Mapping types might include:

```text
equivalent
subset
superset
contextual
approximate
legacy
unknown
```

These align with SKOS mapping relations where possible (see Semantic Interchange). This is broader than a metric binding because it applies to concepts, not measurements.

---

## 16. Conflict handling

Conflicts can resolve in several ways.

### Duplicate

Two definitions mean the same thing.

Merge or alias.

### Contextual distinction

Both are valid in different contexts.

Keep both and define resolution.

### Hierarchical distinction

One is broader/narrower.

Record relationship.

### Unresolved disagreement

Do not fake consensus.

State:

```text
CONFLICT
```

and assign an owner.

---

## 17. Catalog relationship

Semantic Authority should not replace a catalog.

A catalog may remain the home for:

- assets;
- glossary UI;
- stewardship workflow;
- lineage;
- classification.

Semantic Authority is the governing model that can be implemented in or synchronized with those systems.

For some organizations, the existing catalog may be sufficient to host the practice.

That is acceptable.

---

## 18. Apache Ossie

Ossie can serve as semantic interchange where its model fits.

Potential uses:

- import semantic concepts/relationships;
- export portable metadata;
- connect Semantic Authority to analytical tools.

Do not make the practice's governance model dependent on Ossie.

Governance includes authority, context, conflict and resolution behavior that go beyond an interchange specification. Ossie currently omits trust metadata such as verification and approval records (see [research/landscape.md](research/landscape.md)).

---

## 19. API shape

A lightweight authority service could expose:

```text
GET /concepts/{id}
GET /entities/{id}
GET /terms/{term}/resolve
GET /contexts/{id}
GET /authority/{id}
GET /relationships/{id}
```

Resolution:

```text
resolve(term, context) → state + concept + basis
```

This API is optional infrastructure, not a requirement for adoption.

---

## 20. Governance workflow

Minimal workflow:

```text
DISCOVER
   ↓
DEFINE
   ↓
ASSIGN AUTHORITY
   ↓
RESOLVE CONFLICT
   ↓
CERTIFY / PUBLISH
   ↓
VERSION
```

Keep the workflow lightweight. Where an organization already has a governance council or stewardship workflow, run this inside it rather than beside it.

The practice should not require a governance board for every semantic change.

Use delegated domain authority.

---

## 21. Operating model

Recommended pattern:

### Enterprise layer

Defines:

- shared concepts;
- global identifiers;
- default resolution;
- cross-domain relationships.

### Domain layer

Defines:

- domain-specific concepts;
- local aliases;
- contextual meaning;
- proposed mappings.

### Escalation

Only cross-domain conflicts or enterprise defaults need centralized resolution.

This avoids turning Semantic Authority into centralized bureaucracy. It fits naturally with domain-oriented models such as data mesh.

---

## 22. Practice success criteria

Semantic Authority is working when:

- important concepts have stable IDs;
- conflicting meanings are explicit;
- context-specific meanings are documented rather than hidden;
- authority is assigned;
- consumers can resolve ambiguous terms deterministically or receive a clarification state;
- other practices can reference concepts without recreating them.

Avoid vanity goals such as cataloging every business noun.

---

## 23. Risks

### It becomes an ontology project

Mitigation:

Start only with concepts that create real ambiguity or downstream governance value.

### It duplicates the catalog

Mitigation:

Use the catalog as a host/integration when possible.

### It becomes centralized bureaucracy

Mitigation:

Delegate authority by domain/context.

### It absorbs measurement

Mitigation:

Use the boundary test:

> **Meaning → Semantic Authority. Measurement → Measurement Management.**

### It becomes a required hub

Mitigation:

Keep stable references and integrations optional. Every other practice must keep a standalone mode using local references.

---

## 24. Core message

> **Semantic Authority is the practice for deciding what business meaning is authoritative, who owns it, and how context-dependent ambiguity is resolved.**

And its relationship to measurement is:

> **Semantic Authority governs meaning. Measurement Management governs measurement.**
