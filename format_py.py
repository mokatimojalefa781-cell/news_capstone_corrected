"""Utility script to normalize whitespace in Python source files.

This script strips trailing whitespace from each line and ensures every file ends
with a single newline. It skips common generated directories (venv, migrations, docs).
"""

import pathlib
import re

EXCLUDE_DIRS = {"venv", ".git", "docs", "migrations", "__pycache__"}

if __name__ == "__main__":
    base = pathlib.Path(__file__).resolve().parent
    for path in base.rglob("*.py"):
        if any(part in EXCLUDE_DIRS for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8")
        lines = [re.sub(r"[ \t]+$", "", line) for line in text.splitlines()]
        new_text = "\n".join(lines).rstrip() + "\n"
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
