#!/usr/bin/env python3
"""test_run_all_counts.py — the runner refuses a green file that reports nothing (F49).

run_all.py used to print `PASS  test_x.py ()` for any file whose summary line it could not find, so a test file
that wrote its count to the wrong stream — or never counted anything — looked identical to one that ran 32
assertions. The counts quoted in README and ORDERS are summed from these lines, so a silent contributor does not
just hide itself: it silently lowers the number everyone else quotes as the size of the evidence.
"""
import os, subprocess, sys, tempfile, time

HERE = os.path.dirname(os.path.abspath(__file__))
RUNNER = os.path.join(HERE, "run_all.py")

FAKE_OK = "import sys\nprint('7 assertions ok (0.0s)', file=sys.stderr)\n"
FAKE_SILENT = "print('I did something but never said what')\n"
FAKE_RED = "import sys\nsys.exit(3)\n"


def main():
    t0 = time.time()
    d = tempfile.mkdtemp(prefix="agency-runner-")
    n = 0
    try:
        def write(name, body):
            open(os.path.join(d, name), "w").write(body)

        def run(spec):
            """`spec` is {filename: source}. A `*names` signature here packed the dict into a tuple and the
            first run raised TypeError inside the fixture, not inside the code under test — the failure looked
            like a runner bug for a minute, which is why fixtures get the same care as assertions."""
            for nm in ("test_a.py", "test_b.py"):
                if os.path.exists(os.path.join(d, nm)):
                    os.remove(os.path.join(d, nm))
            for nm, body in spec.items():
                write(nm, body)
            return subprocess.run([sys.executable, RUNNER, d], capture_output=True, text=True)

        r = run({"test_a.py": FAKE_OK})
        assert r.returncode == 0 and "7 assertions" in r.stdout, (r.returncode, r.stdout, r.stderr)
        n += 1

        r = run({"test_a.py": FAKE_OK, "test_b.py": FAKE_SILENT})
        assert r.returncode == 1, "a green file with no count must fail the runner"
        assert "no 'N assertions' summary" in r.stdout, r.stdout
        n += 2

        # the count is read from either stream — a file that prints to stdout is fine, one that prints nothing
        # is not; that distinction is the whole point and it must not depend on which stream was chosen
        r = run({"test_a.py": FAKE_OK.replace("file=sys.stderr", "file=sys.stdout")})
        assert r.returncode == 0 and "7 assertions" in r.stdout, (r.stdout, r.stderr)
        n += 1

        r = run({"test_a.py": FAKE_RED})
        assert r.returncode == 1 and "FAIL" in r.stdout
        n += 1

        empty = tempfile.mkdtemp(prefix="agency-runner-empty-")
        r = subprocess.run([sys.executable, RUNNER, empty], capture_output=True, text=True)
        assert r.returncode == 1 and "no test_*.py" in r.stderr, "an empty suite is not a pass"
        n += 1

        print(f"run_all_counts: {n} assertions ok ({time.time() - t0:.1f}s)", file=sys.stderr)
    finally:
        import shutil
        shutil.rmtree(d, ignore_errors=True)


if __name__ == "__main__":
    main()
