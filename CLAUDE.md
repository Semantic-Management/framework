# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Read and follow AGENTS.md; it is the authoritative instruction file for this repo.

## Local checks

Set up once, from the repository root (Git Bash; on macOS or Linux use `.venv/bin/python`):

```bash
python -m venv .venv
.venv/Scripts/python -m pip install -r reference/tools/requirements.txt
```

Run the four validate/test commands and the link check:

```bash
PY=.venv/Scripts/python
$PY reference/tools/smf.py validate reference/examples/gross-margin --strict
$PY reference/tools/smf.py validate reference/examples/northwind --strict
$PY reference/tools/smf.py test reference/examples/gross-margin
$PY reference/tools/smf.py test reference/examples/northwind
$PY reference/tools/check-links.py
```

If you changed `docs/`, `templates/`, `site/` or `mkdocs.yml`, also run the website build (the `checks` job does):

```bash
$PY -m pip install -r site/requirements.txt
$PY site/build.py && $PY -m mkdocs build --strict
```

Expected: 0 errors and 0 warnings; gross-margin 7 passed / 0 failed / 1 skipped; northwind 9 / 0 / 2; 0 broken links.

The CLI has four subcommands (`validate`, `resolve`, `test`, `import-csv`); all take an example directory, and there is no per-test selector. To try one resolution:

```bash
$PY reference/tools/smf.py resolve reference/examples/gross-margin --term "gross margin" --context audience=leadership
```

`test --results <file>` scores an AI assistant's answers (see `reference/examples/consumer-results/`); those sample files fail one check on purpose, so a failure there is expected.

## Architecture

Two layers with a hard audience split (details in AGENTS.md):

- **Framework prose** (`docs/`, `README.md`, `templates/`): plain business language, no schema identifiers. Technical detail goes in `reference/` and is linked to.
- **Reference implementation** (`reference/`): `spec/schemas/*.json` define the document types, `reference/tools/smf.py` is a single-file CLI that validates and resolves them, and `examples/` holds two worked sets of YAML (`gross-margin` flagship, `northwind` broader). Each example's `tests/*.yaml` are the `TestCase` documents that `smf.py test` runs against the reference resolver, so schema, resolver and examples must change together.

The website is derived, not authored: `site/build.py` copies `docs/`, `templates/`, `reference/` and the root project pages into `_site_src/` (home page from `site/home.md`), then `mkdocs build --strict` renders it to `_site/`. Both are gitignored. Edit the sources, never the output. To preview: `pip install -r site/requirements.txt`, `python site/build.py`, `mkdocs serve`. The `pages` workflow runs the same steps.

## Workflow

Work on a branch, open a pull request against `main`, and merge only when the `checks` job (workflow `reference-checks`) passes. If it fails, stop and look at the log.

Each release adds a dated entry to `CHANGELOG.md` (the version string also appears in the README status line).
