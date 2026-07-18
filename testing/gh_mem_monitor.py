#!/usr/bin/env python3
"""
gh_mem_monitor.py
Monitors Grey Hack process memory and reports increases/decreases.
Usage: python3 gh_mem_monitor.py [--interval SECONDS] [--threshold KB]
"""

import time
import argparse
import subprocess
import sys
from datetime import datetime

try:
    import psutil
    USE_PSUTIL = True
except ImportError:
    USE_PSUTIL = False


def find_greyhack_pids():
    """Find all PIDs associated with Grey Hack."""
    keywords = ["greyhack", "grey_hack", "GreyHack", "Grey Hack"]
    pids = []

    if USE_PSUTIL:
        for proc in psutil.process_iter(["pid", "name", "cmdline"]):
            try:
                name = (proc.info["name"] or "").lower()
                cmdline = " ".join(proc.info["cmdline"] or []).lower()
                if any(k.lower() in name or k.lower() in cmdline for k in keywords):
                    pids.append(proc.info["pid"])
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
    else:
        try:
            out = subprocess.check_output(["pgrep", "-f", "-i", "greyhack"], text=True)
            pids = [int(p) for p in out.strip().splitlines()]
        except subprocess.CalledProcessError:
            pass

    return pids


def get_mem_mb(pid):
    """Return RSS memory in MB for the given PID, or None if unavailable."""
    if USE_PSUTIL:
        try:
            p = psutil.Process(pid)
            return p.memory_info().rss / (1024 * 1024)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return None
    else:
        try:
            with open(f"/proc/{pid}/status") as f:
                for line in f:
                    if line.startswith("VmRSS:"):
                        return int(line.split()[1]) / 1024
        except (FileNotFoundError, PermissionError, ValueError):
            return None
    return None


def fmt_delta(delta_mb):
    """Format an MB delta with sign and colour (ANSI)."""
    if delta_mb > 0:
        return f"\033[91m+{delta_mb:.2f} MB\033[0m"   # red = increase
    elif delta_mb < 0:
        return f"\033[92m{delta_mb:.2f} MB\033[0m"    # green = decrease
    else:
        return f"  {delta_mb:.2f} MB"


GH_SCRIPT_RAM_MB = 512.0


def fmt_remaining(used_mb):
    remaining = GH_SCRIPT_RAM_MB - used_mb
    pct = (used_mb / GH_SCRIPT_RAM_MB) * 100
    if remaining < 50:
        colour = "\033[91m"   # red
    elif remaining < 150:
        colour = "\033[93m"   # yellow
    else:
        colour = "\033[92m"   # green
    return f"{colour}{remaining:.2f} MB free ({pct:.1f}% used)\033[0m"


def monitor(interval, threshold_kb):
    print(f"Searching for Grey Hack process...")
    pids = find_greyhack_pids()

    if not pids:
        print("ERROR: Grey Hack process not found. Is the game running?", file=sys.stderr)
        sys.exit(1)

    print(f"Found PID(s): {pids}")
    print(f"Polling every {interval}s, reporting changes >= {threshold_kb} MB")

    prev = {}
    baseline = {}

    try:
        while True:
            now = datetime.now().strftime("%H:%M:%S")
            # Re-check pids each cycle (game may restart)
            current_pids = find_greyhack_pids() or pids

            for pid in current_pids:
                mem = get_mem_mb(pid)
                if mem is None:
                    print(f"{now:<12}  {pid:<8}  [process gone]")
                    prev.pop(pid, None)
                    baseline.pop(pid, None)
                    continue

                if pid not in baseline:
                    baseline[pid] = mem
                    prev[pid] = mem
                    print(f"\n  Start memory (PID {pid}): {mem:.2f} MB  |  {fmt_remaining(mem)}  [{now}]")
                    print(f"  Script RAM cap: {GH_SCRIPT_RAM_MB:.0f} MB")
                    print(f"  {'Time':<12}  {'RSS (MB)':>10}  {'Delta':>14}  {'From start':>14}  {'Free':>20}")
                    print(f"  " + "-" * 78)
                    continue

                delta = mem - prev[pid]
                total = mem - baseline[pid]

                if abs(delta) >= threshold_kb:
                    print(
                        f"  {now:<12}  {mem:>10.2f}  {fmt_delta(delta):>22}  {fmt_delta(total):>22}  {fmt_remaining(mem):>28}"
                    )

                prev[pid] = mem

            time.sleep(interval)

    except KeyboardInterrupt:
        print("\nMonitoring stopped.")
        for pid in baseline:
            mem = get_mem_mb(pid)
            if mem is not None:
                total = mem - baseline[pid]
                print(f"  PID {pid}: final RSS {mem:.2f} MB  total change {fmt_delta(total)}  |  {fmt_remaining(mem)}")


def main():
    parser = argparse.ArgumentParser(description="Monitor Grey Hack memory usage")
    parser.add_argument("--interval", "-i", type=float, default=1.0,
                        help="Poll interval in seconds (default: 1.0)")
    parser.add_argument("--threshold", "-t", type=float, default=0.0,
                        help="Min MB change to report (default: 0 = report all)")
    args = parser.parse_args()
    monitor(args.interval, args.threshold)


if __name__ == "__main__":
    main()
