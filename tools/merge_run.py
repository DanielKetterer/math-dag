"""Apply critic verdicts to the union of proposer edges and write node files.

    python3 tools/merge_run.py pilot/run

Writes nodes/<concept>/<id>.yaml for every pilot node, <dir>/dropped.json
(edges removed by the critic, for audit), and <dir>/merge_report.md.

Verdict handling:
  necessary            kept, status proposed
  task-only            kept, scope task, points to assess, status proposed
  route-only           kept in the route it came from, status disputed
  undecided            kept, status disputed
  scaffold / indirect / wrong   removed (logged in dropped.json)
  related              moved to `related`
Critic's missing prerequisites join the main route as disputed; its missing
routes become extra routes (the node's necessary edges plus the new ones),
disputed.
"""
import collections
import copy
import glob
import json
import os
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALIASES = {"division.by-zero-undefined": "division.by-zero.undefined"}
RELATED = {"generalizes", "specializes", "same_idea_different_form", "contrasts_with"}


class NoAlias(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True


def why_ok(text):
    return text and len(text.split()) >= 8


def main(d):
    nodes = {}
    for p in sorted(glob.glob(os.path.join(d, "batches", "*.yaml"))):
        for n in yaml.safe_load(open(p, encoding="utf-8")):
            nodes[n["id"]] = n
    union = {(u["node"], u["target"]): u for u in json.load(open(os.path.join(d, "union.json")))}
    mapping = json.load(open(os.path.join(d, "critic", "_mapping.json")))
    verdicts, node_notes = {}, {}
    for p in sorted(glob.glob(os.path.join(d, "critic", "verdicts-*.json"))):
        v = json.load(open(p, encoding="utf-8"))
        for eid, x in v["edges"].items():
            m = mapping[eid]
            verdicts[(m["node"], m["target"])] = x
        node_notes.update(v.get("nodes", {}))
    missing_v = [k for k in union if k not in verdicts]

    # which non-first pass clauses each edge belonged to
    passes = {}
    for lab in ("P", "Q"):
        passes[lab] = {}
        for p in glob.glob(os.path.join(d, "passes", f"{lab}-*.json")):
            passes[lab].update(json.load(open(p, encoding="utf-8"))["nodes"])

    dropped, counts = [], collections.Counter()
    written = 0
    old = glob.glob(os.path.join(ROOT, "nodes", "**", "*.yaml"), recursive=True)
    for nid, n in nodes.items():
        main_edges, alt = [], collections.OrderedDict()
        related = []
        for (a, t), u in union.items():
            if a != nid:
                continue
            x = verdicts.get((a, t), {"verdict": "undecided", "reason": "no critic verdict"})
            verdict = x.get("verdict")
            counts[verdict] += 1
            e0 = u["edges"][0]
            if verdict in ("scaffold", "indirect", "wrong"):
                dropped.append({"node": nid, "target": t, "verdict": verdict, "reason": x.get("reason"),
                                "via": x.get("via"), "proposed_by": u["passes"], "why": e0.get("why")})
                continue
            if verdict == "related":
                rel = x.get("relation") if x.get("relation") in RELATED else "same_idea_different_form"
                related.append({"node": t.replace("new:", ""), "relation": rel,
                                "note": (x.get("reason") or "")[:300]})
                continue
            edge = {"node": ALIASES.get(t.replace("new:", ""), t.replace("new:", "")), "relation": e0.get("relation"),
                    "points_to": e0.get("points_to"), "why": e0.get("why")}
            if verdict == "task-only" or e0.get("scope") == "task":
                edge["scope"] = "task"
                edge["points_to"] = "assess"
            ev = [{"kind": "content", "source": f"pass-{p}"} for p in u["passes"]]
            reason = (x.get("reason") or "").strip()
            ev.append({"kind": "content", "source": "critic-sonnet",
                       "note": f"{verdict}: {reason[:240]}" if reason else verdict})
            edge["evidence"] = ev
            edge["status"] = "proposed" if verdict in ("necessary", "task-only") else "disputed"
            # was it only ever in a second (or later) route of its passes?
            alt_names = []
            for p in u["passes"]:
                routes = passes[p].get(nid, {}).get("routes", [])
                where = [i for i, r in enumerate(routes) if any(ee.get("node") == t for ee in r.get("edges", []))]
                if where and min(where) > 0:
                    alt_names.append((routes[min(where)].get("clause", "alt"), routes[min(where)].get("procedure")))
            if alt_names and verdict != "necessary":
                name, proc = alt_names[0]
                alt.setdefault(name, {"procedure": proc, "edges": []})["edges"].append((edge, e0))
            else:
                main_edges.append((edge, e0))

        def fix_points(edge, proc):
            pt = edge["points_to"]
            if pt.startswith("procedure."):
                steps = proc or n.get("procedure") or []
                if not 1 <= int(pt.split(".")[1]) <= len(steps):
                    edge["points_to"] = "statement" if edge.get("scope") != "task" else "assess"
            return edge

        requires = []
        main_procs = [e0.get("route_procedure") for _, e0 in main_edges if e0.get("route_procedure")]
        main_proc = None if n.get("procedure") else (main_procs[0] if main_procs else None)
        # the critic's missing prerequisites join the main route
        notes = node_notes.get(nid, {})
        for mp in notes.get("missing_prerequisites", []) or []:
            t = ALIASES.get((mp.get("node") or "").replace("new:", ""), (mp.get("node") or "").replace("new:", ""))
            if not t or t == nid or any(e["node"] == t for e, _ in main_edges):
                continue
            why = mp.get("why") or ""
            if not why_ok(why):
                why = f"Critic: {why} (proposed as a missing direct prerequisite of this node)."
            main_edges.append(({"node": t, "relation": "definitional", "points_to": "statement", "why": why,
                                "evidence": [{"kind": "content", "source": "critic-sonnet", "note": "missing prerequisite"}],
                                "status": "disputed"}, {}))
            counts["missing-prerequisite added"] += 1
        main = [fix_points(e, main_proc) for e, _ in main_edges]
        necessary = [e for e in main if e["status"] == "proposed"]
        if main:
            c = {"clause": "standard"}
            if main_proc:
                c["procedure"] = main_proc
            c["all_of"] = main
            requires.append(c)
        for name, a in alt.items():
            proc = a["procedure"]
            edges = [fix_points(e, proc) for e, _ in a["edges"]]
            nm = name if name != "standard" else "alt"
            if any(r["clause"] == nm for r in requires):
                nm = nm + "-2"
            c = {"clause": nm}
            if proc:
                c["procedure"] = proc
            c["all_of"] = copy.deepcopy(necessary) + [e for e in edges if e["node"] not in {x["node"] for x in necessary}]
            requires.append(c)
            counts["alt route from passes"] += 1
        for i, mr in enumerate(notes.get("missing_routes", []) or []):
            pre = [ALIASES.get(t.replace("new:", ""), t.replace("new:", "")) for t in (mr.get("prerequisites") or []) if t and t != nid]
            if not pre:
                continue
            desc = (mr.get("description") or "").strip()
            extra = []
            for t in pre:
                if any(e["node"] == t for e in necessary):
                    continue
                why = f"Alternative route proposed by the critic: {desc}"
                extra.append({"node": t, "relation": "definitional", "points_to": "statement", "why": why[:600],
                              "evidence": [{"kind": "content", "source": "critic-sonnet", "note": "missing route"}],
                              "status": "disputed"})
            if not extra:
                continue
            requires.append({"clause": f"critic-route-{i + 1}", "note": desc[:500],
                             "all_of": copy.deepcopy(necessary) + extra})
            counts["alt route from critic"] += 1

        doc = {k: n[k] for k in ("id", "concept", "facet", "level", "type", "name", "statement") if k in n}
        if n.get("procedure"):
            doc["procedure"] = n["procedure"]
        doc["assess"] = n["assess"]
        src = n.get("sources") or {}
        doc["sources"] = {"ccss": [str(s) for s in src.get("ccss", [])],
                          "learning_components": [str(s) for s in src.get("lc", [])]}
        doc["requires"] = requires
        if not requires:
            reasons = [passes[p].get(nid, {}).get("root_reason") for p in ("P", "Q")]
            doc["root_reason"] = next((r for r in reasons if r), "Every proposed prerequisite was removed by the critic; check this node.")
        if related:
            seen = set()
            doc["related"] = [r for r in related if not (r["node"] in seen or seen.add(r["node"]))]
        doc["status"] = "proposed"
        path = os.path.join(ROOT, "nodes", n["concept"], nid + ".yaml")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(doc, f, Dumper=NoAlias, sort_keys=False, width=100, allow_unicode=False)
        written += 1

    # remove example files superseded by pilot nodes (same id, different place)
    pilot_paths = {os.path.join(ROOT, "nodes", n["concept"], i + ".yaml") for i, n in nodes.items()}
    removed = []
    for p in old:
        base = os.path.basename(p)[:-5]
        if base in nodes and p not in pilot_paths:
            os.remove(p)
            removed.append(os.path.relpath(p, ROOT))

    json.dump(dropped, open(os.path.join(d, "dropped.json"), "w"), indent=1)
    rep = ["# Merge report", "", f"- Node files written: {written}",
           f"- Example files superseded and removed: {removed or 'none'}",
           f"- Union edges with no critic verdict: {len(missing_v)}"]
    rep += [f"- {k}: {v}" for k, v in counts.most_common()]
    open(os.path.join(d, "merge_report.md"), "w").write("\n".join(rep) + "\n")
    print("\n".join(rep))


if __name__ == "__main__":
    main(sys.argv[1])
