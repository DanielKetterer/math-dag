"""Apply critic verdicts to the union of proposer edges and write node files.

    python3 tools/merge_run.py pilot/run

Writes nodes/<concept>/<id>.yaml for every pilot node, <dir>/dropped.json
(edges removed by the critic, for audit), and <dir>/merge_report.md.

Verdict handling:
  necessary            kept, status proposed
  task-only            kept, scope task, points to assess, status proposed
  route-only           kept, status disputed, in its own OR clause: each
                       alternative route = the core edges + that route's edges
                       (core = every kept edge that is not route-only)
  undecided            kept, status disputed
  scaffold / indirect / wrong   removed (logged in dropped.json)
  related              moved to `related`
Critic's missing prerequisites join the main route as disputed; its missing
routes become extra routes (the node's necessary edges plus the new ones),
disputed.

Human review (<dir>/overrides.yaml, optional) is applied last and outranks the
critic. Edge actions: add (an edge no pass proposed), keep (status reviewed), drop, task, related (moved to
`related` as common_path), require (put in every route), replace (point the
edge at another node), restore (bring back an edge the critic dropped),
uphold (confirm a critic drop). Route entries add an OR clause: a copy of the
node's first route minus `without` plus `add`. Then every route that needs
everything another route needs, and more, is removed; edges left only on
removed routes move to `related` as common_path. `rename` maps node ids last.
Everything the review changed is logged in <dir>/review_applied.md.
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
RELATED = {"generalizes", "specializes", "same_idea_different_form", "contrasts_with", "common_path"}
KEEPING = {"keep", "task", "require", "replace", "restore", "related"}
ABSORBED = collections.defaultdict(dict)  # node -> {target: edge} from routes removed as supersets


def load_overrides(d):
    p = os.path.join(d, "overrides.yaml")
    if not os.path.exists(p):
        return None
    ov = yaml.safe_load(open(p, encoding="utf-8")) or {}
    ov.setdefault("edges", [])
    ov.setdefault("routes", [])
    ov.setdefault("rename", {})
    ov.setdefault("set_routes", [])
    ov["by_edge"] = collections.defaultdict(list)
    for o in ov["edges"]:
        ov["by_edge"][(o["node"], o["target"])].append(o)
    return ov


def review_ev(o, reviewer):
    note = f"{o['item']} {o['action']}: {o.get('reason') or ''}".strip()
    return {"kind": "review", "source": reviewer, "note": note[:700]}


def apply_overrides(nid, requires, related, ov, dropped, counts, log):
    """Apply Daniel's verdicts to one node's routes. Returns True if it changed anything."""
    reviewer = ov.get("reviewer", "review")
    touched = False
    done = set()
    for o in [o for o in ov["edges"] if o["node"] == nid]:
        t, act = o["target"], o["action"]
        if act == "uphold":
            continue
        if act == "add":  # an edge no pass proposed, by the reviewer's decision
            edge = {"node": t, "relation": o["relation"], "points_to": o["points_to"], "why": o["why"],
                    "evidence": [review_ev(o, reviewer)], "status": "reviewed"}
            if o.get("scope") == "task":
                edge["scope"], edge["points_to"] = "task", "assess"
            if not requires:
                requires.append({"clause": "standard", "all_of": []})
            for c in requires:
                if not any(e["node"] == t for e in c["all_of"]):
                    c["all_of"].append(copy.deepcopy(edge))
            touched = True
            counts["review: add"] += 1
            log.append(f"- {o['item']} {nid} -> {t}: added on every route")
            continue
        hits = [(c, e) for c in requires for e in c["all_of"] if e["node"] == t]
        if not hits and act in ("drop", "related") and (nid, t) in done:
            continue  # a duplicate item already applied this
        if not hits and t in ABSORBED[nid]:
            counts[f"review: {act} on an absorbed route"] += 1
            log.append(f"- {o['item']} {nid} -> {t}: {act} noted; its route needed everything another route "
                       f"needs and more, so the edge is in related (common_path)")
            continue
        if not hits:
            counts["review: target not found"] += 1
            log.append(f"- {o['item']} {nid} -> {t}: {act} NOT APPLIED (edge not found)")
            continue
        done.add((nid, t))
        if act not in ("keep", "task"):  # these never change which routes exist
            touched = True
        counts[f"review: {act}"] += 1
        if act == "drop":
            for c in requires:
                c["all_of"] = [e for e in c["all_of"] if e["node"] != t]
            dropped.append({"node": nid, "target": t, "verdict": "review", "item": o["item"],
                            "reason": o.get("reason"), "why": hits[0][1].get("why")})
            log.append(f"- {o['item']} {nid} -> {t}: dropped")
            continue
        if act == "related":
            for c in requires:
                c["all_of"] = [e for e in c["all_of"] if e["node"] != t]
            related.append({"node": t, "relation": "common_path",
                            "note": f"Common path, not required ({o['item']}): {o.get('reason') or ''}"[:500]})
            log.append(f"- {o['item']} {nid} -> {t}: moved to related (common_path)")
            continue
        for c, e in hits:
            if act == "task" or (act == "restore" and o.get("scope") == "task"):
                e["scope"], e["points_to"] = "task", "assess"
            if act == "replace":
                e["node"], e["why"] = o["with"], o["why"]
            e["status"] = "reviewed"
            e["evidence"].append(review_ev(o, reviewer))
        if act == "replace":
            for c in requires:  # one edge per node per route
                seen, out = set(), []
                for e in c["all_of"]:
                    if e["node"] not in seen:
                        seen.add(e["node"])
                        out.append(e)
                c["all_of"] = out
            log.append(f"- {o['item']} {nid} -> {t}: replaced by {o['with']}")
        elif act == "require":
            proto = hits[0][1]
            for c in requires:
                if not any(e["node"] == t for e in c["all_of"]):
                    c["all_of"].append(copy.deepcopy(proto))
            log.append(f"- {o['item']} {nid} -> {t}: required on every route")
        elif act in ("task", "restore"):
            log.append(f"- {o['item']} {nid} -> {t}: {act}" + (" (task)" if o.get("scope") == "task" else ""))
    for r in [r for r in ov["routes"] if r["node"] == nid]:
        if not requires:
            log.append(f"- {r['item']} {nid}: route {r['name']} NOT APPLIED (node has no route to copy)")
            continue
        touched = True
        base = requires[0]
        new = {"clause": r["name"]}
        if r.get("note"):
            new["note"] = r["note"]
        if base.get("procedure"):
            new["procedure"] = base["procedure"]
        new["all_of"] = [copy.deepcopy(e) for e in base["all_of"] if e["node"] not in r.get("without", [])]
        for a in r.get("add", []):
            new["all_of"].append({"node": a["node"], "relation": a["relation"], "points_to": a["points_to"],
                                  "why": a["why"], "evidence": [review_ev({"item": r["item"], "action": "route",
                                                                           "reason": r.get("note")}, reviewer)],
                                  "status": "reviewed"})
            if a.get("scope") == "task":
                new["all_of"][-1]["scope"], new["all_of"][-1]["points_to"] = "task", "assess"
        requires.append(new)
        counts["review: route added"] += 1
        log.append(f"- {r['item']} {nid}: added route {r['name']} (without {r.get('without', [])}, "
                   f"plus {[a['node'] for a in r.get('add', [])]})")
    for sr in [r for r in ov.get("set_routes", []) if r["node"] == nid]:
        pool = {}
        for c in requires:
            for e in c["all_of"]:
                pool.setdefault(e["node"], e)
        for t, e in ABSORBED[nid].items():
            pool.setdefault(t, e)
        new_routes, missing = [], []
        for r in sr["routes"]:
            c = {"clause": r["name"]}
            if r.get("note"):
                c["note"] = r["note"]
            c["all_of"] = []
            for t in r["nodes"]:
                tid, scope = (t[:-5], "task") if t.endswith(":task") else (t, None)
                if tid not in pool:
                    missing.append(tid)
                    continue
                e = copy.deepcopy(pool[tid])
                if scope:
                    e["scope"], e["points_to"] = "task", "assess"
                e["status"] = "reviewed"
                e["evidence"].append(review_ev({"item": sr["item"], "action": "set_routes",
                                                "reason": sr.get("reason")}, reviewer))
                c["all_of"].append(e)
            new_routes.append(c)
        if missing:
            log.append(f"- {sr['item']} {nid}: set_routes NOT APPLIED (no existing edge to {missing})")
            continue
        current = {e["node"] for c in requires for e in c["all_of"]}
        left = sorted(current - {e["node"] for c in new_routes for e in c["all_of"]})
        have = {r["node"] for r in related}
        for t in sr.get("to_related", []):
            if t in left and t not in have:
                related.append({"node": t, "relation": "common_path",
                                "note": f"Common path, not required ({sr['item']}): {sr.get('reason') or ''}"[:500]})
        for t in left:
            if t not in sr.get("to_related", []):
                dropped.append({"node": nid, "target": t, "verdict": "review", "item": sr["item"],
                                "reason": sr.get("reason"), "why": pool[t].get("why")})
        used = {e["node"] for c in new_routes for e in c["all_of"]}
        related[:] = [r for r in related if not (r["relation"] == "common_path" and r["node"] in used)]
        requires[:] = new_routes
        touched = True
        counts["review: set_routes"] += 1
        log.append(f"- {sr['item']} {nid}: routes set to {[(r['name'], r['nodes']) for r in sr['routes']]}; "
                   f"related {sr.get('to_related', [])}; dropped {[t for t in left if t not in sr.get('to_related', [])]}")
    if not touched:
        return False
    absorb(nid, requires, related, counts, log)
    return True


def absorb(nid, requires, related, counts, log):
    """A route that needs everything another route needs, and more, adds nothing (A or (A and B) = A).
    Remove it; edges left only on removed routes move to related as common_path (RULES 3.5)."""
    # a route that needs everything another route needs, and more, adds nothing
    sets = [frozenset(e["node"] for e in c["all_of"]) for c in requires]
    keep = [i for i, s in enumerate(sets)
            if not any(j != i and (sets[j] < s or (sets[j] == s and j < i)) for j in range(len(sets)))]
    survivors = set().union(*[sets[i] for i in keep]) if keep else set()
    have = {r["node"] for r in related}
    for i in [i for i in range(len(requires)) if i not in keep]:
        for e in requires[i]["all_of"]:
            ABSORBED[nid].setdefault(e["node"], e)
        moved = sorted({e["node"] for e in requires[i]["all_of"]} - survivors - have)
        for t in moved:
            related.append({"node": t, "relation": "common_path",
                            "note": f"Common path, not required: route '{requires[i]['clause']}' needed everything "
                                    f"another route needs and more, so it was removed."})
            have.add(t)
        counts["dominated route removed"] += 1
        log.append(f"- {nid}: route {requires[i]['clause']} removed (superset of another route); "
                   f"moved to related: {moved or 'nothing'}")
    requires[:] = [requires[i] for i in keep if requires[i]["all_of"]]
    if len(requires) == 1 and requires[0]["clause"] != "standard":
        log.append(f"- {nid}: only route left, renamed {requires[0]['clause']} -> standard")
        requires[0]["clause"] = "standard"
        requires[0].pop("note", None)


def rename_all(doc, rename):
    for c in doc.get("requires", []):
        for e in c["all_of"]:
            e["node"] = rename.get(e["node"], e["node"])
    for r in doc.get("related", []):
        r["node"] = rename.get(r["node"], r["node"])


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
    complete_routes = False
    for p in sorted(glob.glob(os.path.join(d, "critic", "verdicts-*.json"))):
        v = json.load(open(p, encoding="utf-8"))
        for eid, x in v["edges"].items():
            m = mapping[eid]
            verdicts[(m["node"], m["target"])] = x
        node_notes.update(v.get("nodes", {}))
        complete_routes = complete_routes or v.get("route_semantics") == "complete"
    missing_v = [k for k in union if k not in verdicts]

    # which non-first pass clauses each edge belonged to
    passes = {}
    for lab in ("P", "Q"):
        passes[lab] = {}
        for p in glob.glob(os.path.join(d, "passes", f"{lab}-*.json")):
            passes[lab].update(json.load(open(p, encoding="utf-8"))["nodes"])

    ov = load_overrides(d)
    review_log = []
    dropped, counts = [], collections.Counter()
    written = 0
    old = glob.glob(os.path.join(ROOT, "nodes", "**", "*.yaml"), recursive=True)
    for nid, n in nodes.items():
        main_edges, alt = [], collections.OrderedDict()
        related = []
        core_ids = set()  # edges the critic called necessary (or task-only): on every route
        split_from_main = False
        for (a, t), u in union.items():
            if a != nid:
                continue
            x = verdicts.get((a, t), {"verdict": "undecided", "reason": "no critic verdict"})
            verdict = x.get("verdict")
            counts[verdict] += 1
            e0 = u["edges"][0]
            if ov and verdict in ("scaffold", "indirect", "wrong") and any(
                    o["action"] in KEEPING for o in ov["by_edge"].get((a, t.replace("new:", "")), [])):
                counts[f"critic {verdict} overruled by review"] += 1
                verdict = "necessary"
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
            elif verdict == "route-only":
                # its own alternative route; never left in the AND clause with other alternatives
                short = t.replace("new:", "").split(".")[-1]
                name = f"via-{short}"
                if x.get("other_route"):
                    edge["evidence"][-1]["note"] = (edge["evidence"][-1]["note"] + f" | other route: {x['other_route']}")[:600]
                alt.setdefault(name, {"procedure": e0.get("route_procedure"), "edges": []})["edges"].append((edge, e0))
                counts["route-only split into own clause"] += 1
                split_from_main = True
            else:
                main_edges.append((edge, e0))
                if verdict in ("necessary", "task-only"):
                    core_ids.add(edge["node"])

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
        # core: every kept edge outside the alternative routes (necessary, task, undecided,
        # critic-missing). Each alternative route is core + its own edges.
        necessary = list(main)
        # The core alone is a route unless route-only edges were split out of it:
        # then every route needs one of those alternatives (or a pass/critic route).
        if main and not split_from_main:
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
        # The critic's missing routes list the route's prerequisites. A route is the critic's
        # core (edges it called necessary or task-only, which every route needs) plus that list;
        # it is NOT every kept edge plus extras, which made an alternative method keep the
        # edges it was meant to skip (the old superset-route flaw). Listed prerequisites that
        # are already edges of this node reuse that edge, with its why and evidence.
        pool = {}
        for e in main:
            pool.setdefault(e["node"], e)
        for a in alt.values():
            for e, _ in a["edges"]:
                pool.setdefault(e["node"], e)
        for i, mr in enumerate(notes.get("missing_routes", []) or []):
            pre = [ALIASES.get(t.replace("new:", ""), t.replace("new:", "")) for t in (mr.get("prerequisites") or []) if t and t != nid]
            if not pre:
                continue
            desc = (mr.get("description") or "").strip()
            # Critic files that declare "route_semantics": "complete" list every prerequisite of
            # the route; older files listed only the extras, so their routes start from every
            # main-route edge (and the absorption below removes those that add nothing).
            base = core_ids if complete_routes else {e["node"] for e in main}
            route = [copy.deepcopy(e) for e in main if e["node"] in base]
            for t in pre:
                if any(e["node"] == t for e in route):
                    continue
                if t in pool:
                    route.append(copy.deepcopy(pool[t]))
                    continue
                why = f"Alternative route proposed by the critic: {desc}"
                route.append({"node": t, "relation": "definitional", "points_to": "statement", "why": why[:600],
                              "evidence": [{"kind": "content", "source": "critic-sonnet", "note": "missing route"}],
                              "status": "disputed"})
            requires.append({"clause": f"critic-route-{i + 1}", "note": desc[:500], "all_of": route})
            counts["alt route from critic"] += 1
        if len(requires) > 1:
            absorb(nid, requires, related, counts, review_log)

        emptied_by_review = False
        if ov:
            had = bool(requires)
            if apply_overrides(nid, requires, related, ov, dropped, counts, review_log) and had and not requires:
                emptied_by_review = True

        doc = {k: n[k] for k in ("id", "concept", "facet", "level", "type", "name", "statement") if k in n}
        if n.get("procedure"):
            doc["procedure"] = n["procedure"]
        doc["assess"] = n["assess"]
        src = n.get("sources") or {}
        doc["sources"] = {"ccss": [str(s) for s in src.get("ccss", [])],
                          "learning_components": [str(s) for s in src.get("lc", [])]}
        if src.get("prek"):
            doc["sources"]["prek"] = [str(s) for s in src["prek"]]
        if src.get("other"):
            doc["sources"]["other"] = [str(s) for s in src["other"]]
        doc["requires"] = requires
        if not requires:
            reasons = [passes[p].get(nid, {}).get("root_reason") for p in ("P", "Q")]
            reasons.append(n.get("root_reason"))
            if emptied_by_review:
                doc["root_reason"] = ("Every prerequisite was dropped or moved to related in review; "
                                      "a root by review decision, check this node.")
                review_log.append(f"- {nid}: now a root (every prerequisite dropped or moved in review)")
            else:
                doc["root_reason"] = next((r for r in reasons if r), "Every proposed prerequisite was removed by the critic; check this node.")
        if related:
            seen = set()
            doc["related"] = [r for r in related if not (r["node"] in seen or seen.add(r["node"]))]
        if ov and ov["rename"]:
            rename_all(doc, ov["rename"])
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

    if ov:
        for o in ov["edges"]:
            if o["action"] == "uphold":
                for x in dropped:
                    if (x["node"], x["target"]) == (o["node"], o["target"]):
                        x["review"] = f"upheld by {ov.get('reviewer', 'review')} ({o['item']})"
                        counts["review: critic drop upheld"] += 1
        unknown = sorted({o["node"] for o in ov["edges"]} - set(nodes))
        if unknown:
            review_log.append(f"- overrides name nodes outside this run: {unknown}")
        open(os.path.join(d, "review_applied.md"), "w").write(
            "# Review verdicts applied by merge_run\n\n" + "\n".join(review_log) + "\n")
    json.dump(dropped, open(os.path.join(d, "dropped.json"), "w"), indent=1)
    rep = ["# Merge report", "", f"- Node files written: {written}",
           f"- Example files superseded and removed: {removed or 'none'}",
           f"- Union edges with no critic verdict: {len(missing_v)}"]
    rep += [f"- {k}: {v}" for k, v in counts.most_common()]
    open(os.path.join(d, "merge_report.md"), "w").write("\n".join(rep) + "\n")
    print("\n".join(rep))


if __name__ == "__main__":
    main(sys.argv[1])
