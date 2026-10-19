"""Lint two proposer passes, measure agreement, and build blinded critic batches.

    python3 tools/union_passes.py pilot/run

Reads <dir>/batches/*.yaml, <dir>/index.txt, <dir>/passes/<P|Q>-<batch>.json.
Writes <dir>/union.json (every edge, with which pass proposed it), critic
batches <dir>/critic/in-<batch>.json (no votes, no pass labels, edges in
alphabetical order), and <dir>/critic/_mapping.json (kept from the critic).
"""
import collections
import glob
import json
import os
import re
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from check import VAGUE, MIN_WHY_WORDS  # noqa: E402
from combine_passes import clean  # noqa: E402

PASSES = ("P", "Q")


def boundary_ids(packet):
    return set(re.findall(r"^\| `([a-z0-9.-]+)` \|", open(packet, encoding="utf-8").read(), re.M))


def lint(node, route, e, ids, boundary):
    errs = []
    t = e.get("node", "")
    if not (t in ids or t in boundary or t.startswith("new:")):
        errs.append(f"unknown target {t}")
    if t == node["id"]:
        errs.append("self edge")
    if e.get("relation") not in ("definitional", "procedural", "representational", "justificatory"):
        errs.append(f"bad relation {e.get('relation')}")
    pt, scope = e.get("points_to", ""), e.get("scope", "concept")
    if pt.startswith("procedure."):
        steps = route.get("procedure") or node.get("procedure") or []
        try:
            n = int(pt.split(".")[1])
        except ValueError:
            n = 0
        if not 1 <= n <= len(steps):
            errs.append(f"points_to {pt} with {len(steps)} steps")
    elif pt not in ("statement", "assess"):
        errs.append(f"bad points_to {pt}")
    if scope == "task" and pt != "assess":
        errs.append("task edge not on assess")
    if scope == "concept" and pt == "assess":
        errs.append("concept edge on assess")
    why = (e.get("why") or "").lower()
    if len(why.split()) < MIN_WHY_WORDS:
        errs.append("why too short")
    errs += [f"vague '{v}'" for v in VAGUE if v in why]
    return errs


def main(d):
    boundary = boundary_ids(os.path.join(d, "proposer.md"))
    batches = {}
    for p in sorted(glob.glob(os.path.join(d, "batches", "*.yaml"))):
        b = os.path.basename(p)[:-5]
        batches[b] = yaml.safe_load(open(p, encoding="utf-8"))
    nodes = {n["id"]: n for ns in batches.values() for n in ns}
    ids = set(nodes)
    targets = set(ids)  # every node the passes may point at, not only this run's batch
    idx = os.path.join(d, "index.txt")
    if os.path.exists(idx):
        targets |= {l.split("|")[0].strip() for l in open(idx, encoding="utf-8") if l.strip()}
    passes = {}
    for lab in PASSES:
        passes[lab] = {}
        for b in batches:
            p = os.path.join(d, "passes", f"{lab}-{b}.json")
            passes[lab].update(clean(json.load(open(p, encoding="utf-8")))["nodes"])

    report = ["# Proposer passes: lint and agreement", ""]
    lint_log = collections.defaultdict(list)
    union = collections.OrderedDict()   # (node, target) -> {passes, edges}
    routes_ct = collections.Counter()
    for lab in PASSES:
        missing = sorted(ids - set(passes[lab]))
        if missing:
            report.append(f"- Pass {lab} skipped {len(missing)} nodes: {missing}")
        for nid in nodes:
            entry = passes[lab].get(nid, {"routes": []})
            if len(entry.get("routes", [])) > 1:
                routes_ct[lab] += 1
            for r in entry.get("routes", []):
                for e in r.get("edges", []):
                    errs = lint(nodes[nid], r, e, targets, boundary)
                    if errs:
                        lint_log[lab].append(f"{nid} -> {e.get('node')}: {'; '.join(errs)}")
                    key = (nid, e.get("node", ""))
                    u = union.setdefault(key, {"passes": [], "edges": []})
                    if lab not in u["passes"]:
                        u["passes"].append(lab)
                        u["edges"].append({"pass": lab, "clause": r.get("clause"),
                                           "route_procedure": r.get("procedure"), **e})

    per = {lab: {k for k, u in union.items() if lab in u["passes"]} for lab in PASSES}
    both = per["P"] & per["Q"]
    report += [
        f"- Edges proposed: P {len(per['P'])}, Q {len(per['Q'])}",
        f"- Distinct edges (union): {len(union)}",
        f"- Proposed by both: {len(both)} ({100 * len(both) / len(union):.0f}% of union; "
        f"Jaccard {len(both) / len(union):.2f})",
        f"- Nodes given two or more routes: P {routes_ct['P']}, Q {routes_ct['Q']}",
        f"- Targets outside the map (new:): {sum(1 for k in union if k[1].startswith('new:'))}",
        f"- Rule violations: P {len(lint_log['P'])}, Q {len(lint_log['Q'])}", ""]
    for lab in PASSES:
        for line in lint_log[lab][:40]:
            report.append(f"  - {lab}: {line}")
    by_batch = collections.Counter()
    for b, ns in batches.items():
        bid = {n["id"] for n in ns}
        bu = [k for k in union if k[0] in bid]
        report.append(f"- {b}: {len(bu)} edges, {100 * sum(1 for k in bu if k in both) / max(1, len(bu)):.0f}% proposed by both")
    new_targets = collections.Counter(k[1] for k in union if k[1].startswith("new:"))
    if new_targets:
        report += ["", "New targets proposed (outside the map):", ""]
        report += [f"- {t} ({c})" for t, c in new_targets.most_common()]

    json.dump([{"node": k[0], "target": k[1], **v} for k, v in union.items()],
              open(os.path.join(d, "union.json"), "w"), indent=1)

    # blinded critic batches
    os.makedirs(os.path.join(d, "critic"), exist_ok=True)
    mapping, k_id = {}, 0
    for b, ns in batches.items():
        out = {"boundary_nodes": sorted(boundary), "nodes": []}
        for n in ns:
            entry = {x: n[x] for x in ("id", "concept", "facet", "level", "type", "name", "statement", "assess") if x in n}
            if n.get("procedure"):
                entry["procedure"] = n["procedure"]
            entry["proposed_edges"] = []
            for (nid, t) in sorted((key for key in union if key[0] == n["id"]), key=lambda x: x[1]):
                e = union[(nid, t)]["edges"][0]
                k_id += 1
                eid = f"e{k_id}"
                mapping[eid] = {"node": nid, "target": t}
                ed = {"edge_id": eid, "prerequisite": t.replace("new:", ""), "relation": e.get("relation"),
                      "points_to": e.get("points_to"), "scope": e.get("scope", "concept"), "rationale": e.get("why")}
                if (e.get("points_to") or "").startswith("procedure.") and e.get("route_procedure"):
                    ed["route_procedure"] = e["route_procedure"]
                entry["proposed_edges"].append(ed)
            out["nodes"].append(entry)
        json.dump(out, open(os.path.join(d, "critic", f"in-{b}.json"), "w"), indent=1)
    json.dump(mapping, open(os.path.join(d, "critic", "_mapping.json"), "w"))
    report.append(f"\nCritic input: {k_id} edges in {len(batches)} batches.")
    open(os.path.join(d, "passes_report.md"), "w").write("\n".join(report) + "\n")
    print("\n".join(report))


if __name__ == "__main__":
    main(sys.argv[1])
