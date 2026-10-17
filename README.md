# math-dag

A research map of how school mathematics, pre-K through grade 12, fits
together: what there is to learn, what has to be learned first and exactly
why, and how curricula order it.

**Status:** pilot built. The slice from equal sharing (grade 1) to slope
(grade 8) has 190 nodes and 725 prerequisite edges; it passes the checker
with nothing unlearnable and no cycles. It recovers 85% of the Coherence Map's
links in the slice. Awaiting human review: `pilot/run/REVIEW.md`.

## Layout

| Path | What it is |
|---|---|
| `RULES.md` | The rules every node and link must follow. Start here. |
| `concepts.yaml` | The list of concepts and their facets (distinct meanings). |
| `nodes/<concept>/<id>.yaml` | One file per node: what it is, how it is tested, what it requires and why. |
| `pathways/` | How particular curricula order the nodes, and at which grade. |
| `schema/node.schema.json` | Machine-checkable form of the node rules. |
| `explorer/index.html` | Interactive map: search a skill, read its prerequisites and why, trace its chain. Open it in a browser. Rebuild with `python3 tools/build_explorer.py`. |
| `tools/check.py` | Checks the map: schema, precise whys, learnability, merge candidates, pathway order. |
| `tools/pilot_scope.py` | Gathers seed material for the pilot slice. |
| `pilot/` | The first slice, built end to end before scaling. |
| `sources/learning-commons/` | Math subset of the Learning Commons Knowledge Graph, with attribution. |
| `scripts/` | Download and extract the source data. |

## Run the checker

```sh
pip install pyyaml jsonschema
python3 tools/check.py
```

It exits nonzero if any rule is broken. Warnings list nodes referenced but
not written yet; that list is the frontier of the work.

## Sources and licenses

The source data in `sources/learning-commons/` comes from the Learning
Commons Knowledge Graph (CC BY 4.0), including the Student Achievement
Partners Coherence Map (CC0), Achievement Network learning components,
Illustrative Mathematics 360, and the Eedi Misconceptions Graph. Full
attribution is in `sources/learning-commons/ATTRIBUTION.md`.

## Explorer link

https://danielketterer.github.io/math-dag/
