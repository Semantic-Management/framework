# Research Agenda

The framework should be developed with explicit comparison to adjacent disciplines rather than assuming novelty.

**Type:** Non-normative

## Primary research question

> Does an established framework already provide a comparable operating model for managing organizational meaning across authority, contextual resolution, measurement, implementation, machine consumption, assurance and lifecycle, as independently adoptable practices?

## Initial findings (v0.2, 2026-09-28)

Sourced detail: [research/landscape.md](research/landscape.md). Citations: [research/bibliography.md](research/bibliography.md).

- **No reviewed framework covers this as composable practices.** Each concern has established prior art, but no single work combines them in a form that can be adopted piece by piece.
- **Scoped meaning is established, not new:** Domain-Driven Design bounded contexts, SBVR semantic/speech communities, Business Semantics Management, ISO/IEC 11179 contexts. SMF should cite these.
- **Registration status and lifecycle:** ISO/IEC 11179-6 statuses exist and can be adopted.
- **Mapping relations:** SKOS exact/close/broad/narrow/related match can be adopted.
- **Metric representation is served by technology** (Apache Ossie, dbt MetricFlow, vendor semantic layers), not by vendor-neutral frameworks.
- **Interchange omits trust metadata:** Apache Ossie does not carry confidence, lineage, freshness, provenance or approval records.
- **Closest open peer:** EKGF Maturity Model (CC BY-SA). It is knowledge-graph-centric and maturity-scored, not modular.
- **Least covered areas, and candidate contributions:**
  - explicit resolution states for AI consumers;
  - interpretation assurance (testing whether a consumer used meaning correctly);
  - independently adoptable practices sharing one small core.
- **Naming:** "Semantic Authority" is widely used as an SEO/AEO term, which may hurt discoverability.

## Adjacent areas to map

Research and compare:

- data governance / DAMA;
- semantic governance;
- business glossary practices;
- ontology governance;
- knowledge graph governance;
- semantic web standards;
- semantic interoperability;
- enterprise architecture;
- semantic layers;
- metric layers / metrics stores;
- data contracts;
- data product operating models;
- master data management;
- metadata management;
- knowledge management;
- AI governance;
- model governance;
- AI grounding / context engineering;
- semantic testing and evaluation;
- provenance and claim verification.

## Interoperability targets

Beyond prior art, identify how each practice plugs into frameworks organizations already run:

| Framework / model | Practices most affected |
| --- | --- |
| DAMA-DMBOK-based governance programs | Authority, Modeling, Discovery |
| Data mesh / data product operating models | Authority, core IDs |
| Data contracts (ODCS) | Measurement, Implementation |
| ISO/IEC 42001, NIST AI RMF | Assurance |
| IT service management (incident, change) | Assurance, Lifecycle |
| Enterprise architecture | Modeling, Implementation |
| ISO/IEC 11179 registries | Modeling, Lifecycle |

## Comparison dimensions

For each adjacent framework or standard, determine whether it addresses:

| Dimension | Question |
| --- | --- |
| Meaning | Does it govern business concept definitions? |
| Identity | Does meaning have stable identifiers? |
| Authority | Does it specify who can establish meaning? |
| Scope | Can authority vary by business area or context? |
| Resolution | Can a term be deterministically resolved in context? |
| Ambiguity | Is unresolved ambiguity an explicit state? |
| Relationships | Can concepts and variants be related? |
| Measurement | Does it govern metric contracts? |
| Implementation | Does it bind meaning to technical implementations? |
| Interchange | Can semantics move across systems? |
| Machine consumption | Is the model designed for AI/application consumption? |
| Assurance | Can semantic use be tested? |
| Claim tracing | Can quantitative outputs be traced? |
| Lifecycle | Are versioning/effective dating supported? |
| Modularity | Can parts be adopted independently? |
| Operating model | Are roles, practices and workflows defined? |

## Novelty discipline

Do not claim that SMF:

- invents semantic governance;
- invents semantic intelligence;
- invents contextual semantics;
- invents ontologies or semantic layers;
- is the first framework for organizational meaning.

Potential differentiation should instead be evaluated around the **integration and composable operating model** across these concerns.

## Research outputs

1. landscape map (started: `research/landscape.md`);
2. framework comparison matrix;
3. terminology collision analysis;
4. gaps/overlaps;
5. standards and framework interoperability map;
6. bibliography (started: `research/bibliography.md`);
7. revised framework boundaries based on findings.
