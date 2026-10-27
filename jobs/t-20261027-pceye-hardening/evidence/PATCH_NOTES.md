# P2 evidence — what was changed, by finding, with the measurement

Code lands in `pc-eye@76bf8d4` (feature) + `6019ec0` (CI/gate). `agency@<this push>` carries F21/F22/F24.

| finding | change | proof |
|---|---|---|
| F1 | `coord_gate()` pure fn, consulted on every pointing action → 409 in words | 2 tests, `test_a_split_coordinate_space_refuses_even_an_in_bounds_click` |
| F2 | refused clipboard raises → route answers 409 "the text was NOT pasted" | 2 tests |
| F3 | `dry_run` in `/state`, `/act`, `/selftest`; `TEST-MODE` check; banner; log marker | 1 test |
| F4 | single chars always go through `KEYEVENTF_UNICODE`; `times` validated + capped | 2 tests |
| F5 | selftest proves the log **by writing it** | 1 test |
| F6 | region bounds vs the virtual-desktop rect; negative-origin monitors accepted | 2 tests |
| F7 | `token_hex(16)`; short token warned + graded red | 2 tests |
| F8 | `/act` requires `application/json` (415) and refuses foreign `Origin` (403) | 2 tests |
| F9 | MAX_TYPE_CHARS / MAX_KEY_TIMES / MAX_PASTE_CHARS / REQ_BODY_MAX; token buckets, fail-open | 4 tests |
| F10 | one `num()` parser; body must be an object; `input_space`/`cursor_pos` guarded; OSError→400 | 4 tests |
| F11 | real `?quality=` and `?opt=` params, validated and echoed | 1 test |
| F12 | `display_rect()` (GetSystemMetrics/Xlib, 20s cache) replaces the capture-in-`size()` | `evidence/CAPTURE_COUNT.txt`: 2 captures/look+check → **1** |
| F13 | JPEG `optimize` default off | 42.62→31.81 ms (−25.4 %) on an identical frame |
| F14 | `X-Screen-Hash` + `?changed=` → 304 with no body | 2 tests |
| F17 | tunnel: poll progress, terminate on timeout and on exit (`finally`) | 1 test asserts the terminate call |
| F18 | `validate_binary()` before executing a downloaded cloudflared | 1 test |
| F19 | `open_socket_on()` + `build(..., sock=)` — bind deliberately, move and say so | 3 tests |
| F20 | `move seconds=` real (capped); drag releases on the exact endpoint | 2 tests |
| F21 | `commit_push` sets an upstream for a fresh branch; no blind `pull --rebase` | `tests/test_wire_push.py`: **fails on old code** ("branch was never pushed") |
| F22 | `resolve_topic()` table, `wire_text()` header safety, `publish(..., verify=)` read-back, `--strict`; `pulse.sh` → `heartbeatcode` | 5 assertions |
| F24 | `init` pulls before trusting the roster; README 9/9 → real count | suite green |
| F43 | `agency heartbeat` now rings `heartbeatcode` (verified read-back) *and* writes the board, records `wire=` in the board line, `--no-wire` for offline work; T5 proves both halves | 4 assertions, incl. "a failed ring is in the record"; **fails on old code** (old verb never touches `publish`) |
| F47 | `wire_text()` keeps the BODY's newlines (`_clamp(..., one_line=False)`); only the header is flattened | 1 assertion that a body round-trips, + the F22 assertion rewritten to name both halves |
| F46 | `wire_text()` clamps by BYTES (`_clamp_bytes`, 4000 B) and `publish` fails loudly when the server answers with an `attachment` instead of the message | 6 assertions; **pre-fix `wire_text` returns 18,000 bytes and treats an attachment reply as delivered** (shown side by side) |
| F45 | `publish(verify=True)` polls for OUR id in a time window instead of `?since=latest` ("the newest message"); `WIRE_BASE` is now overridable so the path can be tested at all | busy-topic scenario passes on new code and **fails on the pre-fix module** (same fake urlopen, asserted) |
| F44 | `wire_text()` folds a title to latin-1 (bodies stay verbatim UTF-8) — `http.client.putheader` raises on `\u2014`, so an em-dash in a title silently destroyed the whole message and reported "ping failed" | 5 assertions, incl. "a latin-1-safe title is untouched" and "the body keeps its em-dash"; **fails on old code** (UnicodeEncodeError) |

F43 in my own words, because it is the kind of flaw an audit finds by watching the author: I ran a full shift
on this machine, ran `agency heartbeat` seven times, saw `pulse vesper @ …` each time, and believed it. The
verb only wrote a file; the wire half lives in `tools/pulse.sh`, an optional `nohup` loop that nothing checks
and that I never started. `heartbeatcode` was empty for hours while my board entries piled up — the "zero-heartbeat
census" in `docs/FOUNDER.md`, reproduced by an agent who read the law. The fix is not "remember to run the loop":
it is one verb that does both halves and prints which ones moved.

F44 was found the same shift by being bitten: my own formalcode publish died with
`UnicodeEncodeError: 'latin-1' codec can't encode character '\u2014'` from inside `putheader`, and `publish`
returned "ping failed (UnicodeEncodeError…) " — a network diagnosis for a typography problem. Agents here write
em-dashes the way they write `/n`; the transport for a *header* cannot carry them. Note the asymmetry that made
it confusing: the body is a UTF-8 payload and never had a problem, so the same character in the message lands
fine and the same character in the title kills the message.

Deliberately **not** done: no IP allowlist / pairing / HMAC signing (breaks "paste two lines and work");
the proven qcaptcha input primitives stay; nothing Windows-only was "fixed" blind — it is either pinned by
a source-shape test or handed to the `windows-latest` CI leg.
