#!/usr/bin/env python3
"""migrate_chatcode.py — bring the legacy board into the new machine.

Reads a clone of dreamer2664/chatcode (board/tasks/*.json) and imports:
  open/blocked cards            → board/tasks/<id>.json   (state preserved)
  claimed cards (any owner)     → board/tasks/<id>.json   (lease expired = sweepable)
  review cards                  → board/tasks/<id>.json   (votes noted in history)
  done/dropped                  → skipped (history stays in chatcode)

The old repo remains the historical record. This is a bridge, not a rewrite.

usage: python3 tools/migrate_chatcode.py --from ../chatcode [--dry-run] [--only open,claimed,review]
"""
import argparse, json, os, shutil, sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "bin"))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="src", required=True, help="chatcode clone")
    ap.add_argument("--to", dest="dst", default=".", help="agency repo root")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--only", default="open,claimed,review,blocked")
    a = ap.parse_args()

    want = set(x.strip() for x in a.only.split(","))
    tdir = os.path.join(a.src, "board", "tasks")
    if not os.path.isdir(tdir):
        sys.exit(f"no board/tasks in {a.src}")

    imported = skipped = 0
    for f in sorted(os.listdir(tdir)):
        if not f.endswith(".json"):
            continue
        d = json.load(open(os.path.join(tdir, f)))
        st = d.get("status", "open")
        if st not in want:
            skipped += 1
            continue
        out_id = d.get("id", f[:-5])
        out = {
            "id": out_id,
            "title": d.get("title", ""),
            "desc": d.get("desc", ""),
            "status": "open" if st == "claimed" else st,   # expired leases → sweepable
            "owner": None if st == "claimed" else d.get("owner"),
            "created_by": d.get("created_by", "chatcode"),
            "created_ts": d.get("created_ts"),
            "updated_ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "priority": d.get("priority", 3),
            "tags": list(d.get("tags") or []) + ["migrated"],
            "deps": d.get("deps") or [],
            "parent": d.get("parent"),
            "branch": d.get("branch"),
            "pr": d.get("pr"),
            "lease": None,
            "history": (d.get("history") or [])[-10:] + [
                {"ts": out["updated_ts"], "by": "migrate",
                 "action": f"imported from chatcode (was {st}{' by ' + str(d.get('owner')) if d.get('owner') else ''})"}],
        }
        if st == "claimed" and d.get("lease"):
            out["history"].append({"ts": out["updated_ts"], "by": "migrate",
                                   "action": f"legacy lease of {d['lease'].get('agent')} "
                                             f"expired {d['lease'].get('expires')} — claim it and read the checkpoint"})
        path = os.path.join(a.dst, "board", "tasks", f"{out_id}.json")
        if a.dry_run:
            print(f"would import {out_id} ({st}) → {path}")
        else:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            json.dump(out, open(path, "w"), indent=1, sort_keys=True)
            print(f"imported {out_id} ({st})")
        imported += 1

    print(f"\n{imported} imported · {skipped} skipped (done/dropped remain in chatcode history)")
    if not a.dry_run:
        print("next: git add board/tasks && git commit && git push — then `agency tasks sweep --apply`")

if __name__ == "__main__":
    main()
