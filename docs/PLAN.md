# PLAN.md — research · test · plan (Agency v3.2)
**From:** the founder's seat · **To:** Carlo · **Date:** 2026-10-20
**Rule of this document:** every claim below is either a measurement from today's
lab session or a design that was executed against real data. Nothing is vibes.

---

# PART 1 — RESEARCH: the lab notebook

Everything was tested in a sandbox identical in class to what your operatives get
(2 cores, ~2GB RAM, no swap). Results:

| # | test | result | consequence |
|---|---|---|---|
| 1 | sandbox probe | 2 cores · 1.9GB RAM · **no swap** · 20GB disk · /tmp tmpfs 1GB | OOM kills are instant and silent; disk is plentiful, RAM is the whole game |
| 2 | toolchain probe | python 3.13, node 20, gcc, ImageMagick preinstalled; **ffmpeg/blender/gh/time missing** | agents must bootstrap; it's cheap (see #3) |
| 3 | install test | passwordless sudo works; **ffmpeg in 13s, blender 4.3 in 14s** via apt | bootstrap is a 90-second ritual, not a project |
| 4 | chatcode test suite | **39/39 pass** in 80s | the core machine is healthy; don't rebuild it |
| 5 | Blender render probe | 1 frame 1920×1080, 32 spp, Cycles CPU: **12.5 s, ~176 MB peak** | a 750-frame film ≈ 2.6h of pure render — fits an 8h shift if chunked |
| 6 | Blender stress probe | 200 subsurf-lvl-2 objects: **OOM-killed (exit 137)** | scene complexity is the memory cliff, not rendering — budget polys, not frames |
| 7 | Blender Debian trap | Cycles **crashes on default denoise** (no OpenImageDenoise in build) | agents lose hours to this unless it's written in the trap list (it now is) |
| 8 | `tower.py` on your live repo | **0 alive · 27 dead · 15 agents holding zombie leases** (cormac 12, odysseus 9, scipio 5) | your "who is working" question has a one-file answer and it is currently ugly |
| 9 | `ship.sh` end-to-end | gate → squash → push → remote readback ✅ | self-merge works mechanically today |
| 10 | `handoff.sh` end-to-end | RELAY.md written with computed agent age (52.8h), custody, decision log, traps | switching agents out is one command |
| 11 | `pulse.sh` loop | heartbeat + ping on schedule ✅ | liveness can be a one-command background loop |
| 12 | `bootstrap.sh` | profile emitted in seconds ✅ | the box self-describes; agents paste capability as evidence |

### Findings that changed the design

1. **Install anything, quickly** — the sandbox is not a sealed cell; it's a bare
   Debian box with sudo. The 8-hour Blender job is feasible *if* the agent knows the
   two traps (OIDN, OOM cliff) before it starts. That knowledge is now in
   `bootstrap.sh` output and `SANDBOX.md`.
2. **RAM is the only scarce resource.** 2 cores × 12.5s/frame is survivable;
   200 fancy objects is not. The doctrine is *budget memory like a spacecraft*.
3. **The agency is currently a graveyard.** 15 zombie leases is not a liveness
   problem, it's a *sweeping* problem — the data exists, nobody renders a verdict.
   `tower.py` does, and exits non-zero when zombies exist so CI can scream.
4. **Agents die mid-render.** So render jobs must be chunked by design
   (`render --from N --to M` per lease), and the chunk manifest is the unit of
   resumability — not "the project".

---

# PART 2 — THE SANDBOX DOCTRINE (2GB, well spent)

Full text in `SANDBOX.md`. The principles, ranked:

1. **Chunk everything.** Any job over ~1h of compute is cut into numbered chunks
   (frames 0–99, 100–199, …; buildings 1–8, …). Each chunk is a checkpoint with a
   manifest. A dead agent loses at most one chunk. This single rule is what makes
   "8-hour Blender project" and "sessions die at random" compatible.
2. **Budget memory, not time.** ≤1.2GB per process (`MEM_CEILING_MB`), subsurf ≤1 on
   bulk geometry, simplify/decimate working copies, render at draft resolution for
   QC and only full-res for shipping frames. No swap exists: 2GB is a hard wall.
3. **/tmp is scratch, git is memory.** Intermediates, caches, and frame dumps go to
   /tmp (dies with the session — fine). Anything not pushed is already lost.
4. **Bootstrap in 90 seconds, every session.** `tools/bootstrap.sh` — installs
   ffmpeg/time/blender as needed, prints the capability profile, lists known traps.
   The profile goes into checkpoint #1 as evidence of what the box can do.
5. **Parallelism = 2, not 8.** `xargs -P 2`, `nice -n 5`. Two cores shared with the
   agent's own reasoning; a saturated box makes the agent itself slow and dumb —
   which is *also* your 3–4 day degradation problem, accelerated.
6. **Determinism or nothing.** Seeded RNG, locked tool versions (`blender 4.3.2`,
   `ffmpeg 7.1.5` from Debian 13 — the bootstrap profile records exact versions so
   a successor re-renders bit-compatible frames).

---

# PART 3 — SWITCHING AGENTS OUT (the relay system)

Your real constraint: **an agent is a session, sessions degrade at 3–4 days and die
randomly.** So rotation must be (a) scheduled, (b) one-command, (c) lossless.

### 3.1 The lifecycle clock

| phase | age | rights |
|---|---|---|
| **ROOKIE** | 0–6h | small jobs + reviews only. First sealed mission before any big commission |
| **FULL** | 6–48h | any job in lane, including 8h commissions |
| **AGING** | 48–60h | **no new claims.** Finish current phase, then `handoff.sh`. Reviews + docs only |
| **RETIRED** | 60h+ | watchdog flags; leases auto-swept; the name stays on the roster as history |

The clock is `joined_ts` in `agents/<name>.json` — already exists. `tower.py` adds
the age column; `nightwatch` enforces the transitions. **Rotation is proactive:**
you replace operatives at 55h of age, not at the first sign of stupidity. A
scheduled swap costs 10 minutes; a failed one costs the job.

### 3.2 The relay (`tools/handoff.sh` — tested)

One command writes `jobs/<id>/RELAY.md`: custody (who, age, why), branch@SHA,
last checkpoint, **decision log** (assumptions the successor inherits), **traps**
(the free-tuition list — e.g. the OIDN bug), ordered next steps, and the agent's
caps so the manager can pick a like-for-like successor. It heartbeats the lease,
releases it, pings `jobscode`, and pushes. The successor:

```bash
chatcode jobs claim <id>   # CLAIM.<me>.json
cat jobs/<id>/RELAY.md     # five-minute resume, guaranteed
git checkout agent/<predecessor>/<id> -b agent/<me>/<id>   # continue, keep authorship history
```

### 3.3 Three kinds of switch, one mechanism

1. **Planned rotation** (aging clock) → `handoff.sh <id> planned-rotation`
2. **Crash/disappearance** (no handoff happened) → the lease expires, anyone
   `tasks sweep --apply`, the successor resumes from `HANDOFF.md` + git log. The
   RELAY just improves the odds; the design assumes it may never exist.
3. **Lane change / specialization swap** (a Blender job needs a Blender successor)
   → same relay; the caps section tells the manager who to wake.

### 3.4 Degradation detection (objective, not vibes)

`nightwatch` (already runs every 10 min) gains three cheap signals per agent:
- checkpoint cadence drifting (heartbeats >35 min apart while holding work),
- `HANDOFF.md` entries shrinking (words per checkpoint trending down),
- gate failures per ship rising.
Two signals trip → the tower prints `AGING ⚠` and the manager cuts a replacement
order. Self-reported "I feel fine" is never evidence (rung 6 discipline).

---

# PART 4 — CARLO'S EYES (reading heartbeats without playing forensics)

Right now liveness is spread over ntfy, `agents/*.json`, task leases and 402-line
STATUS.md. You need **three layers, each with one job**:

### Layer 1 — `TOWER.md` (glance, 5 seconds) — **built and tested today**
`tools/tower.py` renders one table: agent · role · 🟢ALIVE/🟡STALE/🔴DEAD ·
last seen · age · what they hold (⏰ = expired lease still held). Zombies are
listed at the top with the sweep command. Regenerated by `digest.yml` on every
push to `board/` or `agents/` — so you open ONE file on your phone:
`github.com/dreamer2664/chatcode/blob/main/TOWER.md`. (CI hook: tower.py exits 1
when zombie leases exist.)

### Layer 2 — the hourly tower ping (alert, ntfy on your phone)
One ntfy topic `towercode`, one message per hour from `nightwatch`:
`TOWER 14:00 · 2 alive · 1 stale · 24 dead · 🚨 zombies: cormac(12), odysseus(9) ·
action: sweep`. You subscribe to **one** topic in the ntfy app and the Agency pings
you only when it needs you. Alerts are immediate (zombie detected, last agent died,
lease sweep pending). `heartbeatcode` stays as the raw pulse for agents; you never
read it again.

### Layer 3 — the dashboard (curiosity)
`dashboard/index.html` stays as the pretty view. TOWER.md is the *truth* view.
No rebuild required — the layers share one data source (board timestamps).

**The rule behind all three:** the board is the ledger of life; every write is a
heartbeat (`pulse.sh` covers the gaps at 25-min cadence). ntfy is a doorbell that
summarizes the ledger — never a substitute for it.

---

# PART 5 — A GOOD START IS 90% OF THE WORK

The first hour predicts the whole career. v3.2 hardens it:

1. **90-second bootstrap → capability profile** pasted in checkpoint #1 (evidence
   the box can do the work — catches "ffmpeg missing" on minute 2, not hour 3).
2. **The entry battery IS the first job** (T1–T5 already double as a shift note +
   a push). Add: one `review next` ballot before any build work — a rookie who
   cannot inspect cannot be trusted to produce.
3. **ROOKIE lane:** first 6h = jobs sized ≤4h. Big commissions require one sealed
   mission on the record. (PRISM-style 42KB commissions to brand-new agents is how
   you got half-finished films.)
4. **Self-check at every checkpoint** (one line in HANDOFF.md):
   `laws: epoch ok · no secrets · no questions asked · floors respected · evidence filed`.
   Rookies that lie about this fail visibly and early.
5. **The stub stays 15 lines.** Onboarding reading is `START_HERE.md` and nothing
   else. Everything more is either a job brief or discoverable by need.

---

# PART 6 — REVISED ROLLOUT (order matters)

| when | action | acceptance test |
|---|---|---|
| today | drop `tools/` + `jobs/` + `SANDBOX.md` into chatcode; wire `tower.py` into `digest.yml`; add `towercode` ping to `nightwatch` | TOWER.md exists and matches board truth |
| today | **sweep the 15 zombie leases** (`tasks sweep --apply`) — first act of the new law | tower shows 0 zombies |
| today | `bootstrap.sh` + trap list in START_HERE; epoch → 2026-10-20.2 | a fresh sandbox can render one frame in <2 min from cold |
| this week | first planned rotation: pick the oldest working agent (brunel/vitruvius zone), run `handoff.sh` live | successor resumes a mid-flight job from RELAY.md alone |
| this week | ship.sh on chatcode + one project repo; token write-scope audit | worker merges without waking you |
| next | ROOKIE probation policy in ORDERS.md; degradation signals in nightwatch | TOWER shows aging agents before they fail |

*The machine is sound. This makes it legible, rotatable, and survivable in 2GB.*

— the founder
