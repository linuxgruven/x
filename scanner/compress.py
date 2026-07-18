#!/usr/bin/env python3
"""Compress a GreyScript .src file by joining all lines with semicolons.

Also checks menu → alias → cmds drift for scanner host/main wiring.

Usage:
  python3 compress.py                    # scanner.src -> scanner_op.src
  python3 compress.py input.src          # input.src -> input_op.src
  python3 compress.py input.src out.src  # input.src -> out.src
  python3 compress.py --check-only       # drift check only (exit 1 on fail)
"""
import re
import sys
from pathlib import Path

MAX_CHARS = 160000

# Menu keys that never resolve through alias→cmds (handled by menu loops).
META_KEYS = {"#", "b"}


def _parse_map(name: str, text: str) -> dict[str, str]:
    m = re.search(rf"{re.escape(name)}\s*=\s*\{{([^}}]+)\}}", text)
    if not m:
        return {}
    return dict(re.findall(r'"([^"]+)":"([^"]+)"', m.group(1)))


def _parse_acts(name: str, text: str) -> list[str]:
    m = re.search(rf"{re.escape(name)}\s*=\s*\[(.*?)\](?=\s*\n|\s*_)", text, re.S)
    if not m:
        return []
    return re.findall(r'\["([^"]+)"\s*,', m.group(1))


def _parse_host_act_keys(text: str) -> list[str]:
    m = re.search(r"_hostActs\s*=\s*function.*?^end function", text, re.M | re.S)
    if not m:
        return []
    # Keys only — labels may be string concat like "rshell ("+rsCnt+")".
    return re.findall(r'\["([^"]+)"\s*,', m.group(0))


def _cmd_names(prefix: str, text: str) -> set[str]:
    # Avoid matching cmds. inside _cmds. when prefix is "cmds".
    if prefix == "cmds":
        names = set(re.findall(r"(?<![_\w])cmds\.([A-Za-z_]\w*)\s*=\s*function", text))
        names |= set(re.findall(r'(?<![_\w])cmds\["([^"]+)"\]\s*=\s*function', text))
        return names
    names = set(re.findall(rf"{re.escape(prefix)}\.([A-Za-z_]\w*)\s*=\s*function", text))
    names |= set(re.findall(rf'{re.escape(prefix)}\["([^"]+)"\]\s*=\s*function', text))
    return names


def check_menu_drift(text: str) -> list[str]:
    """Return list of drift errors (empty = ok)."""
    errors: list[str] = []
    ha = _parse_map("_ha", text)
    ma = _parse_map("_ma", text)
    host_cmds = _cmd_names("cmds", text)
    main_cmds = _cmd_names("_cmds", text)

    if not ha:
        errors.append("_ha map not found")
    if not ma:
        errors.append("_ma map not found")

    # Alias targets must exist as commands.
    for alias, target in sorted(ha.items()):
        if target not in host_cmds:
            errors.append(f"_ha[{alias!r}] -> {target!r} missing cmds.{target}")
    for alias, target in sorted(ma.items()):
        if target not in main_cmds:
            errors.append(f"_ma[{alias!r}] -> {target!r} missing _cmds.{target}")

    # Menu keys must be aliasable (or already cmd names / meta).
    for key in _parse_host_act_keys(text):
        if key in META_KEYS:
            continue
        resolved = ha.get(key, key)
        if resolved not in host_cmds:
            errors.append(f"_hostActs key {key!r} -> {resolved!r} missing cmds.{resolved}")

    for act_name in ("_mainMenuActs",):
        for key in _parse_acts(act_name, text):
            if key in META_KEYS:
                continue
            resolved = ma.get(key, key)
            if resolved not in main_cmds:
                errors.append(f"{act_name} key {key!r} -> {resolved!r} missing _cmds.{resolved}")

    return errors


def compress(src, dst, check=True):
    data = Path(src).read_text()
    if check:
        drift = check_menu_drift(data)
        if drift:
            print(f"DRIFT: {len(drift)} menu/alias/cmd issue(s) in {src}")
            for err in drift:
                print(f"  - {err}")
            return 1
        print(f"Drift:      ok (menu ⊆ alias ⊆ cmds)")

    lines = data.split("\n")
    stripped = [l.strip() for l in lines if l.strip()]
    result = ";".join(stripped)
    Path(dst).write_text(result)
    saved = len(data) - len(result)
    headroom = MAX_CHARS - len(result)
    print(f"Source:     {src} ({len(data)} chars, {len(lines)} lines)")
    print(f"Output:     {dst} ({len(result)} chars, 1 line)")
    print(f"Saved:      {saved} chars")
    print(f"Join size:  {len(result)} (whitespace-only; GreyBel uglify is the real budget)")
    print(f"Join vs {MAX_CHARS}: {headroom:+d} (informational only)")
    if headroom < 0:
        print(f"NOTE: join exceeds {MAX_CHARS}; GreyBel build is usually smaller — check IDE compile size.")
    return 0


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--check-only"]
    check_only = "--check-only" in sys.argv[1:]
    src = args[0] if args else "scanner.src"
    if check_only:
        text = Path(src).read_text()
        drift = check_menu_drift(text)
        if drift:
            print(f"DRIFT: {len(drift)} issue(s)")
            for err in drift:
                print(f"  - {err}")
            sys.exit(1)
        print("Drift: ok")
        sys.exit(0)
    dst = args[1] if len(args) > 1 else Path(src).stem + "_op.src"
    sys.exit(compress(src, dst))
