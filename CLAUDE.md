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

Expected: 0 errors and 0 warnings; gross-margin 6 passed / 0 failed / 1 skipped; northwind 9 / 0 / 2; 0 broken links.

## Workflow

Work on a branch, open a pull request against `main`, and merge only when the `checks` workflow passes. If it fails, stop and look at the log.
