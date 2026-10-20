# Node writer, big run phase 2: instructions

You turn learning components (granular skills attached to Common Core
standards) into **nodes** for a research map of school mathematics. You write
nodes only, never prerequisites. One agent writes one strand.

## Read only these

- this file
- `pilot/run/writer.md`, sections "What a node is", "Rules learned from the
  calibration run" and "Fields" (rules 1-7 apply unchanged)
- your strand's input file `pilot/run/p2/input/<strand>.json`
- `pilot/run/p2/input/existing_ids.txt`
- `concepts.yaml`
- `pilot/run/skeletons/S0.yaml` (finished nodes: copy their style and precision)

Do not read anything else in the repository. Read each file once.

## Your input

Each record is one standard with its text and the learning components (`lc`,
8-character ids) that no written node cites yet. `already_cited` lists
components a written node already cites; they are context, not work.

## Rules added for this run (follow strictly)

1. **Reserved ids.** `existing_ids.txt` ends with ids that written nodes
   already point at but nobody has written. For an id your strand owns:
   - if exactly one of your nodes has the meaning a reader of that id would
     expect, use the id exactly for that node;
   - if the id is broader than one node (for example `addition.whole-number`
     covers adding within 10, within 20, two-digit with place value and the
     multi-digit algorithm), do not use it. Write the finer nodes and record
     the id under `retires` in the extra file, listing which of your new ids
     together cover it. A later pass re-points the old edges.
   Ids owned by another strand or a later phase: never write them; you may
   name them in `notes`.
2. **Do not duplicate written nodes.** Many K components (joining, separating,
   composing numbers to 10, counting) are already covered by pre-K and K
   nodes in `existing_ids.txt`. A component fully covered by one goes under
   `covered_by`. Partly covered: write only the missing part, and say so in
   `notes`.
3. **The test problem tests the node and nothing else.** Most wrong edges in
   the pilot came from test problems that asked for more than the node (writing
   symbols, simplest form, a second computation, reading a word problem when
   the node is a computation). Keep each `assess` to the one skill; give the
   numbers, the model or the picture it needs; ask for no extra recording.
   Application nodes are the exception: a word problem is their skill.
4. **Assess items must rule out shortcuts.** A fluency or fact node says
   "without counting or computing aloud"; a place-value node cannot be passed
   by reading digits off without their values; a strategy node names the
   strategy to use.
5. **Range rule (RULES 2.4).** A number range changes the mathematics exactly
   when it changes the prerequisite set. Before merging two components that
   differ in range (or in grade), ask whether the larger range needs something
   the smaller does not (hundreds, fractions of a unit, a formula). If it does,
   write two nodes. Phase 1 merged across grades and had to split nine nodes.
6. **A computation inside a measurement or geometry task is not a method.**
   When a test problem needs a sum, product or quotient, the proposers point
   at a method-neutral computation node; do not write method steps
   ("count all", "use partial products") into a statement unless the method is
   the skill being taught.
7. **The pre-K and K floor is written.** Shapes (recognize, match, name,
   closed boundary, compose), direct comparison of length and weight, position
   words and sorting already exist in `existing_ids.txt`. Use `covered_by`
   for components they cover; write only what is new.
8. **Strategy versus algorithm versus fluency are different nodes** when the
   test differs in kind: a place-value strategy with a model (level 2), the
   standard algorithm (level 3, procedure), recall within a range (fact).
9. **Ages and grades never go on a node.** No "in grade 2" in any field.
   Number ranges are fine.
10. Plain keyboard characters only: no curly quotes, no long dashes, write "x"
   for multiplication and "divided by" for division (the slash means fraction).

## Coverage

Every learning component in your input ends up in exactly one place: in the
`lc` list of a node you write (a component may be cited by two nodes when it
carries two skills), in `covered_by`, or in `dropped` with a one-line reason.

## Checkpointing (required)

Write nodes to `pilot/run/p2/skeletons/<strand>.yaml` as a plain YAML list,
appending about 15 nodes at a time with a shell heredoc (`cat >> file <<'EOF'`),
so a failure leaves a usable partial file. Never rewrite earlier entries. If
the file already exists when you start, read it and continue after its last
id. Plan the strand first (in your head, not in a file), then write; do not
write drafts.

## Output

1. `pilot/run/p2/skeletons/<strand>.yaml`: the node list (fields as in
   writer.md "Fields"), each node with `strand: <strand>` added.
2. `pilot/run/p2/skeletons/<strand>.extra.yaml`:

```yaml
new_concepts:          # concepts or facets not in concepts.yaml
  - {concept: area, facet: unit-squares, reason: "..."}
retires:               # reserved ids too broad for one node
  - {id: addition.whole-number, replaced_by: [addition.within-10.fluency, "..."], note: "..."}
covered_by:
  - {lc: "1a2b3c4d", node: counting.objects}
dropped:
  - {lc: "9f8e7d6c", reason: "..."}
notes: "anything a reviewer should know, including merges you were unsure of"
```

Validate that both files parse as YAML and contain only ASCII before
finishing. Reply with one line: paths written, number of nodes, reserved ids
used, ids retired, counts of covered_by and dropped.
