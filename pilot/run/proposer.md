# Prerequisite proposer: instructions

You are one of two independent passes proposing prerequisites for math skills
("nodes") in a research map of school mathematics. Work only from this file,
your batch file (`pilot/run/batches/<batch>.yaml`), and `pilot/run/index.txt`
(every node in the map, one line each). **Do not read any other file.**

## Task

For each node in your batch, propose what must be known first, and exactly
why.

Each node has a level: 1 concrete, 2 representational (a model with symbols),
3 symbolic, 4 justified in general. Each node has a facet: which meaning of the
concept it uses.

## Structure

A node has one or more **routes** (alternative ways in). Any one route is
enough; every edge inside a route is required for that route.

- Give a second route only for a genuinely different way to learn **this same
  node**. A route may draw on prerequisites of any facet. But if the
  alternative would change the node's own level or meaning, it is a different
  node, not a route; do not add it.
- Different ways of carrying out the same sub-computation (recalled facts
  versus skip counting, for example) are not different routes.
- **List direct prerequisites only.** If A needs B and B needs C, A lists B,
  not C, unless A's own statement, procedure, or test problem uses C directly.
- A node with no prerequisites among the allowed targets: `"routes": []` and a
  `"root_reason"`.

## Each edge

```json
{"node": "<target id>", "relation": "definitional", "points_to": "statement", "scope": "concept", "why": "..."}
```

- `node`: an id from `index.txt`, an id from the boundary list below, or, only
  if nothing fits, `new:<concept>.<short-name>`.
- `relation`: `definitional` (the meaning uses it), `procedural` (a step
  performs it), `representational` (stated in its model or notation), or
  `justificatory` (the explanation of why uses it).
- `points_to`: `statement`, `procedure.N` (step N exists), or `assess`.
- `scope`: `concept`, or `task` when only the test problem needs it. A task
  edge must point to `assess`; a concept edge must not.
- `why`: at least 8 words, naming the specific part of this node that uses the
  prerequisite. Never use: "foundational", "builds on", "builds toward",
  "important for", "needed for", "is a prerequisite", "lays the groundwork",
  "helps with", "related to".

## Boundary list (outside the pilot; use these exact ids)

| id | meaning |
|---|---|
| `counting.objects` | Count a collection of objects (root) |
| `comparing.size.direct` | Compare two quantities by size directly: longer, more area, more objects (root) |
| `shapes.recognize` | Recognize and name basic shapes (root) |
| `comparing.whole-numbers.symbols` | Compare whole numbers and record with >, =, < |
| `addition.whole-number` | Add whole numbers, including multi-digit |
| `subtraction.whole-number` | Subtract whole numbers, including multi-digit |
| `place-value.base-ten` | Base-ten place value of whole numbers |
| `multiplication.facts.within-100` | Fluent single-digit multiplication facts |
| `multiplication.multi-digit` | Multiply multi-digit whole numbers |
| `multiplication.properties` | Commutative, associative, distributive properties |
| `multiplication.by-one` | Multiplying by 1 leaves a number unchanged |
| `multiplication.comparison` | Multiplicative comparison: "n times as many" (4.OA.A.1-2) |
| `division.multi-digit` | Divide multi-digit whole numbers, with remainders |
| `factors-multiples.whole-number` | Factors, multiples, common multiples, GCF, LCM |
| `area.rectangle.tiling` | Area of a rectangle by tiling and as length times width |
| `measurement.unit-conversion` | Convert measurements within one system |
| `decimal.operations` | Add, subtract, multiply, divide decimals |
| `coordinate-plane.first-quadrant` | Plot and read points in the first quadrant |
| `coordinate-plane.four-quadrants` | Plot and read points in all four quadrants |
| `patterns.numerical.two-rules` | Generate two numerical patterns and form ordered pairs |
| `expressions.variables` | Write and evaluate expressions with variables |
| `equations.one-step` | Solve one-step equations |
| `equations.linear.solve` | Solve linear equations in one variable |
| `rational-numbers.operations` | Operations with signed rational numbers |
| `geometry.scale-drawings` | Scale drawings and scale factor |
| `geometry.similar-triangles` | Similar triangles and dilations |
| `functions.definition` | A function as a rule assigning one output to each input |
| `data.graphs.read` | Read values from graphs and tables |

## Output

Write the JSON file at the path you were given:

```json
{"pass": "<label>", "batch": "<batch>",
 "nodes": {"<node id>": {"routes": [{"clause": "standard", "edges": [ ... ]}]},
           "<root id>": {"routes": [], "root_reason": "..."}}}
```

Include every node in your batch. A route may carry its own `"procedure"`
when its method differs from the node's. Clause names are lowercase words with
hyphens. Valid JSON only; check that it parses. Reply with one line: path and
number of edges.
