# Handoff: phase 2 review applied; 5 items wait on Daniel (2026-10-20, later session)

Read this first in a new session. Then RULES.md.

## Phase 2 review: applied

- Answers: pilot/run/p2/REVIEW_ANSWERS.txt, encoded in pilot/run/p2/overrides.yaml
  (126 edge entries, 6 routes, 6 set_routes) and applied with `sh tools/rebuild.sh`.
  Phase 1 side: p1/overrides.yaml (D91 re-pointed, F107 entry); N3 and N4 batches and
  skeletons (F107, F106); p2/retarget/out.json r87 (kept on the two-step node);
  p1/skeletons/N3.extra.yaml (LC 44a2143c moved to the reserved upper half).
- Map: 675 nodes, 2,364 edges, 0 errors. Findings 87 -> 72: Common Core order 15 -> 7,
  IM 67 -> 61. Unwritten ids referenced 36 -> 41 (the new reserved nodes).
- Benchmark: 81% direct, 90% through chains (was 92%). The lost link, 3.NF.A.1 ->
  3.G.A.2, ran 3.G.A.2 -> rectangle definition -> right angle (4.G.A.1) -> degrees
  (4.MD.C.5) -> unit fractions, through the right-angle edge CC and IM refuted (F104).
  The real link sits inside fraction.unit.part-whole, which cites both standards
  (pilot item E104). 90% is the honest number.
- Precision of kept edges, random 40: 27/40 = 68% (about 52-80%) as marked; 29/40 =
  73% (about 57-84%) if Claude's pushback on A11 and A28 stands. Below phase 1 (30/40)
  and the pilot (35/40); the intervals overlap. Critic drops: 18/20 upheld (B44, B54
  restored).
- The 13 marked edges by pattern: a definition pointing at a stronger recognition node
  (A14, A25, A29); a teaching order taken as necessary (A4, A30, time); a method-specific
  step inside a method-neutral node (A7, A17); an application node's class wider than its
  test (A5, A10); other (A1, A22, and A11, A28 pending). Five of the 13 are G2 shape
  definitions and attributes.
- Subagent tokens this session: 0. Running total 6,229,396.

## Pending Daniel

1. **A11, not applied (Claude pushes back): keep parallel.meaning -> segment.meaning.**
   The node is also about parallel sides: its statement's second clause, and its test asks
   which sides of a trapezoid are parallel. Two segments that are not parallel can also
   never meet, so "never meet" says nothing about sides; sides are parallel only through
   the lines they lie on, which is what segment.meaning states (a segment is the part of a
   line between two endpoints; sides are segments). Keep, or split parallel lines from
   parallel sides and move the edge to the sides node.
2. **A28, not applied: keep decimal.thousandths.notation -> decimal.hundredths.notation.**
   The test writes 43/1000 as 0.043, a 4 in the hundredths place. Both alternatives the
   answer names pass through hundredths in the map: "place-value structure" is
   place-value.tenth-of-left, which requires decimal.hundredths.notation, and the
   power-of-ten rule requires tenth-of-left or ten-times-right.decimal. A route that
   skips hundredths has to produce 0.043 without knowing what the second place is
   ("count the zeros"). Name it if that is the route meant.
3. **Application-node scope.** A5, A10, C66, C69, C73 were applied as test scope (an
   edge stays only if the test uses it). Phase 1 A35 went the other way (statement scope:
   'unknown in any position' kept start-unknown problems). Both readings are now in the
   map, and under test scope some statements claim more than their edges require:
   measurement.application.conversion.multistep says "whole-number, decimal, or fraction
   results" and still requires to-larger.fraction and both decimal conversions;
   data.line-plot.fraction.multistep names four operations. Claude's recommendation:
   statement scope stays the rule (the node is what its statement says), and a statement
   that spans number types with different prerequisites is split by the range rule
   (whole-number vs fraction results). Pick one; then Claude makes statements and edges
   agree.
4. **Same argument, not applied (yes or no each):**
   a. shapes.rectangle.define -> shapes.quadrilateral.recognize: replace with
      shapes.polygon.name-by-sides, as A14 and A29 did for rhombus and square.
   b. shapes.quadrilateral.subcategories-included -> shapes.rectangle.define: replace
      with shapes.name.any-orientation, as A25 did for square. rhombus.define stays: no
      earlier node names rhombuses.
   c. measurement.application.fraction -> fraction.application.addition-same-whole:
      drop. It is the unlike-denominator word-problem node (grade 5); this node is grade 4
      and its test is 3/8 + 7/8. CC and IM order both refute it; it is the only finding
      left on the node.
   d. division.partial-quotients.one-digit-divisor -> subtraction.within-1000, and the
      .remainder sibling's addition and subtraction edges: the same past-1000 gap as F116,
      which would also need subtraction.multi-digit.
5. **D78** read as keep plus a new node (the answer says "insufficient as modeled", not
   wrong); confirm.

## Claude's calls in the encoding (reverse in the overrides files)

- A4: replaced by time.analog.hour rather than dropped; dropping left the node with no
  clock face. A25: replaced by shapes.name.any-orientation (the learner must know which
  figures are squares).
- A7: kept on the three meaning routes; added route via-standard-algorithm without
  multiples of ten, pointing at division.standard-algorithm.long-division (6.NS.B.2,
  unwritten). Method-neutral nodes were meant to take methods as routes (phase 1 F); the
  proposers built meaning routes with method steps inside them instead.
- set_routes: A17 coins (counting | adding), A30 nearest minute (by fives | by ones),
  C64/D74 sum within 10 (count all | fingers | count on), C65/D81 difference within 10
  (take away | count back | related addition). Recall is not a route into the within-10
  nodes: fluency requires them. The verbal action nodes moved to related (common_path).
- F111: the within-10 node joins the make-ten and decompose-to-ten routes. The statements
  cover sums of 10 or less, which those methods do not do (direct-use rule; make-ten's
  chain reaches within-10 only through the equal sign's meaning).
- F113: no conversion edges were missing. Every conversion test supplies its fact in
  parentheses ("1 ft = 12 in"), which is why the fact nodes have no dependents. The
  system-specific difference is in prerequisites, so the mass, weight and liquid-volume
  fact nodes now point at the F115 unit nodes, and mass/weight is no longer a merge
  candidate. The length pair still is: both systems' units come from
  measurement.length.ruler. Proposal: the checker should not treat two nodes as one
  position when neither has dependents.
- F107: narrowed to 3.OA.D.8 with a new test (412 - 189 + 6 x 8 = 271, claimed 371,
  estimate about 250); the 4.OA.A.3 half is reserved. F106: the LC moved with the
  citation (41093be0 is the 2.NBT.B.5 within-100 component; now 18fca54d, 3.NBT.A.2).
- F105 recorded in RULES section 6 (inclusive trapezoid).

## Next

1. Daniel: the 5 pending items above.
2. Phase 3 (grades 6-8; strands 8-11 of the big-run plan below: NS; EE and F, two strands;
   G, two strands; SP), with the 17 reserved nodes in pilot/run/p2/next_slice.yaml written
   inline into its F skeleton and attached to one batch, as in phase 2. Estimate: about
   276 nodes at phase 2's measured 14k subagent tokens per node, about 3.9M (3.6-4.2M);
   phase 2 ran 12% over its estimate. The running total would reach about 10.1M. Needs a
   go-ahead.
3. The published explorer copy (claude.ai/artifact/Q7RWducGX1KtkuZeSAu6Vq) is still stale.

# Earlier: big run phase 2 merged (2026-10-20)

## Phase 2 (K-5 measurement, data, geometry): done

- 5 strands (pilot/run/p2): M1 K-2 measurement and data (41), M2 grade 3
  measurement and data (44), M3 grades 4-5 measurement (54), G1 K-2 geometry
  (22), G2 grades 3-5 geometry (38); plus 26 fix-up nodes written inline by
  Claude (skeletons/F.yaml, proposed and criticized inside batch G1 via
  prepare_phase ATTACH): method-neutral computation nodes (within 10, 20, 100,
  1000; by one digit; two-digit by two-digit; with and without remainder),
  the upper halves of the F97 range splits (lower halves keep their ids,
  narrowed in pilot/run/p1 skeletons and batches, overrides there), and
  parentheses, order of operations, unknown symbol, two-way table, thousandths,
  angle.meaning (both G2 and M3 left it to the other).
- Map: 675 nodes, 2,352 edges, 0 errors. Benchmark 81% direct, 92% chains.
  Common Core order findings 15 (queue F), IM 69.
- Retired: data.graphs.read, measurement.unit-conversion,
  coordinate-plane.first-quadrant. p2 retarget (spec-driven: retired ids, range
  splits, method edges, attach checks; pilot/run/p2/retarget/spec.yaml):
  59 re-pointed, 45 kept, 13 boundary, 6 attach edges.
- Late, by hand (pilot/run/p2/overrides.yaml, items L1-L5, flagged in queue F):
  addition.within-20 and subtraction.within-20 routes; weight cycle broken;
  my parentheses test problem fixed; unknown-symbol task edge made
  method-neutral.
- Passes agree on 69% (Jaccard 0.69). Critic: 535 necessary, 70 scaffold,
  68 task-only, 47 route-only, 8 wrong.
- Cost: phase 2 about 3.15M subagent tokens against an estimate of 2.8M:
  writers 696,790; proposers 1,422,735; retarget 148,779; critics 817,577
  (G2, M2, M3 are ESTIMATES of 160k each: the session limit stopped them after
  their files were complete); 67,572 wasted on a placeholder agent Claude
  launched by mistake. Running total 6,229,396.
- Review queue: pilot/run/p2/REVIEW.md, 116 items (A-E as usual, F structural
  and Claude's own calls). Answers go to pilot/run/p2/overrides.yaml (append;
  L items are already there).
- Session limits: two stops in two phases even at 4 agents. Each stop costs
  only the unreported usage, since files are complete; resume with SendMessage.

# Earlier: big run phase 1 reviewed and applied (2026-10-20)

## Phase 1 review (2026-10-20)

- Answers: pilot/run/p1/REVIEW_ANSWERS.txt, encoded in pilot/run/p1/overrides.yaml
  and applied (sh tools/rebuild.sh). Precision of kept edges, random 40:
  30/40 = 75% (about 60-86%), below the pilot (35/40) and pre-K (32/40).
  Critic drops: 19/20 upheld (B56 restored).
- 7 of the 10 wrong edges name one method for a sub-computation (count all,
  partial products, partial sums, base-ten model) where any method would do.
  Cause: retiring addition.whole-number etc. left no method-neutral node to
  point at, and the N4 writer folded fluency into strategy nodes. Proposed:
  method-neutral computation nodes by range (add/subtract within 100 and
  within 1000, multiply and divide by a one-digit number), with strategy and
  algorithm as routes into them.
- Pending Daniel (Claude pushed back): A4, A14, A17, D91 (a method edge
  dropped or made a route leaves the sub-computation with no prerequisite;
  point at the method-neutral node instead), A35 (two-step node says 'unknown
  in any position', so either keep the subtype edges or narrow the statement).
- Applied: cycles of F95 and F96 removed (set_routes); F99 regrouping edges now
  point at compose-unit/decompose-unit; C63 now points at ten-times-right.
- Next slice (fold into phase 2 rather than run alone): splits of F97 by the
  new range rule (RULES 2.4, accepted), expressions.parentheses (F98),
  expressions.order-of-operations (D90), equation.unknown-symbol (D94),
  table.read-two-way (C61-62), decimal.thousandths.notation, the
  method-neutral computation nodes, and the F100 multistep split.

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
