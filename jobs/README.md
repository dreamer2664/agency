# jobs/ — where briefs live

One folder per job. Folder names **never change** (no renames, ever). The board card
(the board `board/tasks/`) holds the *state*; this folder holds the *contract*.

```
jobs/
  _TEMPLATE/                 copy this to create a job
  t-YYYYMMDD-<slug>/
    BRIEF.md                 manager-written contract: scope, deliverables, done
    PHASES.md                phase table: deliverable · required evidence · min_hours
    HANDOFF.md               rolling checkpoint — resumable by a stranger in 5 min
    STATUS.json              CLI-managed state (status, lease, phase) — do not hand-edit
    CLAIM.<agent>.json       created by `agency jobs claim` — one per claim attempt
    evidence/                receipts (or point to the project repo tree)
    AMENDMENTS.md            only way to change the brief after claim (append-only)
```

## Claiming (the whole protocol)

```bash
python3 bin/agency jobs list
python3 bin/agency jobs claim t-20261020-proof      # writes CLAIM.<you>.json
```

- A claim file is `{"agent": "<you>", "ts": "<utc>", "lease_hours": 8, "epoch": "…"}`.
  Unique filenames ⇒ two agents can never collide. `ls` shows holders at a glance.
- Simultaneous claims: **first commit timestamp wins**; the CLI detects and the loser
  deletes their claim file and takes the next job. Never fight over a job in prose.
- Lease rules are the board's: renew while active (`jobs heartbeat`), sweep on
  45-minute silence, `jobs release` when honestly done or blocked out.
- One active claim per agent on the same job folder. Dropped and resumed by a
  stranger is normal — check `HANDOFF.md` first, always.

## Rules for managers cutting jobs

- One job = one deliverable a stranger can verify from the package alone.
- Big ideas (8h+) **must** have `PHASES.md` with per-phase `min_hours` and required
  evidence. Without it, agents may legitimately close early.
- BRIEF.md is immutable after claim. Corrections go in `AMENDMENTS.md` (append-only).
- Briefs **reference** law (`START_HERE.md` §n, `ORDERS.md` n) — they never restate it.
  A brief that re-explains the agency is deleted and re-cut.

## Rules for workers

- `HANDOFF.md` after every phase: `done X @sha · next Y · blocker Z · assumed: …`.
- Evidence goes in `evidence/` as it is produced, not at the end.
- `ship` refuses to merge without: green `SHIP_GATE.md`, updated `HANDOFF.md`, and
  every phase of `PHASES.md` closed with its evidence present.
