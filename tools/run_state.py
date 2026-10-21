"""Report and update the state of a run from pilot/run/manifest.yaml.

    python3 tools/run_state.py                       # status table, running total, next units
    python3 tools/run_state.py --mark UNIT running
    python3 tools/run_state.py --mark UNIT done --tokens 182000 --commit abc1234
    python3 tools/run_state.py --mark UNIT failed
    python3 tools/run_state.py --validate UNIT       # run one unit's validator

A unit can be marked done only when its validator passes and every unit in its
`after` list is done. The manifest is edited in place so its comments survive.
"""
import argparse
import glob
import json
import os
import re
import subprocess
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(ROOT, "pilot", "run", "manifest.yaml")

NODE_TYPES = {"concept", "procedure", "representation", "fact", "justification", "application"}
NODE_FIELDS = ["id", "concept", "facet", "level", "type", "name", "statement", "assess", "sources"]


def load_manifest():
    with open(MANIFEST, encoding="utf-8") as f:
        return yaml.safe_load(f)


def path(rel):
    return os.path.join(ROOT, rel)


def non_ascii(text):
    return sorted({c for c in text if ord(c) > 127})


# ---------------------------------------------------------------- validators

def v_exists(unit):
    p = path(unit["output"])
    if not os.path.exists(p) or os.path.getsize(p) == 0:
        return [f"missing or empty: {unit['output']}"]
    return []


def collect_ids(obj, out):
    if isinstance(obj, dict):
        if "id" in obj and isinstance(obj["id"], str):
            out.append(obj["id"])
        for v in obj.values():
            collect_ids(v, out)
    elif isinstance(obj, list):
        for v in obj:
            collect_ids(v, out)


def prek_source_ids():
    ids = []
    for p in glob.glob(path("sources/prek/*.yaml")):
        with open(p, encoding="utf-8") as f:
            collect_ids(yaml.safe_load(f), ids)
    return set(ids)


def v_source(unit):
    errs = v_exists(unit)
    if errs:
        return errs
    raw = open(path(unit["output"]), encoding="utf-8").read()
    bad = non_ascii(raw)
    if bad:
        errs.append(f"non-ASCII characters: {bad}")
    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError as e:
        return errs + [f"YAML does not parse: {e}"]
    if not data.get("source"):
        errs.append("no top-level `source`")
    if not data.get("retrieved"):
        errs.append("no top-level `retrieved` date")
    ids = []
    collect_ids(data, ids)
    if not ids:
        errs.append("no item ids")
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    if dupes:
        errs.append(f"duplicate ids: {dupes}")
    return errs


def v_writer(unit):
    errs = v_exists(unit)
    if errs:
        return errs
    raw = open(path(unit["output"]), encoding="utf-8").read()
    bad = non_ascii(raw)
    if bad:
        errs.append(f"non-ASCII characters: {bad}")
    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError as e:
        return errs + [f"YAML does not parse: {e}"]
    nodes = data.get("nodes", data) if isinstance(data, dict) else data
    if not isinstance(nodes, list) or not nodes:
        return errs + ["no node list"]
    known = prek_source_ids()
    seen = set()
    for i, n in enumerate(nodes):
        where = n.get("id", f"#{i}") if isinstance(n, dict) else f"#{i}"
        if not isinstance(n, dict):
            errs.append(f"{where}: not a mapping")
            continue
        for k in NODE_FIELDS:
            if k not in n:
                errs.append(f"{where}: missing `{k}`")
        if n.get("id") in seen:
            errs.append(f"{where}: duplicate id")
        seen.add(n.get("id"))
        if n.get("level") not in (1, 2, 3, 4):
            errs.append(f"{where}: level must be 1-4")
        if n.get("type") not in NODE_TYPES:
            errs.append(f"{where}: bad type {n.get('type')!r}")
        cited = (n.get("sources") or {}).get("prek", [])
        for s in cited:
            if s not in known:
                errs.append(f"{where}: cites unknown pre-K source id {s}")
    return errs


def v_proposer(unit):
    errs = v_exists(unit)
    if errs:
        return errs
    try:
        data = yaml.safe_load(open(path(unit["output"]), encoding="utf-8"))
    except yaml.YAMLError as e:
        return [f"YAML does not parse: {e}"]
    if not data:
        errs.append("empty pass")
    return errs


def v_critic(unit):
    errs = v_exists(unit)
    if errs:
        return errs
    try:
        json.load(open(path(unit["output"]), encoding="utf-8"))
    except json.JSONDecodeError as e:
        errs.append(f"JSON does not parse: {e}")
    return errs


def v_check(unit):
    errs = v_exists(unit)
    r = subprocess.run([sys.executable, path("tools/check.py")], capture_output=True, text=True)
    if r.returncode != 0:
        errs.append("tools/check.py reports errors")
    return errs


def v_writer_lc(unit):
    """Writer from learning components: node fields, lc ids from the input, full coverage."""
    errs = v_exists(unit)
    if errs:
        return errs
    raw = open(path(unit["output"]), encoding="utf-8").read()
    bad = non_ascii(raw)
    if bad:
        errs.append(f"non-ASCII characters: {bad}")
    try:
        nodes = yaml.safe_load(raw)
    except yaml.YAMLError as e:
        return errs + [f"YAML does not parse: {e}"]
    if not isinstance(nodes, list) or not nodes:
        return errs + ["no node list"]
    inp = json.load(open(path(unit["input"]), encoding="utf-8"))
    want = {c["lc"] for s in inp for c in s["learning_components"]}
    got, seen = set(), set()
    for i, n in enumerate(nodes):
        where = n.get("id", f"#{i}") if isinstance(n, dict) else f"#{i}"
        if not isinstance(n, dict):
            errs.append(f"{where}: not a mapping")
            continue
        for k in NODE_FIELDS:
            if k not in n:
                errs.append(f"{where}: missing `{k}`")
        if n.get("id") in seen:
            errs.append(f"{where}: duplicate id")
        seen.add(n.get("id"))
        if n.get("level") not in (1, 2, 3, 4):
            errs.append(f"{where}: level must be 1-4")
        if n.get("type") not in NODE_TYPES:
            errs.append(f"{where}: bad type {n.get('type')!r}")
        for lc in (n.get("sources") or {}).get("lc", []) or []:
            if str(lc) not in want and str(lc) not in unit.get("merged_lc", []):
                errs.append(f"{where}: cites lc {lc} not in its input")
            got.add(str(lc))
    extra = unit["output"].replace(".yaml", ".extra.yaml")
    if not os.path.exists(path(extra)):
        return errs + [f"missing {extra}"]
    try:
        x = yaml.safe_load(open(path(extra), encoding="utf-8")) or {}
    except yaml.YAMLError as e:
        return errs + [f"extra file does not parse: {e}"]
    for k in ("covered_by", "dropped", "merged_into"):
        for r in x.get(k) or []:
            got.add(str(r.get("lc")))
    missing = sorted(want - got)
    if missing:
        errs.append(f"{len(missing)} learning components unaccounted for: {missing[:8]}")
    return errs


VALIDATORS = {
    "exists": v_exists, "source": v_source, "writer": v_writer, "writer-lc": v_writer_lc,
    "proposer": v_proposer, "critic": v_critic, "check": v_check,
}


def validate(unit):
    fn = VALIDATORS.get(unit.get("validate", "exists"))
    if fn is None:
        return [f"unknown validator {unit.get('validate')!r}"]
    return fn(unit)


# ---------------------------------------------------------------- state

def effective_status(unit):
    s = unit.get("status", "pending")
    if s == "done":
        return "done" if not validate(unit) else "done-but-invalid"
    if s in ("pending", "running") and os.path.exists(path(unit["output"])):
        return "partial"
    return s


def report(m):
    units = m["units"]
    by_id = {u["id"]: u for u in units}
    status = {u["id"]: effective_status(u) for u in units}
    total = sum(int(u.get("tokens") or 0) for u in units)
    print(f"# Run: {m.get('run')}\n")
    print(f"{'unit':40} {'stage':11} {'status':17} tokens")
    for u in units:
        print(f"{u['id']:40} {u.get('stage',''):11} {status[u['id']]:17} {int(u.get('tokens') or 0):,}")
    counts = {}
    for s in status.values():
        counts[s] = counts.get(s, 0) + 1
    print(f"\nRunning total: {total:,} subagent tokens")
    print("Counts: " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())))
    ready = [u["id"] for u in units
             if status[u["id"]] in ("pending", "partial", "failed")
             and all(status.get(a) == "done" for a in u.get("after", []))]
    print("\nCan run next:" + ("" if ready else " nothing (waiting on review or dependencies)"))
    for r in ready:
        note = " (partial output exists: resume, do not restart)" if status[r] == "partial" else ""
        if by_id[r].get("stage") == "review":
            note = " (awaiting Daniel's review)"
        print(f"  - {r}{note}")
    broken = [i for i, s in status.items() if s == "done-but-invalid"]
    if broken:
        print("\nMarked done but failing validation:")
        for b in broken:
            for e in validate(by_id[b]):
                print(f"  - {b}: {e}")


def edit_unit(unit_id, status=None, tokens=None, commit=None):
    text = open(MANIFEST, encoding="utf-8").read()
    m = re.search(r"id: " + re.escape(unit_id) + r"(?=[,\s])", text)
    if not m:
        sys.exit(f"unit not found: {unit_id}")
    start = m.start()
    nxt = text.find("\n  - ", start)
    end = nxt if nxt != -1 else len(text)
    seg = text[start:end]
    flow = seg.rstrip().endswith("}")
    if status:
        seg = re.sub(r"status: \S+?(?=[,\s}])", f"status: {status}", seg, count=1)
    if tokens is not None:
        if re.search(r"tokens: \d+", seg):
            seg = re.sub(r"tokens: \d+", f"tokens: {tokens}", seg, count=1)
        elif flow:  # the unit had no tokens field yet: add one rather than drop the value
            seg = re.sub(r"(status: \S+?)(?=[,}])", r"\1, tokens: " + str(tokens), seg, count=1)
        else:
            sys.exit(f"{unit_id}: no tokens field to update in a block-style entry")
    if commit:
        if "commit:" in seg:
            seg = re.sub(r"commit: \S+?(?=[,\s}])", f"commit: {commit}", seg, count=1)
        elif flow:
            i = seg.rstrip().rfind("}")
            seg = seg[:i] + f", commit: {commit}" + seg[i:]
        else:
            seg = re.sub(r"(\n(\s+)tokens: \d+)", r"\1\n\2commit: " + commit, seg, count=1)
    open(MANIFEST, "w", encoding="utf-8").write(text[:start] + seg + text[end:])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mark", nargs=2, metavar=("UNIT", "STATUS"))
    ap.add_argument("--tokens", type=int)
    ap.add_argument("--commit")
    ap.add_argument("--validate", metavar="UNIT")
    a = ap.parse_args()
    m = load_manifest()
    by_id = {u["id"]: u for u in m["units"]}

    if a.validate:
        errs = validate(by_id[a.validate])
        print("valid" if not errs else "\n".join(errs))
        sys.exit(1 if errs else 0)

    if a.mark:
        uid, st = a.mark
        if uid not in by_id:
            sys.exit(f"unit not found: {uid}")
        if st not in ("pending", "running", "done", "failed"):
            sys.exit(f"bad status: {st}")
        if st == "done":
            waiting = [x for x in by_id[uid].get("after", []) if by_id[x].get("status") != "done"]
            if waiting:
                sys.exit(f"cannot mark done; waiting on {waiting}")
            errs = validate(by_id[uid])
            if errs:
                sys.exit("cannot mark done; validator fails:\n  " + "\n  ".join(errs))
            if a.tokens is None:
                sys.exit("marking done needs --tokens (0 for script or inline work)")
        edit_unit(uid, st, a.tokens, a.commit)
        print(f"{uid}: {st}")
        return

    report(m)


if __name__ == "__main__":
    main()
