"""Benchmark the map against the Coherence Map and build curriculum pathways.

    python3 tools/benchmark.py

Writes pathways/im360.yaml and pathways/ccss-grades.yaml (checked by
tools/check.py) and reports/benchmark.md.
"""
import collections
import glob
import json
import os

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "sources", "learning-commons")


def jl(name):
    return [json.loads(line) for line in open(os.path.join(SRC, name), encoding="utf-8")]


def std4(code):
    """Standard-level code: 3.NF.A.2.a -> 3.NF.A.2."""
    return ".".join(code.split(".")[:4]) if code else code


def related_codes(a, b):
    return a == b or a.startswith(b + ".") or b.startswith(a + ".")


def main():
    nodes = {}
    for p in glob.glob(os.path.join(ROOT, "nodes", "**", "*.yaml"), recursive=True):
        n = yaml.safe_load(open(p, encoding="utf-8"))
        nodes[n["id"]] = n
    codes = {i: [str(c) for c in (n.get("sources") or {}).get("ccss", [])] for i, n in nodes.items()}
    edges = {(i, e["node"]) for i, n in nodes.items() for c in n["requires"] for e in c["all_of"]}
    out = ["# Benchmark", ""]

    # ---- Coherence Map recall at the standard level
    seed_codes = {json.loads(l)["code"] for l in open(os.path.join(ROOT, "pilot", "seed.jsonl"))}
    slice4 = {std4(c) for c in seed_codes}
    cm = {(std4(e["from"]), std4(e["to"])) for e in jl("coherence_map.jsonl")
          if e["relation"] == "buildsTowards" and std4(e["from"]) in slice4 and std4(e["to"]) in slice4
          and std4(e["from"]) != std4(e["to"])}
    ours = collections.defaultdict(set)   # standard -> standards it directly requires
    for a, b in edges:
        for ca in codes.get(a, []):
            for cb in codes.get(b, []):
                if std4(ca) != std4(cb):
                    ours[std4(ca)].add(std4(cb))
    pairs = {(b, a) for a, bs in ours.items() for b in bs}   # (from, to) like the Coherence Map

    def reach(s):
        seen, stack = set(), [s]
        while stack:
            x = stack.pop()
            for y in ours.get(x, ()):
                if y not in seen:
                    seen.add(y)
                    stack.append(y)
        return seen
    closure = {(b, a) for a in list(ours) for b in reach(a)}
    direct = cm & pairs
    trans = cm & closure
    reverse = {(f, t) for (f, t) in cm if (t, f) in pairs}
    out += ["## Coherence Map (standard level, inside the slice)", "",
            f"- Coherence Map `buildsTowards` links inside the slice: {len(cm)}",
            f"- Recovered directly by the map: {len(direct)} ({100 * len(direct) / max(1, len(cm)):.0f}%)",
            f"- Recovered through a chain of prerequisites: {len(trans)} ({100 * len(trans) / max(1, len(cm)):.0f}%)",
            f"- Pointing the opposite way in the map: {len(reverse)} {sorted(reverse)}",
            f"- Standard-level links the map has that the Coherence Map lacks: {len(pairs - cm)}", ""]
    missed = sorted(cm - closure)
    if missed:
        out.append("Coherence Map links the map does not recover, even through chains:")
        out += [f"- {f} -> {t}" for f, t in missed]
        out.append("")

    # ---- CCSS grade pathway
    grade_of = {}
    for s in jl("ccss_math_standards.jsonl"):
        if s["code"] and s["grades"]:
            grade_of[s["code"]] = min(int(g) if g.isdigit() else 0 for g in s["grades"])
    steps = collections.defaultdict(list)
    for i, cs in codes.items():
        gs = [grade_of.get(c, grade_of.get(std4(c))) for c in cs]
        gs = [g for g in gs if g is not None]
        if gs:
            steps[min(gs)].append(i)
    os.makedirs(os.path.join(ROOT, "pathways"), exist_ok=True)
    yaml.safe_dump({"name": "Common Core grade order",
                    "source": "sources/learning-commons/ccss_math_standards.jsonl",
                    "note": "Each node is placed at the earliest grade of its standards. Nodes in the same grade share a step.",
                    "steps": [{"position": g, "grade": str(g), "nodes": sorted(v)} for g, v in sorted(steps.items())],
                    # nodes below Kindergarten (no CCSS grade) are what Common Core takes as known
                    "assumes": sorted(i for i in nodes if not any(i in v for v in steps.values()))},
                   open(os.path.join(ROOT, "pathways", "ccss-grades.yaml"), "w"), sort_keys=False, width=100)

    # ---- IM 360 pathway, grades 1-8
    im = {r["id"]: r for r in jl("im360_curriculum.jsonl")}
    parent = {}
    for r in im.values():
        for c in r["children"]:
            parent[c] = r["id"]

    def key(lesson_id):
        chain, x = [], lesson_id
        while x in im:
            chain.append(im[x])
            x = parent.get(x)
        course = next((c for c in chain if c["kind"] == "Course"), None)
        g = (course or {}).get("course", "") or chain[0].get("course", "")
        g = g.split(":")[-1]
        if not g.isdigit():
            return None
        pos = [int(c["position"]) if str(c.get("position", "")).isdigit() else 0
               for c in reversed(chain) if c["kind"] != "Course"]
        return (int(g), *pos)

    lesson_keys = {}
    for r in im.values():
        if r["kind"] == "Lesson" and r["standards"]:
            k = key(r["id"])
            if k:
                lesson_keys[r["id"]] = k
    place = {}
    for i, cs in codes.items():
        ks = [lesson_keys[l] for l in lesson_keys for c in cs
              if any(related_codes(c, s) for s in im[l]["standards"])]
        if ks:
            place[i] = min(ks)
    order = sorted(set(place.values()))
    rank = {k: n + 1 for n, k in enumerate(order)}
    by = collections.defaultdict(list)
    for i, k in place.items():
        by[rank[k]].append((i, k))
    yaml.safe_dump({"name": "Illustrative Mathematics 360 (grades 1-8)",
                    "source": "sources/learning-commons/im360_curriculum.jsonl",
                    "note": "Each node is placed at the first IM lesson aligned to one of its standards.",
                    "steps": [{"position": p, "grade": str(v[0][1][0]), "lesson_key": list(v[0][1]),
                               "nodes": sorted(i for i, _ in v)} for p, v in sorted(by.items())],
                    # IM 360 here starts at grade 1: unplaced pre-K and Kindergarten nodes are assumed
                    "assumes": sorted(i for i in nodes if i not in place and
                                      min([g for g in (grade_of.get(c, grade_of.get(std4(c))) for c in codes.get(i, []))
                                           if g is not None] or [0]) == 0)},
                   open(os.path.join(ROOT, "pathways", "im360.yaml"), "w"), sort_keys=False, width=100)
    out += ["## Pathways", "",
            f"- Common Core grade order: {sum(len(v) for v in steps.values())} of {len(nodes)} nodes placed",
            f"- IM 360: {len(place)} of {len(nodes)} nodes placed at their first aligned lesson, {len(order)} distinct positions",
            "- Order findings are reported by tools/check.py.", ""]
    os.makedirs(os.path.join(ROOT, "reports"), exist_ok=True)
    open(os.path.join(ROOT, "reports", "benchmark.md"), "w").write("\n".join(out) + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    main()
