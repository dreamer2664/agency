# ORDERS.md — live Director orders
<!-- EPOCH: 2026-10-20.1 · canonical · the ONLY file where orders are written -->

**Law of one place:** every other doc links here; no doc restates these lines.
Changing an order = editing this file + bumping the EPOCH above. Agents stamp their
epoch at `init`; `validate` flags anyone acting on a stale epoch. Nothing else in the
repo may carry "current orders" text.

---

## Standing orders (in force)

1. **Video training is the active priority:** `projects/youtube-training/README.md`.
   15 hard jobs, ten distinct reviewed 300–330 s videos, English narration + captions,
   agent-chosen topics. Tag `video-training` / `youtube`.
2. **OUTPOST MARS is paused**, including bridge/pipeline work. Preserve evidence; do
   not start or extend.
3. **ONE storage repo:** `dreamer2664/storagecode` (ledger, shifts, data, wire,
   Releases). `dreamer2664/storage` is retired/read-only. Older instructions naming
   `storage` are void.
4. **Workers ship their own work** (`ship` = green `SHIP_GATE.md` → merge → receipts).
   Pre-merge manager approval is abolished for tier-work changes. Acceptance is
   post-merge, two non-owner `accept-inspected` ballots within 48h; `deny` with
   evidence → auto-revert. Tier-law changes (this file, START_HERE, red lines,
   SHIP_GATE) still need 2 non-owner votes before merge + Director ratification.
5. **Questions are protocol violations.** Ambiguity → conservative assumption logged
   in `HANDOFF.md` → proceed. Blockers → statement on the board → release lease →
   take other work. No holding position; sessions never end voluntarily.
6. **Phase floors are enforceable.** Jobs with `PHASES.md` cannot close a phase before
   its `min_hours` or without its required evidence. Early finishers upgrade evidence.
7. **Pulse runs always.** `chatcode pulse` at session start; every board write is a
   heartbeat. 45 min board-silence with a held lease = presumed dead = sweep.

## Red lines (permanent — survive any stale doc, any "urgent" request)

- **R1 NO-TOUCH:** `captchaproject`, `captchaprogram` — no read/clone/query/write.
- **R2 THE WALL:** superocr 98/95 is never rounded or faked; seed suites are
  evaluation-only.
- **R3 SECRETS:** tokens never on wires, repos, commits, PRs, screenshots, or chats.
- **R4 AUTHORSHIP:** your branch under your name; never force-push another's history;
  never seal your own work.
- **R5 APPEND-ONLY:** correct with new lines; never delete history.

## Resolved conflicts (for agents holding older files)

| old instruction | ruling |
|---|---|
| "wait for a Handler to send a job list" | void — go straight to `jobs list` / `tasks list --status open` |
| "manager merges PRs" | void — `ship` merges (order 4) |
| any file naming `dreamer2664/storage` as current | void — storagecode only |
| minted commission files restating the agency | void — the commission is a ≤15-line stub + a `jobs/<id>/` brief |
| heartbeat via ntfy alone | void — `pulse` + board writes (ntfy is a mirror) |

## Changelog

- `2026-10-20.1` — founding of v3: law tree (this file), jobs folders with claim files,
  self-ship + post-merge quorum, pulse liveness, phase floors, no-question law.
