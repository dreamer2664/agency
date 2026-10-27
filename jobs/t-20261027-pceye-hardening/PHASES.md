# PHASES — t-20261027-pceye-hardening

| phase | deliverable | required evidence | min_hours |
|---|---|---|---|
| P1 | read the whole system, measure the baseline, write the flaw register | `evidence/AUDIT.md` + `evidence/BENCH_BEFORE.json` | 0.25 |
| P2 | implement fixes for CRIT/HIGH + the measurable speed work | `evidence/PATCH_NOTES.md` + `evidence/BENCH_AFTER.json` | 0.25 |
| P3 | tests pin every fixed flaw; CI leg added; docs resynced | `evidence/P3-TESTLOG.txt` | 0.25 |
| P4 | QC loop: re-run suite + bench, ≥1 real defect-fix-reinspection cycle | `evidence/P4-SELF_REVIEW.md` | 0.25 |

**Total floor: 1.0 h.** Clock starts at each `phase start` line in HANDOFF.md.
Early finisher rule applies: upgrade evidence (negative tests, an extra inspection
pass) rather than stopping — do NOT paper over a floor with `--override` unless the
reason is written into HANDOFF.md first.
