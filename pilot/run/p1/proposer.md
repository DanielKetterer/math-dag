# Prerequisite proposer: instructions

You are one of two independent passes proposing prerequisites for math skills
("nodes") in a research map of school mathematics. Work only from this file,
your batch file (`pilot/run/p1/batches/<batch>.yaml`), and `pilot/run/p1/index.txt`
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
- **Simplest form** is its own node. List it only as a `task` edge, and only
  when the test problem asks for simplest form.
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

## Allowed targets

Your batch is one strand of the map. Every node it could need is in
`index.txt`, which lists the whole map (pre-K through grade 8 as far as it is
written, including the other strands of this run), or in the boundary list
below (referenced but not yet written; use these exact ids). Use
`new:<concept>.<short-name>` only if a genuinely needed earlier skill is
missing from both.

- A node may be a root (nothing earlier in the map is needed). Give
  `"routes": []` and a `root_reason` when that is your judgment; do not invent
  a prerequisite to avoid a root.
- Developmental or curricular order is not prerequisite order. Apply the
  counterfactual test to the node's statement and test problem: could a
  learner meet this node, at its stated level, by a credible route without the
  prerequisite?
- Some ids were retired as too broad (for example `addition.whole-number`);
  they are not in the index. Point at the specific node instead.

## Boundary list (referenced, not yet written)

| id | meaning |
|---|---|
| `area.rectangle.length-times-width` | Area of a rectangle as length times width |
| `area.rectangle.tiling` | Area of a rectangle by tiling and as length times width |
| `coordinate-plane.first-quadrant` | Plot and read points in the first quadrant |
| `coordinate-plane.four-quadrants` | Plot and read points in all four quadrants |
| `data.graphs.read` | Read values from graphs and tables |
| `division.nonunit-fraction-by-whole` | Divide a non-unit fraction by a whole number |
| `equations.linear.solve` | Solve linear equations in one variable |
| `equations.one-step` | Solve one-step equations |
| `expressions.variables` | Write and evaluate expressions with variables |
| `fraction.reciprocal` | The reciprocal of a fraction |
| `fraction.subtraction.comparison` | Subtraction of fractions as comparison (how much more) |
| `functions.definition` | A function as a rule assigning one output to each input |
| `geometry.similar-triangles` | Similar triangles and dilations |
| `measurement.unit-conversion` | Convert measurements within one system |
| `measurement.weight.attribute` | Weight as an attribute of an object, separate from its size |
| `rational-numbers.operations` | Operations with signed rational numbers |

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
