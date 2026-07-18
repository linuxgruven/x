#!/usr/bin/env python3
"""
Function audit for the x project.
Finds: duplicate function names, potentially dead (never-called) functions.
Efficient single-pass approach.
"""
import os
import re
import sys
from collections import defaultdict

ROOT = "/home/brian/Programming/GitHub/x"

# Only scan these subdirs for DEFINITIONS (actual source code, not man pages)
CODE_DIRS = [
    "src",
    "exploits",
    "utilities",
    "Bash",
    "scanner",
]

# For CALL SITE scanning we also include root-level .src files (e.g. main.src)
CALL_DIRS = CODE_DIRS  # keep same; man pages are docs not calls

import os as _os
ROOT_SRC_FILES = [_os.path.join(ROOT, f) for f in _os.listdir(ROOT) if f.endswith(".src")]

# Patterns for GreyScript function definitions
# e.g.  Foo.bar = function(...)  or  myFunc = function(...)
DEF_PAT = re.compile(
    r'^[ \t]*([A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*)\s*=\s*function\s*\('
)

# -----------------------------------------------------------------------
# Collect source files from relevant dirs only
# -----------------------------------------------------------------------
def collect_src_files(dirs):
    result = []
    for d in dirs:
        path = os.path.join(ROOT, d)
        if not os.path.isdir(path):
            continue
        for dirpath, dirnames, filenames in os.walk(path):
            # Skip test subdirs in Bash
            dirnames[:] = [x for x in dirnames if x not in {"tests", "Original"}]
            for fn in filenames:
                if fn.endswith(".src"):
                    result.append(os.path.join(dirpath, fn))
    result.sort()
    return result

code_files = collect_src_files(CODE_DIRS)
all_scan_files = code_files + ROOT_SRC_FILES

# -----------------------------------------------------------------------
# Phase 1: Single-pass — collect definitions AND build call index
# For each file, read once:
#   - match DEF_PAT for definitions
#   - collect all identifier tokens for reverse lookup
# -----------------------------------------------------------------------

# definitions[full_name] = [(rel_path, lineno)]
definitions = defaultdict(list)

# usage_count[full_name] = count of non-definition occurrences
# We'll build a token frequency map across all files, then subtract definition lines
# token_counts[name] = total raw occurrences (including definition lines)
token_occurrences = defaultdict(list)  # name -> [(rel, lineno)]

# Token pattern: any dotted identifier  (e.g. Io.readFile  or  myFunc)
TOKEN_PAT = re.compile(r'[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*')

for fpath in all_scan_files:
    rel = os.path.relpath(fpath, ROOT)
    try:
        with open(fpath, encoding="utf-8", errors="replace") as fh:
            lines = fh.readlines()
    except Exception as e:
        sys.stderr.write(f"[WARN] {rel}: {e}\n")
        continue

    for lineno, line in enumerate(lines, 1):
        # Strip comments (// ...)
        stripped = re.sub(r'//.*', '', line)

        # Check for definition
        m = DEF_PAT.match(line)
        if m:
            definitions[m.group(1)].append((rel, lineno))

        # Collect all identifier tokens on this line
        for tm in TOKEN_PAT.finditer(stripped):
            tok = tm.group()
            token_occurrences[tok].append((rel, lineno))

# -----------------------------------------------------------------------
# Phase 2: call counts = total occurrences MINUS definition occurrences
#          + self.method occurrences within the file(s) where it's defined
#          (GreyScript: calls within the same object use self.foo, not Obj.foo)
# -----------------------------------------------------------------------
call_counts = {}
for fname, def_locs in definitions.items():
    total = len(token_occurrences.get(fname, []))
    external = total - len(def_locs)

    # Count self.shortname calls in the same file(s) as the definition
    short = fname.split(".")[-1]
    self_key = "self." + short
    def_files = {rel for rel, _ in def_locs}
    self_count = sum(1 for rel, _ in token_occurrences.get(self_key, [])
                     if rel in def_files)

    call_counts[fname] = external + self_count

# -----------------------------------------------------------------------
# Phase 3: Identify DEAD functions (defined but never referenced elsewhere)
# -----------------------------------------------------------------------
dead = {fname: locs for fname, locs in definitions.items()
        if call_counts.get(fname, 0) == 0}

# -----------------------------------------------------------------------
# Phase 4: Redefined functions (same full name in multiple files)
# -----------------------------------------------------------------------
redefined = {fname: locs for fname, locs in definitions.items() if len(locs) > 1}

# -----------------------------------------------------------------------
# Phase 5: Duplicate short names across different objects
# -----------------------------------------------------------------------
by_short = defaultdict(list)
for fname in definitions:
    short = fname.split(".")[-1]
    by_short[short].append(fname)
duplicates = {short: names for short, names in by_short.items() if len(names) > 1}

# -----------------------------------------------------------------------
# Report
# -----------------------------------------------------------------------
SEP = "-" * 80
out = []

out.append(SEP)
out.append(f"FUNCTION AUDIT REPORT — {ROOT}")
out.append(SEP)
out.append(f"Source files scanned : {len(code_files)}")
out.append(f"Total function defs  : {len(definitions)}")
out.append(f"Dead functions (0 external calls) : {len(dead)}")
out.append(f"Redefined functions  : {len(redefined)}")
out.append(f"Shared short names   : {len(duplicates)}")
out.append("")

# --- Dead functions grouped by file ---
out.append(SEP)
out.append("DEAD FUNCTIONS (defined but never called or referenced)")
out.append(SEP)
dead_by_file = defaultdict(list)
for fname, locs in dead.items():
    for rel, lineno in locs:
        dead_by_file[rel].append((lineno, fname))
for rel in sorted(dead_by_file):
    out.append(f"  {rel}")
    for lineno, fname in sorted(dead_by_file[rel]):
        out.append(f"    L{lineno:<5} {fname}")
out.append("")

# --- Redefined functions ---
out.append(SEP)
out.append("REDEFINED FUNCTIONS (same full name defined in multiple files)")
out.append(SEP)
if redefined:
    for fname, locs in sorted(redefined.items()):
        out.append(f"  {fname}")
        for rel, lineno in locs:
            out.append(f"    {rel}:{lineno}")
else:
    out.append("  (none)")
out.append("")

# --- Duplicate short names ---
out.append(SEP)
out.append("SHARED SHORT NAMES (same method name on different objects)")
out.append(SEP)
for short, names in sorted(duplicates.items()):
    out.append(f"  .{short:<30}  {', '.join(sorted(names))}")
out.append("")

# --- Rarely called ---
out.append(SEP)
out.append("RARELY CALLED (called exactly 1 time — worth reviewing)")
out.append(SEP)
rare_by_file = defaultdict(list)
for fname in definitions:
    if call_counts.get(fname, 0) == 1:
        for rel, lineno in definitions[fname]:
            rare_by_file[rel].append((lineno, fname))
for rel in sorted(rare_by_file):
    out.append(f"  {rel}")
    for lineno, fname in sorted(rare_by_file[rel]):
        out.append(f"    L{lineno:<5} {fname}")
out.append("")

out.append(SEP)
out.append("Done.")

print("\n".join(out))
