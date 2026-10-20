# Handoff: big run phase 1 complete, awaiting Daniel's review (2026-10-20)

Read this first in a new session. Then RULES.md.

## Phase 1 (K-5 number and operations): done

- 4 strands (pilot/run/p1): N1 counting and place value (42 nodes), N2 K-2
  addition and subtraction (56 -> 54 after 2 range merges into N4), N3
  multiplication and division (47), N4 multi-digit, decimals, expressions,
  patterns (53). 196 new nodes; map now 450 nodes, 1,556 edges, 0 errors.
- Pipeline: tools/build_phase.py (inputs), writers (Opus, pilot/run/p1/writer.md),
  tools/prepare_phase.py (id and concept checks, batches, index, packets),
  2 Sonnet proposers per strand, 1 blinded Sonnet critic per strand, then
  `sh tools/rebuild.sh` (every merge in order, then retarget, then check),
  tools/benchmark.py (also rebuilds pathways/), tools/build_explorer.py,
  tools/review_queue.py.
- 8 broad ids retired (addition.whole-number, subtraction.whole-number,
  place-value.base-ten, multiplication.properties, multiplication.multi-digit,
  division.multi-digit, decimal.operations, factors-multiples.whole-number);
  pilot/run/p1/retired.json. 67 old edges re-pointed by one Sonnet agent
  (tools/retarget.py, out.json); 10 symbolic decimal edges moved by Claude to
  later-phase ids decimal.*.algorithm (6.NS.B.3); 9 fraction edges held at
  multiples.common-multiple (6.NS.B.4). retarget apply MUST run after every
  merge_run; rebuild.sh does it.
- Passes agree on 68% of edges (Jaccard 0.68). Critic: 475 necessary,
  88 scaffold, 75 route-only, 38 task-only, 2 wrong.
- Benchmark unchanged (81% direct, 90% chains): the Coherence slice is the
  pilot slice. Pathway findings: Common Core order 17, IM 52 (new; see queue F).
- Cost: writers 444,590; proposers 1,053,645; retarget 105,649; critics
  662,108 (N4 is an ESTIMATE of 160k: the agent wrote a complete file, then
  hit a session rate limit before reporting usage). Phase 1 total 2,265,992;
  running total 3,075,943 subagent tokens. Estimate was 2.4M for phase 1 alone
  (the estimate excluded retarget).
- Review queue: pilot/run/p1/REVIEW.md, 100 items (A 40 sample, B drops,
  C 4 questions, D disputed, E benchmark, F structural findings with Claude's
  proposals). Answers go to pilot/run/p1/overrides.yaml.

Open for the next slice:
- Range-merge rule (queue F): a range changes the mathematics exactly when it
  changes the prerequisite set. Splits pending Daniel.
- Proposers found two missing nodes: decimal.thousandths.notation (5.NBT.A.3)
  and division.standard-algorithm.long-division (6.NS.B.2).
- The rate limit stopped 2 critics mid-run: run at most ~6 agents at a time.
- Phases 2 (K-5 measurement, data, geometry) and 3 (6-8) not started.

# Earlier: state after the fixes-run review (2026-10-19, second session)

The reviews themselves are in
pilot/run/review-daniel.md (pilot, K-8) and pilot/run/prek/REVIEW_ANSWERS.txt
(pre-K); both are now encoded in `overrides.yaml` files (see below).

## This session (2026-10-19, second): fixes review applied

- Daniel's answers (pilot/run/fixes/Daniels_review.txt) are in
  pilot/run/fixes/overrides.yaml. Precision sample: 7/9 kept edges right (A7
  wrong; A8 right only as a route, now related/common_path). Both critic drops
  upheld. Section C was handed to Claude: C12 split the boundary node
  comparing.whole-numbers.symbols (every magnitude use, 10 edges in pilot and
  fixes, now points at comparing.whole-numbers.magnitude; only
  fraction.compare.record-symbols and multiplication.scaling.compare-without-computing
  keep .symbols); C13 dropped the negative-meaning edge (negatives enter at
  6.NS.C.5 through opposite-quantity contexts, this node is one of them).
- fraction.compare.to-one now has two complete routes (1 = b/b with
  same-denominator comparison; a copies of 1/b). The passes had split the first
  into two half-routes.
- Section E (pilot): E106 task edges, E107 and E111 routes applied; E104 needs
  no edge (fraction.unit.part-whole carries both standards); E110 not applied.
- merge_run: superset routes are now absorbed at merge time for every node
  (A or A&B = A), extras to related/common_path. New override `set_routes`
  (reviewer states a node's whole route list; `id:task` for task scope). Route
  `add` entries may be task-scoped. Critic files that declare
  `route_semantics: complete` build each critic route from its listed
  prerequisites plus the critic's necessary edges; the critic template now asks
  for complete routes, one per alternative. Old runs keep the old reading.
- Checker: 254 nodes, 861 edges, 0 errors, findings 15 -> 8 (all 7 superset
  routes gone). Benchmark: 81% of Coherence links direct, 90% through chains.
- Subagent tokens this session: 0. Running total unchanged: 809,951.

Open for Daniel:
1. Cycle comparing.more-than / count.matching / count.by-counting (queue items
   19, 20, unanswered). Claude's position: the matching node's own test (5 cups
   in a tight row, 6 saucers in a longer row) does not pit number against size,
   so its 'has more' does not need comparing.more-than; the D53/D54 edge was set
   before comparing.more-than existed. Proposed: drop matching -> more-than (and
   by-counting's via-matching route then stands on its own). Clements-Sarama
   places the matching comparer first, which the current edge contradicts. Also
   comparing.more-than is sourced to cs.compare.perceptual; the number-over-size
   level is the counting comparer for different sizes.
2. E110 (7.RP.A.2 -> 7.RP.A.3): no 7.RP.A.3 node uses a proportional-relationship
   node in its statement, procedure, or test; name the node and step or call it
   not a prerequisite.
3. cardinality.conservation by-small-equal route: the test uses rows of 6, past
   the small-set range; applied as Daniel said (D28), but probably wrong.
4. New roots by review: shapes.closed-boundary, shapes.name.receptive,
   rational-number.negative-as-decrease.
5. The 4 old superset routes resolved by absorption lost real alternative
   methods (mixed numbers by converting to fractions; unlike-denominator
   comparison by same numerator). They sit in related as common_path; the old
   critic files listed only extras, so the true routes were never written down.

## Measured (first session)

- Pilot (K-8) precision of kept edges, Daniel's random sample of 40: 35/40
  (about 77-96%). Critic drops: 19/20 upheld.
- Pre-K precision, Daniel's random sample of 40: 32/40 = 80% (about 65-90%).
  Critic drops: 7/7 upheld. The 8 wrong edges are over-specification again
  (A7, A9, A15, A32 dropped; A17, A34 moved to related; A25, A39 pointed at
  receptive shape names). Seven of Daniel's first-draft rejections (A3, A10,
  A14, A16, A29, A31, A35) were reversed after discussion, and A38 was kept as
  required; the reasons are in the overrides file.
- Coherence Map benchmark unchanged by the review: 75% of links recovered
  directly, 85% through chains, the same 8 misses.
- Checker: 242 nodes, 852 edges, 0 errors, 40 unwritten nodes referenced.
  Clements-Sarama findings fell from 4 to 1 (the side-counting refutations
  are resolved: shapes.recognize now has a visual route).

## How review verdicts are applied (new)

`<run>/overrides.yaml` holds every human verdict as (item, node, target,
action, reason). `tools/merge_run.py` applies it after the critic, so a rerun
never loses a review. Actions: keep, drop, task, related, require, replace,
restore, uphold; plus extra routes (copy of the first route minus `without`,
plus `add`) and id renames. After applying, any route that needs everything
another route needs, and more, is removed and its extra edges move to
`related` as `common_path` (Daniel's decision, RULES 3.5). This cleanup runs
only on nodes whose structure the review changed. Every change is logged in
`<run>/review_applied.md`. To change a verdict, edit overrides.yaml and rerun
`python3 tools/merge_run.py pilot/run` and `... pilot/run/prek`.

Decisions taken this session (Daniel, 2026-10-19):
- `related` gains relation `common_path`: a common way in that is not
  required. Edges whose only alternative is not a node ("varied examples",
  "exploring") go there, as do edges on a superset route.
- shapes.closed-boundary is required on every route of shapes.recognize.
- counting.cardinal.last-word means the cardinal principle; its edge to the
  small number words stays required.
- Order irrelevance and number conservation are to be split (A35).
- Receptive shape names are a node (shapes.name.receptive).
- Ids renamed into existing concepts: quantity.more-than -> comparing.more-than,
  graphomotor.digit-formation -> numeral.digit-formation; number.word.zero is
  replaced by counting.number-words.vocabulary (zero to nine as words).

Flagged for Daniel (applied, confirm or reverse in overrides.yaml):
- D71: turn-flip on shapes.compare.same-different made a task edge (the test
  credits only overlaying), rather than moved to related.
- handoff-2: fraction.mixed-number.multiplication now needs
  division.facts.within-100, not division.multi-digit (from the earlier
  handoff, not from a review item).
- ratio.composed-unit is now a root (C66 dropped its only edge). A grade 6 root
  is suspicious; it probably needs some whole-number prerequisite.
- New pre-K roots by review: cardinality.small-number-words,
  spatial.motion.turn-flip, classifying.sort.given-attribute.
- A23 range gap: small number words cover one to three, subitizing names sets
  to five. Left with a scope note.

## Done this session

1. Route-grouping fix (#1 of the old list) applied: pilot nodes regenerated;
   70 nodes regrouped, no edge sets changed by the fix itself.
2. Both reviews applied through overrides.yaml.
3. RULES.md: simplest-form rule; direct-only exception covers test problems;
   common_path. Same rules added to proposer.md and critic.md (both copies).
4. tools/review_queue.py: counterfactual wording for section E, run-scoped
   title and section E, real counts, skips pairs already ruled on, samples
   fewer than 40 when fewer unreviewed edges remain.
5. tools/check.py: new finding "superset route".

## Fixes run (2026-10-19): reviewed and applied (see top)

- 12 new nodes (pilot/run/fixes/batches/fixes.yaml), written inline;
  two Sonnet proposers and a blinded Sonnet critic; merged. Checker: 254
  nodes, 0 errors. Queue: pilot/run/fixes/REVIEW.md (29 items).
- Cost: P 98,236; Q 93,950; critic 98,545; total 290,731 subagent tokens,
  well over the 110-170k estimate. Each agent costs about 95k whatever the
  batch size (reading the prompt and the 254-line index dominates), so a
  12-node batch is the least efficient size. Fold future fix-ups into the
  next real slice instead of running them alone.
- Rewritten in place (own batches): ratio.composed-unit test (no notation)
  plus review edges to counting.unitize and counting.objects;
  counting.cardinal.last-word test ('give me seven' after counting);
  counting.cardinal.order-irrelevance narrowed to order (conservation split
  out as cardinality.conservation); fraction.multiply-whole.symbolic scoped to
  products within 100.
- Raise with Daniel first:
  1. Cycle: both passes made comparing.more-than require comparing by counting
     and by matching, which his review made require comparing.more-than (D53,
     D54). The meaning of 'more' cannot be grounded in methods that presuppose
     it; likely wrong edges (queue items 19, 20), which would leave
     comparing.more-than a root.
  2. Critic routes misread: for comparing.more-than the critic asked for an OR
     of counting and matching, which the passes already gave, but merge_run
     built an AND of both (a superset route). For fraction.compare.to-one,
     critic-route-1 duplicates unit-fraction-count. Same merge_run flaw as the
     4 older superset routes: critic missing_routes are read as AND.
  3. shapes.name.receptive requires shapes.match (critic: necessary), though
     A17 moved matching out of shapes.recognize. IM 360 places division facts
     before the unknown-factor meaning, which refutes that edge or shows a
     missing route (fact recall from multiplication facts alone).
  4. rational-number.negative-as-decrease points at an unwritten
     new:rational-number.negative-meaning (undecided).
- Queue item 29 (7.RP.A.1 -> 7.RP.A.2) was already answered as pilot item 109.
- Running total: 809,951 subagent tokens.

## Still open

- Superset routes and section E: done (see top), except E110.
- The 13 K-8 nodes pointing at counting.objects may want the split nodes.
- The 34-node boundary slice (whole-number addition and subtraction,
  expressions with variables, multiplication facts) is the next slice after
  step 2.

## Running a run: manifest and run_state

`pilot/run/manifest.yaml` lists every unit (one strand through one stage).
`python3 tools/run_state.py` prints status, the running subagent-token total,
and what can run next. Mark a unit done only through
`--mark UNIT done --tokens N --commit SHA`. Commit and push after every unit.
Running total: 809,951 subagent tokens (after the fixes run).

## Explorer

`tools/build_explorer.py` rebuilds `explorer/index.html` (and docs/) from
`nodes/`. Rebuilt 2026-10-19. A private published copy lives at
https://claude.ai/artifact/Q7RWducGX1KtkuZeSAu6Vq and was NOT refreshed this
session; to update it, publish the rebuilt page with that URL.

## Big run: proposed plan (2026-10-19, awaiting Daniel's go-ahead)

Scope measured from the Learning Commons data: 212 K-8 content standards not yet
covered (practice standards MP1-8 excluded), with 765 learning components. The
pilot turned 218 components into 190 nodes (0.87 per component), so expect
about 650 new nodes. Most of the 31 unwritten boundary ids fall inside it.

Strands of 40-60 nodes (components in brackets):
1. K-2 counting and place value: K.CC rest, K.NBT, 1.NBT, 2.NBT [67]
2. K-2 addition and subtraction: K.OA, 1.OA, 2.OA [46]
3. 3-5 multiplication and division: 3.OA, 4.OA, 5.OA, 3.NBT [73]
4. 4-5 multi-digit and decimals: 4.NBT, 5.NBT [63]
5. K-2 measurement, data, geometry: 1.MD, 2.MD, K-2.G [62]
6. 3-5 measurement and data: 3.MD, 4.MD, 5.MD [97, two strands]
7. 3-5 geometry: 3.G, 4.G, 5.G [40]
8. 6-8 number system: 6.NS, 7.NS, 8.NS [65]
9. 6-8 expressions, equations, functions: 6.EE, 7.EE, 8.EE, 8.F [99, two strands]
10. 6-8 geometry: 6.G, 7.G, 8.G [94, two strands]
11. 6-8 statistics and probability: 6.SP, 7.SP, 8.SP [59]

Order within a phase: all writers first, then a script pass (id clashes, merge
candidates, reserved boundary ids, one compact index of every node), then both
proposer passes and the critic with the full index. Splitting a coarse boundary
id (addition.whole-number is referenced 14 times) leaves pilot edges pointing at
a retired id: one Sonnet agent re-targets them (~150 edges).

Cost model from measured runs: an agent costs ~95k fixed plus ~0.75k per node
(proposer) or ~1.25k (critic); the prek writer was 157k for 38 nodes. Per
48-node strand: writer ~180k, proposers 2 x ~130k, critic ~145k, ~585k. Full
K-8 (14 strands) ~8.2M, plus ~10% reruns: about 9M subagent tokens, 11x the
total so far. Cost driver is turns times context, so agents get a script-built
packet and a compact id index and write their output in a few large appends.

Recommended: phase 1 = strands 1-4 (~250 nodes, ~2.4M), since the pilot and the
pre-K floor hang on those boundary nodes; review a 40-edge sample; then phases
2 (strands 5-7) and 3 (strands 8-11).
