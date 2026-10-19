"""Build writer inputs for one phase of the big run.

    python3 tools/build_phase.py pilot/run/p1

Reads the strand table below, the Learning Commons standards and learning
components, and every written node. Writes, per strand, <dir>/input/<strand>.json
(each standard with its text and the learning components no written node cites
yet), and <dir>/input/existing_ids.txt (written nodes, then referenced-but-
unwritten ids with their meaning and the strand that owns them). Prints the
component count per strand. No model calls.
"""
import collections
import glob
import json
import os
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "sources", "learning-commons")

PHASES = {
    "p1": {
        "N1": ("K-5 counting sequence and place value",
               ["K.CC.A.1", "K.CC.A.2", "K.CC.C.7", "K.NBT.A.1", "1.NBT.A.1", "1.NBT.B.2", "1.NBT.B.3",
                "1.NBT.C.5", "2.NBT.A", "2.NBT.B.8", "3.NBT.A.1", "4.NBT.A", "5.NBT.A.1", "5.NBT.A.3",
                "5.NBT.A.4"]),
        "N2": ("K-2 addition and subtraction: meanings, situations and word problems, properties, "
               "strategies and fluency within 20, the equal sign, adding and subtracting tens",
               ["K.OA.A", "1.OA", "2.OA.A", "2.OA.B", "1.NBT.C.4", "1.NBT.C.6"]),
        "N3": ("Grades 2-4 multiplication and division: meanings, properties, facts, factors, comparison, "
               "word problems, patterns",
               ["2.OA.C", "3.OA", "4.OA"]),
        "N4": ("Grades 2-5 multi-digit operations (place-value strategies and standard algorithms for all "
               "four operations), decimal operations, numerical expressions and patterns",
               ["2.NBT.B.5", "2.NBT.B.6", "2.NBT.B.7", "2.NBT.B.9", "3.NBT.A.2", "4.NBT.B.4",
                "3.NBT.A.3", "4.NBT.B.5", "4.NBT.B.6", "5.NBT.A.2", "5.NBT.B", "5.OA"]),
    },
}

# Referenced-but-unwritten ids: meaning and the strand that writes them.
RESERVED = {
    "place-value.base-ten": ("Base-ten place value of whole numbers", "N1"),
    "comparing.whole-numbers.magnitude": ("Decide which of two whole numbers is greater", "N1"),
    "comparing.whole-numbers.symbols": ("Record a whole-number comparison with >, =, <", "N1"),
    "addition.whole-number": ("Add whole numbers, including multi-digit", "N4"),
    "subtraction.whole-number": ("Subtract whole numbers, including multi-digit", "N4"),
    "multiplication.facts.within-100": ("Fluent single-digit multiplication facts", "N3"),
    "multiplication.properties": ("Commutative, associative, distributive properties", "N3"),
    "multiplication.by-one": ("Multiplying by 1 leaves a number unchanged", "N3"),
    "multiplication.comparison": ("Multiplicative comparison: n times as many (4.OA.A.1-2)", "N3"),
    "multiplication.array.rows-columns": ("An array as rows of equal columns", "N3"),
    "factors-multiples.whole-number": ("Factors, multiples, common multiples, GCF, LCM", "N3"),
    "division.by-zero.undefined": ("Division by zero is undefined", "N3"),
    "multiplication.multi-digit": ("Multiply multi-digit whole numbers", "N4"),
    "division.multi-digit": ("Divide multi-digit whole numbers, with remainders", "N4"),
    "decimal.operations": ("Add, subtract, multiply, divide decimals", "N4"),
    "patterns.numerical.two-rules": ("Generate two numerical patterns and form ordered pairs", "N4"),
    # left by the p1 retarget pass for skills a later phase writes (6.NS.B.3, 6.NS.B.4)
    "decimal.addition.algorithm": ("Add multi-digit decimals with the standard algorithm", "later"),
    "decimal.subtraction.algorithm": ("Subtract multi-digit decimals with the standard algorithm", "later"),
    "decimal.multiplication.algorithm": ("Multiply multi-digit decimals with the standard algorithm", "later"),
    "decimal.division.algorithm": ("Divide multi-digit decimals with the standard algorithm", "later"),
    "multiples.common-multiple": ("A common multiple of two whole numbers, including the least", "later"),
}


def jl(name):
    with open(os.path.join(SRC, name), encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def in_any(code, prefixes):
    return any(code == p or code.startswith(p + ".") for p in prefixes)


def written_nodes():
    out = {}
    for p in glob.glob(os.path.join(ROOT, "nodes", "**", "*.yaml"), recursive=True):
        d = yaml.safe_load(open(p, encoding="utf-8"))
        out[d["id"]] = d
    return out


def main(d):
    phase = os.path.basename(d.rstrip("/"))
    strands = PHASES[phase]
    os.makedirs(os.path.join(d, "input"), exist_ok=True)
    stds = [s for s in jl("ccss_math_standards.jsonl") if s["type"] == "Standard" and s["code"]]
    codes = {s["code"] for s in stds}
    leaf = [s for s in stds if not any(o != s["code"] and o.startswith(s["code"] + ".") for o in codes)]
    lcs = jl("math_learning_components.jsonl")
    nodes = written_nodes()
    cited = collections.defaultdict(list)
    for nid, n in nodes.items():
        for lc in (n.get("sources") or {}).get("learning_components") or []:
            cited[str(lc)].append(nid)
    by_std = collections.defaultdict(list)
    for r in lcs:
        for c in r["ccss"]:
            by_std[c].append(r)
    owner = {}
    for sid, (_, prefixes) in strands.items():
        recs, n_lc = [], 0
        for s in sorted(leaf, key=lambda s: s["code"]):
            if not in_any(s["code"], prefixes):
                continue
            if s["code"] in owner:
                sys.exit(f"{s['code']} in two strands: {owner[s['code']]} and {sid}")
            owner[s["code"]] = sid
            todo, done = [], []
            for r in by_std.get(s["code"], []):
                lid = r["id"][:8]
                if cited.get(lid) or cited.get(r["id"]):
                    done.append({"lc": lid, "text": r["text"], "cited_by": cited.get(lid) or cited.get(r["id"])})
                else:
                    todo.append({"lc": lid, "text": r["text"]})
            if not todo:
                continue
            n_lc += len(todo)
            rec = {"code": s["code"], "grades": s.get("grades"), "text": s["text"], "learning_components": todo}
            if done:
                rec["already_cited"] = done
            recs.append(rec)
        json.dump(recs, open(os.path.join(d, "input", f"{sid}.json"), "w"), indent=1)
        print(f"{sid}: {len(recs)} standards, {n_lc} learning components")
    referenced = collections.Counter()
    for n in nodes.values():
        for c in n.get("requires") or []:
            for e in c["all_of"]:
                if e["node"] not in nodes:
                    referenced[e["node"]] += 1
    lines = ["# Written nodes (do not duplicate; list a component under covered_by instead)"]
    for nid in sorted(nodes):
        n = nodes[nid]
        lines.append(f"{nid}  |  L{n['level']} {n['type']}  |  {n['name']}")
    lines += ["", "# Reserved ids: referenced by written nodes, not yet written. The owning strand writes",
              "# them; reuse the id exactly if one node fits its meaning, or retire it (see writer.md)."]
    for rid in sorted(set(RESERVED) | set(referenced)):
        mean, own = RESERVED.get(rid, ("(later phase)", "later"))
        lines.append(f"{rid}  |  owner {own}  |  referenced {referenced.get(rid, 0)} times  |  {mean}")
    open(os.path.join(d, "input", "existing_ids.txt"), "w").write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main(sys.argv[1])
