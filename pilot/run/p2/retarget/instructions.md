# Re-pointing and attaching edges, phase 2: instructions

Work only from this file and `pilot/run/p2/retarget/in.json`. Do not read
anything else.

In a research map of school mathematics, each node lists the prerequisites it
needs. Three changes leave some edges pointing at the wrong node:

1. **Retired ids.** Some prerequisite ids were too broad and were replaced by
   finer nodes.
2. **Range splits.** Some nodes were split by number range (for example
   comparing two-digit numbers, three-digit numbers, and multi-digit numbers are
   now three nodes). An edge should point at the range the source actually uses.
3. **Method-neutral nodes.** New nodes such as "Add within 100" or "Multiply a
   whole number by a one-digit number" mean the computation by any method. An
   edge that points at one method (count all, partial products, the standard
   algorithm, a base-ten model) should point at the method-neutral node when any
   method would do, and keep the method only when the source node's statement,
   procedure, or test problem itself requires that method.

For each entry in `edges`, read the source node's statement, procedure, test
problem (`assess`), the edge's `points_to`, `scope`, and `why`, and choose from
`candidates[old_target]`. The old target is itself a candidate: list it to keep
the edge as it is.

- Pick the **least** that is needed, using the test problem's actual numbers:
  comparing 3/8 with 5/8 compares 3 and 5, numerals within 10; 46 + 30 needs
  4 + 3 tens, a sum within 10.
- More than one target only when the source genuinely uses each.
- If nothing fits, answer `keep_boundary` with a short id `concept.short-name`.

For each entry in `attach`, decide whether the source node needs the new node
`new` (its card is in `candidates["_attach"]`) as a direct prerequisite, by the
counterfactual test: could a learner meet the source node at its stated level
without it? Say `add: false` unless the source's statement, procedure or test
problem uses it.

## Output

Write valid JSON to `pilot/run/p2/retarget/out.json`, one entry per edge id and
per attach id:

```json
{
  "r1": {"targets": ["comparing.whole-numbers.numerals-within-10"], "reason": "one sentence"},
  "r2": {"targets": ["addition.base-ten.strategy"], "reason": "the test names partial sums"},
  "a1": {"add": true, "relation": "definitional", "points_to": "statement", "why": "at least eight words naming the part that uses it"},
  "a2": {"add": false, "reason": "one sentence"}
}
```

Write the file in one or two writes, check it parses, and reply with one line:
the path, how many edges kept their target, how many were re-pointed, and how
many attach edges were added.
