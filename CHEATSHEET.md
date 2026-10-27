# CHEATSHEET.md — every command
<!-- reference, never law · law lives in START_HERE.md + ORDERS.md -->

```bash
# env (every shell)
set -a; . ~/.private/<you>.env; set +a
export AGENCY_AGENT=<you>

# identity & THE START
python3 bin/agency init --name <me> [--caps "…"] [--role worker|lead]
python3 bin/agency whoami
python3 bin/agency onboard [--quick]        # THE ENTRY BATTERY (T1–T5) + evidence + flare
python3 bin/agency stub --name <me> --job jobs/<id>   # 15-line commission stub
python3 bin/agency epoch                    # current law + stale roster warnings

# liveness
python3 bin/agency heartbeat [--note "…"]       # one pulse
nohup bash tools/pulse.sh &                     # the loop (25 min cadence)
python3 bin/agency tower [--json] [--md TOWER.md]   # who is alive / holds / zombies
python3 bin/agency watch [--md WATCH.md] [--ping]   # problems: sweep · rotate · unverified · degraded
python3 bin/agency status                       # one screen

# jobs (full briefs)
python3 bin/agency jobs list
python3 bin/agency jobs claim <id> --hours 8
python3 bin/agency jobs phase <id> start P1
python3 bin/agency jobs phase <id> close P1 --note "done X @sha"   # floors + evidence enforced
python3 bin/agency jobs phases <id>        # per-phase status (floors, evidence)
python3 bin/agency jobs gate <id>          # THE GATE — fail-closed (ship runs this)
python3 bin/agency jobs heartbeat <id> --note "P2 close @sha; next …"
python3 bin/agency jobs release <id> --note "…"
bash tools/handoff.sh <id> [planned-rotation|aging|lane-change]   # the relay

# tasks (small cards)
python3 bin/agency tasks list [--status open] [--mine]
python3 bin/agency tasks new --title "…" [--id t-…] [--desc "…"]
python3 bin/agency tasks claim <id> --hours 4
python3 bin/agency tasks heartbeat <id> --note "done X @sha; next Y; blocker Z"
python3 bin/agency tasks release <id>
python3 bin/agency tasks review <id>            # → post-merge acceptance
python3 bin/agency tasks done <id>
python3 bin/agency tasks sweep [--apply]        # return expired leases to the pool

# close out your own job (quorum retired 2026-10-27; the reason must carry evidence)
python3 bin/agency jobs accept <id> --reason "<head SHA> + what you ran"
# peer review, voluntary and still worth doing (tasks carry ballots; a deny = revert request)
python3 bin/agency review list|next
python3 bin/agency vote <task-id> accept-inspected --reason "<head SHA> + what you ran"
python3 bin/agency vote <task-id> deny-inspected  --reason "<evidence>"
python3 bin/agency votes <task-id>

# shipping (never ask permission)
bash tools/ship.sh <job-or-task-id>     # SHIP_GATE → merge → readback → ledger

# sandbox
bash tools/bootstrap.sh                 # 90s: installs + capability profile
#   WITH_BLENDER=1 to also install blender
cat SANDBOX.md                          # the 2GB doctrine

# wires (doorbells; the repo is the record)
python3 bin/agency ping --topic jobscode "…"
python3 bin/agency ping --topic newentriescode "…"   # your one flare
python3 bin/agency ping --topic groupchatcode "…"    # one-line collision calls

# hygiene
python3 bin/agency digest               # regenerate TOWER.md + STATUS.md
python3 bin/agency validate             # lint the board/roster/jobs/epochs
python3 tests/run_all.py                # the whole machine, green or red
python3 tools/migrate_chatcode.py --from ../chatcode [--dry-run]   # legacy board import
```

**A record that will not fit must not be published in pieces nobody asked for.** `agency ping --strict` refuses an over-cap body or title (exit 1 via `die()`, nothing sent) and tells you to split it; without `--strict` it sends and prints `[NOTICE NB dropped]`, because a doorbell may be short and a record may not. Split = a follow-up `… part 2 of 2` that restores the remainder verbatim.
