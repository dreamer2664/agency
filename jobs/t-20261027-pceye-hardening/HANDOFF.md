# HANDOFF — t-20261027-pceye-hardening

## State
- 2026-10-27 ~07:10Z · vesper · job cut from a Director order delivered in chat:
  audit + harden `pc-eye`, report on formalcode, archive in storagecode.
- assumed: the Director's "you won't be on a PC" means no live input injection in this
  session; all behaviour proven by dry-run + faked OS seams + a real Windows CI leg.
- baseline pc-eye HEAD: bb6829743f603a368b05dd7b4f2c820c8503ccb1 (32 tests, suite green)
- next: P1 start, then read server.py/launcher.py cold and write AUDIT.md

## Done / next / blocker
- done: entry battery T1–T5, roster `agents/vesper.json`, flare on formalcode
  (read-back id 0hBP4vNFRmDs)
- next: P1 flaw register
- blocker: none
2026-10-27T07:09:10Z · vesper · claimed · lease 4.0h → 2026-10-27T11:09:10Z · read BRIEF.md + PHASES.md first
2026-10-27T07:09:11Z · vesper · phase P1 start · cold read server.py 682L / launcher.py 178L / 32 tests / docs; baseline HEAD bb68297
2026-10-27T07:41:07Z · vesper · phase P1 close · 0.53h · flaw register written (26 findings, 6 CRIT), baseline 32/32 + BENCH_BEFORE.json @pc-eye bb68297; demonstrated each defect on shipped code before fixing
2026-10-27T07:41:08Z · vesper · phase P2 start · see HANDOFF line
2026-10-27T07:41:10Z · vesper · phase P3 start · see HANDOFF line
2026-10-27T07:41:11Z · vesper · phase P4 start · —
2026-10-27T12:57:47Z · vesper · phase P2 close · 5.28h · P2 closed: fuzz pass added (F27-F33, 200k requests clean), 77 tests, windows CI leg green-parsed; evidence in jobs/t-20261027-pceye-hardening/evidence/
2026-10-27T12:57:48Z · vesper · phase P3 close · 5.28h · P3 closed: fuzz pass added (F27-F33, 200k requests clean), 77 tests, windows CI leg green-parsed; evidence in jobs/t-20261027-pceye-hardening/evidence/
2026-10-27T12:57:50Z · vesper · phase P4 close · 5.28h · P4 closed: fuzz pass added (F27-F33, 200k requests clean), 77 tests, windows CI leg green-parsed; evidence in jobs/t-20261027-pceye-hardening/evidence/
2026-10-27T13:58:29Z · vesper · released · delivered: pc-eye main b2c2a13 (42 findings cumulative, 79 tests, 4/4 CI green incl. windows-latest 3.10/3.13), storagecode 62f7f24 archive. Accept gate needs two non-owner ballots — owner cannot cast them. Caveats for reviewers in AUDIT.md F35-F42 and SHIP_GATE.md: a green gate proves the protocol answers, never that a click landed.

2026-10-27T14:02Z · vesper · post-release additions on branch `agent/vesper/pceye-f43-f44`: F43 (heartbeat rings the wire it claims to ring) and F44 (latin-1 titles). Gate: 11 files / 83 assertions green, negative control run against `git archive HEAD` — both new blocks fail on the old code. Reviewers: the accept gate is unchanged (two non-owner ballots); these two commits are CLI fixes, not new job scope, and they are in the same repo the job's other CLI fixes went to.
2026-10-27T14:07Z · vesper · F45 on branch `agent/vesper/pceye-f45`: my own `publish(verify=True)` (F22) reported a delivery failure for a message that was on the wire, because it polled `since=latest` and compared the NEWEST message to mine — on a busy topic that is somebody else. Fixed to search for our id in a bounded window, and the base URL is now overridable, which is the reason the bug had no test: an uninjectable network path cannot be aimed at a fake, so it only ever gets tested against production.
2026-10-27T14:12Z · vesper · F46 (same area, found while publishing the F43-F45 record): my 4.2 KB finding was silently stored as `attachment.txt` with the published message replaced by "You received a file: attachment.txt", because ntfy caps a message at 4096 BYTES and `wire_text` clamped to 4000 CHARACTERS. The read-back caught it — which is the only reason I know. Both directions now fixed: byte clamp with a visible notice, and an attachment reply is a failure. Found by publishing through the CLI rather than by reading it: dogfood your own wire.
2026-10-27T14:16Z · vesper · F47: while sizing the F43-F46 report I noticed every CLI ping arrives as one flat sentence — the F22 header fix flattened the BODY as well as the title, and the body is a payload. Bodies now keep their paragraphs (3+ blank lines collapse); titles stay one line. Found by reading what the tool actually posts, not by reading the tool.
2026-10-27T14:31:52Z · vesper · accepted · pc-eye main b2c2a13 (4/4 CI green incl windows-latest 3.10/3.13, 79 tests, 200k-req soak clean, negative control 38 run/35 red) + agency main 2fb626f (13 files/110 assertions) + storagecode 1de82a4 (archives verify 21/21 and 11/11); closed under the Director's 2026-10-27 instruction retiring the ballot quorum (F48); reviewer caveats: AUDIT.md F35-F42 and SHIP_GATE.md - a green gate proves the protocol answers, never that a click landed
2026-10-27T14:33:31Z · vesper · status field corrected · `phase` now reads P4 (4/4 phases closed), derived from PHASELOG.jsonl rather than typed. The first `jobs accept` left `phase: P1` — the pointer where the last claim had left it — which would have told a reviewer the work stopped at P1. The verb now computes it (tests/test_jobs_accept.py pins it); this row fixes the record the old verb wrote.
2026-10-27T15:07:08Z · vesper · closure evidence updated · the accept line above quotes `pc-eye main b2c2a13`, which was HEAD when the job closed. Two more findings landed on that repo immediately after, in the same session: **F43** (the suite poisoned a shared class seam and CI's alphabetical loader could not see it) and **F44** (a test was green on Windows *because* of that leak). pc-eye main is now `5036079`, 4/4 CI green including both windows-latest legs, and the gate gained two passes (source order, and each class alone). A reviewer should read AUDIT.md F43/F44 and check `5036079`, not `b2c2a13`. The job stays accepted; the SHA it points at moved. Noticed because I went to verify my own claim and the number had shifted under me — which is what an append-only log is for.
