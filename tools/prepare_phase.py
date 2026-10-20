"""After a phase's writers: check their nodes and build the proposer and critic packets.

    python3 tools/prepare_phase.py pilot/run/p1 [--apply-concepts]

Reads <dir>/skeletons/<strand>.yaml and .extra.yaml. Checks ids (unique, not
clashing with written nodes except reserved ids, no retired id reused),
concepts and facets (in concepts.yaml or proposed under new_concepts), and
reports merge suspects (same name). Writes <dir>/batches/<strand>.yaml,
<dir>/index.txt (every written node plus this phase's), <dir>/retired.json,
<dir>/proposer.md and <dir>/critic.md (from the latest prompts, with this run's
paths and boundary list). With --apply-concepts, adds proposed concepts and
facets to concepts.yaml. No model calls.
"""
import collections
import glob
import json
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from build_phase import RESERVED, written_nodes  # noqa: E402

# Extra skeleton files proposed and criticized inside another strand's batch
# (fix-up nodes written inline are too few to pay an agent's start-up cost).
ATTACH = {"p2": {"F": "G1"}}
FIELDS = ("id", "concept", "facet", "level", "type", "name", "statement", "procedure", "assess", "sources",
          "strand")
LATER_MEANINGS = {}  # boundary meanings from earlier proposer packets


def old_meanings():
    out = {}
    for p in glob.glob(os.path.join(ROOT, "pilot", "run", "**", "proposer.md"), recursive=True):
        for m in re.finditer(r"^\| `([a-z0-9.-]+)` \| (.+?) \|$", open(p, encoding="utf-8").read(), re.M):
            out.setdefault(m.group(1), m.group(2))
    return out


def main(d, apply_concepts):
    rel = os.path.relpath(d, ROOT)
    written = written_nodes()
    concepts = yaml.safe_load(open(os.path.join(ROOT, "concepts.yaml"), encoding="utf-8"))
    strands, extras = {}, {}
    for p in sorted(glob.glob(os.path.join(d, "skeletons", "*.yaml"))):
        if p.endswith(".extra.yaml"):
            continue
        s = os.path.basename(p)[:-5]
        strands[s] = yaml.safe_load(open(p, encoding="utf-8")) or []
        x = p[:-5] + ".extra.yaml"
        extras[s] = (yaml.safe_load(open(x, encoding="utf-8")) or {}) if os.path.exists(x) else {}
    problems, notes = [], []
    retired = {}
    for s, x in extras.items():
        for r in x.get("retires") or []:
            retired[r["id"]] = {"strand": s, "replaced_by": r.get("replaced_by") or [], "note": r.get("note", "")}
    new_conc = collections.defaultdict(set)
    for s, x in extras.items():
        for c in x.get("new_concepts") or []:
            new_conc[c["concept"]].add(c.get("facet") or "core")
    seen = {}
    for s, ns in strands.items():
        for n in ns:
            i = n["id"]
            if i in seen:
                problems.append(f"{i}: written by both {seen[i]} and {s}")
            seen[i] = s
            if i in written:
                problems.append(f"{i} ({s}): already written")
            if i in retired:
                problems.append(f"{i} ({s}): uses an id retired by {retired[i]['strand']}")
            if i in RESERVED and RESERVED[i][1] != s:
                problems.append(f"{i} ({s}): reserved for {RESERVED[i][1]}")
            c, f = n.get("concept"), n.get("facet")
            known = c in concepts and f in (concepts[c].get("facets") or [])
            if not known and f not in new_conc.get(c, set()):
                problems.append(f"{i} ({s}): concept/facet {c}/{f} neither in concepts.yaml nor proposed")
    for rid, r in retired.items():
        bad = [t for t in r["replaced_by"] if t not in seen and t not in written]
        if bad:
            problems.append(f"retired {rid}: replaced_by names unknown ids {bad}")
    names = collections.defaultdict(list)
    for n in list(written.values()) + [n for ns in strands.values() for n in ns]:
        names[n["name"].strip().lower()].append(n["id"])
    for k, v in names.items():
        if len(v) > 1:
            notes.append(f"same name, check for a duplicate: {v}")

    os.makedirs(os.path.join(d, "batches"), exist_ok=True)
    attach = ATTACH.get(os.path.basename(d.rstrip("/")), {})
    for s, ns in strands.items():
        if s in attach:
            continue
        ns = ns + [n for a, host in attach.items() if host == s for n in strands.get(a, [])]
        out = [{k: n[k] for k in FIELDS if k in n} for n in ns]
        with open(os.path.join(d, "batches", f"{s}.yaml"), "w", encoding="utf-8") as f:
            yaml.safe_dump(out, f, sort_keys=False, width=100, allow_unicode=False)
    idx = []
    for i in sorted(written):
        n = written[i]
        idx.append(f"{i} | L{n['level']} {n['type']} | {n['name']}")
    for s, ns in strands.items():
        for n in ns:
            idx.append(f"{n['id']} | L{n['level']} {n['type']} | {n['name']}")
    open(os.path.join(d, "index.txt"), "w").write("\n".join(idx) + "\n")
    json.dump(retired, open(os.path.join(d, "retired.json"), "w"), indent=1)

    # boundary: referenced-but-unwritten ids that this phase did not write or retire
    refs = collections.Counter()
    for n in written.values():
        for c in n.get("requires") or []:
            for e in c["all_of"]:
                refs[e["node"]] += 1
    have = set(written) | set(seen)
    meaning = old_meanings()
    boundary = sorted((set(refs) | {r for r, (_, o) in RESERVED.items() if o == "later"}) - have - set(retired))
    rows = [f"| `{b}` | {RESERVED.get(b, (meaning.get(b, 'see the nodes that reference it'),))[0]} |"
            for b in boundary]

    tmpl = open(os.path.join(ROOT, "pilot", "run", "fixes", "proposer.md"), encoding="utf-8").read()
    head = tmpl[:tmpl.index("## Allowed targets")]
    tail = tmpl[tmpl.index("## Output"):]
    head = head.replace("pilot/run/fixes/batches/fixes.yaml", f"{rel}/batches/<batch>.yaml")
    head = head.replace("pilot/run/fixes/index.txt", f"{rel}/index.txt")
    allowed = f"""## Allowed targets

Your batch is one strand of the map. Every node it could need is in
`index.txt`, which lists the whole map (pre-K through grade 8 as far as it is
written, including the other strands of this run), or in the boundary list
below (referenced but not yet written; use these exact ids). Use
`new:<concept>.<short-name>` only if a genuinely needed earlier skill is
missing from both.

- A node may be a root (nothing earlier in the map is needed). Give
  `"routes": []` and a `root_reason` when that is your judgment; do not invent
  a prerequisite to avoid a root.
- Developmental or curricular order is not prerequisite order. Apply the
  counterfactual test to the node's statement and test problem: could a
  learner meet this node, at its stated level, by a credible route without the
  prerequisite?
- Some ids were retired as too broad (for example `addition.whole-number`);
  they are not in the index. Point at the specific node instead.

## Boundary list (referenced, not yet written)

| id | meaning |
|---|---|
""" + "\n".join(rows) + "\n\n"
    open(os.path.join(d, "proposer.md"), "w").write(head + allowed + tail)
    crit = open(os.path.join(ROOT, "pilot", "run", "critic", "critic.md"), encoding="utf-8").read()
    crit = crit.replace("pilot/run/critic/in-<batch>.json", f"{rel}/critic/in-<batch>.json")
    crit = crit.replace("pilot/run/index.txt", f"{rel}/index.txt")
    open(os.path.join(d, "critic.md"), "w").write(crit)

    if apply_concepts:
        for c, fs in new_conc.items():
            entry = concepts.setdefault(c, {"name": c.replace("-", " ").capitalize(), "facets": []})
            for f in sorted(fs):
                if f not in entry["facets"]:
                    entry["facets"].append(f)
        with open(os.path.join(ROOT, "concepts.yaml"), "w", encoding="utf-8") as f:
            yaml.safe_dump(concepts, f, sort_keys=False)

    print(f"strands: {', '.join(f'{s} {len(ns)}' for s, ns in strands.items())}; "
          f"total {sum(len(ns) for ns in strands.values())} nodes")
    print(f"retired ids: {sorted(retired)}")
    print(f"boundary ids left: {len(boundary)}")
    print(f"problems ({len(problems)}):")
    for p in problems:
        print(" -", p)
    print(f"notes ({len(notes)}):")
    for n in notes:
        print(" -", n)


if __name__ == "__main__":
    main(sys.argv[1], "--apply-concepts" in sys.argv)
