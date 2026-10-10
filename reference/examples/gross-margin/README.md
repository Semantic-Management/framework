# Example: Gross Margin, Three Perspectives

**Fictional company:** Lakeview Supply & Service, a small business that sells appliances (**products**) and installs and maintains them (**services**).

Two things are true at once:

| Perspective | Owner | Gross margin means… |
| --- | --- | --- |
| Product | Product Line Lead | (Product revenue − landed cost of goods) ÷ product revenue. Cost includes materials, freight-in and duties. |
| Service | Services Lead | (Service revenue − technician labor, subcontractors and parts used) ÷ service revenue |
| Consolidated | Controller | (Total revenue − total cost of revenue) ÷ total revenue, as reported. Broader than Product and Service. Enterprise default for board and external reporting only. |

The formulas look alike, but "cost" means different things in each. None of the three is comparable with another as a margin, and they must not be averaged. Consolidated is computed from totals and will not reconcile to Product and Service by arithmetic; the Controller owns the reconciliation.

Resolution: context selects the perspective. When context can't (a cross-functional leadership meeting, or no context), the answer is "which perspective?"

Try it from the repository root:

```bash
python reference/tools/smf.py validate reference/examples/gross-margin --strict
python reference/tools/smf.py resolve reference/examples/gross-margin --term "gross margin" --context audience=leadership
python reference/tools/smf.py resolve reference/examples/gross-margin --term GM --context business_area=services
python reference/tools/smf.py test reference/examples/gross-margin
```

## One contract, four standards

Product Gross Margin is also written out in the other standards it touches, so the connections can be read from real files. These files are illustrative and are not SMF documents: the CLI skips them and says so in its summary line.

| File | Standard | What it shows |
| --- | --- | --- |
| [`metric-contracts.yaml`](metric-contracts.yaml) | SMF | The Metric Contract `product.gross_margin`, and one `Binding` for each place it is implemented |
| [`dbt/sales_metrics.yml`](dbt/sales_metrics.yml) | dbt MetricFlow (dbt 1.12 YAML spec) | The metric that computes it, pointing back at the contract under `config.meta.smf` |
| [`models/sales_analytics.ossie.yaml`](models/sales_analytics.ossie.yaml) | Apache Ossie (draft `0.2.0.dev0`) | The same metric as a portable model, pointing back through `custom_extensions` |
| [`data-contracts/sales-order-lines.odcs.yaml`](data-contracts/sales-order-lines.odcs.yaml), [`data-contracts/landed-cost.odcs.yaml`](data-contracts/landed-cost.odcs.yaml) | ODCS 3.2 | The datasets the contract is built on; the revenue and cost columns point up at the contract with `authoritativeDefinitions` |
| [`data-products/sales-analytics.odps.yaml`](data-products/sales-analytics.odps.yaml) | ODPS 1.1 | The data product whose output port carries those datasets, with the data contract version behind the port |

The field-by-field mapping between these is in the [spec](../../spec/README.md#crosswalk-one-metric-contract-four-standards-non-normative).
