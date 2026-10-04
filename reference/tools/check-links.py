#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Check that relative links and heading anchors in every Markdown file resolve.

Run from the repository root:  python reference/tools/check-links.py
Exits 1 if any link is broken. Links inside code blocks and code spans and external URLs are
skipped. Inline links (with or without a title), reference-style link definitions and HTML
`href` attributes are checked.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
# site/ holds the website home page, whose links are relative to the built site;
# `mkdocs build --strict` checks those. _site_src/ and _site/ are build output.
SKIP_DIRS = {".git", ".venv", "node_modules", "site", "_site_src", "_site"}


def slug(heading: str) -> str:
    h = re.sub(r"[`*_]", "", heading.strip().lower())
    h = re.sub(r"[^\w\s-]", "", h)
    return re.sub(r"\s", "-", h)


INLINE = re.compile(r"\[[^\]]*\]\(\s*<?([^)\s>]+)>?(?:\s+(?:\"[^\"]*\"|'[^']*'))?\s*\)")
REFERENCE = re.compile(r"^ {0,3}\[[^\]]+\]:\s*<?(\S+?)>?(?:\s+.*)?$", re.M)
HREF = re.compile(r"""<a\s[^>]*href=["']([^"']+)["']""", re.I)


def anchors(text: str) -> set:
    """Heading anchors as GitHub makes them, including -1, -2 suffixes for repeated headings."""
    seen, out = {}, set()
    for h in re.findall(r"^#+\s+(.*)$", text, flags=re.M):
        s = slug(h)
        n = seen.get(s, 0)
        seen[s] = n + 1
        out.add(s if n == 0 else f"{s}-{n}")
    return out


def links(body: str):
    for rx in (INLINE, REFERENCE, HREF):
        for m in rx.finditer(body):
            yield m.group(1)


def main() -> int:
    checked = problems = 0
    for f in sorted(ROOT.rglob("*.md")):
        if SKIP_DIRS & set(f.relative_to(ROOT).parts):
            continue
        body = re.sub(r"```.*?```", "", f.read_text(encoding="utf-8"), flags=re.S)
        body = re.sub(r"`[^`\n]*`", "", body)
        for target in links(body):
            if re.match(r"^(https?:|mailto:)", target):
                continue
            checked += 1
            path, _, frag = target.partition("#")
            dest = f if not path else (f.parent / path).resolve()
            rel = f.relative_to(ROOT)
            if not dest.exists():
                print(f"BROKEN      {rel} -> {target}")
                problems += 1
            elif frag and dest.suffix == ".md":
                if frag not in anchors(dest.read_text(encoding="utf-8")):
                    print(f"BAD ANCHOR  {rel} -> {target}")
                    problems += 1
    print(f"{checked} relative links checked, {problems} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
