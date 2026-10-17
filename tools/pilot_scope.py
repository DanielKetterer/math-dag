"""Gather the seed material for the pilot slice: equal sharing to slope.

    python3 tools/pilot_scope.py

Writes pilot/seed.jsonl (one record per in-scope standard, with its learning
components, Coherence Map links, IM lessons) and pilot/eedi_seed.jsonl, and
prints a summary used in pilot/README.md.
"""
import collections
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "sources", "learning-commons")
OUT = os.path.join(ROOT, "pilot")

# Standards in the slice, by exact code or by prefix ending in "."
SCOPE = [
    "1.G.A.3", "2.G.A.3", "3.G.A.2",            # equal shares
    "1.MD.A.2", "2.MD.B.6",                     # unit iteration, number line
    "3.OA.A.1", "3.OA.A.2", "3.OA.B.6",         # meanings of multiplication and division
    "3.NF.", "4.NF.", "5.NF.",                  # fractions
    "6.RP.", "6.NS.A.1",                        # ratio, rate, fraction division
    "7.RP.",                                    # proportional relationships
    "8.EE.B.5", "8.EE.B.6", "8.F.B.4",          # slope, rate of change
]
EEDI_WORDS = re.compile(
    r"fraction|ratio|\brate\b|proportion|slope|gradient|\bshare|partition|number line|unit fraction|divide|division",
    re.I)


def in_scope(code):
    if not code:
        return False
    for s in SCOPE:
        if s.endswith(".") and code.startswith(s):
            return True
        if code == s or code.startswith(s + "."):
            return True
    return False


def jl(name):
    with open(os.path.join(SRC, name), encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def main():
    os.makedirs(OUT, exist_ok=True)
    stds = [s for s in jl("ccss_math_standards.jsonl") if s["type"] == "Standard" and in_scope(s["code"])]
    codes = {s["code"] for s in stds}
    lcs = jl("math_learning_components.jsonl")
    coh = jl("coherence_map.jsonl")
    im = jl("im360_curriculum.jsonl")
    eedi = jl("eedi_constructs.jsonl")

    lc_by = collections.defaultdict(list)
    for r in lcs:
        for c in r["ccss"]:
            if c in codes:
                lc_by[c].append({"id": r["id"], "text": r["text"]})
    lessons_by = collections.defaultdict(list)
    for r in im:
        if r["kind"] == "Lesson":
            for c in r["standards"]:
                if c in codes:
                    lessons_by[c].append({"course": r["course"], "position": r["position"], "name": r["name"]})

    internal = [e for e in coh if e["from"] in codes and e["to"] in codes]
    entering = [e for e in coh if e["relation"] == "buildsTowards" and e["to"] in codes and e["from"] not in codes]
    with open(os.path.join(OUT, "seed.jsonl"), "w", encoding="utf-8") as f:
        for s in sorted(stds, key=lambda s: s["code"]):
            rec = {
                "code": s["code"], "grades": s["grades"], "text": s["text"],
                "learning_components": lc_by.get(s["code"], []),
                "builds_from": sorted({e["from"] for e in coh if e["relation"] == "buildsTowards" and e["to"] == s["code"]}),
                "builds_to": sorted({e["to"] for e in coh if e["relation"] == "buildsTowards" and e["from"] == s["code"]}),
                "im360_lessons": lessons_by.get(s["code"], []),
            }
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    eedi_hits = [r for r in eedi if EEDI_WORDS.search(r["text"])]
    with open(os.path.join(OUT, "eedi_seed.jsonl"), "w", encoding="utf-8") as f:
        for r in eedi_hits:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    leaf = [s for s in stds if not any(o["code"].startswith(s["code"] + ".") for o in stds)]
    lc_ids = {x["id"] for v in lc_by.values() for x in v}
    by_grade = collections.Counter(g for s in leaf for g in s["grades"])
    print(f"standards in scope: {len(stds)} ({len(leaf)} leaf standards)")
    print("leaf standards by grade:", dict(sorted(by_grade.items(), key=lambda kv: (len(kv[0]), kv[0]))))
    print(f"learning components aligned: {len(lc_ids)}")
    print(f"leaf standards with no learning component: {[s['code'] for s in leaf if not lc_by.get(s['code'])]}")
    print(f"Coherence Map links inside the slice: {len(internal)} "
          f"({sum(e['relation'] == 'buildsTowards' for e in internal)} buildsTowards)")
    print(f"buildsTowards links entering from outside the slice: {len(entering)} from "
          f"{sorted({e['from'] for e in entering})}")
    print(f"IM 360 lessons aligned: {len({(l['course'], l['position'], l['name']) for v in lessons_by.values() for l in v})}")
    print(f"Eedi constructs matched by keyword: {len(eedi_hits)}, "
          f"misconceptions attached: {sum(len(r['misconceptions']) for r in eedi_hits)}")


if __name__ == "__main__":
    main()
