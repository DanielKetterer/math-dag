# Prerequisite proposer: instructions

You are one of two independent passes proposing prerequisites for math skills
("nodes") in a research map of school mathematics. Work only from this file,
your batch file (`pilot/run/prek/batches/prek.yaml`), and `pilot/run/prek/index.txt`
(every node in this layer, one line each). **Do not read any other file.**

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

## Allowed targets (pre-K layer)

This batch is the floor of the map: what children learn before Kindergarten,
plus the Kindergarten nodes from splitting `counting.objects`. Every node it
could need is in `index.txt`; nodes in later grades cannot be prerequisites of
this layer. Use an id from `index.txt`, or `new:<concept>.<short-name>` only if
a genuinely needed earlier skill is missing.

Notes for this layer:

- Several nodes are expected roots (things a child can do with nothing earlier
  in the map). Give `"routes": []` and a `root_reason` when that is your
  judgment; do not invent a prerequisite to avoid a root.
- Developmental order is not prerequisite order. That children usually learn
  A before B does not make A a prerequisite of B; apply the counterfactual test
  to the node's statement and test problem.

| id | meaning |
|---|---|

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
