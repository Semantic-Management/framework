# Contributing

SMF is early and open. Contributions that improve evidence, clarity and real-world fit are the most valuable.

## Where to start
- **Pick an issue.** Every open issue labelled [`help wanted`](https://github.com/Semantic-Management/framework/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22) is one deliverable with acceptance criteria written in. By kind:
  - [`example`](https://github.com/Semantic-Management/framework/labels/example): a worked example (plain-language page plus machine-form YAML). Needs domain knowledge, not framework knowledge.
  - [`crosswalk`](https://github.com/Semantic-Management/framework/labels/crosswalk): a mapping from one named framework or standard to SMF. Needs familiarity with that framework.
  - [`interop`](https://github.com/Semantic-Management/framework/labels/interop): a converter or generator in `reference/tools/`. Python, stdlib plus PyYAML.
  - [`prior-art`](https://github.com/Semantic-Management/framework/labels/prior-art): review one existing project and say what SMF should credit or defer to.
  - [`boundary-case`](https://github.com/Semantic-Management/framework/labels/boundary-case): try to break a practice with a real case and report what happened.
  - [`good first issue`](https://github.com/Semantic-Management/framework/labels/good%20first%20issue): finishable in an evening.
- **Review a page.** Read one document from the reading order in `AGENTS.md` and open a Discussion saying where it is wrong or unclear. Reviewers are as valuable as authors at this stage.
- **Questions and ideas:** [GitHub Discussions](https://github.com/Semantic-Management/framework/discussions)
- **Specific changes or prior art:** open an issue using one of the templates

Comment on an issue before starting so two people do not do the same work. Issues labelled `owner-action` need the framework owner's own input; skip those.

## Most helpful
- **Prior art:** a framework, standard or project that already does something SMF claims. Add it to `docs/research/` with a source.
- **Field cases:** anonymized examples where a practice boundary held or broke.
- **Golden questions:** realistic `TestCase` documents for common business terms.
- **Interop mappings:** how SMF documents map to Egeria, ODCS, OpenLineage, Ossie or a semantic layer.
- **Boundary cases:** questions that map to zero or multiple practices.

## Before opening a pull request
```bash
pip install -r reference/tools/requirements.txt
python reference/tools/smf.py validate reference/examples/gross-margin --strict
python reference/tools/smf.py validate reference/examples/northwind --strict
python reference/tools/smf.py test reference/examples/gross-margin
python reference/tools/smf.py test reference/examples/northwind
python reference/tools/check-links.py
```

If you changed `docs/`, `templates/`, `site/` or `mkdocs.yml`, also check that the website builds:

```bash
pip install -r site/requirements.txt
python site/build.py && mkdocs build --strict
```

If you use an AI assistant on this repository, start it from [prompts/bootstrap-repo.md](https://github.com/Semantic-Management/framework/blob/main/prompts/bootstrap-repo.md) and `AGENTS.md`.

## Rules
1. Keep practices independently adoptable. No practice may require another.
2. Label non-normative content (examples, patterns, research).
3. Don't name proprietary products in framework or spec documents.
4. Don't copy text from proprietary frameworks.
5. For framework or spec changes, open a proposal issue first (see GOVERNANCE.md).
6. Update CHANGELOG.md.

By contributing, you agree that your contribution is licensed under the same license as the part of the repository it changes: **CC BY 4.0** for documentation and templates, **Apache-2.0** for anything under `reference/`. See [LICENSING.md](LICENSING.md).
