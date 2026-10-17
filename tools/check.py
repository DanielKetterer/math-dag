"""Check the map against RULES.md.

    python3 tools/check.py            # print the report, exit 1 on any error
    python3 tools/check.py --report reports/check.md

Errors break a rule. Warnings and findings are things to look at, not failures.
"""
import argparse
import collections
import glob
import json
import os
import sys

import yaml
from jsonschema import Draft202012Validator

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

VAGUE = [
    "foundational", "builds on", "builds toward", "builds towards", "important for",
    "needed for", "is a prerequisite", "lays the groundwork", "helps with", "related to",
]
MIN_WHY_WORDS = 8


def load_yaml(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


class Report:
    def __init__(self):
        self.errors, self.warnings, self.findings, self.stats = [], [], [], {}

    def err(self, where, msg):
        self.errors.append(f"{where}: {msg}")

    def warn(self, where, msg):
        self.warnings.append(f"{where}: {msg}")

    def find(self, msg):
        self.findings.append(msg)

    def render(self):
        out = ["# Check report", ""]
        for k, v in self.stats.items():
            out.append(f"- {k}: {v}")
        for title, items in (("Errors", self.errors), ("Warnings", self.warnings), ("Findings", self.findings)):
            out += ["", f"## {title} ({len(items)})", ""]
            out += [f"- {i}" for i in items] or ["- none"]
        return "\n".join(out) + "\n"


def lint_edge(node, clause, edge, rep):
    where = f"{node['id']} [{clause['clause']}] -> {edge['node']}"
    if edge["node"] == node["id"]:
        rep.err(where, "a node cannot require itself")
    pt = edge["points_to"]
    if pt.startswith("procedure."):
        n = int(pt.split(".")[1])
        steps = clause.get("procedure") or node.get("procedure") or []
        if not 1 <= n <= len(steps):
            rep.err(where, f"points_to {pt} but the route has {len(steps)} procedure steps")
    scope = edge.get("scope", "concept")
    if scope == "task" and pt != "assess":
        rep.err(where, "a task-only prerequisite must point_to assess")
    if scope == "concept" and pt == "assess":
        rep.err(where, "points_to assess implies scope: task; mark it or point elsewhere")
    why = edge["why"].strip()
    if len(why.split()) < MIN_WHY_WORDS:
        rep.err(where, f"why has fewer than {MIN_WHY_WORDS} words")
    low = why.lower()
    for phrase in VAGUE:
        if phrase in low:
            rep.err(where, f"why leans on a vague phrase: '{phrase}'")


def learnable(nodes):
    """Least fixed point over OR-of-AND clauses. Unwritten nodes count as known."""
    known = {i for i, n in nodes.items() if not n["requires"]}
    changed = True
    while changed:
        changed = False
        for i, n in nodes.items():
            if i in known:
                continue
            for c in n["requires"]:
                if all(e["node"] in known or e["node"] not in nodes for e in c["all_of"]):
                    known.add(i)
                    changed = True
                    break
    return known


def sccs(graph):
    """Tarjan's algorithm; returns components with more than one node or a self loop."""
    index, low, stack, on, out = {}, {}, [], set(), []
    counter = [0]
    sys.setrecursionlimit(10000)

    def visit(v):
        index[v] = low[v] = counter[0]
        counter[0] += 1
        stack.append(v)
        on.add(v)
        for w in graph.get(v, ()):
            if w not in index:
                visit(w)
                low[v] = min(low[v], low[w])
            elif w in on:
                low[v] = min(low[v], index[w])
        if low[v] == index[v]:
            comp = []
            while True:
                w = stack.pop()
                on.discard(w)
                comp.append(w)
                if w == v:
                    break
            if len(comp) > 1:
                out.append(sorted(comp))

    for v in list(graph):
        if v not in index:
            visit(v)
    return out


def _all_refs(nodes):
    return [e["node"] for n in nodes.values() for c in n["requires"] for e in c["all_of"]]


def check_pathways(nodes, rep):
    """Unwritten prerequisites count as met, matching the learnability check."""
    for path in sorted(glob.glob(os.path.join(ROOT, "pathways", "*.yaml"))):
        pw = load_yaml(path) or {}
        name = pw.get("name", os.path.basename(path))
        seen = set(pw.get("assumes") or [])
        steps = sorted(pw.get("steps") or [], key=lambda s: s["position"])
        ok = bad = 0
        by_pos = collections.defaultdict(list)
        for s in steps:
            by_pos[s["position"]].append(s)
        for pos in sorted(by_pos):
            here = [nid for s in by_pos[pos] for nid in s.get("nodes", [])]
            avail = seen | set(here) | (set(_all_refs(nodes)) - set(nodes))
            for nid in here:
                n = nodes.get(nid)
                if n is None:
                    rep.warn(name, f"step {pos} lists unwritten node {nid}")
                    continue
                if not n["requires"]:
                    ok += 1
                    continue
                if any(all(e["node"] in avail for e in c["all_of"]) for c in n["requires"]):
                    ok += 1
                else:
                    bad += 1
                    missing = [sorted({e["node"] for e in c["all_of"]} - avail) for c in n["requires"]]
                    rep.find(f"{name}, step {pos}: {nid} comes before every clause is met; missing per clause {missing}")
            seen |= set(here)
        rep.stats[f"pathway '{name}'"] = f"{ok} placements consistent, {bad} findings"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report")
    args = ap.parse_args()
    rep = Report()

    concepts = load_yaml(os.path.join(ROOT, "concepts.yaml")) or {}
    with open(os.path.join(ROOT, "schema", "node.schema.json"), encoding="utf-8") as f:
        validator = Draft202012Validator(json.load(f))

    nodes = {}
    for path in sorted(glob.glob(os.path.join(ROOT, "nodes", "**", "*.yaml"), recursive=True)):
        rel = os.path.relpath(path, ROOT)
        data = load_yaml(path)
        errs = sorted(validator.iter_errors(data), key=lambda e: list(e.path))
        if errs:
            for e in errs:
                rep.err(rel, f"schema: {'/'.join(map(str, e.path)) or '(top)'}: {e.message}")
            continue
        nid = data["id"]
        if nid in nodes:
            rep.err(rel, f"duplicate id {nid}")
            continue
        expect = os.path.join("nodes", data["concept"], nid + ".yaml")
        if rel != expect:
            rep.err(rel, f"file should live at {expect}")
        if data["concept"] not in concepts:
            rep.err(rel, f"concept '{data['concept']}' is not in concepts.yaml")
        elif data["facet"] not in concepts[data["concept"]].get("facets", []):
            rep.err(rel, f"facet '{data['facet']}' is not listed for concept '{data['concept']}'")
        if not data["requires"] and not data.get("root_reason"):
            rep.err(rel, "a node with no prerequisites must give root_reason")
        names = [c["clause"] for c in data["requires"]]
        if len(names) != len(set(names)):
            rep.err(rel, "clause names must be unique within a node")
        for c in data["requires"]:
            for e in c["all_of"]:
                lint_edge(data, c, e, rep)
        nodes[nid] = data

    # unresolved references
    unresolved = collections.Counter()
    for n in nodes.values():
        for c in n["requires"]:
            for e in c["all_of"]:
                if e["node"] not in nodes:
                    unresolved[e["node"]] += 1
        for r in n.get("related", []):
            if r["node"] not in nodes:
                unresolved[r["node"]] += 1
    for nid, k in sorted(unresolved.items()):
        rep.warn(nid, f"referenced {k} time(s) but not written yet")

    # learnability and cycles
    known = learnable(nodes)
    stuck = set(nodes) - known
    graph = {i: {e["node"] for c in n["requires"] for e in c["all_of"] if e["node"] in nodes} for i, n in nodes.items()}
    comps = sccs(graph)
    in_cycle = {i for comp in comps for i in comp}
    for nid in sorted(stuck):
        if nid in in_cycle:
            rep.err(nid, "unlearnable: caught in a cycle with no clause that escapes it (see RULES 3.4)")
        else:
            rep.err(nid, "unlearnable: every clause needs a node that is itself unlearnable")
    for comp in comps:
        if stuck & set(comp):
            rep.find(f"cycle with no escape through {comp}: fix by splitting a node, adding a clause, or moving an edge to related")
        else:
            rep.find(f"cycle through {comp}: every node still has a way in through another clause; check the cycle is real")

    # merge candidates: same prerequisites and same dependents
    dependents = collections.defaultdict(set)
    for i, n in nodes.items():
        for c in n["requires"]:
            for e in c["all_of"]:
                dependents[e["node"]].add(i)
    sig = collections.defaultdict(list)
    for i, n in nodes.items():
        req = frozenset(frozenset(e["node"] for e in c["all_of"]) for c in n["requires"])
        dep = frozenset(dependents.get(i, ()))
        if req or dep:
            sig[(n["concept"], req, dep)].append(i)
    for ids in sig.values():
        if len(ids) > 1:
            rep.find(f"merge candidates (same prerequisites and same dependents): {sorted(ids)}")

    check_pathways(nodes, rep)

    edges = sum(len(c["all_of"]) for n in nodes.values() for c in n["requires"])
    multi = sum(1 for n in nodes.values() if len(n["requires"]) > 1)
    rep.stats = {"nodes": len(nodes), "prerequisite edges": edges,
                 "nodes with more than one route in": multi,
                 "unwritten nodes referenced": len(unresolved), **rep.stats}

    text = rep.render()
    if args.report:
        os.makedirs(os.path.dirname(os.path.join(ROOT, args.report)), exist_ok=True)
        with open(os.path.join(ROOT, args.report), "w", encoding="utf-8") as f:
            f.write(text)
    print(text)
    sys.exit(1 if rep.errors else 0)


if __name__ == "__main__":
    main()
