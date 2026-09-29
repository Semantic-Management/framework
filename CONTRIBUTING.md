# Contributing

SMF is early and open. Contributions that improve evidence, clarity and real-world fit are the most valuable.

## Where to start
- **Questions and ideas:** [GitHub Discussions](https://github.com/Semantic-Management/framework/discussions)
- **Specific changes or prior art:** open an issue using one of the templates

## Most helpful
- **Prior art:** a framework, standard or project that already does something SMF claims. Add it to `docs/research/` with a source.
- **Field cases:** anonymized examples where a practice boundary held or broke.
- **Golden questions:** realistic `TestCase` documents for common business terms.
- **Interop mappings:** how SMF documents map to Egeria, ODCS, OpenLineage, Ossie or a semantic layer.
- **Boundary cases:** questions that map to zero or two practices.

## Before opening a pull request
```bash
pip install -r reference/tools/requirements.txt
python reference/tools/smf.py validate reference/examples/gross-margin --strict
python reference/tools/smf.py test reference/examples/gross-margin
```

## Rules
1. Keep practices independently adoptable. No practice may require another.
2. Label non-normative content (examples, patterns, research).
3. Don't name proprietary products in framework or spec documents.
4. Don't copy text from proprietary frameworks.
5. For framework or spec changes, open a proposal issue first (see GOVERNANCE.md).
6. Update CHANGELOG.md.

By contributing, you agree that your contribution is licensed under the same license as the part of the repository it changes: **CC BY 4.0** for documentation and templates, **Apache-2.0** for anything under `reference/`. See [LICENSING.md](LICENSING.md).
