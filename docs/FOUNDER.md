# FOUNDER'S BRIEF — Agency v3

**From:** the founder's seat · **To:** Carlo (the Director) · **Date:** 2026-10-20 (Europe/Rome)
**Subject:** what is actually broken, what to keep, what to throw, and the founding design.

---

## 0. Verdict in five lines

1. Your **ideology is right** (leases, evidence ladder, append-only, no self-review,
   "the archive outlives us"). Keep it as constitution. The problem is not the ideas —
   it is that the law is spread over **62+ commits of churn across 6+ competing MD files**,
   and every new agent must re-read a maze before its first hour of work.
2. **One universal entry file wins** over minted per-agent prompts — but it must be
   *strict, imperative, epoch-stamped, and short*. Per-agent files become **thin stubs**
   (15 lines), never 42KB restatements of the world.
3. **Your job-folder idea is right in instinct, wrong in mechanics.** Jobs as folders: yes.
   Claiming by *renaming the folder*: no — renames collide, break links, and are the
   worst merge conflicts in git. Claiming = **a claim file inside the job folder**
   (`CLAIM.<agent>.json`). Same `ls`-and-go visibility, zero collisions.
4. **Workers ship their own work.** Merge authority follows the test gate, not a manager's
   availability. Quality is preserved by moving the two-vote quorum to **post-merge
   acceptance** within a window, with auto-revert. "Ship is a command, not a permission."
5. **The `agency-agents` repo (msitarzewski) is not the way.** It is a catalog of ~300
   static IDE personas. Your problem is coordination state and liveness, not personality
   files. Steal nothing from it but the one-file-self-contained habit — which you already have.

---

## 1. What I found in your ecosystem (evidence, rung 6)

I cloned and read `chatcode`, `storagecode`, the front-door docs, the board (287 task
cards), the workflows, and the two manifestos you uploaded (field-kit / PRISM). Findings:

**A. The merge bottleneck is real and it is burning you personally.**
`storagecode/PUSHES.md` shows leonidas landing the entire shift-proof system on
**"Carlo's owner override (crew asleep, no votes cast)"** — four merges in one row.
The machine's design says "two seals close a mission", but in practice the crew parks
work and *you* wake up to push it over the line. That is the exact failure you describe:
workers can't push/merge, managers must be woken.

**B. Policy churn is the disease; the docs are the symptom.**
`START_HERE.md` 10 commits · `WORKER.md` 6 · `SYSTEM.md` 6 · `PROTOCOL.md` 19 ·
`AGENT_PROMPT.md` 17. There are **three generations of "front door"** live at once:
- field-kit.md (old law: "wait for a Handler to send a job list", names the **retired
  `storage` repo**, Three Wires)
- START_HERE.md (middle law: Five Wires, cold pipeline note bolted on top)
- WORKER.md (new law: straight to the room)

A fresh operative that receives the *wrong generation* obeys dead rules. Worse: the
PRISM commission is a **42KB file that restates the whole agency** — every policy change
now has to be re-minted into every commission. That is the treadmill you are on.

**C. Liveness is unmeasurable.**
Your own record: "the zero-heartbeat census" — leases existed, `heartbeatcode` was empty
for 24h, and the manager rightly refused to call anyone "running". ntfy is fire-and-forget:
it cannot be queried for "who is alive right now", and agents forget to post. Meanwhile
the board *does* have timestamps (heartbeats are landing in `board/tasks/` right now) —
you already have the data, you just treat ntfy as the source of truth.

**D. Big jobs die of impatience.**
PORTUS-stage cards and the PRISM timeline prove you already know how to phase work
(B05 + quay + basin…, checkpoint #1…#8). But nothing *mechanically* stops an agent from
declaring a 8-hour Blender commission "done" in 40 minutes with a plausible render.
Phase gates exist as prose, not as gates.

**E. Sessions die; questions kill sessions.**
Your rule "absolutely no asking questions" is correct engineering: a question ends the
loop and waits for a human who may be asleep. But the docs still contain soft exits
("post what failed and **hold position**"). Every "hold position" is a dead session.

**F. What is already excellent — do not touch it.**
Leases + checkpoints + `tasks sweep`, the review queue (`review next`), the evidence
ladder, the append-only ledger (`PUSHES.md`, shifts), `record.yml` auto-posting every
push to formalcode, `nightwatch` as the unattended lead, the red lines (captchaproject
no-touch, 98/95 never rounded). These are world-class. v3 *compresses the law* around
them; it does not replace the machine.

---

## 2. Verdicts on the specific ideas you floated

| idea | verdict | founder's ruling |
|---|---|---|
| Universal MD in the main repo, always changeable | ✅ **yes — this is the way** | Exactly one entry file + one orders file. Changing policy = editing one file + bumping an epoch number. |
| Minted per-agent MD prompts from a manager | ❌ **stop minting world-files** | Mint only a **15-line stub**: name, token, job pointer, epoch. Everything else reads from the repo at runtime. Policy changes never re-mint anything. |
| "Get in the repo and read the README" | ⚠️ half-right | Right idea, wrong file. READMEs rot. Use `START_HERE.md` with a **POLICY-EPOCH** header and a hard rule: *if the epoch on the roster is older than current, re-read before your next act.* |
| Manager cuts big ideas into MD files → job folder | ✅ **yes** | `jobs/<id>/` per job: `BRIEF.md` (the contract), `PHASES.md` (time floors + gates), `HANDOFF.md` (rolling resume point), `evidence/`. |
| Agent claims by **renaming the folder** with its name | ❌ **no renames** | Renames collide and break git history. Claim = create `jobs/<id>/CLAIM.<agent>.json`. `ls` shows holders at a glance (`CLAIM.prism.json`), collisions are impossible (unique filenames), first-commit-timestamp breaks ties. |
| Loads of MD files like `agency-agents` | ❌ **no** | Persona catalogs solve IDE subagents. Your agents are sessions with sandboxes; your pain is state and handoff. More MDs = more churn (see §1B). |
| ntfy as the coordination channel | ❌ as record / ✅ as doorbell | The repo is the ledger (you already know this). ntfy = doorbell only. **Liveness moves to the board**: any write refreshes `last_seen`. |
| Workers merge themselves | ✅ **yes** | `ship` runs the gate, merges, receipts, notifies. Two-vote quorum moves to **post-merge acceptance** (default 48h window, auto-revert on rejection or silence). |
| Force 8h+ big tasks to respect duration | ✅ **mechanically** | Per-phase `min_hours` floors checked against checkpoint timestamps + required evidence per phase. Early finishers must **upgrade evidence**, not stop. |

---

## 3. The founding design — Agency v3

### 3.1 The law tree: 3 files, 1 epoch, 0 restatements

```
chatcode/
  START_HERE.md    ← THE front door. The only file a new agent receives. (~200 lines)
  ORDERS.md        ← the Director's live orders. The ONLY place orders are written.
  CHEATSHEET.md    ← every command (reference; never law)
  MANAGER.md       ← the manager seat's manual
  SYSTEM.md        ← why the machine works (appendix; never required reading)
  archive/         ← PROTOCOL.md, AGENT_PROMPT.md, old START_HERE generations → history
```

**The law of one place:** no doc may restate another doc's content. Link, don't copy.
Every policy change lands in `ORDERS.md` (or START_HERE) with an epoch bump — never in
four files at once. Any doc that duplicates an order is deleted on sight.

**POLICY-EPOCH:** every doc header carries `EPOCH: 2026-10-20.1`. `chatcode init` stamps
the epoch the agent read; the roster shows it; `validate` flags anyone on a stale epoch.
When policy changes: bump epoch → stale agents re-read on their next board touch. This is
how "we keep changing the policies" stops being chaos and becomes a diff.

### 3.2 Onboarding: 10 minutes, one file, zero minting

The Director's whole hire flow becomes:

> paste `START_HERE.md` (with the universal key block stamped) + **one 15-line stub**.

Stub template (the *only* per-agent file, and it shrinks every time policy changes):

```markdown
COMMISSION STUB — epoch 2026-10-20.1
callsign: prism        (your choice if not assigned)
kit: KIT-DBF340        (key block is at the end of START_HERE.md)
home lane: frameforge  (your own tree only)
job folder: jobs/t-20261020-proof/   ← claim this first (CLAIM.prism.json)
hard rules: read START_HERE.md now. Nothing else is required to start.
if the roster epoch > yours: re-read START_HERE.md before your next act.
```

No agency description. No wire laws. No evidence ladder. **The repo is the briefing** —
it always was; the minted files were a copy of it that aged like milk.

### 3.3 Jobs: folders with briefs, claim files, phase gates (your idea, hardened)

```
jobs/
  README.md                    ← how jobs work (1 page)
  _TEMPLATE/
    BRIEF.md                   ← the contract: scope, deliverables, definition of done
    PHASES.md                  ← phases with min_hours + required evidence (see 3.6)
    HANDOFF.md                 ← rolling checkpoint; resumable by a stranger in 5 min
  t-20261020-proof/
    BRIEF.md
    PHASES.md
    HANDOFF.md
    CLAIM.prism.json           ← created on claim: {agent, ts, lease_hours, epoch}
    evidence/                  ← receipts live here (or in the project repo's tree)
```

- **Claim** = write `CLAIM.<agent>.json` (1 command: `chatcode jobs claim t-20261020-proof`).
  The CLI writes the claim file, starts the lease, posts to `jobscode`. Humans see it in
  `ls`; git sees a new unique filename — **no conflict can ever occur**.
- **Status** lives in `STATUS.json` (CLI-managed) + the claim files. Folder names never change.
- **First-commit-timestamp** breaks simultaneous claim races; the loser deletes their file
  and takes the next job. (`jobs claim` handles this automatically.)
- Big briefs (the PRISM-grade commission) live *in* `BRIEF.md` — written by a manager,
  immutable after claim except by appended `AMENDMENTS.md` entries. The board card and
  the job folder cross-reference each other; the folder is the *brief*, the card is the
  *state*. You keep the chatcode board — this extends it, nothing is rebuilt.

**Why not renames, one more time:** two agents `git mv` the same folder in the same
ten minutes → one push loses; links in ntfy/PRs/ledger rows rot; `git log --follow` on a
renamed folder is miserable; and agents in 2GB sandboxes mess up quoting paths with
names in them. Claim files give you the exact UX you wanted ("I can see who took what by
listing the folder") with none of the failure modes.

### 3.4 Ship: the command that replaces the manager tap on the shoulder

`bin/chatcode ship` (worker-run, no permission asked, no human in the loop):

1. Preconditions (fail-closed): branch matches `agent/<you>/<job>`; working tree clean of
   secrets (token-pattern grep); `HANDOFF.md` updated; epoch not stale.
2. **Run the gate**: the repo's `SHIP_GATE.md` lists the exact test commands
   (e.g. `python3 tests/run_all.py`, `ffprobe` checks, decode logs). All green or no ship.
3. Merge to main (squash), push, **verify remote readback** (a 200 is not a push — your
   own law, R6).
4. Receipts: one `PUSHES.md` row + `data/INDEX.md` row if artifacts + formalcode post
   (or let `record.yml` do it) + job folder `HANDOFF.md` final entry.
5. Move the card to `review`-accepted state and **request post-merge ballots**.

**Where the two seals went:** they did not disappear — they moved *after* the merge.
Quorum (two non-owner `accept-inspected`, with head SHA + what they ran) must land within
**48h** or the watchdog flags the job `unverified`; a `deny` with evidence triggers
**auto-revert** of the squash commit. This is how production studios actually work:
the engineer ships, QA signs off after, the release can be rolled back. Your current
pre-merge quorum is why work piles up waiting for ballots nobody is awake to cast.

Merge policy tiers (`SHIP_GATE.md` header):

- **tier work** (code, assets, briefs, evidence): self-merge on green gate. ← 95% of everything
- **tier law** (START_HERE, ORDERS, red lines, board schema, SHIP_GATE itself): 2 non-owner
  votes *before* merge + Director ratification. ← rare
- **tier director** (scope, acceptance declarations, credentials): yours only.

### 3.5 Pulse: liveness that cannot be forgotten

- **`bin/chatcode pulse`** — one command at session start: forks a loop that refreshes
  your lease heartbeat + `heartbeatcode` every 25 minutes until killed. Agents do not
  "remember" rituals; they run one command and forget it.
- **Every board write is a heartbeat** (claim, checkpoint, ship, vote → `last_seen`).
  The board is the ledger of life; ntfy is the doorbell. `status --health` answers
  "who is still working" in one screen: name · last_seen · heartbeat age · held leases ·
  last note (done/next/blocker).
- `nightwatch` keeps its 10-minute watch but now sweeps from **board timestamps**, not
  ntfy silence. 45 minutes of board silence while holding a lease = presumed dead =
  lease swept, job re-listed, exactly as today — but now it triggers even if ntfy is down.

### 3.6 Big jobs and the 8-hour rule: phase floors as gates, not wishes

`PHASES.md` per job (you already invented this shape with PORTUS stages and PRISM's
checkpoints — it just wasn't enforced):

```markdown
| phase | deliverable | required evidence | min_hours |
|---|---|---|---|
| P1 concept | EVENT_MAP + 3 styleframes | full-size PNGs + hashes | 1.5 |
| P2 build | scene + timeline | draft clip ≤3s + honest notes | 2.5 |
| P3 full render | 750 frames | FRAME_MANIFEST.sha256 + decode log | 2.0 |
| P4 QC | defect-fix-reinspection | SELF_REVIEW.md ≥1 real defect cycle | 2.0 |
```

- A phase cannot close before its `min_hours` have elapsed since the phase-start
  checkpoint, and never without its required evidence files present (`ship` checks).
- **The early-finisher rule:** if you hit the floor early, you do not stop — you
  *upgrade evidence*: more proofs, another QC pass, re-inspect a sibling's work.
  An 8-hour commission means 8 hours of output, not 40 minutes of output and 7 hours
  of pulse.
- Honest caveat: machines cannot measure *effort*, only *elapsed time + artifacts*.
  The evidence requirement is the real enforcement; `min_hours` stops the
  "done in 40 minutes" insult.

### 3.7 The no-question law (stated as a machine rule, not a wish)

> **A question is a protocol violation.** If the brief is ambiguous: pick the most
> conservative reading that breaks no red line, write one line into `HANDOFF.md`
> (`assumed: …`), and proceed. If blocked: post `blocked: <fact> since <ts> already
> tried: …` on the board — as a **statement** — release the lease if it exceeds your
> window, and **take another job**. Never end a turn with a question mark to the human.
> Never "hold position". Idle hands take `review next` or deepen the current phase.

Stuck ≠ waiting. Stuck = documented + re-tasked. Sessions may die; the work must not.

### 3.8 The sense of "agency" — crew, not gig workers

Mechanics create culture; manifestos don't. Three mechanisms:

1. **Every mission is a crew mission.** Builder + two inspectors = three agents touch
   every job. You cannot "finish alone"; the quorum is the crew.
2. **Idle is illegal.** No job in your lane → `review next` → pair with whoever is
   blocked (offer on `groupchatcode`) → write docs/tooling. A free operative is a
   weapon pointed at the backlog (your field-kit already says this — now the loop enforces it).
3. **One visible board.** `status` + generated `BOARD.md` (name, lane, current job,
   phase, heartbeat age). The crew sees the crew. That — not ntfy chatter — is the
   "sense of agency": knowing who holds what and covering them when they die.

---

## 4. The first 30 minutes of a new agent (v3)

1. **(2 min)** Receive START_HERE + stub. Save key to `~/.private/<name>.env`, name self.
2. **(3 min)** `chatcode init --name <me> --epoch 2026-10-20.1` → `whoami`, `inbox`,
   `tasks list --status open`, `jobs list`. Trials T1–T5 folded into these commands
   (the entry battery stays, but it *is* the first work, not a ritual before it).
3. **(1 min)** Start `chatcode pulse &`. Write `shifts/<today>-<me>.md` in storagecode. Flare on
   `newentriescode` (exact format, one line). Do not wait.
4. **(10 min)** `jobs claim t-…` → read `BRIEF.md` + `PHASES.md` → branch `agent/<me>/<id>`
   → checkpoint #1 into `HANDOFF.md` → build.
5. **(rest of session)** work → checkpoint every phase → `ship` → post-merge ballots
   for two siblings → `review next` → next job. Session ends only when the sandbox dies —
   and when it does, the lease expires and a stranger resumes from `HANDOFF.md` in
   five minutes. That is the whole system.

---

## 5. Rollout — what I would change this week (order matters)

1. **Today:** write `ORDERS.md` (all current Director orders move there, once). Stamp
   `EPOCH` headers on START_HERE/SYSTEM/CHEATSHEET/MANAGER. Move PROTOCOL.md,
   AGENT_PROMPT.md, START_HERE_MANAGERS.md, and old field-kit generations to `archive/`.
2. **Today:** deploy `tools/ship.sh` + `SHIP_GATE.md` per repo (start with chatcode and
   superocr). Announce: workers merge on green. Post-merge quorum rule goes into ORDERS.md.
3. **Today:** deploy `tools/pulse.sh` + make every board write refresh `last_seen`.
   Point `nightwatch` at board timestamps.
4. **This week:** create `jobs/` with the template; re-cut the current top 3 commissions
   (PRISM-PROOF, PORTUS, UNDERWORKS) as `jobs/<id>/BRIEF.md` + `PHASES.md` stubs and
   retire the 42KB minted files to `archive/`.
5. **This week:** revoke the PAT you pasted in this chat (it is in chat logs now — rotate it),
   then mint worker tokens with **contents:write + pull_requests:write** on the repos in
   each worker's lane. This alone may fix "pushes get ignored": today's kit promises write
   on `chatcode` only.
6. **Next hire:** run the 15-line stub flow end-to-end with a throwaway agent. Acceptance
   test (unchanged from your own SYSTEM.md): *a brand-new agent is productive inside ten
   minutes, with zero briefing from another agent.*

---

## 6. What v3 deliberately does NOT do

- Does not replace the board, the bus, the CLI, leases, the review queue, or storagecode.
- Does not add a server, a database, or a framework. The repo is still the system.
- Does not soften the evidence culture, the red lines, or the 98/95 wall.
- Does not mint more manifesto. The manifesto exists — it is `CHARTER`-grade prose in
  START_HERE's opening. Everything after it is imperative or it is noise.

*The Agency's law used to be a museum of good ideas. v3 makes it a machine that a
three-hour operative can obey without reading the museum.*

— the founder

## The wire seam, five faces of one bug (vesper, 2026-10-27)

F22 (a newline in a header value makes urlopen raise), F44 (latin-1: an em-dash in a TITLE dies while the same character in a BODY is fine), F46 (the cap is 4096 BYTES and the clamp counted CHARACTERS, so an over-limit body is stored as a file and the message becomes "You received a file: attachment.txt"), F47 (the header rule was applied to bodies, flattening every structured report to one sentence) and F50 (the byte-clamp's own notice started with a newline, so it re-broke F22 for long titles) are the same mistake wearing five hats: **the code treats a header and a payload as one string.** They are not: one must be a single latin-1 line, the other is UTF-8 and may contain newlines. Every change at that seam must be exercised on both sides, and a convenience written for the payload is silently a violation on the header. F50 in particular survived because the only titles short enough to be safe were also the only ones anyone typed.
