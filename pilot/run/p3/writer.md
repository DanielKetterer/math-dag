# Node writer, big run phase 3 (grades 6-8): instructions

You turn learning components (granular skills attached to Common Core
standards) into **nodes** for a research map of school mathematics. You write
nodes only, never prerequisites. One agent writes one strand.

## Read only these

- this file
- `pilot/run/writer.md`, sections "What a node is", "Rules learned from the
  calibration run" and "Fields" (rules 1-7 apply unchanged)
- your strand's input file `pilot/run/p3/input/<strand>.json`
- `pilot/run/p3/input/existing_ids.txt`
- `concepts.yaml`
- `pilot/run/skeletons/S0.yaml` (finished nodes: copy their style and precision)

Do not read anything else in the repository. Read each file once.

## Your input

Each record is one standard with its text and the learning components (`lc`,
8-character ids) that no written node cites yet. `already_cited` lists
components a written node already cites; they are context, not work. Pre-K
through grade 5 is written: 675 nodes, listed in `existing_ids.txt`. Ratios,
rates, percent and proportional relationships (6.RP, 7.RP) are written too.

## Rules added for this run (follow strictly)

1. **Reserved ids.** `existing_ids.txt` ends with ids that written nodes
   already point at but nobody has written. For an id your strand owns:
   - if exactly one of your nodes has the meaning a reader of that id would
     expect, use the id exactly for that node;
   - if the id is broader than one node (for example `expressions.variables`
     covers writing, reading and evaluating expressions with a letter for a
     number), do not use it. Write the finer nodes and record the id under
     `retires` in the extra file, listing which of your new ids together cover
     it. A later pass re-points the old edges, so say in `note` which of your
     ids fits which use.
   Ids owned by another strand, by `F` (written by the main session) or by an
   earlier strand: never write them; you may name them in `notes`.
2. **Do not duplicate written nodes.** Many 6-8 components restate K-5 or
   ratio skills that are written. A component fully covered by one goes under
   `covered_by`. Partly covered: write only the missing part, and say so in
   `notes`.
3. **The test problem tests the node and nothing else.** Most wrong edges came
   from test problems that asked for more than the node (a second computation,
   simplest form, writing symbols, reading a word problem when the node is a
   computation). Keep each `assess` to the one skill; give the numbers, the
   model or the picture it needs; ask for no extra recording. Use numbers whose
   arithmetic is not the hard part (small integers, friendly fractions) unless
   the arithmetic is the skill.
4. **Application nodes: the statement and the test name the same problem
   class.** A word-problem node says exactly which problems it covers, and its
   test is one of them. When a standard's problems span number types or
   operations that need different prerequisites (whole-number answers versus
   fraction answers; one operation versus all four), write one node per class
   (the range rule below). Never list operations or number types in a statement
   that its test and its siblings do not cover. (Daniel's phase 2 review: five
   application nodes claimed more than they tested.)
5. **Assess items must rule out shortcuts.** A fluency or fact node says
   "without computing aloud"; a strategy node names the strategy to use; a
   definition node's test turns on the defining conditions (show cases that
   meet one condition and not the other), not on recognizing every example of
   the larger category.
6. **Range rule (RULES 2.4).** A number range changes the mathematics exactly
   when it changes the prerequisite set. Before merging two components that
   differ in range, number type or grade, ask whether the larger one needs
   something the smaller does not (negative numbers, fractions, exponents, a
   formula). If it does, write two nodes. Earlier phases merged across grades
   and had to split eleven nodes.
7. **Informal before formal.** When a standard uses a concept informally that
   a later standard makes formal (a rate before a slope, a square corner before
   a right angle, "the same shape" before similarity), write the informal node
   at the level it is used; do not make the early node depend on the formal one.
8. **A computation inside an algebra, geometry or statistics task is not a
   method.** When a test problem needs a sum, product, quotient or signed
   computation, the proposers point at a method-neutral computation node; do
   not write method steps into a statement unless the method is the skill.
9. **Strategy versus algorithm versus fluency are different nodes** when the
   test differs in kind: reasoning with a model or a tape diagram (level 2), a
   symbolic procedure (level 3), recall (fact). For equations: solving by
   reasoning about which number makes the equation true, and solving by
   inverse operations on both sides, are different nodes if the standard asks
   for both.
10. **Justifications are their own nodes.** "Explain why", "verify
    experimentally" and "use informal arguments" components are justification
    nodes, separate from the fact or procedure they explain.
11. **Ages and grades never go on a node.** No "in grade 7" in any field.
    Number ranges and number types are fine.
12. Plain keyboard characters only: no curly quotes, no long dashes. Write "x"
    for multiplication, "divided by" for division (the slash means fraction),
    "^" for exponents (3^2), "sqrt(2)" for roots, "pi" for pi, and "-3" for a
    negative number.

## Coverage

Every learning component in your input ends up in exactly one place: in the
`lc` list of a node you write (a component may be cited by two nodes when it
carries two skills), in `covered_by`, or in `dropped` with a one-line reason.

## Checkpointing (required)

Write nodes to `pilot/run/p3/skeletons/<strand>.yaml` as a plain YAML list,
appending about 15 nodes at a time with a shell heredoc (`cat >> file <<'EOF'`),
so a failure leaves a usable partial file. Never rewrite earlier entries. If
the file already exists when you start, read it and continue after its last
id. Plan the strand first (in your head, not in a file), then write; do not
write drafts.

## Output

1. `pilot/run/p3/skeletons/<strand>.yaml`: the node list (fields as in
   writer.md "Fields"), each node with `strand: <strand>` added.
2. `pilot/run/p3/skeletons/<strand>.extra.yaml`:

```yaml
new_concepts:          # concepts or facets not in concepts.yaml
  - {concept: exponent, facet: whole-number-power, reason: "..."}
retires:               # reserved ids too broad for one node
  - {id: expressions.variables, replaced_by: [expressions.variable.meaning, "..."], note: "..."}
covered_by:
  - {lc: "1a2b3c4d", node: ratio.unit-rate}
dropped:
  - {lc: "9f8e7d6c", reason: "..."}
notes: "anything a reviewer should know, including merges you were unsure of"
```

Validate that both files parse as YAML and contain only ASCII before
finishing. Reply with one line: paths written, number of nodes, reserved ids
used, ids retired, counts of covered_by and dropped.
