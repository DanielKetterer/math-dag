# Critic pass: instructions

Work only from this file, your batch file `pilot/run/critic/in-<batch>.json`, and
`pilot/run/index.txt` (every node in the map, for naming missing
prerequisites). **Do not read any other file in the repository.** Independence
is the point.

Your batch file lists math skills ("nodes") from a research map of school
mathematics. Each node has a level (1 concrete, 2 representational with a
model, 3 symbolic, 4 justified in general), a facet (which meaning of the
concept it uses), a statement, sometimes a procedure, a test problem
(`assess`), and a list of proposed prerequisite edges. `boundary_nodes` lists
nodes outside this batch that edges may point to.

## Your task

You are reviewing prerequisite edges for a mathematical learning graph. Your
task is to determine whether each proposed edge is a genuine **direct**
prerequisite of the target node, not merely a useful teaching sequence or
conceptual association.

For each edge, read the target node's statement, procedure, assessment, level,
and facet. Identify the specific part of the target that allegedly requires the
source.

Apply a counterfactual test: could a learner who lacks the source still meet the
target **at its stated level and type** (no more, no less) by a credible
alternative route? A level 3 procedure does not require knowing why it works; a
level 4 justification does. A route is credible if a real curriculum teaches it,
research documents it, or you can sketch a coherent sequence of lessons for it.
A route at a different level is a different node, not an alternative route.
Likewise, if the alternative would change the target's own meaning (its facet),
it is a different node; a route may still draw on prerequisites of any facet.
Different ways of carrying out the same sub-computation (recalled facts versus
skip counting, for example) are not different routes; do not mark an edge
`route-only` for that reason. Do
not reject an edge merely because an alternative is imaginable.

Classify each edge as exactly one of:

- `necessary`: required, directly, by every credible route
- `route-only`: required for one route; state the other route
- `indirect`: required, but only through another prerequisite; name it. Not
  `indirect` when this node's own statement, procedure, or test problem uses
  the skill itself: then the edge is direct (`task-only` if only the test
  problem uses it), even though a chain of prerequisites also reaches it
- `task-only`: required by the test problem, not by the idea
- `scaffold`: helpful for teaching, not required
- `related`: an associated idea or alternative representation; give the relation
- `wrong`: incorrect or circular
- `undecided`: say what fact would decide it

Simplifying a fraction to lowest terms is its own node. It is a prerequisite
only as a `task-only` edge, and only when the test problem asks for simplest
form; "simplify if wanted" in a procedure does not make it one.

Do not infer necessity from shared vocabulary, from a skill appearing in an
example, or from a curriculum's ordering. Judge the relationship, not the
quality of its explanation: a fluent, specific rationale is not evidence that an
edge is true.

For every classification other than `necessary`, explain the precise failure.
Where it fits, propose an OR-clause or a `related` link rather than deletion.

After the edges, for each node: name any **missing** direct prerequisite and any
**missing** alternative route at the same level.

Preserve uncertainty. Do not force a verdict the evidence does not support.

## Output

Write valid JSON to the path you were given:

```json
{
  "edges": {
    "e1": {
      "verdict": "necessary | route-only | indirect | task-only | scaffold | related | wrong | undecided",
      "reason": "one or two sentences; required unless necessary",
      "via": "for indirect: the node it goes through",
      "other_route": "for route-only: the alternative route in a sentence",
      "relation": "for related: generalizes | specializes | same_idea_different_form | contrasts_with",
      "would_decide": "for undecided: the fact that would settle it"
    }
  },
  "nodes": {
    "<node id>": {
      "missing_prerequisites": [{"node": "<id from index.txt or boundary_nodes, or new:concept.name>", "why": "..."}],
      "missing_routes": [{"description": "...", "prerequisites": ["<id>", "..."]}]
    }
  }
}
```

Give a verdict for every edge id. Include every node under `nodes`, with empty
lists when nothing is missing. When done, reply with one line: the path you
wrote and the count of each verdict.
