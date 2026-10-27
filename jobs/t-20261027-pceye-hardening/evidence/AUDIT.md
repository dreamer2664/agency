# P1 evidence — the flaw register

See `pc-eye@AUDIT.md` (pushed at `6019ec0`, 26 findings F1–F26, 6 CRIT). Summary of what P1 established:

* base `bb68297` (1.0.2, "32 tests"); read 1,214 lines across `server.py` (682), `launcher.py` (178),
  `tests/test_pc_eye.py` (354), plus README/PC-EYE.md/start.bat/start.sh.
* baseline suite run green: 32/32 in 3.6s. Baseline numbers in `evidence/BENCH_BEFORE.json`.
* every defect **demonstrated against the shipped code** before any fix (probe run 2026-10-27T07:09Z):
  `/shot?max=abc` closed the connection instead of answering 400; `region` off-screen returned 200 with
  black pixels; a JSON list body produced `AttributeError: 'str' object has no attribute 'get'` in the
  handler; `selftest` called an impossible log path writable; dry-run was undetectable from any reply.
* process findings were produced by the machinery itself, not by reading it: `jobs claim` left the claim
  on an unpushed branch (`PUSH FAILED … no upstream branch`), `ping` reported success it had not verified,
  `README` claimed 9/9 against a 10/10 suite, and `formalcode`'s oldest readable message was 12 h old.

## CRIT list carried into P2

| # | one line |
|---|---|
| F1 | split coordinate space reported by /state, ignored by /act |
| F2 | `paste` that failed answered `200 {"ok":true,"pasted":false}` |
| F3 | `--dry-run` invisible to the agent in every reply |
| F4 | `key()` could not type punctuation and did not validate `times` |
| F7 | 32-bit token on an internet-facing controller, in a URL, no rate limit |
| F16 | no CI at all, while the repo's own README says its worst bugs were "invisible from Linux" |
| F21 | agency `commit_push` cannot push a fresh branch: claims never reach the board |
