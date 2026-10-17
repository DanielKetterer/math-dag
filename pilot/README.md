# Pilot: equal sharing to slope

The first slice of the map, built end to end before anything is scaled up.
It runs from splitting a shape into equal shares (grade 1) through fractions,
ratio, and proportional relationships to slope (grade 8).

Why this slice: it contains every hard case the rules have to survive.

- **Helix.** "Fraction" is at least three nodes (part of a whole, a number on the line, a quotient).
- **The knot.** Multiplication, division, and fractions explain each other in a cycle at the concept level.
- **Real alternative routes.** Proportions by unit rate, scale factor, or cross-multiplication; fraction division by common denominators or invert-and-multiply; fractions on the number line via the part-whole picture or measure-first.
- **Rule before reason.** Invert-and-multiply is drilled years before it is justified, if it ever is.
- **Every kind of evidence.** Learning components, the Coherence Map, a full curriculum (IM 360), and misconception data.

## What the data gives us (from `tools/pilot_scope.py`)

| | Count |
|---|---|
| Common Core standards in scope | 63 (54 leaf standards, grades 1-8) |
| Learning components aligned to them | 218 |
| Coherence Map links inside the slice | 94 (70 `buildsTowards`) |
| `buildsTowards` links entering from outside | 37, from 21 standards |
| Illustrative Mathematics 360 lessons aligned | 490 |
| Eedi constructs matched by keyword | 428 (a loose pool; most will be cut) |

Every leaf standard in scope has at least one learning component.

**Boundary to decide.** The 37 entering links come mostly from addition and
subtraction (grades 1-2), the area model (3.MD.C.7.b), multiplicative comparison
(4.OA.A.1, 4.OA.A.2), and the coordinate plane (5.G.A.2). Multiplicative
comparison is the strongest candidate to pull inside, since ratio leans on it.

## Files

- `seed.jsonl`: one line per in-scope standard, with its learning components, its Coherence Map links in and out, and its IM 360 lessons.
- `eedi_seed.jsonl`: Eedi constructs and misconceptions matched by keyword.

## Plan

1. **Nodes.** Turn the 218 learning components into nodes under `RULES.md`: merge variants that differ only in number range ("dividends through 50"), assign concept, facet, and level, and write each node's statement and test problem.
2. **Prerequisites, three blind passes.** Three independent passes propose routes and edges for every node. They see the node files only, never the Coherence Map and never each other.
3. **Combine.** Edges all three passes agree on become `proposed`. Partial agreement is marked `disputed` and goes to the top of the review queue.
4. **Grade against the yardstick.** Project the edges up to standards and measure how many of the 70 Coherence Map links the map recovers, and which ones it adds.
5. **Pathways.** Encode IM 360 and the Common Core grade order in `pathways/`, and run the checker for out-of-order findings.
6. **Review.** A review page ranks edges by disagreement times how much depends on them. Daniel's calls are recorded as `review` evidence.

Success means all of the following:

- the checker passes with no unlearnable nodes
- every edge has a type and a specific why
- a measured precision from a random sample of reviewed edges
- every pathway finding explained
- the measure-first route into fractions found without being told
