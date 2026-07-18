#!/usr/bin/env python3
"""count.py

Counts words/characters/lines across the project.

- Default: analyzes multiple project directories and prints summary stats.
- If one or more file paths are provided: prints per-file stats.

"Chars" always includes whitespace and newlines.
"Code chars" is the character count with `//` comments removed while preserving newlines.
"Comment chars" excludes the trailing newline.
"""

import argparse
import os
from pathlib import Path


def _is_url_comment_false_positive(line: str, idx: int) -> bool:
    if idx <= 0:
        return False
    if line[idx - 1] != ":":
        return False
    prefix = line[max(0, idx - 6) : idx + 2].lower()
    return prefix.endswith("http://") or prefix.endswith("https://") or prefix.endswith("file://")


def _find_line_comment_start(line: str) -> int:
    """Return index of // comment start, or -1 if none.

    Heuristics:
    - Ignores // inside double-quoted strings.
    - Ignores common URL schemes like https://.
    """
    in_string = False
    escaped = False
    i = 0
    while i < len(line) - 1:
        ch = line[i]
        if escaped:
            escaped = False
            i += 1
            continue
        if ch == "\\":
            escaped = True
            i += 1
            continue
        if ch == '"':
            in_string = not in_string
            i += 1
            continue
        if not in_string and line[i : i + 2] == "//":
            if not _is_url_comment_false_positive(line, i):
                return i
        i += 1
    return -1


def _split_code_and_comment(line: str):
    comment_pos = _find_line_comment_start(line)
    if comment_pos == -1:
        return line, "", False

    code_part = line[:comment_pos]
    comment_part = line[comment_pos:]

    # Keep newlines in the code-part to model "remove comments but preserve line breaks".
    if comment_part.endswith("\n"):
        comment_part = comment_part[:-1]
        code_part = code_part + "\n"

    return code_part, comment_part, True


def count_file_stats(filepath):
    """Count words, characters, lines, and comments in a single file."""
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()

        total_lines = len(lines)
        comment_lines = 0
        comment_chars = 0
        comment_words = 0
        code_chars = 0
        code_words = 0
        code_lines = 0

        for line in lines:
            code_part, comment_part, has_comment = _split_code_and_comment(line)

            code_chars += len(code_part)
            code_words += len(code_part.split())

            if has_comment and comment_part.strip() != "":
                comment_lines += 1
                comment_chars += len(comment_part)
                comment_words += len(comment_part.split())

            if code_part.strip() != "":
                code_lines += 1

        total_words = code_words + comment_words
        total_chars = code_chars + comment_chars
        return (
            total_words,
            total_chars,
            comment_lines,
            comment_chars,
            comment_words,
            code_chars,
            code_words,
            total_lines,
            code_lines,
        )
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return 0, 0, 0, 0, 0, 0, 0, 0, 0


def _print_single_file_stats(script_dir: Path, filepath: Path):
    filepath = filepath.resolve()
    display_path = None
    try:
        display_path = str(filepath.relative_to(script_dir.resolve()))
    except Exception:
        display_path = str(filepath)

    (
        total_words,
        total_chars,
        comment_lines,
        comment_chars,
        comment_words,
        code_chars,
        code_words,
        total_lines,
        code_lines,
    ) = count_file_stats(filepath)

    print("=" * 80)
    print(f"FILE: {display_path}")
    print("=" * 80)
    print("LINES:")
    print(f"  Total Lines:          {total_lines:>15,}")
    print(f"  Code Lines:           {code_lines:>15,}")
    print(f"  Comment Lines:        {comment_lines:>15,}")
    print()
    print("WITH COMMENTS:")
    print(f"  Total Words:          {total_words:>15,}")
    print(f"  Total Characters:     {total_chars:>15,}")
    print()
    print("WITHOUT COMMENTS:")
    print(f"  Code Words:           {code_words:>15,}")
    print(f"  Code Characters:      {code_chars:>15,}")
    print()
    print("COMMENTS ONLY:")
    print(f"  Comment Words:        {comment_words:>15,}")
    print(f"  Comment Characters:   {comment_chars:>15,}")

def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("paths", nargs="*", help="Optional file paths to analyze")
    args, _unknown = parser.parse_known_args()

    # Get the script's directory and find src relative to it
    script_dir = Path(__file__).parent

    # Per-file mode
    if args.paths:
        for p in args.paths:
            _print_single_file_stats(script_dir, (script_dir / p) if not os.path.isabs(p) else Path(p))
        return

    # Point to the src/ subdirectory
    src_dir = script_dir / "src"
    if not src_dir.exists():
        print(f"Error: {src_dir} does not exist")
        return
    total_words = 0
    total_chars = 0
    total_comment_lines = 0
    total_comment_chars = 0
    total_comment_words = 0
    total_code_chars = 0
    total_code_words = 0
    total_lines = 0
    total_code_lines = 0
    file_count = 0
    file_stats = []
    
    # Separate counters for src files only (for statistics and percentage)
    src_words = 0
    src_chars = 0
    src_comment_lines = 0
    src_comment_chars = 0
    src_comment_words = 0
    src_code_chars = 0
    src_code_words = 0
    src_total_lines = 0
    src_code_lines = 0
    src_file_count = 0
    
    # Count total project files first
    project_file_count = sum(1 for _ in script_dir.rglob('*') if _.is_file())
    
    # Define directories to analyze
    analyze_dirs = ['src', 'database', 'man', 'Bash', 'dictionary']
    
    print("="*80)
    print(f"Total Project Files: {project_file_count:,}")
    print(f"Analyzing files in: {', '.join(analyze_dirs)}")
    print("="*80)
    print()
    
    # Walk through all specified directories
    for dir_name in analyze_dirs:
        target_dir = script_dir / dir_name
        if not target_dir.exists():
            continue
        for root, dirs, files in os.walk(target_dir):
            for filename in files:
                filepath = Path(root) / filename
                words, chars, comment_lines, comment_chars, comment_words, code_chars, code_words, file_lines, file_code_lines = count_file_stats(filepath)
                total_words += words
                total_chars += chars
                total_comment_lines += comment_lines
                total_comment_chars += comment_chars
                total_comment_words += comment_words
                total_code_chars += code_chars
                total_code_words += code_words
                total_lines += file_lines
                total_code_lines += file_code_lines
                file_count += 1
                # Track src files separately for statistics
                if dir_name == 'src':
                    src_words += words
                    src_chars += chars
                    src_comment_lines += comment_lines
                    src_comment_chars += comment_chars
                    src_comment_words += comment_words
                    src_code_chars += code_chars
                    src_code_words += code_words
                    src_total_lines += file_lines
                    src_code_lines += file_code_lines
                    src_file_count += 1
                # Store for detailed output
                rel_path = filepath.relative_to(script_dir)
                file_stats.append((str(rel_path), words, chars, code_chars, comment_chars))
    
    # Sort by character count (descending)
    file_stats.sort(key=lambda x: x[2], reverse=True)
    
    # Filter to only src files for top 20 display
    src_file_stats = [f for f in file_stats if f[0].startswith('src/')]
    
    # Print total file count
    print(f"TOTAL FILES: {file_count:,}")
    print()
    
    # Print detailed stats for top 20 files from src
    print("TOP 20 LARGEST FILES (src folder only):")
    print("-"*100)
    print(f"{'File':<50} {'Total':>12} {'Code Only':>12} {'Comments':>12}")
    print("-"*100)
    top_20_total = 0
    for filepath, words, file_total_chars, file_code_chars, file_comment_chars in src_file_stats[:20]:
        print(f"{filepath:<50} {file_total_chars:>12,} {file_code_chars:>12,} {file_comment_chars:>12,}")
        top_20_total += file_total_chars
    print("-"*100)
    print(f"{'TOP 20 TOTAL:':<50} {top_20_total:>12,}")
    print()
    print("="*80)
    print("SUMMARY STATISTICS")
    print("="*80)
    print(f"Total Files:            {src_file_count:>15,}")
    print()
    print("LINES:")
    print(f"  Total Lines:          {src_total_lines:>15,}")
    print(f"  Code Lines:           {src_code_lines:>15,}")
    print(f"  Comment Lines:        {src_comment_lines:>15,}")
    print(f"  Average Lines/File:   {src_total_lines/src_file_count if src_file_count > 0 else 0:>15,.1f}")
    print()
    print("WITH COMMENTS:")
    print(f"  Total Words:          {src_words:>15,}")
    print(f"  Total Characters:     {src_chars:>15,}")
    print(f"  Average Chars/File:   {src_chars/src_file_count if src_file_count > 0 else 0:>15,.1f}")
    print()
    print("CODE ONLY (WITHOUT COMMENTS):")
    print(f"  Code Words:           {src_code_words:>15,}")
    print(f"  Code Characters:      {src_code_chars:>15,}")
    print(f"  Average Chars/File:   {src_code_chars/src_file_count if src_file_count > 0 else 0:>15,.1f}")
    print()
    print("COMMENTS ONLY:")
    print(f"  Comment Lines:        {src_comment_lines:>15,}")
    print(f"  Comment Words:        {src_comment_words:>15,}")
    print(f"  Comment Characters:   {src_comment_chars:>15,}")
    print()
    print("PERCENTAGE (src files only):")
    src_total = src_code_chars + src_comment_chars
    print(f"  Code:                 {(src_code_chars/src_total*100) if src_total > 0 else 0:>14,.1f}%")
    print(f"  Comments:             {(src_comment_chars/src_total*100) if src_total > 0 else 0:>14,.1f}%")
    print()
    print("LINE PERCENTAGE:")
    print(f"  Code Lines:           {(src_code_lines/src_total_lines*100) if src_total_lines > 0 else 0:>14,.1f}%")
    print(f"  Comment Lines:        {(src_comment_lines/src_total_lines*100) if src_total_lines > 0 else 0:>14,.1f}%")
    print("="*80)
if __name__ == "__main__":
    main()
