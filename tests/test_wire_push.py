#!/usr/bin/env python3
"""test_wire_push.py — the two paths that silently did nothing: the wire publish and the branch push.

Found the hard way (2026-10-27, vesper): `jobs claim` checked out a fresh branch, then `commit_push`
ran a bare `git push`, which dies on "no upstream branch" — the claim, the phase-start and the handoff
stayed in a working tree that no one can read. And `ping` printed "pinged <topic>" from a response it
never inspected, while pulse.sh was ringing a topic the law does not name. A doorbell nobody verifies is
a rumour machine; these tests pin both.
"""
import json
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

            # ---- unit: header safety (a multiline TITLE used to look like a dead wire) ----
            msg, title = cli.wire_text("line one\nline two", "a\nb")
            assert "\n" not in title, "newlines in a header value make urlopen raise"
            assert "line one" in msg
            # F47 reversed the body half of the old rule deliberately: the payload is what the crew reads, so
            # it keeps its paragraphs. The assertion states both halves, because the earlier version ("no
            # newlines anywhere") is exactly what mangled every structured ping into one sentence.
            assert "\n" in msg, "a body must keep its newlines (F47)"
            n += 3

        # ---- unit F44: the transport cannot carry what an agent types most (em-dashes) ----
        for bad in ("[pulse] vesper \u2014 green", "[pulse] \u2013 arrows \u2192 here",
                    "[pulse] \u201cquoted\u201d \u2026"):
            _, ttl = cli.wire_text("body", bad)
            ttl.encode("latin-1")                       # would raise UnicodeEncodeError before the fix
            assert "\u2014" not in ttl and "\u2013" not in ttl and "\u201c" not in ttl
        n += 3
        _, plain = cli.wire_text("body", "[pulse] vesper \u00b7 ok")
        assert plain == "[pulse] vesper \u00b7 ok", "latin-1-safe titles must pass through untouched"
        body, _ = cli.wire_text("em-dash in the body \u2014 stays", "t")
        assert "\u2014" in body, "only the HEADER is folded; the body is UTF-8 and must keep its text"
        n += 2

        # ---- unit F46: the wire's limit is BYTES, and an oversize body becomes a FILE silently ----
        long = "\u2014" * 6000                                  # 18,000 bytes, 6,000 characters
        msg, _ = cli.wire_text(long, "t")
        assert len(msg.encode("utf-8")) <= 4096, "the clamp must count bytes, not characters"
        assert msg.endswith("]") and "bytes dropped" in msg, f"truncation must be visible: {msg[-60:]}"
        assert "\ufffd" not in msg, "cutting mid-character would put U+FFFD in the crew's message"
        short, _ = cli.wire_text("plain ascii", "t")
        assert short == "plain ascii", "a normal message must not be touched"
        n += 3
        body47, _ = cli.wire_text("para one\n\n\n\npara two\n- bullet", "t")
        assert body47 == "para one\n\npara two\n- bullet", f"F47: paragraphs survive, 3+ blanks collapse: {body47!r}"
        n += 1

        # an attachment reply is a FAILURE, not a success with odd text
        att = {"hit": False}

        def att_urlopen(req, timeout=None):
            att["hit"] = True

            class R:
                def read(self):
                    return (b'{"id":"A1","attachment":{"url":"https://ntfy.sh/attach/A1/x.txt",'
                            b'"filename":"attachment.txt"}}')

                def __enter__(self):
                    return self

                def __exit__(self, *a):
                    return False
            return R()

        real = __import__("urllib.request", fromlist=["x"]).urlopen
        __import__("urllib.request", fromlist=["x"]).urlopen = att_urlopen
        try:
            ok_att, det_att = cli.publish("formalcode", "x" * 5000, title="t", verify=True, timeout=1)
        finally:
            __import__("urllib.request", fromlist=["x"]).urlopen = real
        assert ok_att is False, "an attachment reply must not be reported as a delivered message"
        assert "FILE" in det_att, det_att
        n += 2

        # ---- unit F45: the read-back must look for OUR id, not for "the newest message" ----
        # One fake serves both the new code and the pre-fix module: the POST always answers with an id, and
        # the poll answers `since=latest` with somebody else's message (a busy topic) while `since=<ts>`
        # returns the window that contains ours. So the old code cannot pass and the new code must.
        import io
        import urllib.request as _ur

        def run_publish(mod):
            state = {"body": "", "urls": []}

            class _Resp:
                def __init__(self, payload):
                    self._p = payload

                def read(self):
                    return self._p

                def __enter__(self):
                    return self

                def __exit__(self, *a):
                    return False

            def fake(req, timeout=None):
                url = getattr(req, "full_url", str(req))
                state["urls"].append(url)
                if "/json?" in url:
                    mine = json.dumps({"id": "MINE123", "topic": "heartbeatcode",
                                       "message": state["body"]}).encode()
                    other = json.dumps({"id": "OTHER9", "topic": "heartbeatcode",
                                        "message": "fledge \u00b7 entry battery (T5)"}).encode()
                    if "since=latest" in url:
                        return _Resp(other + b"\n")          # the newest message is not mine
                    return _Resp(other + b"\n" + mine + b"\n")
                state["body"] = req.data.decode()
                return _Resp(b'{"id":"MINE123"}')

            real = _ur.urlopen
            _ur.urlopen = fake
            try:
                ok, detail = mod.publish("heartbeat", "vesper \u00b7 still working", title="[pulse] vesper",
                                         verify=True, timeout=1)
            finally:
                _ur.urlopen = real
            return ok, detail, state

        ok_new, det_new, urls_new = run_publish(cli)
        assert ok_new is True, f"the fixed read-back still fails on a busy topic: {det_new}"
        assert "MINE123" in det_new, det_new
        assert not any("since=latest" in u for u in urls_new["urls"]), \
            "polling since=latest is the bug: it asks for the newest message, not for ours"
        n += 3

        old_cli_path = os.environ.get("AGENCY_OLD_CLI")
        if old_cli_path and os.path.exists(old_cli_path):
            import importlib.machinery as _mf
            ld = _mf.SourceFileLoader("agency_old", old_cli_path)
            old = importlib.util.module_from_spec(importlib.util.spec_from_loader("agency_old", ld))
            ld.exec_module(old)
            ok_old, det_old, _ = run_publish(old)
            assert ok_old is False, ("the pre-fix read-back passed the busy-topic scenario, so this test "
                                     f"proves nothing (got {det_old})")
            n += 1

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

        # ---- unit F43: `heartbeat` must ring the wire it prints about, and record the outcome ----
        seen = {}

        def fake_publish(topic, message, title=None, verify=False, timeout=None, **kw):
            seen.update(topic=topic, message=message, title=title, verify=verify)
            return True, "pinged heartbeatcode \u00b7 read back id TESTID"

        real_publish, real_push = cli.publish, cli.commit_push
        cli.publish, cli.commit_push = fake_publish, lambda *a, **k: None
        try:
            os.environ["AGENCY_DIR"] = repo
            os.environ["AGENCY_AGENT"] = "wires"
            import argparse
            # SystemExit from an in-process call would otherwise end the file with exit code 0 and a test
            # that verified nothing at all — which is the failure mode this whole repo exists to catch.
            try:
                cli.cmd_heartbeat(argparse.Namespace(agent="wires", note="still working", kind="pulse",
                                                     no_wire=False))
            except SystemExit as e:
                raise AssertionError(f"cmd_heartbeat exited instead of running: {e}")
        finally:
            cli.publish, cli.commit_push = real_publish, real_push
        assert seen.get("topic") == "heartbeatcode", f"heartbeat must ring the topic the law names, saw {seen}"
        assert seen.get("verify") is True, "a pulse that is not read back is a rumour (see F22)"
        hb = [json.loads(l) for l in open(os.path.join(repo, "board", "heartbeats", "wires.jsonl"))
              if l.strip()]
        assert hb and hb[-1].get("wire") is True, "the board line must record that the doorbell moved"
        cli.publish = lambda *a, **k: (False, "wire refused heartbeatcode with HTTP 500")
        try:
            try:
                cli.cmd_heartbeat(argparse.Namespace(agent="wires", note="x", kind="pulse", no_wire=False))
            except SystemExit as e:
                raise AssertionError(f"cmd_heartbeat exited instead of running: {e}")
        finally:
            cli.publish = real_publish
        hb = [json.loads(l) for l in open(os.path.join(repo, "board", "heartbeats", "wires.jsonl"))
              if l.strip()]
        assert hb[-1].get("wire") is False, "a failed ring must be in the record, not only on stdout"
        n += 4

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

        # ---- F34: a board commit may carry ONLY the paths its label names ----
        # agency@81ea552 was labelled "jobs: t-… P1 close" and contained bin/agency, a new test, pulse.sh
        # and README. Root cause: `git add <paths>` followed by a BARE `git commit` commits the index, and
        # one earlier `git add -A` — by a human mid-fix, exactly as happened here — is enough. Two
        # assertions: the commit stays narrow, and a writer that tries to smuggle source refuses.
        os.makedirs(os.path.join(repo, "jobs", "t-wire", "evidence"), exist_ok=True)
        open(os.path.join(repo, "jobs", "t-wire", "PHASELOG.jsonl"), "a").write(
            ' {"ts":"now","by":"wires","phase":"P1","action":"evidence"}\n')
        open(os.path.join(repo, "README"), "a").write("staged by a human mid-fix\n")
        open(os.path.join(repo, "bin", "agency"), "a").write("# edited in the same sweep\n") \
            if os.path.exists(os.path.join(repo, "bin", "agency")) else None
        subprocess.run(["git", "-C", repo, "add", "-A"], check=True, capture_output=True)
        r = cli.commit_push(repo, ["jobs/t-wire/PHASELOG.jsonl"], "jobs: t-wire P1 evidence by wires")
        files = subprocess.run(["git", "-C", repo, "show", "--name-only", "--pretty=format:", "HEAD"],
                              capture_output=True, text=True).stdout.split()
        assert files == ["jobs/t-wire/PHASELOG.jsonl"], \
            f"a jobs commit swept in other staged files: {files}"
        n += 1

        refused = {}
        real_die, cli.die = (cli.die, lambda m: refused.setdefault("m", m) or sys.exit(2))
        try:
            cli.commit_push(repo, ["jobs/t-wire/HANDOFF.md", "README"], "jobs: t-wire P1 by wires")
        except SystemExit:
            pass
        finally:
            cli.die = real_die
        assert "README" in refused.get("m", ""), \
            "a writer accepted a source file inside a 'jobs:' commit — F34 still open"
        n += 1

        print(f"{n} assertions ok ({time.time()-t0:.1f}s)", file=sys.stderr)
    finally:
        shutil.rmtree(repo, ignore_errors=True)


if __name__ == "__main__":
    main()
