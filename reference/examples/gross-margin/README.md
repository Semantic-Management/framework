# Example: Gross Margin, Three Perspectives

**Fictional company:** Lakeview Supply & Service, a small business that sells appliances (**products**) and installs and maintains them (**services**).

Two things are true at once:

| Perspective | Owner | Gross margin means… |
| --- | --- | --- |
| Product | Product Line Lead | (Product revenue − landed cost of goods) ÷ product revenue. Cost includes materials, freight-in and duties. |
| Service | Services Lead | (Service revenue − technician labor, subcontractors and parts used) ÷ service revenue |
| Consolidated | Controller | (Total revenue − total cost of revenue) ÷ total revenue, as reported. Enterprise default for board and external reporting. |

The formulas look alike, but "cost" means different things in each. The product and service margins are **not** comparable and must not be averaged.

Resolution: context selects the perspective. When context can't (a cross-functional leadership meeting, or no context), the answer is "which perspective?"

Try it from the repository root:

```bash
python reference/tools/smf.py validate reference/examples/gross-margin --strict
python reference/tools/smf.py resolve reference/examples/gross-margin --term "gross margin" --context audience=leadership
python reference/tools/smf.py resolve reference/examples/gross-margin --term GM --context domain=services
python reference/tools/smf.py test reference/examples/gross-margin
```
