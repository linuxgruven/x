#!/usr/bin/env python3
"""Generate GreyScript wrapper .src files for bash test scripts.

Each wrapper defines a variable containing the test script content,
with quotes doubled for GreyScript string literals.

Usage: python3 gen_wrappers.py
Run from the Bash/tests/ directory.
"""
import os

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))

FILES = [
    ("learn_bash.src", "testLearnBash"),
    ("bash_map_test.src", "testBashMapTest"),
    ("return_test.src", "testReturnTest"),
    ("func_test.src", "testFuncTest"),
    ("cast_test.src", "testCastTest"),
    ("edge_test.src", "testEdgeTest"),
    ("switch_test.src", "testSwitchTest"),
    ("stress_test.src", "testStressTest"),
    ("bash_pipe_test.src", "testBashPipeTest"),
    ("find_pipe_test.src", "testFindPipeTest"),
    ("bash_try_catch.src", "testTryCatch"),
    ("builtin_vars_test.src", "testBuiltinVars"),
    ("menu_test.src", "testMenuTest"),
    ("bounce_test.src", "testBounceTest"),
    ("lan_test.src", "testLanTest"),
    ("local_test.src", "testLocalTest"),
    ("scan_test.src", "testScanTest"),
    ("shell_test.src", "testShellTest"),
    ("wifi_test.src", "testWifiTest"),
    ("fmon.src", "testFmon"),
    ("dmon.src", "testDmon"),
]

for fname, varname in FILES:
    fpath = os.path.join(TESTS_DIR, fname)
    if not os.path.exists(fpath):
        print(f"SKIP missing {fname}")
        continue
    with open(fpath, "r") as f:
        content = f.read()
    # Double all quotes for GreyScript string literal embedding
    escaped = content.replace('"', '""')
    # Write wrapper file
    wrapper_name = fname.replace(".src", "_w.src")
    wrapper_path = os.path.join(TESTS_DIR, wrapper_name)
    with open(wrapper_path, "w") as f:
        f.write(f'{varname}="{escaped}"\n')
    print(f"Generated {wrapper_name} ({len(content)} chars)")

print("Done. Update _installer.src to import_code the _w.src files.")
