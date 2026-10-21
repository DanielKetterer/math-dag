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
    "p2": {
        "M1": ("K-2 measurement and data: attributes, length units and tools, estimating length, time, money, "
               "picture and bar graphs, line plots of lengths",
               ["K.MD", "1.MD", "2.MD"]),
        "M2": ("Grade 3 measurement and data: time intervals, liquid volume and mass, scaled graphs, line plots, "
               "area (unit squares, tiling, length times width, decomposing), perimeter",
               ["3.MD"]),
        "M3": ("Grades 4-5 measurement and data: unit conversion, area and perimeter formulas, line plots with "
               "fractions, angles and protractors, volume (unit cubes, length times width times height)",
               ["4.MD", "5.MD"]),
        "G1": ("K-2 geometry: naming, describing, analyzing, comparing and composing shapes; attributes; "
               "partitioning rectangles into rows and columns",
               ["K.G", "1.G", "2.G"]),
        "G2": ("Grades 3-5 geometry: categories of shapes and their attributes, lines, rays, angles, "
               "perpendicular and parallel, symmetry, the first-quadrant coordinate plane, classifying 2D figures",
               ["3.G", "4.G", "5.G"]),
    },
    "p3": {
        "Q1": ("Grades 6-8 number system: dividing fractions, multi-digit and decimal algorithms, factors and "
               "multiples, negative numbers and absolute value, the four-quadrant coordinate plane, operations "
               "with rational numbers, irrational numbers",
               ["6.NS", "7.NS", "8.NS"]),
        "E1": ("Grades 6-7 expressions and equations: exponents, variables and expressions, equivalent "
               "expressions, one-variable equations and inequalities, two-step equations, rewriting expressions",
               ["6.EE", "7.EE"]),
        "E2": ("Grade 8 expressions, equations and functions: integer exponents, roots, scientific notation, "
               "proportional relationships and slope, linear equations and systems, functions",
               ["8.EE", "8.F"]),
        "G3": ("Grades 6-7 geometry: area of triangles and polygons, volume with fractional edges, nets and "
               "surface area, scale drawings, constructing triangles, cross sections, circles, angle "
               "relationships, area, surface area and volume problems",
               ["6.G", "7.G"]),
        "G4": ("Grade 8 geometry: rigid motions, congruence, dilations and similarity, angle facts for "
               "triangles and parallel lines, the Pythagorean theorem and its converse, volume of cylinders, "
               "cones and spheres",
               ["8.G"]),
        "S1": ("Grades 6-8 statistics and probability: statistical questions, distributions, center and "
               "spread, data displays, sampling and inference, comparing populations, probability and "
               "simulation, scatter plots, bivariate data and two-way tables",
               ["6.SP", "7.SP", "8.SP"]),
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
    # phase 2 owners
    "area.rectangle.tiling": ("Area of a rectangle by tiling with unit squares", "M2"),
    "area.rectangle.length-times-width": ("Area of a rectangle as length times width", "M2"),
    "measurement.unit-conversion": ("Convert measurements within one system", "M3"),
    "measurement.weight.attribute": ("Weight as an attribute of an object, separate from its size", "M1"),
    "data.graphs.read": ("Read values from graphs and tables", "M1"),
    "coordinate-plane.first-quadrant": ("Plot and read points in the first quadrant", "G2"),
    # left by the p1 retarget pass for skills phase 3 writes (6.NS.B.3, 6.NS.B.4)
    "decimal.addition.algorithm": ("Add multi-digit decimals with the standard algorithm", "Q1"),
    "decimal.subtraction.algorithm": ("Subtract multi-digit decimals with the standard algorithm", "Q1"),
    "decimal.multiplication.algorithm": ("Multiply multi-digit decimals with the standard algorithm", "Q1"),
    "decimal.division.algorithm": ("Divide multi-digit decimals with the standard algorithm", "Q1"),
    "multiples.common-multiple": ("A common multiple of two whole numbers, including the least", "Q1"),
    # phase 3 owners (2026-10-20): grades 6-8 ids referenced by written nodes
    "coordinate-plane.four-quadrants": ("Plot and read points in all four quadrants", "Q1"),
    "fraction.reciprocal": ("The reciprocal of a fraction; a number times its reciprocal is 1", "Q1"),
    "rational-numbers.operations": ("Add, subtract, multiply and divide rational numbers (signed)", "Q1"),
    "division.nonunit-fraction-by-whole": ("Divide a non-unit fraction by a whole number", "Q1"),
    "expressions.variables": ("A letter stands for a number; write and evaluate expressions with variables", "E1"),
    "equations.one-step": ("Solve one-step equations x + p = q and px = q", "E1"),
    "equations.linear.solve": ("Solve linear equations in one variable, two-step and multi-step", "E2"),
    "functions.definition": ("A function assigns to each input exactly one output", "E2"),
    "geometry.similar-triangles": ("Similar triangles: corresponding sides are proportional", "G4"),
    # written inline by Claude in this run's F1 and F2 skeletons (owner = the skeleton) (Daniel's phase 2 review and K-5 orphans)
    "shapes.square-corner": ("A square corner, informally (the corner of a sheet of paper)", "F2"),
    "area.attribute": ("Area as the amount of flat surface a figure covers", "F2"),
    "shapes.name.prototype.rectangle-hexagon": ("Name typical rectangles and hexagons", "F2"),
    "measurement.liquid-volume.liter-unit": ("The liter as a unit of liquid volume", "F2"),
    "measurement.mass.gram-kilogram-unit": ("The gram and the kilogram as units of mass", "F2"),
    "measurement.weight.ounces-pounds.measure": ("Measure weight in ounces and pounds", "F2"),
    "shapes.rectangle.opposite-sides-equal": ("Opposite sides of a rectangle are equal", "F2"),
    "counting.skip.twenty-fives": ("Skip count by 25s", "F1"),
    "division.by-two-digit": ("Divide by a two-digit number, no remainder, by any method", "F1"),
    "division.by-two-digit.remainder": ("Divide by a two-digit number with a remainder, by any method", "F1"),
    "volume.space-occupied": ("Volume as the space a solid occupies", "F2"),
    "data.table-graph.read-values": ("Read values from a table or graph", "F1"),
    "addition.multi-digit": ("Add multi-digit whole numbers, by any method", "F1"),
    "operations.application.reasonableness.multi-digit": ("Judge a multistep answer reasonable by estimating", "F1"),
    "measurement.length.whole-plus-fraction": ("A length of whole units plus a fraction of a unit", "F2"),
    "time.hour.sixty-minutes": ("An hour is 60 minutes", "F1"),
    "division.standard-algorithm.long-division": ("Divide multi-digit numbers with the standard algorithm", "Q1"),
    "coordinate.ordered-pair.notation": ("An ordered pair (a, b): first number, then second; order matters", "F1"),
    "counting.skip.twos": ("Skip count by 2s", "F1"),
    "counting.number-word.thousand": ("The number word one thousand, after nine hundred ninety-nine", "F1"),
    "counting.number-word.thousand-million": ("The period names thousand and million", "F1"),
    "division.remainder.meaning": ("A remainder is what is left after as many whole groups as possible", "F1"),
    "division.successive-division": ("Dividing by a and then by b is dividing by a x b", "F1"),
    "fraction.subtraction.comparison": ("Subtraction as comparison of two fractional amounts (how much more)", "F1"),
    "number.halfway-between": ("The number halfway between two numbers", "F1"),
    "parallel.perpendicular-to-same-line": ("Two lines perpendicular to the same line are parallel", "F2"),
    "time.parts-of-day": ("The parts of a day in order: morning, afternoon, evening, night", "F1"),
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
