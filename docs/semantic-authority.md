# Semantic Authority (Practice 3)

**Status:** v0.5 working draft (detail for Practice 3)
**Type:** Practice detail, adoptable on its own
**Purpose:** Define how an organization establishes, scopes and resolves authoritative business meaning

> This is the most detailed practice page. YAML examples now live in [reference/](../reference/examples/semantic-authority-examples.md) for technical teams; the practice itself needs only named owners, written perspectives and recorded decisions.

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

- business area;
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

- is a;
- part of;
- associated with;
- variant of;
- replaced by;
- maps to.

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

A minimal practice needs seven objects, and the second one, Entity, is an optional refinement. Concept, Term and Context are defined in the [vocabulary](vocabulary.md). Machine-readable versions are in the [reference](../reference/spec/README.md).

### 6.1 Concept

A stable identity for a business meaning.

For example, Customer is given a stable ID and a one-sentence definition: a party with an established commercial relationship with the organization. See the [example](../reference/examples/semantic-authority-examples.md#61-concept).

### 6.2 Entity

An optional refinement, not a separate artifact: a concept with identity/key semantics.

For example, the Customer entity is tied to the Customer concept and describes the canonical organizational customer identity. See the [example](../reference/examples/semantic-authority-examples.md#62-entity).

Semantic Authority does not need to own the actual MDM records.

### 6.3 Term

A label or alias used by people/systems.

For example, "client" is recorded as a word that means Customer in a sales context. See the [example](../reference/examples/semantic-authority-examples.md#63-term).

### 6.4 Context

A named condition under which meaning or resolution may differ.

For example, external reporting is recorded as a named context. See the [example](../reference/examples/semantic-authority-examples.md#64-context).

### 6.5 Authority Assignment

Who can establish or approve meaning within a scope. In the [role and artifact list](roles-and-artifacts.md) this is the owner named for a concept or perspective.

For example, Customer is owned by Customer Operations and stewarded by Data Governance, across the whole enterprise. See the [example](../reference/examples/semantic-authority-examples.md#65-authority-assignment).

### 6.6 Resolution Rule

How ambiguity is resolved.

For example, "customer" means Customer by default, but means the support account when the question comes from support. See the [example](../reference/examples/semantic-authority-examples.md#66-resolution-rule).

### 6.7 Classification Rule

What counts as an instance of a concept.

For example, an Active Customer is one with at least one paid order in the trailing 365 days, as of the evaluation date. See the [example](../reference/examples/semantic-authority-examples.md#67-classification-rule).

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
- business-area meanings;
- explicit relationships;
- resolution rules.

This is better than forcing every business area into one overloaded object.

---

## 8. Canonical identity vs. local meaning

Example:

The term "Region" means different things to different parts of the business:

- In enterprise reporting, it means **Sales Region**.
- In Finance, it means **Legal Reporting Region**.
- In Operations, it means **Service Region**.

Semantic Authority should make these differences explicit.

It should not simply choose one and label the others "wrong."

---

## 9. Ownership model

This practice uses the seven roles defined in [roles and artifacts](roles-and-artifacts.md) and the [vocabulary](vocabulary.md). The ones that matter most here:

### Meaning owner

Has authority to approve what a concept or perspective means within a scope. Older material calls this the accountable owner.

### Steward

Maintains definitions, mappings, aliases and resolution metadata.

### Enterprise authority

Sets enterprise defaults and decides conflicts across business areas.

### Builder

Maintains implementation metadata where relevant. Older material calls this the technical custodian.

### Consumer owner

Is accountable for how a report suite or AI assistant uses the meaning, but does not control it.

Authority can be scoped by:

- enterprise;
- business area;
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

return one of the [five answers](vocabulary.md#the-five-answers): use it, use the replacement, ask, flag the conflict or not governed.

For example, asked for "revenue" in an executive context, the answer is "use it": Revenue, with the rule that decided it. See the [example](../reference/examples/semantic-authority-examples.md#10-resolution).

If two meanings are equally valid and no rule exists, the answer is **ask**.

The practice should prefer explicit ambiguity over silent guessing.

---

## 11. Relationship to Measurement Management

Measurement references meaning; it does not redefine it.

Semantic Authority owns the concept **Revenue**. Measurement Management owns the measures that point to it: **Net Revenue**, **Gross Revenue** and **Operational Revenue**.

Semantic Authority defines the concept identity, context and classification rules.

Measurement Management defines how that concept is measured.

For example, the Net Revenue measure points to Revenue as the concept it measures. See the [example](../reference/examples/semantic-authority-examples.md#11-relationship-to-measurement-management).

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
- business-area migrations;
- renamed or split concepts.

Detailed versioning practice is the Semantic Lifecycle Management practice.

---

## 15. Semantic mapping

Systems may implement local concepts.

Example:

A CRM calls it "Account", the ERP calls it "Sold-To" and Support calls it "Organization". All three are mapped to the one concept, **Customer**.

Semantic Authority may record and approve mappings. For example, the CRM's "Account" is mapped to Customer as a contextual match, not an exact one. See the [example](../reference/examples/semantic-authority-examples.md#15-semantic-mapping).

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

These are the same four outcomes listed under Semantic Authority in [practices](practices.md).

### Merge

Two definitions mean the same thing.

Merge them or record one as an alias.

### Keep both as perspectives

Both are valid in different contexts.

Keep both and define the answer rule that chooses between them.

### Record broader and narrower

One contains the other.

Record the relationship.

### Declare an open conflict

Do not fake consensus.

Flag the conflict, and assign an owner and a date.

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

A lightweight service could expose concepts, perspectives, owners and answer rules to tools and AI; see the [reference](../reference/examples/semantic-authority-examples.md#sample-api-shape-optional) for an illustrative API shape. It is optional, not required to adopt SMF.

---

## 20. Governance workflow

Minimal workflow:

1. Discover what the business already means by a term.
2. Define it.
3. Assign authority.
4. Resolve conflicts.
5. Certify and publish.
6. Version it.

Keep the workflow lightweight. Where an organization already has a governance council or stewardship workflow, run this inside it rather than beside it.

The practice should not require a governance board for every semantic change.

Use delegated business-area authority.

---

## 21. Operating model

Recommended pattern:

### Enterprise layer

Defines:

- shared concepts;
- global identifiers;
- default resolution;
- relationships across business areas.

### Business-area layer

Defines:

- business-area concepts;
- local aliases;
- contextual meaning;
- proposed mappings.

### Escalation

Only conflicts across business areas, or enterprise defaults, need centralized resolution.

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

Delegate authority by business area or context.

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
