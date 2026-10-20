# Rules (draft 1, for Daniel's review)

Purpose: a research map of how school math (pre-K through grade 12) fits
together. Every rule below is tuned for that purpose. Where I made a call you
might make differently, it is marked **DECISION** and collected at the end.

The checker (`tools/check.py`) enforces everything marked **(checked)**.

---

## 1. Three stores, kept apart

| Store | Folder | Holds | Never holds |
|---|---|---|---|
| Ontology | `nodes/` | What there is to know | Grades, order, curricula |
| Dependency | inside each node file, under `requires` | What must be known first, and why | Opinions about good teaching order |
| Pathways | `pathways/` | How a curriculum orders the nodes, and at which grade | New nodes or new prerequisites |

The test of the separation: Common Core's traditional high school sequence
and its integrated sequence must both fit in `pathways/` without changing a
single file in `nodes/`.

## 2. Nodes

One YAML file per node, at `nodes/<concept>/<id>.yaml`.

```yaml
id: fraction.unit.number-line        # concept.short-name, lowercase, dots and hyphens
concept: fraction                    # must exist in concepts.yaml          (checked)
facet: measure                       # which meaning of the concept         (checked)
level: 2                             # how formal: see 2.2                  (checked)
type: representation                 # see 2.1                              (checked)
name: Locate a unit fraction on the number line
statement: >
  1/b is the point reached by partitioning the interval from 0 to 1 into
  b equal parts and taking one part from 0.
procedure:                           # optional; numbered steps an edge can point to
  - Mark 0 and 1 on a number line.
  - Partition the interval from 0 to 1 into b equal lengths.
  - Label the endpoint of the first length from 0 as 1/b.
assess: "Place 1/4 on a number line marked only with 0 and 1."
sources:                             # where this node came from (alignment, not authority)
  ccss: [3.NF.A.2.a]
  learning_components: []
  eedi: []
requires: [...]                      # see section 3
status: proposed                     # proposed | reviewed | disputed       (checked)
```

### 2.1 Node types (checked)

- `concept`: knowing what something is ("a unit fraction is one of b equal parts").
- `procedure`: doing something step by step ("add fractions with like denominators").
- `representation`: moving between forms (picture, number line, symbol, table, graph).
- `fact`: recall without computing (multiplication facts within 100).
- `justification`: knowing why something is true ("why invert and multiply works").
- `application`: a recognizable problem type that combines other nodes (unit rate word problems).

### 2.2 Level: how formal (checked, 1 to 4)

1. **Concrete**: objects, pictures, actions. Folding paper into fourths.
2. **Representational**: a model with symbols attached. 3/4 on a number line.
3. **Symbolic**: rules used in general, without the model. a/b + c/b = (a+c)/b.
4. **Justified**: can explain why the rule holds, in general.

**DECISION 1**: one global 1-4 scale for every concept, rather than a scale
written separately for each concept. A global scale lets the map answer
"where in school does formality jump?" A per-concept scale fits each concept
more tightly but makes concepts incomparable.

### 2.3 Facets

A facet is one meaning of a concept. Fractions have at least five
(part of a whole, measure, quotient, ratio, operator). Facets are listed per
concept in `concepts.yaml`. Two nodes with the same concept and level but
different facets are different nodes.

### 2.4 How big is a node

A candidate is a node only if all three hold:

1. **One problem type tests it.** The `assess` field states one. If you need
   two unrelated problems to test it, it is two nodes.
2. **It has its own position.** If two nodes end up with exactly the same
   prerequisites and exactly the same dependents, they are one node.
   **(checked: reported as merge candidates)**
3. **It is learnable.** See 3.4.

4. **Range rule** (Daniel, 2026-10-20). A number range changes the mathematics
   exactly when it changes the prerequisite set. Two range variants that need
   different prerequisites (adding within 100 needs tens; within 1000 needs
   hundreds) are two nodes; variants with the same prerequisites are one.

Nodes are never split for convenience and never merged for tidiness. Splits
and merges come from rules 1-3 or from a reviewer's call.

## 3. Prerequisites

### 3.1 Shape: OR of ANDs (checked)

```yaml
requires:
  - clause: common-denominators      # one way to learn this node
    all_of:
      - node: fraction.equivalent.symbolic
        relation: procedural
        points_to: procedure.1
        why: Step 1 rewrites both fractions over a common denominator, which is generating equivalent fractions.
        evidence: [{kind: content, source: claude-pass-1}]
  - clause: invert-and-multiply      # a different, sufficient way
    all_of: [...]
```

Any one clause is enough. Every edge inside a clause is needed for that
clause. When the routes differ in method, each clause carries its own
`procedure`, and its edges' `procedure.N` point at that list instead of the
node's.

A route at a different level is not a clause; it is a different node. Dividing
fractions by measuring "how many 3/4 fit in 2/3" on a model is level 2, so it
is its own node, linked to the level 3 symbolic node under `related`. A node with no prerequisites has `requires: []` and must say why
in `root_reason` (for example: "counting objects is where this map starts").

### 3.2 Relation types (checked)

- `definitional`: the meaning of this node uses the other. (Slope is defined as a ratio.)
- `procedural`: a step of this node's procedure performs the other.
- `representational`: this node is stated in the other's model or notation. (Locating 3/4 on a number line needs the number line.)
- `justificatory`: the explanation of why this node is true uses the other.

### 3.3 The "why" rule (checked)

Every edge must say precisely why. Three mechanical checks:

1. `points_to` names the part of **this** node that needs the other one:
   `statement`, `procedure.N` (step N must exist), or `assess`.
2. `why` is at least 8 words.
3. `why` does not lean on vague phrases: "foundational", "builds on",
   "builds toward", "important for", "needed for", "is a prerequisite",
   "lays the groundwork", "helps with", "related to".

**Task-only prerequisites.** Some prerequisites belong to the test problem,
not to the idea. Example: computing a derivative from its definition needs
algebraic cancellation, but understanding what a derivative is does not.
Mark these `scope: task` and point them at `assess`. (checked)

**Direct-only has one exception, and it covers test problems.** An edge to a
skill that a chain of prerequisites already reaches is still listed when this
node's own statement, procedure, or test problem uses that skill. If only the
test problem uses it, it is a task edge (pilot review item 51).

**Simplest form.** Simplifying a fraction to lowest terms is its own node. It
enters another node only as a task edge, and only when that node's test
problem asks for simplest form. "Rewrite in simplest form if wanted" in a
procedure does not make it a prerequisite (pilot review items 8, 65).

### 3.4 Learnability (checked)

With OR-clauses, a cycle is not automatically wrong. What is wrong is a node
that can never be learned: every one of its clauses needs something that, in
turn, needs it. The checker starts from the roots, repeatedly marks any node
with at least one fully-marked clause, and reports every node left unmarked.

An unlearnable node is fixed by one of three moves, recorded in the review:

- split a node by level or facet (the usual fix: the cycle was one concept at two depths),
- add a missing clause (there was another way in),
- move an edge out of `requires` into `related` (it was never a prerequisite).

Never by silently deleting an edge.

### 3.5 Not prerequisites (kept separately, under `related`)

`generalizes`, `specializes`, `same_idea_different_form`, `contrasts_with`.
These record structure the map should show without claiming order.

`common_path` records a route into a node that is common in development or
teaching but not required: a credible way in exists without it. It is where an
edge goes when its only alternative is not a node ("learn from varied
examples", "explore how pieces fit"), or when its route needs everything
another route needs and more, so it never changes what the node requires.
An empty or superset route is never kept in `requires` (Daniel, 2026-10-19).

## 4. Evidence and status

Every edge carries an `evidence` list. Kinds:

- `content`: proposed by reading the node itself (an independent model pass).
- `standards`: suggested by the Coherence Map or by standards structure.
- `curriculum`: ordering observed in a curriculum (can **refute**, never confirm).
- `developmental`: research on how children actually learn it (strongest, where it exists).
- `review`: a human decision, with initials.

Status for nodes and edges: `proposed` (machine-made), `reviewed` (a human
accepted it), `disputed` (reviewers disagree, or curricula contradict it).
A refuted edge is deleted, and its deletion is kept in git history with the
reason in the commit message.

**The refutation rule.** If a reputable curriculum teaches B before A, and B
is not a weaker level or different facet than the B in the map, then A is not
required for B by every route. Either the edge is wrong, or B has a clause the
map is missing. Agreement among curricula proves nothing, because they copy
one another.

## 5. Pathways

One file per curriculum or framework in `pathways/`:

```yaml
name: Illustrative Mathematics 360
source: sources/learning-commons/im360_curriculum.jsonl
steps:
  - {position: 1, grade: "3", unit: "Introducing Fractions", nodes: [fraction.unit.part-whole]}
  - {position: 2, grade: "3", unit: "...", nodes: [fraction.unit.number-line]}
assumes: []            # nodes the pathway takes as already known at its start
```

The checker reports, for every node in a pathway, whether at least one of its
clauses is satisfied by earlier steps. Failures are findings, not errors:
each one is either a missing clause or a wrong edge. (checked)

Grade belongs here, never on a node. 3/4 is not "a grade 3 idea"; it is an
idea Common Core places in grade 3.

## 6. Decisions for Daniel
Done:

1. **Global level scale (2.2)**: one 1-4 scale for all concepts
2. **Facets as a required field (2.3)**: every node names a facet, even concepts with only one.
3. **Application nodes (2.1)**: problem types should be nodes in the map.
4. **Where the map starts (3.1)**: counting objects, comparing
   quantities by size, and recognizing shapes.
5. **The Eedi misconceptions**: attach them to nodes as evidence of where understanding
   breaks.
6. **Trapezoid (Daniel, 2026-10-20)**: the inclusive definition, at least one pair of
   parallel sides, so every parallelogram is a trapezoid (the hierarchy matches squares
   being rectangles; Illustrative Mathematics uses it too).
