# Handoff: state after the pilot review (2026-10-17)

Read this first in a new session. Then RULES.md, pilot/run/REVIEW.md, and
pilot/run/review-daniel.md.

## Measured

- Precision of kept edges (Daniel, random sample of 40): 36/40 = 90%,
  95% interval about 77-96%. Item 8 also fails on inspection (the node says
  "if wanted"; the test problem does not ask for simplest form), so 35/40.
- Critic drops (20 highest-impact): 19/20 upheld. The critic is trustworthy
  at removing edges.
- The 4-5 wrong kept edges are all over-specification on model, justification,
  and application nodes; none point the wrong direction.

## Fix before the next run (in order)

1. **Structural bug in tools/merge_run.py.** Route-only edges were left inside
   the AND clause unless a proposer had put them in a second route. 104 such
   edges sit in AND clauses across 70 nodes, so those nodes require every
   alternative at once. Fix: group route-only edges into OR clauses (each
   alternative route = the necessary edges + that route's edges). Daniel's
   section D answers give the intended groupings for the top 30.
2. **Missing nodes the review exposed:**
   - partitioning.segment.equal-lengths (items 44, 76, 77)
   - fraction.compare.to-one: compare a fraction with 1 by numerator versus
     denominator (item 40; the scaling principle needs this, not the benchmark
     procedure)
   - fraction.complex-fraction (item 68)
   - boundary nodes multiplication.facts.within-100 is used; add
     division.facts.within-100 so single-digit division stops pointing at
     division.multi-digit (items 64, 67; also fraction.mixed-number.multiplication)
   - rational-number.negative-rate or similar (item 71)
3. **Rule to add to RULES.md:** simplifying to lowest terms is its own node and
   enters only as a task edge when the test problem asks for simplest form
   (items 8, 65).
4. **Critic instruction:** the "direct only" exception applies to test problems
   too. If the test problem itself uses a skill, a task edge is correct even
   when the skill is reachable through a chain (item 51).
5. **Benchmark wording:** section E asked "should there be a prerequisite path".
   Answer with the counterfactual test, not "supports". Items 104, 110 are real
   prerequisites; 107 and 111 are route-only (unit-fraction division feeds the
   model route into fraction division; proportional relationships are one route
   into 8.EE.B.6, similar triangles the other); 106 holds because of the
   benchmark reasonableness check, so it is a task-scope link.

## Open decision: where the map's floor is

Decision 4 set the roots as counting objects, comparing quantities by size,
and recognizing shapes. Under the one-meaning-per-node rule, counting.objects
splits into one-to-one correspondence, cardinality, and the successor idea
(K.CC.B.4.a-c), and comparing splits into attribute comparison, comparing
groups by matching, and comparing groups by counting. The true roots would
then be the rote number sequence, one-to-one matching, judging bigger or
smaller by sight, and recognizing shape categories. Daniel decided: floor at 
what Kindergarten assumes.

## Pre-K floor: research done, vetting closed (2026-10-17, second session)

- Sources extracted into `sources/prek/`: `elof.yaml` (Head Start ELOF,
  primary), `clements_sarama.yaml` (Building Blocks developmental levels, the
  authors' own document; five key levels spot-checked against [LT]2),
  `counting_principles.yaml` (principles plus knower/successor findings; four
  findings are from memory and marked so).
- Daniel added `sources/LT2.pdf` ([LT]2 site export, newest and fullest; first
  reference for level descriptions), `sources/Learning_trajectories_math.pdf`
  (the Building Blocks document the yaml came from), and the 2004 Clements and
  Sarama theory paper.
- Decisions, all closed (see `sources/prek/VETTING.md` section 5): floor at the
  preschool band; one `prek` strand; patterning out; split counting.objects in
  the same pass.
- Before the writer unit runs: give `writer.md` a short pre-K variant that cites
  `sources.prek` ids instead of `lc` ids and points at LT2.pdf for level
  descriptions. Get Daniel's go-ahead on cost first (estimate 150-300k subagent
  tokens for the writer).
- Edges touching the successor node wait until the successor-direction dispute
  (VETTING.md section 2, item 3) is read.
- `schema/node.schema.json` accepts `sources.prek: [...]`.

## Running a run: manifest and run_state

`pilot/run/manifest.yaml` lists every unit (one strand through one stage).
`python3 tools/run_state.py` prints status, the running subagent-token total,
and what can run next; it flags partial outputs to resume rather than restart.
Mark a unit done only through `--mark UNIT done --tokens N --commit SHA`, which
refuses unless the unit's validator passes and its dependencies are done.
Commit and push after every unit. Running total so far: 0 subagent tokens.

## Explorer

`tools/build_explorer.py` rebuilds `explorer/index.html` from `nodes/`. Rebuild after every
merge. A private published copy lives at https://claude.ai/artifact/Q7RWducGX1KtkuZeSAu6Vq;
to update it from a new chat, publish the rebuilt fragment with that URL.

## Then

Apply Daniel's verdicts, rerun merge and checker, and either extend the slice or
start the next one. The 34 unwritten boundary nodes (whole-number addition and
subtraction, expressions with variables, multiplication facts) are the natural
next slice.
