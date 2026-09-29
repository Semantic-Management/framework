# Reference (technical)

**You do not need anything in this folder to adopt SMF.** The framework is in [`docs/`](../docs/framework.md) and is written for business and analytics leaders.

This folder is for technical teams that want to put SMF artifacts into tools, semantic layers and AI systems.

| Folder | Contains |
| --- | --- |
| [`spec/`](spec/README.md) | File format for SMF artifacts: JSON Schemas, identifier rules, the five answers, the reference answer algorithm |
| [`examples/gross-margin/`](examples/gross-margin/README.md) | Flagship example: Gross Margin with product, service and consolidated perspectives |
| [`examples/northwind/`](examples/northwind/README.md) | Broader example: deprecated terms, a declared conflict, an ungoverned term |
| [`examples/consumer-results/`](examples/consumer-results/) | Sample AI assistant answers for testing (each fails one check on purpose) |
| [`tools/`](tools/smf.py) | Reference CLI: `validate`, `resolve`, `test`, `import-csv` |

```bash
pip install -r reference/tools/requirements.txt
python reference/tools/smf.py resolve reference/examples/gross-margin --term "gross margin" --context audience=leadership
python reference/tools/smf.py test reference/examples/gross-margin --results reference/examples/consumer-results/gross-margin-assistant.yaml
```
