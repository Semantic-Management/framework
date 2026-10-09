# Reference (technical)

**You do not need anything in this folder to adopt SMF.** The framework is in [`docs/`](../docs/framework.md) and is written for business and analytics leaders.

This folder is for technical teams that want to put SMF artifacts into tools, semantic layers and AI systems.

| Folder | Contains |
| --- | --- |
| [`spec/`](spec/README.md) | File format for SMF artifacts: JSON Schemas, identifier rules, the five answers, the reference answer algorithm |
| [`examples/gross-margin/`](examples/gross-margin/README.md) | Flagship example: Gross Margin with product, service and consolidated perspectives |
| [`examples/northwind/`](examples/northwind/README.md) | Broader example: deprecated terms, a declared conflict, an ungoverned term |
| [`examples/consumer-results/`](https://github.com/Semantic-Management/framework/tree/main/reference/examples/consumer-results) | Sample AI assistant answers for testing (each fails one check on purpose) |
| [`tools/`](tools/smf.py) | Reference CLI: `validate`, `resolve`, `test`, `import-csv` |

```bash
pip install -r reference/tools/requirements.txt
python reference/tools/smf.py resolve reference/examples/gross-margin --term "gross margin" --context audience=leadership
python reference/tools/smf.py test reference/examples/gross-margin --results reference/examples/consumer-results/gross-margin-assistant.yaml
```

## Where the files live

SMF documents are plain files. They can sit in their own folder, or beside other things in a repository: the reference CLI reads only SMF documents and skips the rest.

A layout that works, with the documents next to what they connect to:

```text
<repository or shared folder>/
├── smf/               SMF documents (concepts, perspectives, Metric Contracts, answer rules, checks)
├── data-contracts/    data contracts the Metric Contracts are built on (for example ODCS)
├── models/            interchange models (for example Apache Ossie)
└── results/           answers captured from reports and AI assistants, for `test --results`
```

Point the CLI at `smf/`, or at the top folder:

```bash
python reference/tools/smf.py validate . --strict
```

- A YAML or JSON file with no SMF document in it is skipped, and the summary line says how many were.
- Folders whose name starts with a dot (`.git`, `.github`) are not read.
- A document that names an SMF `kind` and leaves out `smf:` is reported as an error. It is never skipped.
- An empty folder, or one with no SMF documents, is an error: a mistyped path can never read as a pass.
