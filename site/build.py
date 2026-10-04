#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Assemble the website source for MkDocs.

The site mirrors the repository layout (docs/, templates/, reference/ and the
project pages at the root), so every relative link that works on GitHub also
works on the website. The home page comes from site/home.md.

Run from the repository root:
    python site/build.py
    mkdocs build          # or: mkdocs serve
"""
import pathlib
import re
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "_site_src"

DIRS = ["docs", "templates", "reference"]
ROOT_FILES = [
    "CONTRIBUTING.md", "GOVERNANCE.md", "LICENSING.md", "CHANGELOG.md",
    "CODE_OF_CONDUCT.md", "LICENSE", "LICENSE-docs", "NOTICE",
]
IGNORE = shutil.ignore_patterns("__pycache__", "*.pyc")


LIST_ITEM = re.compile(r"^(\s*)([-*+]|\d+\.)\s")


def normalize_lists(text: str) -> str:
    """Make GitHub-style lists render the same way on the website.

    GitHub allows a list straight after a paragraph line and nests lists with
    two spaces. The website's Markdown engine needs a blank line first and four
    spaces per level. Only the website copy is changed; sources stay as they are.
    """
    lines = text.splitlines()
    # Nesting width used by this file's lists: the smallest indent of any nested item.
    in_code, indents = False, []
    for line in lines:
        if line.lstrip().startswith("```"):
            in_code = not in_code
        m = None if in_code else LIST_ITEM.match(line)
        if m and m.group(1):
            indents.append(len(m.group(1).replace("\t", "    ")))
    step = min(indents) if indents else 4
    scale = 4 / step if 0 < step < 4 else 1  # two-space nesting becomes four-space nesting

    out, in_code, prev = [], False, ""
    for line in lines:
        if line.lstrip().startswith("```"):
            in_code = not in_code
        m = None if in_code else LIST_ITEM.match(line)
        if m:
            indent = len(m.group(1).replace("\t", "    "))
            if indent and scale != 1:
                line = " " * round(indent * scale) + line.lstrip()
            prev_is_text = prev.strip() and not LIST_ITEM.match(prev) and not prev.startswith((" ", "|", "#", ">"))
            if prev_is_text and not line.startswith(" "):
                out.append("")
        out.append(line)
        prev = line
    return "\n".join(out) + "\n"


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    for d in DIRS:
        shutil.copytree(ROOT / d, OUT / d, ignore=IGNORE)
    for f in ROOT_FILES:
        shutil.copy2(ROOT / f, OUT / f)
    for md in OUT.rglob("*.md"):
        md.write_text(normalize_lists(md.read_text(encoding="utf-8")), encoding="utf-8")
    shutil.copy2(ROOT / "site" / "home.md", OUT / "index.md")
    shutil.copytree(ROOT / "site" / "assets", OUT / "assets")
    print(f"Site source assembled in {OUT.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
