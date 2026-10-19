# Re-pointing edges at retired ids: instructions

Work only from this file and `pilot/run/p1/retarget/in.json`. Do not read
anything else.

Some nodes in a research map of school mathematics point at prerequisite ids
that turned out too broad for one node (for example `addition.whole-number`,
which spans adding within 10 up to the multi-digit algorithm). Those ids were
retired and replaced by finer nodes, listed in `candidates` under each retired
id.

For each entry in `edges`, read the source node's statement, procedure, and
test problem (`assess`), the edge's `points_to`, `scope`, and `why`, and decide
which candidate(s) the source node actually uses at that point.

- Pick the **least** that is needed: if the node only adds two single-digit
  numerators, that is a within-10 or within-20 node, not the algorithm.
- Pick more than one candidate only when the source genuinely uses each (they
  become edges in the same route).
- If none of the candidates is what the source needs (for example common
  multiples or least common multiples, which a later phase writes), answer
  `keep_boundary` with a short new id of the form `concept.short-name` for the
  missing skill.
- Use the test problem's actual numbers: 3/8 + 4/8 needs 3 + 4, a sum within
  10; 37/100 + 48/100 needs 37 + 48, a two-digit sum.

## Output

Write valid JSON to `pilot/run/p1/retarget/out.json`, one entry per edge id:

```json
{
  "r1": {"targets": ["addition.within-10.fluency"], "reason": "one sentence"},
  "r2": {"keep_boundary": "multiples.common-multiple", "reason": "one sentence"}
}
```

Every edge id gets an entry. Write the file in one or two writes, check it
parses, and reply with one line: the path and how many edges went to each
target.
