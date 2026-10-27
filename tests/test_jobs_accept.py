#!/usr/bin/env python3
"""test_jobs_accept.py — the closure path for jobs, and the fact that the old quorum could not be cast at all.

Why this file exists (F48, 2026-10-27): START_HERE §4, ORDERS.md, README and tools/ship.sh all promised
"two non-owner accept-inspected ballots" after every ship. `vote` reads `board/tasks/<id>.json`; jobs live in
`jobs/<id>/`, so `agency vote <job-id> …` dies with "no such task", and `jobs` had no accept/close verb. For a
job the gate was not strict, it was unaddressable — which is worse, because it looks like a pending step. This
file pins both halves: the verb that closes, and the refusal to accept a closure with no evidence in it.

Negative control: AGENCY_OLD_CLI=<pre-fix bin/agency> adds the assertion that the old build has no such verb at
all, so this test cannot pass by accident on the code it was written against.
"""
import json, os, subprocess, sys, tempfile, time

HERE = os.path.dirname(os.path.abspath(__file__))
CLI = os.environ.get("AGENCY_CLI") or os.path.join(HERE, "..", "bin", "agency")


def fresh_repo():
    d = tempfile.mkdtemp(prefix="agency-accept-")
    for p in ("agents", "board/tasks", "board/heartbeats", "board/votes", "jobs/t-9-work"):
        os.makedirs(os.path.join(d, p), exist_ok=True)
    open(os.path.join(d, "jobs/t-9-work/BRIEF.md"), "w").write("# brief\n")
    open(os.path.join(d, "jobs/t-9-work/PHASES.md"), "w").write("| phase | min_hours |\n")
    open(os.path.join(d, "jobs/t-9-work/HANDOFF.md"), "w").write("# handoff\n")
    return d


def run(repo, *args, expect=0, agent="nova", cli=CLI):
    e = {**os.environ, "AGENCY_DIR": repo, "AGENCY_NO_PUSH": "1", "AGENCY_AGENT": agent}
    r = subprocess.run([sys.executable, cli, *args], capture_output=True, text=True, env=e)
    if expect != "any":
        assert r.returncode == expect, f"{args} -> {r.returncode}\n{r.stdout}\n{r.stderr}"
    return r


def main():
    t0 = time.time()
    n = 0
    repo = fresh_repo()
    try:
        run(repo, "init", "--name", "nova")
        run(repo, "jobs", "claim", "t-9-work", "--hours", "4")

        # closing without evidence is refused — the discipline the quorum was supposedly providing
        r = run(repo, "jobs", "accept", "t-9-work", expect=1)
        assert "evidence claim" in r.stderr, r.stderr
        r = run(repo, "jobs", "accept", "t-9-work", "--reason", "ok", expect=1)
        assert "evidence claim" in r.stderr, r.stderr
        n += 2

        st = json.load(open(os.path.join(repo, "jobs/t-9-work/STATUS.json")))
        assert st["status"] == "claimed", "a refused close must not change state"
        n += 1

        r = run(repo, "jobs", "accept", "t-9-work",
                "--reason", "deadbeef1234 + 93 assertions, 11 files, gate green")
        assert "accepted t-9-work" in r.stdout, r.stdout
        assert "retired" in r.stdout, "the tool should say the rule changed, not silently comply"
        st = json.load(open(os.path.join(repo, "jobs/t-9-work/STATUS.json")))
        assert st["status"] == "accepted" and st["owner"] is None, st
        assert st["accepted_by"] == "nova" and "deadbeef1234" in st["evidence"], st
        assert "director" in st["authority"], "the authority for the waiver must be on the record"
        hand = open(os.path.join(repo, "jobs/t-9-work/HANDOFF.md")).read()
        assert "accepted · deadbeef1234" in hand, hand
        n += 5

        # a closed job must stop looking like a held lease (the ⏰ came from an expired CLAIM)
        lst = run(repo, "jobs", "list").stdout
        assert "⏰" not in lst.split("t-9-work")[1][:60], f"accepted job shown as a zombie holder:\n{lst}"
        claim = json.load(open(os.path.join(repo, "jobs/t-9-work/CLAIM.nova.json")))
        assert claim.get("closed") is True, claim
        n += 2

        # idempotence: the second accept must not overwrite the first record
        r = run(repo, "jobs", "accept", "t-9-work", "--reason", "deadbeef1234 again", expect=1)
        assert "already accepted" in r.stderr, r.stderr
        n += 1

        old = os.environ.get("AGENCY_OLD_CLI")
        if old and os.path.exists(old):
            r = run(repo, "jobs", "accept", "t-9-work", "--reason", "sha + ran it", cli=old, expect="any")
            assert r.returncode != 0 and "accept" in (r.stderr + r.stdout), \
                "the pre-fix build must NOT have this verb, or the test proves nothing"
            n += 1

        # to stderr, the house convention that run_all reads (F49: on stdout it passed while contributing
        # nothing to the count, which is precisely the invisible-green problem run_all now refuses)
        print(f"jobs_accept: {n} assertions ok ({time.time() - t0:.1f}s)", file=sys.stderr)
    finally:
        import shutil
        shutil.rmtree(repo, ignore_errors=True)


if __name__ == "__main__":
    main()
