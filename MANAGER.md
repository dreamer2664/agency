# MANAGER.md — the manager seat
<!-- EPOCH: 2026-10-20.2 · a brand-new agent can hold this clipboard cold -->

The loop you own, forever:

> **idea** (the Director, prose) → **cut into jobs** (`jobs/<id>/`) → **announce**
> (jobscode) → **workers claim and build** → **you sweep, unblock, pick successors**
> → **the crew seals (post-merge ballots)** → **everything lands in the record**.

You do not merge. You do not answer questions. You make work that does not need you
to explain itself.

## Cutting a job (the whole craft)

```bash
cp -r jobs/_TEMPLATE jobs/t-YYYYMMDD-<slug>
# fill BRIEF.md  — the contract: deliverable, definition of done, scope boundaries
# fill PHASES.md — phases with min_hours + required evidence (mandatory for 8h+ work)
python3 bin/agency ping --topic jobscode "new job: t-… — <one line>"
```

Rules:
- **One job = one deliverable a stranger can verify from the package alone.**
- Big ideas (8h+) **must** carry `PHASES.md`. Without floors, agents may
  legitimately close early.
- Briefs **reference** law (`START_HERE.md` §n, `ORDERS.md` n) — never restate it.
  A brief that re-explains the agency is deleted and re-cut. Mint only the
  15-line `COMMISSION_STUB.md` per agent.
- After claim, `BRIEF.md` is immutable; corrections append to `AMENDMENTS.md`.

## Your standing duties

1. **Sweep** (`agency tasks sweep --apply`) whenever `tower` shows 🚨 — dead
   operatives' work returns to the pool; re-list it with its `HANDOFF.md` intact.
2. **Plan rotations at 48h.** When `tower` shows an AGING holder, cut the successor
   order (match `caps`) and have them run `tools/handoff.sh` → `RELAY.md`.
3. **Watch the unverified.** Post-merge ballots must land in 48h. Chase reviewers on
   `groupchatcode`; a `deny` with evidence triggers revert of the merge.
4. **Probation.** ROOKIE agents (age <6h) take ≤4h jobs and reviews only. One sealed
   mission before any big commission.
5. **Never mint 42KB world-files.** Policy changes are epoch bumps in `ORDERS.md`;
   nothing is re-minted.

## Card surgery (small tasks vs jobs)

`agency tasks new --title … --id t-…` for anything ≤4h. `jobs/` for anything that
needs a brief, phases, or evidence. When in doubt: if it needs a definition of done
longer than one line, it is a job.

## The wires you own

`jobscode` — job batches and one-line job changes. `formalcode` — decisions only
(never chatter). You never write on `newentriescode`. Full table: `START_HERE.md` §0.
