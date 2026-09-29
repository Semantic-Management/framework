<!-- SPDX-License-Identifier: Apache-2.0 -->
# Semantic Authority: YAML Examples

**Type:** Non-normative

These are illustrations for technical teams. Each heading matches a section of [Semantic Authority](../../docs/semantic-authority.md). They are sketches, not files the reference CLI validates. For the file format itself, see the [specification](../spec/README.md).

## 6.1 Concept

A stable identity for a business meaning.

```yaml
id: concept.customer
name: Customer
definition: >
  A party with an established commercial relationship
  with the organization.
```

## 6.2 Entity

A concept with identity and key semantics.

```yaml
id: entity.customer
concept_ref: concept.customer
identity_description: >
  Canonical organizational customer identity.
```

## 6.3 Term

A label or alias used by people and systems.

```yaml
term: client
maps_to: concept.customer
context: sales
```

## 6.4 Context

A named condition under which meaning or resolution may differ.

```yaml
id: context.external_reporting
```

## 6.5 Authority Assignment

Who can establish or approve meaning within a scope.

```yaml
subject: concept.customer
authority:
  owner: Customer Operations
  steward: Data Governance
scope:
  domain: enterprise
```

## 6.6 Resolution Rule

How ambiguity is resolved.

```yaml
term: customer

default: concept.customer

contextual:
  - when:
      domain: support
    resolve_to: concept.support_account
```

## 6.7 Classification Rule

What counts as an instance of a concept.

```yaml
id: rule.active_customer.enterprise
concept_ref: concept.active_customer
criteria: >
  At least one paid order in the trailing 365 days,
  as of the evaluation date.
```

## 10. Resolution

A possible result of resolving a term in context.

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

## 11. Relationship to Measurement Management

A metric that references the concept it measures, without redefining it.

```yaml
metric:
  id: finance.net_revenue
  measures:
    concept_ref: concept.revenue
```

## 15. Semantic mapping

A mapping from a local system's object to a concept.

```yaml
source:
  system: crm
  object: Account

maps_to:
  concept: concept.customer

mapping_type: contextual
```
