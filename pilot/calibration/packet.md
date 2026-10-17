# Prerequisite pass: instructions

You are one of several independent passes proposing prerequisites for 20
math skills ("nodes") in a research map of school mathematics. Other passes
are doing the same task without seeing your work. Work only from this file and
`pilot/calibration/nodes.yaml`.

**Do not read any other file in the repository.** In particular, do not read
`sources/`, `pilot/seed.jsonl`, `nodes/`, `RULES.md`, or anything in
`pilot/calibration/passes/`. Independence is the point of the exercise.

## The task

For each of the 20 nodes in `nodes.yaml`, propose what must be known first,
and exactly why.

## How prerequisites are structured

A node has one or more **routes** (alternative ways in). Any one route is
enough. Every edge inside a route is required for that route.

- Most nodes have one route. Give a second route only when there is a
  genuinely different way to learn the node at the **same level** of
  formality. A more concrete or more formal version of a node is a different
  node, not a route.
- A node with no prerequisites among the allowed targets is a root: set
  `"routes": []` and explain in `"root_reason"`.

**List direct prerequisites only.** If A needs B and B needs C, A lists B, not
C, unless A's own statement, procedure, or test problem uses C directly.

## Each edge

```json
{
  "node": "fraction.unit.part-whole",
  "relation": "definitional",
  "points_to": "statement",
  "scope": "concept",
  "why": "..."
}
```

- `node`: the prerequisite. Allowed targets:
  - any of the 20 node ids in `nodes.yaml`;
  - any id in the **boundary list** below;
  - if nothing fits, a new id written as `new:<concept>.<short-name>`, for example
    `new:fraction.unit.area-model`. Use these sparingly.
- `relation`, one of:
  - `definitional`: the meaning of this node uses the other;
  - `procedural`: a step of this node's procedure performs the other;
  - `representational`: this node is stated in the other's model or notation;
  - `justificatory`: the explanation of why this node holds uses the other.
- `points_to`: the part of **this** node that needs the prerequisite:
  `statement`, `procedure.N` (step N of the node's procedure, or of the
  route's own procedure if you give one), or `assess`.
- `scope`: `concept` (the idea needs it) or `task` (only the test problem
  needs it). A `task` edge must point to `assess`, and a `concept` edge must
  not point to `assess`.
- `why`: at least 8 words, naming the specific part of this node that uses the
  prerequisite. These phrases are rejected: "foundational", "builds on",
  "builds toward", "important for", "needed for", "is a prerequisite",
  "lays the groundwork", "helps with", "related to".

A route may carry its own `"procedure"` (a list of steps) when its method
differs from the node's.

## Boundary list (nodes outside this batch you may point to)

| id | meaning |
|---|---|
| `counting.objects` | Count a collection of objects (K) |
| `comparing.area.direct` | Judge whether two regions cover the same amount, by sight or by moving one onto the other |
| `comparing.whole-numbers.symbols` | Compare two whole numbers and record with >, =, < (grade 1) |
| `partitioning.equal-shares.area` | Partition a circle or rectangle into equal shares (grades 1-2) |
| `partitioning.equal-parts.length` | Partition a length or interval into equal parts |
| `measurement.length.unit-iteration` | Measure a length by laying a unit end to end |
| `number-line.whole-number-lengths` | Whole numbers as lengths from 0 on a number line (grade 2) |
| `multiplication.equal-groups` | Multiplication as the total in n equal groups (3.OA.A.1) |
| `multiplication.facts.within-100` | Fluent multiplication facts within 100 (3.OA.C.7) |
| `multiplication.by-one` | Multiplying a number by 1 leaves it unchanged |
| `division.partitive` | Division as the size of each share in equal sharing (3.OA.A.2) |
| `division.measurement.whole-number` | Division as how many groups of a given size fit (3.OA.A.2) |

## Output

Write one JSON file to the path you were given, shaped like this, with an
entry for every one of the 20 nodes:

```json
{
  "pass": "<your pass label>",
  "nodes": {
    "fraction.non-unit.part-whole": {
      "routes": [
        {"clause": "standard", "edges": [ {edge}, {edge} ]}
      ]
    },
    "some.root.node": {"routes": [], "root_reason": "..."}
  }
}
```

Clause names are short lowercase words with hyphens. Valid JSON only. When
done, reply with one line: the path you wrote and the number of edges.
