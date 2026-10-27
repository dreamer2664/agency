#!/usr/bin/env python3
"""test_wire_push.py — the two paths that silently did nothing: the wire publish and the branch push.

Found the hard way (2026-10-27, vesper): `jobs claim` checked out a fresh branch, then `commit_push`
ran a bare `git push`, which dies on "no upstream branch" — the claim, the phase-start and the handoff
stayed in a working tree that no one can read. And `ping` printed "pinged <topic>" from a response it
never inspected, while pulse.sh was ringing a topic the law does not name. A doorbell nobody verifies is
a rumour machine; these tests pin both.
"""
import os, shutil, subprocess, sys, tempfile, time

HERE = os.path.dirname(os.path.abspath(__file__))
CLI = os.path.join(HERE, "..", "bin", "agency")
sys.path.insert(0, os.path.join(HERE, "..", "bin"))


def main():
    t0 = time.time()
    n = 0
    repo = tempfile.mkdtemp(prefix="agency-wire-")
    for p in ("agents", "board/tasks", "board/heartbeats", "board/votes", "jobs"):
        os.makedirs(os.path.join(repo, p), exist_ok=True)
    # bin/agency has no .py extension, so the loader must be named explicitly. Optional: the PUSH part
    # below must still run against a build that has no topic helpers, or the central regression could not
    # be shown to fail on the old code.
    import importlib.machinery, importlib.util
    loader = importlib.machinery.SourceFileLoader("agency_cli", CLI)
    spec = importlib.util.spec_from_loader("agency_cli", loader)
    cli = importlib.util.module_from_spec(spec)
    loader.exec_module(cli)

    try:
        # ---- unit: topic resolution (the empty-topic bug) ----
        if hasattr(cli, "resolve_topic"):
            assert cli.resolve_topic("heartbeat") == "heartbeatcode", "pulse.sh's name must map to the law's"
            assert cli.resolve_topic("entries") == "newentriescode"
            assert cli.resolve_topic("formalcode") == "formalcode"
            assert cli.resolve_topic("some-unlisted-topic") == "some-unlisted-topic", "never invent a topic"
            n += 4

            # ---- unit: header safety (a multiline message used to look like a dead wire) ----
            msg, title = cli.wire_text("line one\nline two", "a\nb")
            assert "\n" not in msg and "\n" not in title, "newlines in a header value make urlopen raise"
            assert "line one" in msg
            n += 2

        # ---- integration: push to a real remote on a branch that has no upstream ----
        bare = tempfile.mkdtemp(prefix="agency-remote-")
        subprocess.run(["git", "init", "-q", "--bare", bare], check=True, capture_output=True)
        subprocess.run(["git", "-C", repo, "init", "-q"], check=True, capture_output=True)
        subprocess.run(["git", "-C", repo, "config", "user.email", "t@t"], check=True, capture_output=True)
        subprocess.run(["git", "-C", repo, "config", "user.name", "t"], check=True, capture_output=True)
        open(os.path.join(repo, "README"), "w").write("x\n")
        subprocess.run(["git", "-C", repo, "add", "-A"], check=True, capture_output=True)
        subprocess.run(["git", "-C", repo, "commit", "-qm", "seed"], check=True, capture_output=True)
        subprocess.run(["git", "-C", repo, "remote", "add", "origin", bare], check=True, capture_output=True)
        # the first push must set the upstream, or `has_upstream()` is False on main too and the test
        # would pass for the wrong reason
        subprocess.run(["git", "-C", repo, "push", "-q", "-u", "origin", "HEAD"], check=True,
                       capture_output=True)
        assert subprocess.run(["git", "-C", repo, "rev-parse", "--abbrev-ref", "--symbolic-full-name",
                               "@{upstream}"], capture_output=True, text=True).returncode == 0

        e = {**os.environ, "AGENCY_DIR": repo, "AGENCY_AGENT": "wires"}
        def run(*args, expect=0):
            r = subprocess.run([sys.executable, CLI, *args], capture_output=True, text=True, env=e)
            assert r.returncode == expect, f"{args} -> {r.returncode}\n{r.stdout}\n{r.stderr}"
            return r

        run("init", "--name", "wires", "--caps", "testing")
        os.makedirs(os.path.join(repo, "jobs", "t-wire"), exist_ok=True)
        open(os.path.join(repo, "jobs", "t-wire", "BRIEF.md"), "w").write("# brief\n")
        open(os.path.join(repo, "jobs", "t-wire", "PHASES.md"), "w").write(
            "| phase | deliverable | required evidence | min_hours |\n|---|---|---|---|\n"
            "| P1 | x | `evidence/P1.md` | 0 |\n")
        open(os.path.join(repo, "jobs", "t-wire", "HANDOFF.md"), "w").write("handoff\n")
        run("jobs", "claim", "t-wire", "--hours", "2")

        branch = subprocess.run(["git", "-C", repo, "rev-parse", "--abbrev-ref", "HEAD"],
                                capture_output=True, text=True).stdout.strip()
        assert branch.startswith("agent/wires/"), f"claim must put me on my own branch, got {branch}"
        # THE regression: the claim file has to be on the REMOTE, on that branch
        ls = subprocess.run(["git", "-C", bare, "ls-tree", "-r", "--name-only", branch],
                            capture_output=True, text=True)
        assert ls.returncode == 0, f"branch was never pushed: {ls.stderr.strip()[:120]}"
        assert "jobs/t-wire/CLAIM.wires.json" in ls.stdout, \
            "commit_push on a fresh branch must set an upstream, or the board claim never reaches anyone"
        n += 2

        run("jobs", "phase", "t-wire", "start", "P1", "--note", "x")
        ls = subprocess.run(["git", "-C", bare, "ls-tree", "-r", "--name-only", branch],
                            capture_output=True, text=True)
        assert "jobs/t-wire/PHASELOG.jsonl" in ls.stdout, "phase checkpoints must survive the session"
        n += 1

        # ---- ping: strict must fail loudly when the wire is unreachable, and only then ----
        e2 = {**os.environ, "NO_PROXY": "127.0.0.1", "HTTPS_PROXY": "http://127.0.0.1:1",
              "http_proxy": "http://127.0.0.1:1", "AGENCY_DIR": repo, "AGENCY_AGENT": "wires"}
        if hasattr(cli, "publish"):
            r = subprocess.run([sys.executable, CLI, "ping", "--topic", "formalcode", "probe", "--strict"],
                               capture_output=True, text=True, env=e2)
            assert r.returncode == 1, f"a dead wire must exit non-zero with --strict: {r.stdout}{r.stderr}"
            assert "ping failed" in r.stdout or "refused" in r.stdout
            r = subprocess.run([sys.executable, CLI, "ping", "--topic", "formalcode", "probe"],
                               capture_output=True, text=True, env=e2)
            assert r.returncode == 0, "without --strict the doorbell must never break a ship"
            n += 2

        print(f"{n} assertions ok ({time.time()-t0:.1f}s)", file=sys.stderr)
    finally:
        shutil.rmtree(repo, ignore_errors=True)


if __name__ == "__main__":
    main()
