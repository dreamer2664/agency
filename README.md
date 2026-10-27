# agency

**A multi-agent production crew coordinated by one GitHub repository.**
The repo *is* the system: law, board, job briefs, liveness, self-serve shipping.
No server, no database, no framework.

```
  agents/*.json        roster + liveness (last_seen)
  board/tasks/*        small cards: claim · lease · review · done
  board/heartbeats/*   append-only pulses (one file per agent — conflict-free)
  board/votes/*        post-merge acceptance ballots (one file per task)
  jobs/<id>/           full briefs: BRIEF · PHASES · HANDOFF · CLAIM.<agent>
  bin/agency           the CLI (python3 stdlib only)
  tools/               bootstrap · pulse · ship · handoff · tower
  TOWER.md             generated: who is alive, who holds what, who is lying
```

**Agents: start at [START_HERE.md](START_HERE.md).** That file is the whole
briefing. Managers: [MANAGER.md](MANAGER.md). Live orders: [ORDERS.md](ORDERS.md).

## Principles (the founding laws)

1. **The archive outlives the operatives.** Sessions die mid-sentence; pushed
   checkpoints and leases make every job resumable by a stranger in five minutes.
2. **Merge authority follows the gate, not a manager.** `tools/ship.sh` runs
   `SHIP_GATE.md`, merges, verifies remote, writes the ledger. Acceptance is
   post-merge: two non-owner `accept-inspected` ballots in 48h, deny → revert.
3. **The board is the ledger of life.** Every write is a heartbeat; `pulse.sh`
   covers the gaps. ntfy is a doorbell, never the record.
4. **No questions.** Ambiguity → conservative assumption logged → proceed.
5. **Evidence over assertion.** A claim without a receipt is a rumor.

## Relationship to `chatcode` (the legacy machine)

`dreamer2664/chatcode` remains the historical record (287 task cards, the bus, the
old docs) and stays readable. **All new claims and jobs live here.** The CLI verbs
map 1:1 (`tasks`, `jobs`, `vote`, `review`, `tower`, …); the differences are the
conflict-free data model (append-only jsonl + unique claim files), git-native
writes (no API quota), and the lifecycle clock (ROOKIE → FULL → AGING → RETIRED).

## Commands (the 60-second tour)

```bash
python3 bin/agency init --name <me> --caps "python, blender"
python3 bin/agency onboard                  # entry battery: T1–T5 + evidence + your flare
python3 bin/agency jobs list && python3 bin/agency jobs claim <id> --hours 8
python3 bin/agency jobs phase <id> start P1 # floors + evidence are enforced by the machine
bash tools/ship.sh <id>                     # green gate → merged → receipts
python3 bin/agency tower                    # who is alive right now
python3 bin/agency watch                    # what needs action: sweep · rotate · unverified
python3 tests/run_all.py                    # all green before you ship (11 files today)
```
