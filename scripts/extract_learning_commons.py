"""Extract the math-relevant subset of the Learning Commons Knowledge Graph export.

Input:  a directory holding nodes.jsonl and relationships.jsonl from
        https://cdn.learningcommons.org/knowledge-graph/<version>/exports/
        (see scripts/fetch_learning_commons.sh)
Output: small JSONL files under sources/learning-commons/, one record per line.

Usage:
    python3 -I scripts/extract_learning_commons.py <export_dir> <out_dir>

Everything written is CC BY 4.0 (Learning Commons, Achievement Network,
Illustrative Mathematics, Eedi) or CC0 (Student Achievement Partners).
See sources/learning-commons/ATTRIBUTION.md.
"""
import collections
import json
import os
import sys

CCSS_MATH_AUTHOR = "Common Good Learning Tools"


def jl(path):
    with open(path, encoding="utf-8") as f:
        for line in f:
            yield json.loads(line)


def parse_grades(raw):
    if not raw:
        return []
    try:
        return json.loads(raw)
    except (TypeError, ValueError):
        return [raw]


def main(src, out):
    os.makedirs(out, exist_ok=True)
    nodes_path = os.path.join(src, "nodes.jsonl")
    rels_path = os.path.join(src, "relationships.jsonl")

    # ---- pass 1: nodes we care about
    sfi = {}          # identifier -> standard record (math only, all frameworks)
    framework_of = {} # framework identifier -> name
    lc = {}
    construct = {}
    misconception = {}
    im = {}           # IM curriculum entities
    for o in jl(nodes_path):
        lab = o["labels"][0]
        p = o["properties"]
        i = o["identifier"]
        if lab == "StandardsFramework" and p.get("academicSubject") == "Mathematics":
            framework_of[i] = {"name": p.get("name"), "jurisdiction": p.get("jurisdiction"),
                               "author": p.get("author")}
        elif lab == "StandardsFrameworkItem" and p.get("academicSubject") == "Mathematics":
            sfi[i] = {
                "id": i,
                "code": p.get("statementCode"),
                "type": p.get("normalizedStatementType") or p.get("statementType"),
                "grades": parse_grades(p.get("gradeLevel")),
                "text": p.get("description"),
                "jurisdiction": p.get("jurisdiction"),
                "author": p.get("author"),
            }
        elif lab == "LearningComponent" and p.get("academicSubject") == "Mathematics":
            ex = p.get("examples")
            try:
                ex = json.loads(ex) if ex else []
            except ValueError:
                ex = [ex]
            lc[i] = {"id": i, "text": p.get("description"), "examples": ex,
                     "author": p.get("author"), "ccss": [], "state_standards": 0}
        elif lab == "Construct" and p.get("academicSubject") == "Mathematics":
            construct[i] = {"id": i, "eedi_id": p.get("publisherIdentifier"),
                            "text": p.get("description"), "misconceptions": []}
        elif lab == "Misconception" and p.get("academicSubject") == "Mathematics":
            misconception[i] = {"id": i, "eedi_id": p.get("publisherIdentifier"),
                                "text": p.get("description")}
        elif lab in ("Course", "LessonGrouping", "Lesson") and p.get("author") == "Illustrative Mathematics":
            im[i] = {"id": i, "kind": lab, "name": p.get("name"),
                     "ordinal": p.get("ordinalName"), "position": p.get("position"),
                     "course": p.get("courseCode"), "grades": parse_grades(p.get("gradeLevel")),
                     "group_level": p.get("groupLevel"), "group_name": p.get("groupName"),
                     "optional": p.get("isOptional"),
                     "children": [], "standards": [], "depends_on": []}

    # ---- pass 2: relationships
    coherence = []
    crosswalk = []
    std_parent = {}
    for o in jl(rels_path):
        lab = o["label"]
        s, t = o["source_identifier"], o["target_identifier"]
        if lab == "supports" and s in lc and t in sfi:
            if sfi[t]["author"] == CCSS_MATH_AUTHOR:
                lc[s]["ccss"].append(sfi[t]["code"])
            else:
                lc[s]["state_standards"] += 1
        elif lab in ("buildsTowards", "relatesTo") and s in sfi and t in sfi:
            coherence.append({"relation": lab, "from": sfi[s]["code"], "to": sfi[t]["code"],
                              "from_grades": sfi[s]["grades"], "to_grades": sfi[t]["grades"]})
        elif lab == "hinders" and s in misconception and t in construct:
            construct[t]["misconceptions"].append(misconception[s]["text"])
        elif lab == "hasStandardAlignment" and s in sfi and t in sfi:
            crosswalk.append({"state": sfi[s]["jurisdiction"], "state_code": sfi[s]["code"],
                              "state_grades": sfi[s]["grades"], "ccss": sfi[t]["code"],
                              "ccss_grades": sfi[t]["grades"]})
        elif lab == "hasPart" and s in im and t in im:
            im[s]["children"].append(t)
        elif lab == "hasDependency" and s in im and t in im:
            im[s]["depends_on"].append(t)
        elif lab == "hasEducationalAlignment" and s in im and t in sfi:
            if sfi[t]["author"] == CCSS_MATH_AUTHOR:
                im[s]["standards"].append(sfi[t]["code"])
        elif lab == "hasChild" and s in sfi and t in sfi:
            std_parent[t] = s

    ccss = [r for r in sfi.values() if r["author"] == CCSS_MATH_AUTHOR]
    for r in ccss:
        par = std_parent.get(r["id"])
        r["parent"] = sfi[par]["code"] if par in sfi else None

    def dump(name, rows):
        path = os.path.join(out, name)
        with open(path, "w", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(f"{name}: {len(rows)} rows, {os.path.getsize(path)/1e6:.2f} MB")

    for r in lc.values():
        r["ccss"] = sorted(set(r["ccss"]))
    for r in im.values():
        r["standards"] = sorted(set(r["standards"]))

    dump("ccss_math_standards.jsonl", sorted(ccss, key=lambda r: (r["code"] or "")))
    dump("math_learning_components.jsonl", sorted(lc.values(), key=lambda r: (r["ccss"][:1], r["text"] or "")))
    dump("coherence_map.jsonl", coherence)
    dump("eedi_constructs.jsonl", sorted(construct.values(), key=lambda r: int(r["eedi_id"] or 0)))
    dump("im360_curriculum.jsonl", list(im.values()))
    dump("state_crosswalk.jsonl", crosswalk)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
