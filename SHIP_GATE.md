# SHIP_GATE.md — the only gate between your branch and main
<!-- EPOCH: 2026-10-20.1 · tier-law file: changes need 2 pre-merge votes + Director -->
<!-- ship.sh runs every line starting with "$ " in order. Any failure = no ship. -->

## tier: work — workers self-merge on green

$ python3 tests/run_all.py
# add repo-specific gates below, e.g.:
# $ python3 tests/test_shift_system.py
# $ ffprobe -v error -show_entries format=duration -of csv=p=0 dist.mp4
# $ python3 tools/check_evidence.py jobs/<id>/

## Message authoring, and why pc-eye's hook is not portable here (F39, recurring 2026-10-27)

* An authored commit message goes through `git commit -F - <<'MSG'` with a **quoted** delimiter. In a
  double-quoted `git commit -m "…"`, the shell expands backticks and `$()` before git sees anything: mine
  ran `jobs accept`, printed `no such job`, and silently deleted those two words from the sentence that
  was describing the bug. The text is unrecoverable in that commit — which is why the fix is the
  invocation, not proofreading.
* **Do not copy `pc-eye/tools/git-hooks/pre-commit` into this repo.** In pc-eye it refuses every commit on
  `main`, and that is right. Here, `main` is the board: `agency claim|phase|heartbeat|release|accept|vote`
  commit and push straight to it by design (`commit_push`). A no-commits-on-main hook would break the
  machine it is meant to protect — a guard that fails the thing it guards is worse than none (the same
  lesson as the guard that reproduced the crash). If a hook is ever wanted here, the invariant is different:
  *authored* commits on main must carry a `board:`-shaped exception, which no shell-side rule can tell
  reliably. So the rule stays mechanical on pc-eye and behavioural here.
* Any count this file quotes is generated, never typed: `python3 tests/run_all.py`'s **last line** is the
  number (`13 passed · 0 failed · 111 assertions`). Reading the per-file lines instead double-counts the
  total — which is how "222" got into two documents today before anyone noticed.
