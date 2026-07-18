#!/usr/bin/env python3
"""Patch Greybel VS extension: keep Grey Hack nightly globals out of uglify rename.

Greybel maps excludedNamespaces -> variablesExcluded -> forbidden[] in the
namespace generator. Names in forbidden are never minified (createNamespace
returns the original name).

Only add identifiers from nightly that Greybel does not already know — see
scanner/greybel-reserved.json (poll_input, meta-mail API, etc.).

Run after extension install/update:
  python3 patch-greybel-plugin.py

Re-run after changing greybel-reserved.json to refresh an existing patch.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RESERVED = json.loads((ROOT / "greybel-reserved.json").read_text())

MARKER = "...e.variablesExcluded||[]"
ANCHOR_RE = re.compile(r"\.\.\.Object\.values\(\w+\.Keyword\),")

EXTENSION_ROOTS = [
    Path.home() / ".cursor/extensions/ayecue.greybel-vs-2.8.13-universal",
    Path.home() / ".vscode/extensions/ayecue.greybel-vs-2.8.13-universal",
]

TARGETS = []
for ext in EXTENSION_ROOTS:
    if not ext.is_dir():
        continue
    for rel in [
        "node_modules/greybel-languageserver/index.js",
        "node_modules/greybel-languageserver-browser/index.js",
    ]:
        p = ext / rel
        if p.is_file():
            TARGETS.append(p)


def insert_for(names: list[str]) -> str:
    return ",".join(f'"{n}"' for n in names) + ","


def strip_old_patch(text: str) -> str:
    """Remove a prior poll_input..* patch block if present."""
    if '"poll_input"' not in text or MARKER not in text:
        return text
    start = text.find('"poll_input"')
    end = text.find(MARKER, start)
    if end == -1:
        return text
    return text[:start] + text[end:]


def find_anchor(text: str) -> re.Match | None:
    """Last ...Object.values(X.Keyword), before variablesExcluded."""
    end = text.find(MARKER)
    if end == -1:
        return None
    head = text[:end]
    matches = list(ANCHOR_RE.finditer(head))
    return matches[-1] if matches else None


def patch_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if MARKER not in text:
        print(f"  skip (marker not found): {path}")
        return False
    insert = insert_for(RESERVED)
    cleaned = strip_old_patch(text)
    if insert in cleaned:
        print(f"  skip (already patched): {path}")
        return False
    anchor = find_anchor(cleaned)
    if not anchor:
        print(f"  skip (anchor not found): {path}")
        return False
    pos = anchor.end()
    new_text = cleaned[:pos] + insert + cleaned[pos:]
    path.write_text(new_text, encoding="utf-8")
    print(f"  patched: {path}")
    return True


def main() -> int:
    if not TARGETS:
        print("No greybel-languageserver files found under Cursor/VS Code extensions.")
        print("Install ayecue.greybel-vs, then re-run this script.")
        return 1
    print(f"Nightly reserved identifiers: {len(RESERVED)}")
    for name in RESERVED:
        print(f"  - {name}")
    n = 0
    for p in TARGETS:
        if patch_file(p):
            n += 1
    if not n:
        print("Nothing patched (already up to date or marker missing).")
    else:
        print(f"Patched {n} file(s). Reload Cursor/VS Code window.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
