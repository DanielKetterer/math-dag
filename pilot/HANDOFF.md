# Handoff: state after applying both reviews (2026-10-19)

Read this first in a new session. Then RULES.md. The reviews themselves are in
pilot/run/review-daniel.md (pilot, K-8) and pilot/run/prek/REVIEW_ANSWERS.txt
(pre-K); both are now encoded in `overrides.yaml` files (see below).

## Measured

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

## Next: step 2, new nodes (needs Daniel's go-ahead on cost)

Write, then two Sonnet proposers and one blinded Sonnet critic on just these:

- Pre-K new: comparing.more-than (test must separate number from size, e.g. a
  few big items against many small ones), shapes.closed-boundary,
  shapes.name.receptive, numeral.digit-formation,
  counting.number-words.vocabulary, number conservation (split from
  counting.cardinal.order-irrelevance).
- Pre-K rewrites: counting.cardinal.last-word test (give-a-number beyond the
  subset-knower range); counting.cardinal.order-irrelevance narrowed to order.
- Pilot new: partitioning.segment.equal-lengths, fraction.compare.to-one,
  fraction.complex-fraction, division.facts.within-100,
  rational-number.negative-as-decrease (concept list needs rational-number).
- Restrict fraction.multiply-whole.symbolic to products within 100 (C62).

Estimate: writing in the main session; proposers and critic about 130-200k
subagent tokens.

## Still open

- 4 superset routes the checker reports (fraction.mixed-number.add and
  .subtract, fraction.addition.unlike-denominators.equivalent-replacement,
  fraction.compare.unlike.justify). Cause: merge_run builds a critic's
  alternative route as the standard route plus extras, so an alternative
  method keeps edges it was meant to skip. Fix the critic-route construction
  or review these four.
- Section E verdicts (pilot items 104-111) are recorded in
  pilot/run/overrides.yaml under benchmark_links but not yet turned into
  edges: 104 and 110 required, 107 and 111 route-only, 106 task.
- The 13 K-8 nodes pointing at counting.objects may want the split nodes.
- The 34-node boundary slice (whole-number addition and subtraction,
  expressions with variables, multiplication facts) is the next slice after
  step 2.

## Running a run: manifest and run_state

`pilot/run/manifest.yaml` lists every unit (one strand through one stage).
`python3 tools/run_state.py` prints status, the running subagent-token total,
and what can run next. Mark a unit done only through
`--mark UNIT done --tokens N --commit SHA`. Commit and push after every unit.
Running total: 519,220 subagent tokens (no subagents used 2026-10-19).

## Explorer

`tools/build_explorer.py` rebuilds `explorer/index.html` (and docs/) from
`nodes/`. Rebuilt 2026-10-19. A private published copy lives at
https://claude.ai/artifact/Q7RWducGX1KtkuZeSAu6Vq and was NOT refreshed this
session; to update it, publish the rebuilt page with that URL.
