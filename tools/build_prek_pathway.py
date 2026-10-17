"""Build the Clements-Sarama developmental pathway for the pre-K layer.

    python3 tools/build_prek_pathway.py

Each node that cites Clements-Sarama levels (sources.prek ids starting `cs.`)
is placed at the earliest starting age among those levels. Nodes at the same
age share a step. Writes pathways/clements-sarama.yaml; tools/check.py then
reports any node placed before every one of its routes is met.

A developmental order is a typical order, like a curriculum: a finding can
refute an edge (or show a missing route), and agreement confirms nothing.
The ELOF is not built as a pathway: its goals are cited at goal level across
many nodes, so it gives no node-level order.
"""
import collections
import glob
import os
import re

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    cs = yaml.safe_load(open(os.path.join(ROOT, "sources", "prek", "clements_sarama.yaml"), encoding="utf-8"))
    age = {}
    for levels in cs["trajectories"].values():
        for lv in levels:
            m = re.match(r"\s*(\d+)", str(lv["age"]))
            if m:
                age[lv["id"]] = int(m.group(1))
    steps = collections.defaultdict(list)
    placed = set()
    nodes = {}
    for p in glob.glob(os.path.join(ROOT, "nodes", "**", "*.yaml"), recursive=True):
        n = yaml.safe_load(open(p, encoding="utf-8"))
        nodes[n["id"]] = n
        ages = [age[s] for s in (n.get("sources") or {}).get("prek", []) if s in age]
        if ages:
            steps[min(ages)].append(n["id"])
            placed.add(n["id"])
    doc = {
        "name": "Clements-Sarama learning trajectories (developmental order)",
        "source": "sources/prek/clements_sarama.yaml",
        "note": "Each node is placed at the earliest starting age of the trajectory levels it cites. "
                "Developmental order can refute an edge; it never confirms one.",
        "steps": [{"position": a, "grade": f"age-{a}", "nodes": sorted(v)} for a, v in sorted(steps.items())],
        # nodes the trajectories do not place: the pathway says nothing about their order
        "assumes": sorted(set(nodes) - placed),
    }
    with open(os.path.join(ROOT, "pathways", "clements-sarama.yaml"), "w", encoding="utf-8") as f:
        yaml.safe_dump(doc, f, sort_keys=False, width=100)
    print(f"placed {len(placed)} nodes at ages {sorted(steps)}")


if __name__ == "__main__":
    main()
