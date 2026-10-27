#!/usr/bin/env python3
"""run_all.py — run every tests/test_*.py; exit 1 if any fails.

F49, found by my own new test file going `PASS  test_jobs_accept.py ()`: the runner printed the last stderr
line as the "count", and a file that writes its summary somewhere else — or nowhere — passed with nothing to
show. That is how a suite accumulates decoration: a green list is only as honest as its quietest contributor,
and the assertion counts quoted in README/ORDERS/shift notes are summed from exactly these lines (mine were
wrong twice today for the same underlying reason — hand-maintained numbers).

So: the count is read from stderr OR stdout, and a file that passes without reporting a count is a FAILURE.
The runner also takes an optional directory argument, which is the seam that lets this behaviour be tested
against a fake tree instead of only against production (the lesson from F45, applied to the test runner).
"""
import glob
import os
import re
import subprocess
import sys

here = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
files = sorted(glob.glob(os.path.join(here, "test_*.py")))


def last_line(stream):
    lines = [l for l in (stream or "").splitlines() if l.strip()]
    return lines[-1] if lines else ""


fails, total = 0, 0
for f in files:
    r = subprocess.run([sys.executable, f], capture_output=True, text=True)
    name = os.path.basename(f)
    summary = last_line(r.stderr) or last_line(r.stdout)
    m = re.search(r"(\d+)\s+assertions?", summary)
    count = int(m.group(1)) if m else None
    if r.returncode == 0 and count is None:
        fails += 1
        print(f"FAIL  {name}  (exit 0 but no 'N assertions' summary — a green file that counts nothing is not "
              f"evidence; print it to stderr like the others)")
        continue
    if count:
        total += count
    if r.returncode == 0:
        print(f"PASS  {name}  ({count} assertions)")
    else:
        fails += 1
        print(f"FAIL  {name}")
        print((r.stdout + r.stderr)[-2000:])

print(f"\n{len(files) - fails} passed · {fails} failed · {total} assertions")
if not files:
    print("run_all: no test_*.py found — that is not a pass", file=sys.stderr)
    sys.exit(1)
sys.exit(1 if fails else 0)
