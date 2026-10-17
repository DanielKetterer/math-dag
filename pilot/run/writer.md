# Node writer: instructions

You turn learning components (granular skills attached to Common Core
standards) into **nodes** for a research map of school mathematics. You write
nodes only, never prerequisites.

Read only: this file, your strand's input file (`pilot/run/input/<strand>.json`),
`pilot/run/input/existing_ids.txt`, `concepts.yaml`, and
`pilot/run/skeletons/S0.yaml` (21 finished nodes: copy their style and
precision). Do not read anything else in the repository.

## What a node is

A node is one thing to know or do, defined by five fields:

- `concept`: from `concepts.yaml`, or a new one you propose (see Output).
- `facet`: which meaning of the concept it uses. Every node names one; use
  `core` for concepts with a single meaning.
- `level`: how formal, on one scale for all concepts.
  1 concrete (objects, pictures, actions); 2 representational (a model with
  symbols attached); 3 symbolic (rules used in general, without the model);
  4 justified (can explain why the rule holds in general).
- `type`: `concept` (knowing what something is), `procedure` (doing it step by
  step), `representation` (moving between forms), `fact` (recall),
  `justification` (knowing why), or `application` (a recognizable problem
  type, such as a kind of word problem).
- `assess`: exactly one test problem. If testing it needs two unrelated
  problems, it is two nodes.

## Rules learned from the calibration run (follow strictly)

1. **One meaning per node.** A statement never says "equivalently", "or
   alternatively", or gives two definitions. Two meanings are two nodes, or
   one node reachable by two routes (routes are added later, not by you).
2. **A rule and its use are different nodes.** The claim of a principle
   (a concept node: "a/b = (n x a)/(n x b)") is separate from the procedure
   that applies it and from the justification of why it holds.
3. **Procedures must be correct in general.** Test every procedure on an
   awkward case before writing it (for example, 4/6 and 6/9 share no
   denominator multiple). If a procedure only works in special cases, say so in
   the statement.
4. **Merge number-range variants.** Components that differ only in allowed
   numbers ("dividends through 50", "denominators 2, 3, 4, 6, 8") are one node,
   unless the range changes the mathematics (for example, whole-number answers
   versus fraction answers).
5. **Different level or facet means different node.** Doing it with a model
   (level 2) and doing it symbolically (level 3) are two nodes.
6. **"Explain" components are justification nodes. "Solve word problems"
   components are application nodes.**
7. **Do not duplicate existing nodes.** `existing_ids.txt` lists nodes already
   written. If a component is fully covered by one, list it under `covered_by`
   instead of writing a node. The four example nodes at the end of that list
   may be rewritten by the strand that owns their standard; reuse their id.

## Fields

```yaml
- id: fraction.addition.like-denominators.model   # concept.what[.how], lowercase, dots and hyphens
  concept: fraction
  facet: part-whole
  level: 2
  type: procedure
  name: Add fractions with like denominators using a model
  statement: One sentence or two, one meaning, precise enough to test.
  procedure:            # only for procedures; numbered steps an edge can point at
    - ...
  assess: "One test problem."
  sources: {ccss: ["4.NF.B.3.a"], lc: ["1a2b3c4d", "5e6f7a8b"]}
```

Quote every `lc` value and every ccss code. Use the 8-character `lc` ids exactly
as given in the input. Plain keyboard characters only: no curly quotes, no long
dashes, write "x" for multiplication.

## Coverage

Every learning component in your input must end up in exactly one place: in
the `lc` list of a node you write, in `covered_by`, or in `dropped` with a
reason. Nothing silently disappears.

## Output

Write `pilot/run/skeletons/<strand>.yaml` as a YAML list of nodes, each with
`strand: <strand>` added. Then write `pilot/run/skeletons/<strand>.extra.yaml`:

```yaml
new_concepts:          # concepts or facets not in concepts.yaml
  - {concept: ratio, facet: tape-diagram, reason: "..."}
covered_by:            # components fully covered by an existing node
  - {lc: "1a2b3c4d", node: fraction.unit.part-whole}
dropped:
  - {lc: "9f8e7d6c", reason: "..."}
notes: "anything a reviewer should know"
```

Validate that both files parse as YAML before finishing. Reply with one line:
paths written, number of nodes, and counts of covered_by and dropped.
