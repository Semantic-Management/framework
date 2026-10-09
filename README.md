# Semantic Management Framework (SMF)

**An open, technology-independent operating model for managing business meaning across people, data, analytics and AI.**

Status: v0.5 working draft · **Looking for reviewers and worked examples** ([where to start](CONTRIBUTING.md#where-to-start)) · Website: [semantic-management.github.io/framework](https://semantic-management.github.io/framework/) · [github.com/Semantic-Management/framework](https://github.com/Semantic-Management/framework) · License: [CC BY 4.0](LICENSE-docs) for the framework, [Apache-2.0](LICENSE) for the reference code ([details](LICENSING.md))

---

## The missing discipline

Organizations already have disciplines for managing the important things they depend on:

| Discipline | Thing being managed |
| --- | --- |
| ITSM / ITIL | IT services |
| DAMA / Data Governance | Data |
| TOGAF | Enterprise architecture |
| COBIT | IT governance and control |
| MDM | Master entities and records |
| Model Risk Management | Analytical models |
| AI Governance | AI systems |
| **Semantic Management (SMF)** | **Business meaning** |

Business meaning is what a number or a term actually *means* to the people and systems that use it. It has no discipline of its own. It lives in glossaries, report footnotes, semantic layers, spreadsheets and people's heads. Now that analytics and AI sit at the foundation of decision-making, that gap shows up as conflicting numbers, confused leaders and AI tools that answer confidently with the wrong meaning.

> **Semantic Management** is the discipline of intentionally managing organizational meaning across its lifecycle, from definition and authority through contextual resolution, measurement, implementation, exchange, consumption, assurance and evolution.

> **The Semantic Management Framework** is a technology-independent operating model of principles, practices, roles, artifacts and lifecycle activities for managing organizational meaning across people, data, analytics and AI.

## Two things can be true

Ask a product leader and a services leader for **gross margin**. Both answer confidently, both are right, and they are talking about different things:

- **Product gross margin:** revenue minus the landed cost of goods (materials, freight, duties).
- **Service gross margin:** revenue minus technician labor, subcontractors and parts.
- **Consolidated gross margin:** what Finance reports to the board.

The formulas even look alike. But "cost" means something different in each, and the numbers can't be averaged together.

SMF doesn't force one answer. It treats each as a legitimate **perspective** with its own owner and its own **Metric Contract**, and it makes one rule explicit:

> **Context selects the perspective. When context can't, ask.**

That rule works the same way for a leader in a meeting, an analyst building a report, and an AI assistant answering a question. See the full [gross margin example](docs/examples/gross-margin.md).

## What SMF gives you

- **A shared vocabulary** for meaning: term, concept, perspective, context, Metric Contract. See the [vocabulary](docs/vocabulary.md).
- **Principles**, starting with *two things can be true*. See the [principles](docs/principles.md).
- **The lifecycle of a meaning**, from definition to evolution. See the [lifecycle](docs/lifecycle.md).
- **Nine practices**, each adoptable on its own, at any size. See the [practices](docs/practices.md).
- **Semantic Contracts**, SMF's signature artifacts:
  - the **Metric Contract**, a one-page agreement on what a number means, who owns it, where it can be used and what it can be compared with ([Metric Contract](docs/metric-contract.md));
  - the **Definition Contract**, the same for business terms like Customer.
  They sit alongside data contracts and metric catalogs rather than replacing them ([contracts in context](docs/contracts-in-context.md)).
- **Clear hand-offs** to the disciplines you already run. See [the discipline](docs/discipline.md).

## Built to plug gaps, not compete

SMF does **not** compete with the following:

- catalogs;
- semantic layers;
- metric stores;
- knowledge graphs;
- ontologies;
- governance platforms.

They are **implementation technologies** for SMF practices. SMF also works **with** your existing frameworks, whether that's DAMA governance, data mesh, IT service management or AI governance. You can run them together, separately, or use SMF for a single function. See [works-with.md](docs/works-with.md).

## Start here

| If you are… | Read |
| --- | --- |
| A business or analytics leader | [The discipline](docs/discipline.md) → [Gross margin example](docs/examples/gross-margin.md) → [Getting started](docs/getting-started.md) |
| A governance or data leader | [Framework overview](docs/framework.md) → [Practices](docs/practices.md) → [Works with](docs/works-with.md) |
| A finance or metric owner | [Metric Contract](docs/metric-contract.md) → [template](templates/metric-contract.md) |
| A data platform or catalog owner | [Contracts in context](docs/contracts-in-context.md) → [Works with](docs/works-with.md) |
| An engineer or AI team | [Reference](reference/README.md): schemas, examples and a CLI to test AI answers |

## Repository map

```text
/
├── README.md
├── docs/
│   ├── framework.md          overview of the operating model
│   ├── discipline.md         the missing discipline and hand-offs to neighbors
│   ├── principles.md         "Two things can be true" and the rest
│   ├── vocabulary.md         term, concept, perspective, context, Metric Contract…
│   ├── lifecycle.md          the lifecycle of a meaning
│   ├── practices.md          nine practices, adoptable on their own
│   ├── metric-contract.md    the signature artifact
│   ├── contracts-in-context.md  data contracts, metric catalogs and SMF contracts
│   ├── roles-and-artifacts.md
│   ├── getting-started.md    by size: small, mid-size, enterprise
│   ├── works-with.md         tools and frameworks SMF plugs into
│   ├── metamodel.md          a model of the models: how the standards connect
│   ├── gaps.md               the connections that should exist and don't
│   ├── examples/gross-margin.md
│   ├── semantic-authority.md, ai-governance-evidence.md, roadmap.md
│   ├── research-agenda.md    open research questions
│   ├── patterns/             reference implementation patterns
│   └── research/             prior art and bibliography
├── templates/                Metric Contract, Definition Contract, answer table
├── reference/                technical: spec, schemas, examples, CLI
├── site/ · mkdocs.yml        the website (built with MkDocs, published to GitHub Pages)
├── prompts/                  starter prompt for AI assistants working on this repository
├── AGENTS.md · CLAUDE.md     instructions for AI assistants and the local checks
├── .github/                  issue templates, pull request template, workflows
├── LICENSE (Apache-2.0) · LICENSE-docs (CC BY 4.0) · NOTICE · LICENSING.md
└── GOVERNANCE.md · CONTRIBUTING.md · CODE_OF_CONDUCT.md · CHANGELOG.md
```

## Status

SMF is early working material, not an established standard. It does not claim to invent semantic governance; it builds on established work (see [research](docs/research/landscape.md)). Challenges, prior art and field experience are welcome: see [CONTRIBUTING.md](CONTRIBUTING.md).

What would help most right now: someone who has lived "three gross margins" reviewing one page and saying where it is wrong, and worked examples from outside finance. The open issues labelled `help wanted` are each one scoped deliverable.
