# Example: Northwind (fictional)

A second, broader example showing deprecated terms, a declared conflict and an ungoverned term. For the flagship example, see `../gross-margin/`.

A complete, fictional example covering Revenue, Customer and Region. The company, systems and figures are invented.

| File | Contains |
| --- | --- |
| `contexts.yaml` | Named contexts |
| `concepts.yaml` | Concepts, including variants and a superseded concept |
| `terms.yaml` | Terms and aliases |
| `ownership.yaml` | Owners and scopes |
| `rules.yaml` | A classification rule, resolution rules and a declared conflict |
| `metrics.yaml` | Metric contracts |
| `bindings.yaml` | Implementation bindings, including a legacy shadow measure |
| `tests/golden-questions.yaml` | Assurance test cases |
| `claims.yaml` | A quantitative claim trace |

Try it:

```bash
python reference/tools/smf.py validate reference/examples/northwind
python reference/tools/smf.py resolve reference/examples/northwind --term revenue --context business_area=sales
python reference/tools/smf.py test reference/examples/northwind
```
