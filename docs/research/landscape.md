# Landscape: Sourced Findings

**Type:** Non-normative

**Status:** v0.2 (2026-09-28)

This file keeps **sourced findings** separate from SMF proposals. Each entry states what the work is, what it covers that matters to SMF, and what it leaves out. Citations are in [bibliography.md](bibliography.md).

---

## Operating and management frameworks

### ITIL 4
- Service management framework (PeopleCert/AXELOS).
- **Relevant to SMF:** an interoperability target, not a model to copy. Semantic Assurance failures and definition changes can flow into existing ITSM incident and change processes.
- **Gap:** the managed object is IT services. Business meaning is not a managed object.

### DAMA-DMBOK
- Data management body of knowledge (DAMA International). Version 2 is current; the v3.0 project kicked off in June 2025 and aims to incorporate AI, cloud and modern data platforms. [DAMA 3.0]
- **Relevant:** data governance, metadata management, reference and master data, stewardship roles.
- **Gap:** organized as knowledge areas; not designed as independently adoptable practices. No explicit resolution or interpretation assurance. Commercially published.

### EDM Council DCAM
- Capability assessment model for data management programs.
- **Relevant:** governance and authority structures, capability scoring.
- **Gap:** assessment of data management capability, not an operating model for meaning.

### ISO/IEC 42001 and NIST AI RMF
- AI management system standard and AI risk framework.
- **Relevant:** accountability, testing/evaluation, lifecycle governance of AI systems. Semantic Assurance can supply semantic test evidence to these.
- **Gap:** neither treats business meaning as a governed object.

## Semantic standards and methods

### ISO/IEC 11179 (metadata registries)
- Registration-based model for metadata items with registration authorities, stewardship and submission roles.
- Part 6 defines registration statuses. Lifecycle statuses: Incomplete, Candidate, Recorded, Qualified, Standard, Preferred Standard, Retired, Superseded. Documentation statuses: Historical, Application. [NSW MDR]
- **Relevant:** authority, identity and lifecycle status model SMF should adopt rather than reinvent.
- **Gap:** no contextual resolution or consumer assurance.

### OMG SBVR and the semantic/speech community distinction
- SBVR (OMG) separates meanings (concepts) from their expressions (designations), enabling multilingual and multi-vocabulary models. [SBVR]
- The SBVR-aligned lexicon distinguishes a **semantic community** (shares understanding of concepts, not necessarily the same terms) from a **speech community** (also shares the same terms). [BRC Lexicon]
- **Relevant:** direct prior art for "concept vs. term" and scoped vocabulary.

### W3C SKOS
- Vocabulary for concept schemes: preferred/alternative labels and mapping relations (exactMatch, closeMatch, broadMatch, narrowMatch, relatedMatch).
- **Relevant:** SMF mapping types should align with SKOS where possible.

### Domain-Driven Design
- Bounded contexts make meaning explicitly local to a model and team. Context maps describe relationships between contexts (e.g., shared kernel, anti-corruption layer, published language).
- **Relevant:** strongest prior art for "authoritative does not mean globally singular."

### Business Semantics Management
- Research-derived method (VUB STARLab; De Leenheer, Meersman) with two cycles: semantic reconciliation among communities, and semantic application committing information systems to agreed patterns. [BSM]
- **Relevant:** closest historical precursor to SMF's discover, define, authority and bind flow. Associated with the origins of Collibra.

### FAIR-IMPACT semantic artefact governance
- Governance and management framework for semantic artefacts in research: lifecycle phases (conceptualization, encoding, publication, maintenance), 18 governance aspects, organizational role domains, versioning and deprecation. [FAIR-IMPACT]
- **Relevant:** a working example of an operating model for semantic artefacts, but for research communities, not enterprises.

### EKGF Maturity Model
- Open maturity model (CC BY-SA 4.0) from the Enterprise Knowledge Graph Foundation, an OMG-managed community. Four pillars (business, organization, data, technology), five maturity levels, and explicit positioning as grounding for generative AI. [EKGF]
- **Relevant:** closest open peer. Useful structural reference for an SMF maturity model.
- **Gap:** assumes knowledge graphs as the vehicle; maturity scoring rather than adoptable practices.

## Representation and technology

### Apache Ossie (formerly Open Semantic Interchange)
- Apache incubating spec for exchanging semantic models across analytics, AI and BI platforms. [Ossie]
- Core building blocks: datasets, fields, relationships, metrics; `ai_context` hints; custom extensions. [Datapace]
- Omits trust metadata: confidence, lineage, freshness, provenance, verification/approval records. [Datapace]
- Industry commentary argues portability and governance are distinct problems: the format describes a metric but does not govern or execute it. [Strategy]
- Spec `0.2.0.dev0` (draft): one model per document, no bundle or cross-model references; a metric is `name`, `expression` (SQL per dialect), `description`, `datatype`, `ai_context` (instructions, synonyms, examples) and `custom_extensions` (vendor name plus a JSON string). [Ossie spec]
- No field for owner, approval, status, effective date, perspective, comparability or data-contract links; two meanings of one metric can only be two metric names. [Ossie spec]
- **Relevant:** preferred interchange target; SMF governance lives above it. Field-level mapping and a linking convention are in the [reference](../../reference/spec/README.md).
- **Gap:** `ai_context` hints are per model, so cross-model agreement (which perspective, when to ask) has nowhere to live inside the format; `custom_extensions` is the only slot for a pointer out.

### Open Data Contract Standard (ODCS)
- Bitol (Linux Foundation) specification for data contracts; v3 documented. [ODCS]
- **Relevant:** reference for dataset-level contracts and implementation bindings.

### dbt Semantic Layer / MetricFlow and similar
- Metric definition and query generation technology with entities, measures, metrics and dimensions.
- **Relevant:** common implementation target for SMF measurement contracts.

### Vendor agent context layers
- Example: Snowflake describes an "agent context layer" combining semantic models, ontology/identity layers, operational playbooks, provenance and decision memory, with explicit attention to disambiguation and confident wrong answers. [Snowflake]
- **Relevant:** confirms market demand for resolution and provenance for agents.
- **Gap:** platform architecture, not a vendor-neutral operating model; limited treatment of roles and testing.

### W3C PROV
- Provenance data model. **Relevant:** substrate for claim assurance records.

## LF AI & Data Foundation projects (reviewed 2026-09-28)

Source: [LF AI & Data projects](https://lfaidata.foundation/projects/).

### Egeria (incubation)
- Open metadata and governance type system, APIs and interchange protocols (Apache-2.0).
- Glossary terms with synonyms, preferred and replacement terms, IsA, and `UsedInContext`, which "distinguish[es] between terms that have the same name but different meanings depending on the context." Semantic assignment links terms to implementations. [Egeria]
- **Relevant:** closest prior art for SMF's Modeling practice and for context-dependent meaning. A natural store for SMF documents.
- **Gap:** a metadata model, not resolution behavior or consumer testing.

### Bitol: ODCS and ODPS (incubation)
- ODCS v3.2.0 and ODPS v1.1.0 (released 2026-09-08) add a `context` block with instructions, verified statements and constraints for AI agents; `semanticType` (column, measure, dimension); synonyms; enums; a `deprecated` flag. [ODCS 3.2]
- **Relevant:** strong overlap with SMF's context package at the dataset level. SMF should reference ODCS rather than duplicate it.
- **Gap:** dataset-scoped; no cross-dataset concepts, classification rules, scoped authority, conflicts or resolution states.

### OpenLineage and Marquez (incubation)
- Open lineage standard and API; custom facets (with `_producer` and `_schemaURL`) can attach to runs, jobs and datasets. [OpenLineage facets]
- **Relevant:** provenance substrate for `ClaimTrace`; candidate home for an SMF semantic facet.

### Monocle (sandbox)
- Tracing framework for GenAI applications. [Monocle]
- **Relevant:** source of agent traces to check against SMF `TestCase` expectations.

### Unity Catalog OSS (sandbox)
- Open catalog for data and AI. Metric views are Databricks-platform features, not part of the open-source project; no semantic layer shipped Ossie import/export as of August 2026. [Atlan UC]
- **Relevant:** possible host for SMF documents and discovery.

### Amundsen (graduated)
- Data discovery and metadata engine. **Relevant:** Discovery practice harvesting source.

### OpenSharing (Linux Foundation, launched 2026-06-10)
- Open protocol for sharing data and AI assets, including agent skills, contributed by Databricks. [OpenSharing]
- **Relevant:** possible cross-organization carrier for semantic context (Interchange).

### Agent frameworks: BeeAI (incubation), RYOMA (sandbox), Open Platform for Enterprise AI (sandbox)
- **Relevant:** realistic SMF consumers to test resolution and clarification behavior. [RYOMA]

### DataPractices (graduated)
- Manifesto of values and principles for data teamwork. **Relevant:** precedent for a principles-first open framework hosted by LF AI & Data.

## Naming collisions checked

- "SemOps" / "Semantic Operations Framework" is used by SemOps.ai (an AI technology offering) and by Semantic Arts.
- "Open Semantic Contracts" was considered and set aside (v0.3): it described one component, not the discipline.
- "Semantic Management Framework" is the chosen name. A formal name and trademark check is still to be done.
- Related but distinct: Apache Ossie (formerly Open Semantic Interchange), ODCS, and the `semantic-mesh` GitHub project (domain contracts), which has not yet been reviewed in detail.
- "MetricProof" is an existing MIT-licensed package (AtomicGlance).

## Market signals (non-authoritative)

- "Semantic drift" and "context drift" are now common vendor terms for AI failure modes (e.g., AtScale, Atlan). [AtScale] [Atlan]
- These describe the symptom Semantic Assurance addresses, without defining an operating model for it.
