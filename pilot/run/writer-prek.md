# Node writer, pre-K floor: instructions

You write **nodes** (never prerequisites) for the floor of a research map of
school mathematics: what children learn before Kindergarten, plus the K nodes
that come from splitting `counting.objects`. One agent writes the whole layer.

## Read only these

- this file
- `pilot/run/writer.md` sections "What a node is" and "Rules learned from the
  calibration run" (rules 1-7 apply here unchanged, except that you cite
  `sources.prek` ids instead of `lc` ids)
- `sources/prek/elof.yaml`, `sources/prek/clements_sarama.yaml`,
  `sources/prek/counting_principles.yaml`
- `sources/prek/VETTING.md` sections 3, 4 and 5 (findings, candidate inventory,
  decisions). The inventory is a scoping guide, not a list to copy.
- `pilot/run/prek/input/existing_ids.txt`
- `concepts.yaml`
- `pilot/run/skeletons/S0.yaml` (copy its style and precision)
- `pilot/run/prek/input/lt2.txt` is the authors' fullest description of each
  trajectory level. Search it (grep) for the levels you use; do not read it end
  to end.

Do not read anything else in the repository.

## Scope (decided by Daniel)

1. **Floor: the preschool band.** Write nodes for distinct competencies in the
   ELOF goals and in the Clements-Sarama levels tagged `preschool`, plus
   `k-overlap` levels that are still pre-K competencies. Toddler levels enter
   only as roots (below). Levels tagged `beyond` are out.
2. **Absences are never nodes**: Pre-Counter, Chanter, Pre-Patterner, Pre +/-,
   Pre-Composer, Dumper, and any level described as "does not" or "no sign".
3. **Patterning is out.** List ELOF P-MATH 7 and every `cs.pattern.*` level in
   `dropped` with reason "patterning excluded by decision".
4. **Split `counting.objects`** into its K meanings, written in this same file:
   one word per object in a count (K.CC.B.4.a), the last word tells how many
   (K.CC.B.4.b, first clause), the count is the same regardless of order or
   arrangement (K.CC.B.4.b, second clause), and each successive number name is
   one more (K.CC.B.4.c). Keep the id `counting.objects` for the node that
   counts a collection to answer "how many" (K.CC.B.5); 13 written nodes point
   at it. Give it the statement of that one meaning only.
5. **Reuse unwritten ids.** If you write a node that `existing_ids.txt` lists as
   referenced-but-unwritten (for example `comparing.size.direct`,
   `shapes.recognize`), use that id exactly and make its meaning fit how a
   reader of that id would expect it.

## Rules specific to this layer

- **Ages and grades never go on a node.** They live in pathways. Do not write
  "preschool", "age 4", or "by kindergarten" in any field.
- **Merge number-range variants unless the mathematics changes** (writer rule 4).
  Counting 5 objects and counting 20 is one node. The range changes the
  mathematics only at: exact meanings of small number words versus the
  cardinal principle; memorized number words through the teens versus the
  decade rule; perceptual subitizing (no parts) versus conceptual subitizing
  (seeing parts). Knower levels (one-, two-, three-knower) are one node.
- **Reliability is not a different node.** "Sorts but switches attribute" and
  "sorts consistently" test the same task; one node.
- **Nonverbal versus verbal is a different node** when the assess differs in
  kind (making a matching set without words versus naming the number).
- **Levels.** Almost everything here is level 1 (objects, actions, pictures).
  Reading or matching numerals is level 2. Use level 3 or 4 only if the
  statement truly works without a model or asks why.
- **Assess items must rule out shortcuts.** For cardinality, the assess must
  not be passable by repeating the last word (see `cp.bermejo-2004`): for
  example, ask the child to give the puppet that many, or ask "how many" after
  the count is finished and the objects are covered.
- **Roots.** A node with no prerequisite inside the map gets `requires: []` and
  a `root_reason` naming the developmental evidence that it needs nothing
  earlier in the map (for example, rote recitation dissociates from quantity
  meaning, `cp.recite-before-meaning`). Expected roots: reciting number words,
  judging which of two very unequal sets has more, naming a set of one to three
  at a glance, matching shapes, seeing objects as alike. Every other node gets
  `requires: []` with no `root_reason`: prerequisites are added later by other
  passes, not by you.
- **Sources.** Cite with `sources: {prek: [...], ccss: [...]}`. Every `prek` id
  must exist in the three source files. K nodes cite their CCSS codes.
- **Concepts.** Use `concepts.yaml` where it fits. New concepts or facets
  (likely: subitizing, classifying, spatial position, ordinal) go in the extra
  file under `new_concepts`.
- Plain keyboard characters only. Write "x" for multiplication.

## Coverage

Every item in the three source files ends up in exactly one place: in the
`prek` list of a node you write, in `covered_by` (fully covered by an existing
written node), or in `dropped` with a reason. Allowed short reasons:
"absence, not a competency", "toddler band, below the floor", "beyond the
floor (K or later; covered by K-8 nodes)", "patterning excluded by decision",
or your own one-line reason. The counting-principles `findings` entries are
evidence, not competencies: cite them in `root_reason` or `notes` where they
apply, and leave them out of coverage.

## Checkpointing (required)

Write nodes to `pilot/run/prek/prek.nodes.yaml` as a plain YAML list, appending
about 10 nodes at a time with a shell heredoc (`cat >> file <<'EOF'`), so a
failure leaves a usable partial file. Never rewrite earlier entries. If the
file already exists when you start, read it and continue after its last id.

## Output

1. `pilot/run/prek/prek.nodes.yaml`: the node list, each node with
   `strand: prek` added.
2. `pilot/run/prek/prek.extra.yaml`:

```yaml
new_concepts:
  - {concept: subitizing, facet: perceptual, reason: "..."}
covered_by:
  - {source: "cs.length.indirect-comparer", node: "<existing id>"}
dropped:
  - {source: "cs.counting.chanter", reason: "absence, not a competency"}
notes: "anything a reviewer should know, including any merge you were unsure of"
```

Validate that both files parse as YAML and contain only ASCII before
finishing. Reply with one line: paths written, number of nodes, number of
roots, counts of covered_by and dropped.
