import pathlib

p = pathlib.Path("/home/user/agency/bin/agency")
s = p.read_text()

old = '''def commit_push(root_, paths, msg):
    """Commit, then push the CURRENT branch — with an upstream if it does not have one yet.'''
new = '''def commit_push(root_, paths, msg):
    """Commit ONLY `paths`, then push the CURRENT branch — with an upstream if it does not have one yet.

    The `-- paths` on the commit is the whole point. `git add <paths>` + bare `git commit` commits the
    *index*, and the index is sticky: one earlier `git add -A` by hand (or by another command) and every
    staged-but-uncommitted file in the tree rides into a commit labelled "jobs: <id> P1 close". That is how
    agency@81ea552 came to contain the production CLI, a new test file, pulse.sh and README under a label
    naming two job files — a bisect lands on it, reads the label, and stops (pc-eye AUDIT.md F34).
    A pathspec on the commit makes the label true by construction.
    """'''
assert old in s
s = s.replace(old, new, 1)

# remove the now-duplicated old docstring line block
s = s.replace('''    """
    sh("git", "-C", root_, "add", *paths)''', '''    for f in paths:                                   # a board commit may carry board files, only
        nf = _foreign_file(f, msg)
        if nf:
            die(f"{msg.split(':')[0]} commit refused: {nf}. Add it in its own commit with its own label — "
                f"an append-only board is only trustworthy if a commit's label describes its content.")
    sh("git", "-C", root_, "add", *paths)''', 1)

old = '''    sh("git", "-C", root_, "commit", "-m", msg)'''
new = '''    sh("git", "-C", root_, "commit", "-m", msg, "--", *paths)'''
assert old in s
s = s.replace(old, new, 1)

anchor = '''def commit_push(root_, paths, msg):'''
helper = '''def _foreign_file(f, msg):
    """The one file in this commit whose content is not what the commit's label is about, or None.

    Board/wire/jobs commits are append-only records that other agents read, so their label has to be
    true on its own. Everything else (an agent's own branch commit) may carry whatever it likes.
    """
    f = str(f).replace("\\\\", "/").lstrip("./")
    kind = (msg or "").split(":")[0].split()[0].lower()
    if kind not in ("jobs", "board", "wires", "entry", "digest", "sweep"):
        return None
    if f.startswith(("jobs/", "board/", "agents/", "evidence/", "wires/", "ledger/")):
        return None
    return (f"{f} is staged into a {kind!r} commit, and this repo's writers commit ONLY the paths they "
            f"name")


'''
assert "def _foreign_file(" not in s
s = s.replace(anchor, helper + anchor, 1)
p.write_text(s)
print("commit_push: pathspec + label guard")

# ---------- the test that proves both ----------
t = pathlib.Path("/home/user/agency/tests/test_wire_push.py")
s = t.read_text()
assert "F34" not in s, "already extended?"
s = s.rstrip() + '''


# ---------------------------------------------------------------- F34: the label must be true
# A board writer that commits the *index* sweeps whatever a human (or another command) staged earlier into
# a commit whose message names two job files. agency@81ea552 did exactly that — bin/agency, a new test,
# pulse.sh and README, all under "jobs: … P1 close". These two assertions pin the fix: the commit carries
# only its paths, and a foreign file in those paths is refused instead of swept.
def test_f34_board_commit_carries_only_its_own_paths(repo):
    """Same repo fixture as the push tests above (a real bare remote + a worktree)."""
    (repo.work / "bin").mkdir(exist_ok=True)
    (repo.work / "bin" / "agency").write_text("#!/bin/sh\\necho edited-by-hand\\n")
    (repo.work / "README.md").write_text((repo.work / "README.md").read_text() + "\\n# note\\n")
    # the exact mistake: a human stages the whole tree, then a writer commits "just" the board file
    repo.git("add", "-A")
    repo.commit_push(["jobs/t-f34/PHASELOG.jsonl"], "jobs: t-f34 P9 start by vesper")
    changed = repo.committed_files(-1)
    assert set(changed) == {"jobs/t-f34/PHASELOG.jsonl"}, \\
        f"a jobs commit swept in other staged files: {sorted(changed)}"
    print("  ok  a jobs commit carries only the paths it names (index is not a to-do list)")


def test_f34_writer_refuses_a_foreign_path_in_a_board_commit(repo):
    try:
        repo.commit_push(["jobs/t-f34/PHASELOG.jsonl", "bin/agency"], "jobs: t-f34 P9 start by vesper")
    except repo.Refused as e:
        assert "bin/agency" in str(e), e
        print("  ok  a board commit refuses to carry source files (label stays true)")
    else:
        raise AssertionError("the writer accepted bin/agency inside a 'jobs:' commit — F34 is still open")
'''
t.write_text(s)
print("F34 assertions added")
