# Prerequisite proposer: instructions

You are one of two independent passes proposing prerequisites for math skills
("nodes") in a research map of school mathematics. Work only from this file,
your batch file (`pilot/run/p3/batches/<batch>.yaml`), and `pilot/run/p3/index.txt`
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
- **A computation is not a method.** When a node needs a sum, difference,
  product or quotient but any method would do, point at the method-neutral
  node for that range (Find a sum within 10, Add within 100, Add within 1000,
  Multiply a whole number by a one-digit number, Divide by a one-digit number,
  the fact nodes). Point at a method (count all, partial products, the standard
  algorithm, a base-ten model) only when this node's statement, procedure or
  test problem requires that method. (Daniel's phase 1 review: 7 of 10 wrong
  edges named a method.) For signed, fraction or decimal arithmetic inside an
  algebra, geometry or statistics node, the same holds: point at the
  method-neutral operation node, not at a model or a rule's explanation.
- **Point at the weakest node that supplies what is used.** When a statement
  only names a category ("a square is a quadrilateral with ..."), point at the
  node that gives that much (naming four-sided figures), not at a stronger one
  (recognizing every quadrilateral, including concave ones). When a statement
  only needs to know which figures are squares, point at naming squares, not
  at the full definition of a square. (Daniel's phase 2 review: 5 of 13 wrong
  edges.)
- **Informal before formal.** When a node uses a concept informally (a square
  corner, "the same shape", a rate in a table), point at the informal node, not
  at the later formal one (a right angle, similarity, slope).
- **A teaching order is not a chain of prerequisites.** When this node's own
  procedure carries a skill (reading the hour hand, counting minute marks),
  the earlier, narrower node that first teaches it (the half hour, the five
  minutes) is not required; point at what the procedure actually uses.

## Boundary list (referenced, not yet written)

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
