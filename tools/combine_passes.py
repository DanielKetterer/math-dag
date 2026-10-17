"""Combine independent prerequisite passes and measure how much they agree.

    python3 tools/combine_passes.py pilot/calibration [--voters A,B,C] [--compare D]

Reads <dir>/nodes.yaml and <dir>/passes/pass-*.json. Writes:
  <dir>/merged/nodes/<concept>/<id>.yaml   merged node files (checkable with tools/check.py --nodes)
  <dir>/review.md                         every proposed edge, numbered, with votes
  <dir>/stats.md                          agreement and lint numbers
"""
import argparse
import collections
import glob
import itertools
import json
import os
import re
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from check import VAGUE, MIN_WHY_WORDS  # noqa: E402

BOUNDARY = {
    "counting.objects", "comparing.area.direct", "comparing.whole-numbers.symbols",
    "partitioning.equal-shares.area", "partitioning.equal-parts.length",
    "measurement.length.unit-iteration", "number-line.whole-number-lengths",
    "multiplication.equal-groups", "multiplication.facts.within-100", "multiplication.by-one",
    "division.partitive", "division.measurement.whole-number",
}


def lint(node, route, e, ids):
    errs = []
    t = e.get("node", "")
    if not (t in ids or t in BOUNDARY or t.startswith("new:")):
        errs.append(f"target not allowed: {t}")
    if t == node["id"]:
        errs.append("self edge")
    if e.get("relation") not in ("definitional", "procedural", "representational", "justificatory"):
        errs.append(f"bad relation {e.get('relation')}")
    pt = e.get("points_to", "")
    scope = e.get("scope", "concept")
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
        errs.append("task edge not pointing to assess")
    if scope == "concept" and pt == "assess":
        errs.append("concept edge pointing to assess")
    why = (e.get("why") or "").lower()
    if len(why.split()) < MIN_WHY_WORDS:
        errs.append("why too short")
    errs += [f"vague phrase '{v}'" for v in VAGUE if v in why]
    return errs


PUNCT = {"\u2014": " - ", "\u2013": "-", "\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"', "\u2026": "...", "\u00d7": "x"}


def clean(obj):
    """Normalize typographic punctuation in pass text to plain keyboard characters."""
    if isinstance(obj, str):
        for k, v in PUNCT.items():
            obj = obj.replace(k, v)
        return obj
    if isinstance(obj, list):
        return [clean(x) for x in obj]
    if isinstance(obj, dict):
        return {k: clean(v) for k, v in obj.items()}
    return obj


def edge_set(pass_node):
    return {e["node"] for r in pass_node.get("routes", []) for e in r.get("edges", [])}


def jaccard(a, b):
    return len(a & b) / len(a | b) if a | b else 1.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dir")
    ap.add_argument("--voters", default="A,B,C")
    ap.add_argument("--compare", default="D")
    args = ap.parse_args()
    d = args.dir
    nodes = {n["id"]: n for n in yaml.safe_load(open(os.path.join(d, "nodes.yaml"), encoding="utf-8"))}
    ids = set(nodes)
    passes = {}
    for p in sorted(glob.glob(os.path.join(d, "passes", "pass-*.json"))):
        label = re.search(r"pass-(\w+)\.json$", p).group(1)
        passes[label] = clean(json.load(open(p, encoding="utf-8"))["nodes"])
    voters = [v for v in args.voters.split(",") if v in passes]
    compare = [c for c in args.compare.split(",") if c in passes]
    stats = []

    # ---- lint and coverage per pass
    stats.append("## Rule compliance per pass\n")
    stats.append("| Pass | Nodes covered | Edges | Rule violations | New (outside) targets | Nodes with 2+ routes |")
    stats.append("|---|---|---|---|---|---|")
    violations = {}
    for lab, pn in passes.items():
        nerr, nedge, nnew, multi = 0, 0, 0, 0
        violations[lab] = []
        for nid, node in nodes.items():
            entry = pn.get(nid, {"routes": []})
            if len(entry.get("routes", [])) > 1:
                multi += 1
            for r in entry.get("routes", []):
                for e in r.get("edges", []):
                    nedge += 1
                    nnew += e.get("node", "").startswith("new:")
                    for msg in lint(nodes[nid], r, e, ids):
                        nerr += 1
                        violations[lab].append(f"{nid} -> {e.get('node')}: {msg}")
        covered = sum(1 for nid in nodes if nid in pn)
        stats.append(f"| {lab} | {covered}/{len(nodes)} | {nedge} | {nerr} | {nnew} | {multi} |")

    # ---- agreement among voters (edge = node -> prerequisite, ignoring route)
    sets = {lab: {nid: edge_set(passes[lab].get(nid, {})) for nid in nodes} for lab in passes}
    allk = lambda lab: {(n, t) for n, ts in sets[lab].items() for t in ts}  # noqa: E731
    votes = collections.Counter()
    for lab in voters:
        votes.update(allk(lab))
    k = len(voters)
    dist = collections.Counter(votes.values())
    union = len(votes)
    stats.append("\n## Agreement among the voting passes (" + ", ".join(voters) + ")\n")
    stats.append(f"- Distinct edges proposed by any voter: {union}")
    for v in range(k, 0, -1):
        stats.append(f"- Proposed by {v} of {k}: {dist.get(v, 0)} ({100 * dist.get(v, 0) / union:.0f}%)")
    stats.append("\nPairwise overlap (Jaccard on all edges):\n")
    labs = voters + compare
    for a, b in itertools.combinations(labs, 2):
        stats.append(f"- {a} vs {b}: {jaccard(allk(a), allk(b)):.2f}")
    majority = {key for key, c in votes.items() if c * 2 > k}
    for c in compare:
        ck = allk(c)
        rec = len(ck & majority) / len(majority) if majority else 0
        prec = len(ck & majority) / len(ck) if ck else 0
        stats.append(f"\n- {c} against the voters' majority: recovers {rec:.0%} of majority edges; "
                     f"{prec:.0%} of {c}'s edges are majority edges")

    # relation agreement on unanimous edges
    rel = collections.defaultdict(list)
    for lab in voters:
        for nid, entry in passes[lab].items():
            for r in entry.get("routes", []):
                for e in r.get("edges", []):
                    rel[(nid, e["node"])].append(e.get("relation"))
    unan = [key for key, c in votes.items() if c == k]
    same_rel = sum(1 for key in unan if len(set(rel[key])) == 1)
    stats.append(f"\n- Unanimous edges whose relation type also matches across voters: {same_rel}/{len(unan)}")
    routes_disagree = [nid for nid in nodes
                       if len({len(passes[lab].get(nid, {}).get('routes', [])) for lab in voters}) > 1]
    stats.append(f"- Nodes where voters disagree on the number of routes: {len(routes_disagree)} {routes_disagree}")

    # ---- merged node files: structure from the most central voter, status from votes
    out_nodes = os.path.join(d, "merged", "nodes")
    for p in glob.glob(os.path.join(out_nodes, "**", "*.yaml"), recursive=True):
        os.remove(p)
    for nid, node in nodes.items():
        best = max(voters, key=lambda lab: sum(jaccard(sets[lab][nid], sets[o][nid]) for o in voters if o != lab))
        entry = passes[best].get(nid, {"routes": []})
        requires = []
        placed = set()
        for r in entry.get("routes", []):
            edges = []
            for e in r.get("edges", []):
                key = (nid, e["node"])
                if votes[key] * 2 <= k or e["node"] in placed and False:
                    continue
                who = sorted(lab for lab in voters if e["node"] in sets[lab][nid])
                ee = {kk: e[kk] for kk in ("node", "relation", "points_to", "why") if kk in e}
                ee["node"] = ee["node"].replace("new:", "")
                if e.get("scope", "concept") == "task":
                    ee["scope"] = "task"
                ee["evidence"] = [{"kind": "content", "source": f"pass-{w}"} for w in who]
                ee["status"] = "proposed" if votes[key] == k else "disputed"
                edges.append(ee)
                placed.add(e["node"])
            if edges:
                c = {"clause": r.get("clause", "standard")}
                if r.get("procedure"):
                    c["procedure"] = r["procedure"]
                c["all_of"] = edges
                requires.append(c)
        # majority edges the central voter left out: attach to the first route, disputed
        missing = sorted(t for (n, t) in majority if n == nid and t not in placed)
        for t in missing:
            src = next(lab for lab in voters if t in sets[lab][nid])
            e = next(e for r in passes[src][nid]["routes"] for e in r["edges"] if e["node"] == t)
            ee = {kk: e[kk] for kk in ("node", "relation", "why") if kk in e}
            ee["node"] = ee["node"].replace("new:", "")
            ee["points_to"] = e["points_to"] if not e["points_to"].startswith("procedure.") or not requires else "statement"
            if e.get("scope") == "task":
                ee["scope"] = "task"
            ee["evidence"] = [{"kind": "content", "source": f"pass-{w}"} for w in voters if t in sets[w][nid]]
            ee["status"] = "disputed"
            if not requires:
                requires.append({"clause": "standard", "all_of": []})
            requires[0]["all_of"].append(ee)
        doc = {k2: node[k2] for k2 in ("id", "concept", "facet", "level", "type", "name", "statement")}
        if node.get("procedure"):
            doc["procedure"] = node["procedure"]
        doc["assess"] = node["assess"]
        src = node.get("sources", {})
        doc["sources"] = {"ccss": [str(x) for x in src.get("ccss", [])],
                          "learning_components": [str(x) for x in src.get("lc", [])]}
        doc["requires"] = requires
        if not requires:
            doc["root_reason"] = entry.get("root_reason") or "No prerequisite reached majority agreement among the passes."
        doc["status"] = "proposed"
        path = os.path.join(out_nodes, node["concept"], nid + ".yaml")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            yaml.safe_dump(doc, f, sort_keys=False, allow_unicode=False, width=100)

    # ---- review sheet: every distinct edge proposed by anyone
    lines = ["# Calibration review", "",
             "Every prerequisite any pass proposed, numbered. Votes show which passes proposed it",
             f"(voters {', '.join(voters)}; comparison {', '.join(compare)}). Reply with the numbers you",
             "judge **wrong** (not a real direct prerequisite), and any you are unsure of.", ""]
    num = 0
    allpasses = voters + compare
    for nid, node in nodes.items():
        lines += [f"## {nid}", "", f"*{node['statement'].strip()}*", ""]
        keys = collections.OrderedDict()
        for lab in allpasses:
            for r in passes[lab].get(nid, {}).get("routes", []):
                for e in r.get("edges", []):
                    keys.setdefault(e["node"], []).append((lab, r.get("clause"), e))
        if not keys:
            lines += ["- (every pass treated this as a root)", ""]
            continue
        for t, props in sorted(keys.items(), key=lambda kv: -len({p[0] for p in kv[1] if p[0] in voters})):
            num += 1
            who = sorted({p[0] for p in props})
            vv = sum(1 for w in who if w in voters)
            lab0, clause0, e0 = props[0]
            rels = "/".join(sorted({p[2].get("relation", "?") for p in props}))
            routes = ", ".join(sorted({f"{p[0]}:{p[1]}" for p in props}))
            lines.append(f"{num}. **{t}**: {vv}/{k} voters {''.join(w for w in who)}; {rels}. Routes: {routes}")
            lines.append(f"   - Why ({lab0}): {e0.get('why', '').strip()}")
        lines.append("")
    with open(os.path.join(d, "review.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    stats.append(f"\n## Rule violations\n")
    for lab, v in violations.items():
        stats.append(f"- {lab}: " + ("; ".join(v) if v else "none"))
    stats.append(f"\nReview sheet: {num} distinct edges.")
    with open(os.path.join(d, "stats.md"), "w", encoding="utf-8") as f:
        f.write("# Calibration stats\n\n" + "\n".join(stats) + "\n")
    print("\n".join(stats))


if __name__ == "__main__":
    main()
