# SHIP_GATE.md — the only gate between your branch and main
<!-- EPOCH: 2026-10-20.1 · tier-law file: changes need 2 pre-merge votes + Director -->
<!-- ship.sh runs every line starting with "$ " in order. Any failure = no ship. -->

## tier: work — workers self-merge on green

$ python3 tests/run_all.py
# add repo-specific gates below, e.g.:
# $ python3 tests/test_shift_system.py
# $ ffprobe -v error -show_entries format=duration -of csv=p=0 dist.mp4
# $ python3 tools/check_evidence.py jobs/<id>/
