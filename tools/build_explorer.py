"""Build the interactive map explorer from the node files.

    python3 tools/build_explorer.py [fragment_out]

Writes explorer/index.html (a standalone page) from explorer/template.html,
with the current map embedded as JSON. If fragment_out is given, also writes
the page body without the doctype wrapper (for publishing as an artifact).
"""
import collections
import glob
import json
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def grade_of(codes):
    gs = []
    for c in codes:
        m = re.match(r"^(\d+)\.", str(c))
        if m:
            gs.append(int(m.group(1)))
        elif str(c).startswith("K."):
            gs.append(0)
        elif str(c).startswith("HS"):
            gs.append(9)
    return min(gs) if gs else None


def boundary_meanings():
    p = os.path.join(ROOT, "pilot", "run", "proposer.md")
    if not os.path.exists(p):
        return {}
    return dict(re.findall(r"^\| `([a-z0-9.-]+)` \| (.+?) \|$", open(p, encoding="utf-8").read(), re.M))


def main():
    nodes = {}
    for p in sorted(glob.glob(os.path.join(ROOT, "nodes", "**", "*.yaml"), recursive=True)):
        n = yaml.safe_load(open(p, encoding="utf-8"))
        nodes[n["id"]] = n
    meanings = boundary_meanings()
    out_nodes, edges, outside = [], {}, collections.Counter()
    for i, n in nodes.items():
        routes = []
        for c in n.get("requires", []):
            items = []
            for e in c["all_of"]:
                note = next((x.get("note", "") for x in e.get("evidence", []) if x.get("source") == "critic-sonnet"), "")
                items.append({"node": e["node"], "relation": e.get("relation"), "status": e.get("status", "proposed"),
                              "task": e.get("scope") == "task", "why": e.get("why", ""), "critic": note,
                              "by": [x["source"].replace("pass-", "") for x in e.get("evidence", [])
                                     if x.get("source", "").startswith("pass-")]})
                key = (e["node"], i)
                cur = edges.get(key)
                status = e.get("status", "proposed")
                rank = {"proposed": 0, "disputed": 1}.get(status, 1)
                if cur is None or rank < cur["rank"]:
                    edges[key] = {"source": e["node"], "target": i, "status": status, "rank": rank,
                                  "task": e.get("scope") == "task",
                                  "alt": c["clause"] != "standard"}
                elif c["clause"] == "standard":
                    cur["alt"] = False
                if e["node"] not in nodes:
                    outside[e["node"]] += 1
            routes.append({"clause": c["clause"], "note": c.get("note", ""), "edges": items})
        src = n.get("sources") or {}
        out_nodes.append({
            "id": i, "name": n["name"], "concept": n["concept"], "facet": n["facet"], "level": n["level"],
            "type": n["type"], "statement": n["statement"], "procedure": n.get("procedure") or [],
            "assess": n["assess"], "ccss": [str(s) for s in src.get("ccss", [])],
            "grade": grade_of(src.get("ccss", [])), "routes": routes,
            "related": n.get("related") or [], "root": n.get("root_reason", ""), "outside": False})
    for o, k in outside.items():
        out_nodes.append({"id": o, "name": meanings.get(o, o.replace(".", " ").replace("-", " ")),
                          "concept": o.split(".")[0], "facet": "", "level": None, "type": "outside",
                          "statement": meanings.get(o, "A skill outside the pilot slice, not written yet."),
                          "procedure": [], "assess": "", "ccss": [], "grade": None, "routes": [],
                          "related": [], "root": "", "outside": True})
    data = {"nodes": out_nodes,
            "edges": [{k: v for k, v in e.items() if k != "rank"} for e in edges.values()],
            "built": "from nodes/ in DanielKetterer/math-dag"}
    blob = json.dumps(data, ensure_ascii=True, separators=(",", ":")).replace("</", "<\\/")
    tpl = open(os.path.join(ROOT, "explorer", "template.html"), encoding="utf-8").read()
    frag = tpl.replace("__GRAPH_DATA__", blob)
    head = ('<!doctype html>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n')
    page = head + frag
    with open(os.path.join(ROOT, "explorer", "index.html"), "w", encoding="utf-8") as f:
        f.write(page)
    # Keep the branch-based GitHub Pages publishing directory in sync.
    # Configure Pages to publish main/docs, since Pages branch publishing
    # supports the repository root or /docs, not arbitrary subdirectories.
    docs = os.path.join(ROOT, "docs")
    os.makedirs(docs, exist_ok=True)
    with open(os.path.join(docs, "index.html"), "w", encoding="utf-8") as f:
        f.write(page)
    if len(sys.argv) > 1:
        with open(sys.argv[1], "w", encoding="utf-8") as f:
            f.write(frag)
    print(f"{len(out_nodes)} nodes ({len(outside)} outside the pilot), {len(edges)} edges, "
          f"{len(frag) / 1e6:.2f} MB")


if __name__ == "__main__":
    main()
