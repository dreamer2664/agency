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
   Pre-merge manager approval is abolished for tier-work changes. **Amended
   2026-10-27 by the Director: acceptance no longer requires a ballot quorum** —
   the owner closes with `agency jobs accept <id> --reason '<head SHA> + what you
   ran'`, and a `deny` with evidence from anyone is still a revert request. The
   quorum was retired because it could not be cast on a job id at all (F48), not
   because review is worthless: `vote`/`review next` remain for tasks and are welcome
   everywhere. Tier-law changes (this file, START_HERE, red lines, SHIP_GATE) no
   longer need 2 pre-merge votes either — they need Director ratification, which for
   this very paragraph is his instruction of 2026-10-27. **The fail-closed SHIP_GATE
   is untouched by this order: the machine still has to be green before main moves.**
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

- `- **2026-10-27.3** (vesper) · F56 — `ping --strict` published a record its own clamp had shortened. `wire_text` truncates to the 4000-byte wire budget and appends a visible `[… N bytes dropped]` notice, so the *reader* could see the loss while the *author's* `--strict` still said "read back id …". That is the tool that exists to promise completeness promising it about an incomplete record. Now `clamp_loss()` is consulted before anything is sent: `--strict` refuses (`die()`, exit 1 — the CLI's convention; I first wrote "exit 2" from intent rather than from a run, and corrected it on the wire as lO5LInhagKR1) and sends nothing, telling you to split the message or shorten it, while a non-strict doorbell still sends and prints `[NOTICE …B dropped …]`. Titles are covered too — the same clamp, the same silence. The rule: **a doorbell may be short; a record may not be silently shortened.** Two side notes, both learned today: the byte counting stays bytes, not characters (an em-dash is 3, and there is an assertion for it), and the F45 negative control correctly refused my stale `/tmp` snapshot of the pre-fix build with "this test proves nothing" instead of passing — a check that cannot fail is the thing being audited, and it caught itself.
- **2026-10-27.2** (vesper) · F51 — finding ids collide across repos. `agency F43` (the ballot quorum) and `pc-eye F43` (order-dependent test seams) are different findings with the same name, and the wire plus this changelog use one shared sequence while each repo's own file keeps its own. The history cannot be renumbered — the ids are already in pushed messages and commit bodies — so the rule from today forward: **write the repo in front of the id** (`pc-eye F44`, `agency F48`), and any new register starts at a per-repo prefix (`PCE-`, `AGC-`) so a reader never has to guess which audit they are in. Cheap to obey, expensive to discover: an ambiguous id in a revert request is how the wrong fix gets shipped.
2026-10-27.1` — **acceptance, per the Director's instruction of that day**: the
  2-ballot quorum is retired and the owner closes a job with an evidence claim
  (`jobs accept`, new). Reason recorded in AUDIT/`PATCH_NOTES` as F48: the quorum was
  unaddressable for jobs (`vote` reads `board/tasks/`, jobs live in `jobs/`), so every
  job ended in a state that looked pending and could never be satisfied; two of my own
  shifts stalled on describing it rather than on the work. `review`/`vote` kept for
  tasks and as voluntary peer review; `deny` with evidence still means revert. SHIP_GATE
  and the red lines are unchanged — the gate is the safety, the ballot was the theatre.
  Also same-day CLI fixes from using it: F43 (heartbeat rang nothing), F44 (latin-1
  titles), F45 (`verify=True` polled "newest message" and declared a delivered message
  lost), F46 (over-4096-BYTE bodies stored as an attachment, silently), F47 (bodies
  flattened to one line). Suite 93 → 120 assertions across 13 files — and F49, found while writing that test: `run_all.py` printed `PASS <file> ()` for a file whose count it could not find, so my first version passed while contributing nothing to the total everyone quotes. The runner now reads the count from either stream and FAILS a green file with no count, and it takes a directory argument so that behaviour is testable against a fake tree (F49); F50 — the byte-clamp from F46 appended its notice with a leading newline, legal in a body and fatal in a header, so any title over 120 bytes died in `putheader` with `ValueError: Invalid header value`: the exact defect F22 was written to prevent, reintroduced by a fix to a neighbouring bug (13th test file, 6 assertions).
- `2026-10-20.3` — enforcement moved from prose into code: `onboard` (entry battery
  as one command), phase floors (`jobs phase/gate` — min_hours + evidence, fail-closed),
  lifecycle claim gating (ROOKIE ≤4h · AGING none · RETIRED none — mechanical),
  `watch` (zombies, silence, unverified post-merge, degradation signals) + nightwatch
  workflow, `migrate_chatcode.py` (legacy board import), `stub`/`epoch` minting and
  drift detection. Test suite 9/9 (54 assertions).
- `2026-10-20.2` — 2GB sandbox doctrine, relay/handoff, TOWER liveness, tools suite.
- `2026-10-20.1` — founding of v3: law tree (this file), jobs folders with claim files,
  self-ship + post-merge quorum, pulse liveness, phase floors, no-question law.
