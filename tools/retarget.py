"""Re-point edges that target a retired id (one too broad for a single node).

    python3 tools/retarget.py packet pilot/run/p1     # build <dir>/retarget/in.json
    python3 tools/retarget.py apply  pilot/run/p1     # apply <dir>/retarget/out.json to nodes/

<dir>/retired.json (from prepare_phase.py) lists each retired id and the new
nodes that together cover it. The packet lists every written edge that points
at a retired id, with the source node's statement, procedure and test problem,
the edge's why, and the candidate nodes with their statements. One agent picks,
for each edge, the candidate(s) the source node actually uses
(out.json: {"<edge id>": {"targets": [...], "reason": "..."}}), or
{"keep_boundary": "<id>", "reason": ...} when the needed skill is not among the
candidates (a later phase writes it).

`apply` rewrites the matching edges in nodes/ (several targets become several
edges in the same route) and must run after every merge_run, since merge_run
rewrites node files from the run data. It logs to <dir>/retarget/applied.md.
"""
import copy
import glob
import json
import os
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Finer nodes outside the retiring strand that an old edge may really mean (an edge
# to addition.whole-number from a fraction node usually needs single-digit sums).
ALSO = {
    "addition.whole-number": ["addition.within-10.fluency", "addition.within-20.fluency"],
    "subtraction.whole-number": ["subtraction.within-10.fluency", "subtraction.within-20.fluency"],
    "multiplication.multi-digit": ["multiplication.facts.within-100"],
    "division.multi-digit": ["division.facts.within-100"],
    "place-value.base-ten": [],
}


class NoAlias(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True


def nodes_on_disk():
    out = {}
    for p in glob.glob(os.path.join(ROOT, "nodes", "**", "*.yaml"), recursive=True):
        out[yaml.safe_load(open(p, encoding="utf-8"))["id"]] = p
    return out


def batch_nodes(d):
    out = {}
    for p in glob.glob(os.path.join(d, "batches", "*.yaml")):
        for n in yaml.safe_load(open(p, encoding="utf-8")):
            out[n["id"]] = n
    return out


def packet(d):
    retired = json.load(open(os.path.join(d, "retired.json")))
    new = batch_nodes(d)
    for nid, p in nodes_on_disk().items():
        new.setdefault(nid, yaml.safe_load(open(p, encoding="utf-8")))
    edges, k = {}, 0
    for nid, p in sorted(nodes_on_disk().items()):
        n = yaml.safe_load(open(p, encoding="utf-8"))
        for c in n.get("requires") or []:
            for e in c["all_of"]:
                if e["node"] in retired:
                    k += 1
                    edges[f"r{k}"] = {"node": nid, "route": c["clause"], "old_target": e["node"],
                                      "statement": n["statement"], "procedure": n.get("procedure"),
                                      "assess": n["assess"], "points_to": e.get("points_to"),
                                      "scope": e.get("scope", "concept"), "why": e.get("why")}
    cands = {rid: [{"id": t, "level": new[t]["level"], "type": new[t]["type"], "name": new[t]["name"],
                    "statement": new[t]["statement"]} for t in r["replaced_by"] + ALSO.get(rid, []) if t in new]
             for rid, r in retired.items()}
    os.makedirs(os.path.join(d, "retarget"), exist_ok=True)
    json.dump({"candidates": cands, "edges": edges}, open(os.path.join(d, "retarget", "in.json"), "w"), indent=1)
    print(f"{len(edges)} edges to re-point, {sum(len(v) for v in cands.values())} candidate nodes")


def apply(d):
    inp = json.load(open(os.path.join(d, "retarget", "in.json")))
    out = json.load(open(os.path.join(d, "retarget", "out.json")))
    paths = nodes_on_disk()
    log, changed = [], set()
    for eid, e in inp["edges"].items():
        v = out.get(eid)
        if not v:
            log.append(f"- {eid} {e['node']} -> {e['old_target']}: no verdict, left as is")
            continue
        if v.get("keep_boundary"):
            new_targets = [v["keep_boundary"]]
        else:
            new_targets = v.get("targets") or []
        if not new_targets:
            log.append(f"- {eid} {e['node']} -> {e['old_target']}: empty verdict, left as is")
            continue
        p = paths[e["node"]]
        n = yaml.safe_load(open(p, encoding="utf-8"))
        for c in n.get("requires") or []:
            if c["clause"] != e["route"]:
                continue
            outl = []
            for x in c["all_of"]:
                if x["node"] != e["old_target"]:
                    outl.append(x)
                    continue
                for t in new_targets:
                    if any(y["node"] == t for y in outl) or any(y["node"] == t for y in c["all_of"]):
                        continue
                    y = copy.deepcopy(x)
                    y["node"] = t
                    y.setdefault("evidence", []).append(
                        {"kind": "content", "source": "retarget-sonnet",
                         "note": f"re-pointed from retired {e['old_target']}: {v.get('reason', '')}"[:500]})
                    outl.append(y)
            c["all_of"] = outl
        with open(p, "w", encoding="utf-8") as f:
            yaml.dump(n, f, Dumper=NoAlias, sort_keys=False, width=100, allow_unicode=False)
        changed.add(e["node"])
        log.append(f"- {eid} {e['node']} ({e['route']}): {e['old_target']} -> {new_targets}")
    open(os.path.join(d, "retarget", "applied.md"), "w").write(
        "# Retarget applied\n\n" + "\n".join(log) + "\n")
    print(f"{len(changed)} node files changed; log in {os.path.join(d, 'retarget', 'applied.md')}")


if __name__ == "__main__":
    {"packet": packet, "apply": apply}[sys.argv[1]](sys.argv[2])
