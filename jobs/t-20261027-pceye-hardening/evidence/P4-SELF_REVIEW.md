# P4 — QC loop: one real defect → fix → re-inspection cycle, plus what I checked and rejected

## Cycle 1 (the one that changes my own claim)
* **Found while writing the evidence:** the first `AUDIT.md` compared 1.0.2's build default against 1.0.3's
  build default and reported `/shot` 33.11 → 31.61 ms as *the* speed win, and `/shot` bytes 7.0 → 18.5 KB
  as if that were a regression. Both were harness artefacts: my fake screen only honoured `optimize` on the
  new tree, so the two runs encoded differently and the byte figure came from a synthetic noisy frame.
* **Fix:** re-ran the A/B with the encode policy **pinned** on both trees, added a same-policy column,
  deleted the byte claim, and wrote down that `optimize` costs time and saves bytes on real content, with
  `?opt=1` one parameter away.
* **Re-inspected:** the new table (F15/C section) is generated from the four files in `evidence/`, and the
  `-0.7 %` on `/act click` is now reported as a **cost** of the safety work rather than hidden in noise.

## Cycle 2 — a test that proved nothing
* `test_state_does_not_grab_the_screen` passed on the OLD code. Cause: it faked `Screen.size()`, so the fake
  never had the bug to demonstrate. **Fixed** by patching the real `PIL.ImageGrab` and the real `Screen`, and
  by testing both worlds (geometry known → 0 captures; unknown → 1, the fallback). Now 26/28 new tests fail
  on 1.0.2 instead of 27/28 with one hollow.

## Deliberate refusals (recorded so nobody "fixes" them back)
* `scroll`/`key` are NOT gated by the coordinate check: a keystroke cannot land on the wrong pixel, and
  gating them would break `type`-while-DPI-broken recovery.
* I did not add an IP allowlist or pairing. It would break the only property that makes pc-eye usable from
  a chat; F7 is fixed by entropy (128 bits) + CSRF + rate limiting, which is honest about the residual risk:
  **a token in a URL is still a token in a URL**, and the docs now say so in the agent's own instruction file.
* I did not touch `captchaproject`/`captchaprogram` (R1) or the superocr wall (R2). No read, no clone.

## What remains unproven (name the rung)
* producer-reported: nothing was executed on a real Windows desktop in this session.
* verified by artifact: 67 tests + CI matrix (incl. windows-latest) + `negative_check.py` +
  `capture_count.py` + `check_docs.py`.
* not independently verified: every claim about actual click landing, black UAC windows, tunnel behaviour
  under a real router, and the 304 path through cloudflared (proxies sometimes strip 304 bodies — the
  response carries no body by design, so this is safe, but it is unverified here).
* pending review: two non-owner `accept-inspected` ballots within 48 h. My own vote counts for zero.
