"""Build the human review queue for a run.

    python3 tools/review_queue.py pilot/run

Writes <dir>/REVIEW.md: a random sample of kept edges (for a precision
estimate), the critic's open questions, the highest-impact disputed edges and
drops, and the benchmark misses. Every item is numbered; reply with numbers.
"""
import collections
import glob
import json
import os
import random
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main(d):
    nodes = {}
    for p in glob.glob(os.path.join(ROOT, "nodes", "**", "*.yaml"), recursive=True):
        n = yaml.safe_load(open(p, encoding="utf-8"))
        nodes[n["id"]] = n
    dependents = collections.defaultdict(set)
    for i, n in nodes.items():
        for c in n["requires"]:
            for e in c["all_of"]:
                dependents[e["node"]].add(i)

    def downstream(i):
        seen, stack = set(), [i]
        while stack:
            for y in dependents.get(stack.pop(), ()):
                if y not in seen:
                    seen.add(y)
                    stack.append(y)
        return len(seen)
    impact = {i: downstream(i) for i in nodes}
    name = lambda i: nodes[i]["name"] if i in nodes else f"(outside the pilot: {i})"  # noqa: E731

    kept, disputed = [], []
    for i, n in nodes.items():
        seen = set()
        for c in n["requires"]:
            for e in c["all_of"]:
                key = (i, e["node"], c["clause"])
                if (i, e["node"]) in seen and e.get("status") == "proposed":
                    continue
                seen.add((i, e["node"]))
                note = next((x.get("note", "") for x in e["evidence"] if x["source"] == "critic-sonnet"), "")
                item = {"node": i, "target": e["node"], "clause": c["clause"], "why": e["why"], "note": note,
                        "status": e.get("status"), "scope": e.get("scope", "concept"), "route_note": c.get("note")}
                (kept if e.get("status") == "proposed" else disputed).append(item)
    rng = random.Random(20261016)
    sample = rng.sample(kept, 40)
    dropped = json.load(open(os.path.join(d, "dropped.json")))
    ver = {}
    for p in glob.glob(os.path.join(d, "critic", "verdicts-*.json")):
        ver.update(json.load(open(p))["edges"])
    mapping = json.load(open(os.path.join(d, "critic", "_mapping.json")))
    undecided = [(mapping[e], v) for e, v in ver.items() if v.get("verdict") == "undecided"]

    lines = ["# Review queue: equal sharing to slope", "",
             "Reply with item numbers. For A, B, and D: list the numbers you judge **wrong**",
             "(and any you are unsure of). For C: answer each question in a few words.",
             "Work top to bottom; sections are in priority order, and each is useful on its own.", ""]
    num = 0

    def item(text, sub=()):
        nonlocal num
        num += 1
        lines.append(f"{num}. {text}")
        for s in sub:
            lines.append(f"   - {s}")

    lines += ["## A. Random sample of kept edges (precision estimate)", "",
              f"40 drawn at random from the {len(kept)} edges both checks kept. The share you mark wrong",
              "estimates the error rate of the whole map.", ""]
    for x in sample:
        tag = " (test problem only)" if x["scope"] == "task" else ""
        item(f"**{name(x['node'])}** needs **{name(x['target'])}**{tag}", [f"Why: {x['why']}"])
    lines.append("")

    lines += ["## B. Edges the critic removed, highest impact first", "",
              f"The critic removed {len(dropped)} edges as scaffold, indirect, or wrong. These 20 sit under the",
              "most other nodes. Mark the ones it should have **kept**.", ""]
    for x in sorted(dropped, key=lambda x: -impact.get(x["node"], 0))[:20]:
        via = f" (via {x['via']})" if x.get("via") else ""
        item(f"**{name(x['node'])}** needs **{name(x['target'])}**? Critic: {x['verdict']}{via}",
             [f"Proposer's why: {x['why']}", f"Critic: {x['reason']}"])
    lines.append("")

    lines += ["## C. Questions the critic could not settle", ""]
    for m, v in undecided:
        item(f"**{name(m['node'])}** needs **{name(m['target'])}**?",
             [f"What would decide it: {v.get('would_decide') or v.get('reason')}"])
    lines.append("")

    lines += ["## D. Disputed edges and new routes, highest impact first", "",
              f"{len(disputed)} edges are disputed (route-only, added by the critic, or on an alternative route).",
              "These 30 matter most. Mark the ones that are **wrong**.", ""]
    for x in sorted(disputed, key=lambda x: -impact.get(x["node"], 0))[:30]:
        route = f" [route: {x['clause']}]" if x["clause"] != "standard" else ""
        sub = [f"Why: {x['why'][:300]}"]
        if x["note"]:
            sub.append(f"Critic: {x['note'][:300]}")
        item(f"**{name(x['node'])}** needs **{name(x['target'])}**{route}", sub)
    lines.append("")

    bench = open(os.path.join(ROOT, "reports", "benchmark.md")).read()
    miss = [l[2:] for l in bench.splitlines() if l.startswith("- ") and " -> " in l]
    lines += ["## E. Coherence Map links the map misses", "",
              "For each: should the map have a prerequisite path here (yes / no)?", ""]
    for m in miss:
        item(f"{m}")
    lines.append("")
    open(os.path.join(d, "REVIEW.md"), "w").write("\n".join(lines) + "\n")
    print(f"{num} items; kept {len(kept)}, disputed {len(disputed)}, dropped {len(dropped)}, undecided {len(undecided)}")


if __name__ == "__main__":
    main(sys.argv[1])
