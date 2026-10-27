# BRIEF — t-20261027-pceye-hardening

<!-- EPOCH: 2026-10-20.3 · briefs reference law, they never restate it -->
**Owner seat:** vesper (self-cut on Director order) · **Lane:** `pc-eye` · **Size:** M ·
**Board card:** t-20261027-pceye-hardening (this folder is the contract)

## Deliverable (the contract — one package a stranger can verify)

In `dreamer2664/pc-eye`, pushed under the author's own name:

1. `AUDIT.md` — a flaw register of the whole process (server + launcher + start.bat +
   docs + tests), each entry: symptom → root cause → why it looked like success →
   the fix → the regression test that pins it. Severity-ranked.
2. Code fixes for every flaw classified CRIT or HIGH, plus the speed work that is
   measurable. Nothing "improved" without a before/after number.
3. `evidence/BENCH_BEFORE.json` / `evidence/BENCH_AFTER.json` + a summary table of
   measured deltas (encode path, route latency, concurrency, per-action cost).
4. `tests/test_pc_eye.py` extended so every fixed flaw has a named regression test;
   the suite stays runnable headless on Linux AND declares what it cannot prove.
5. `.github/workflows/ci.yml` — the repo had no CI; the two bugs the README admits
   were "invisible from Linux" are exactly what a Windows CI leg catches.
6. Docs brought back in sync with the code (README/PC-EYE.md drifted: refusal table
   mis-ordered, version string stale, promised behaviours not implemented).

## Definition of done

- [x] every line of "Deliverable" exists at a pushed SHA
- [x] required evidence of every phase in `PHASES.md` present in `evidence/`
- [x] `HANDOFF.md` current, honest, secret-free
- [x] `python3 -m unittest discover -s tests` green on Linux, dry-run only (no real
      input injected — there is no PC in this session, by Director instruction)
- [x] `tools/ship.sh` green (gate passed, merged, PUSHES.md row written)
- [x] words in the final wire message: "Independent non-owner acceptance remains PENDING"

## Scope boundaries

- in: pc-eye source, tests, docs, CI, its own README claims.
- out: superocr/qcaptcha (read-only provenance only), the Director's real PC (never
  touched — no tunnel, no live input), any repo not named `pc-eye`.

## Hard constraints

No secrets in any pushed file or on any wire (R3). pc-eye's own log must not carry
typed payloads (that was one of the findings). Stdlib + Pillow only, no new deps.
Every "faster" claim must be a measurement from `evidence/bench.py`, not adjectives.
Append-only: correct the ledger with new rows (R5).

## Starting point (if resuming)

Baseline is `bb68297` (tag of the 1.0.2 state, "32 tests"). `evidence/bench.py` in
pc-eye is the harness used for the before/after numbers — run it before claiming any
speed win. The audit register in `AUDIT.md` numbers findings F1..Fn; work the CRITs
first. If a session dies here: the branch holds unshipped fixes, `HANDOFF.md` says which
findings are fixed vs open.
