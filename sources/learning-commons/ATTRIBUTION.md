# Learning Commons Knowledge Graph: math subset

Extracted from the Learning Commons Knowledge Graph export, version v1.15.0
(`https://cdn.learningcommons.org/knowledge-graph/v1.15.0/exports/`), by
`scripts/extract_learning_commons.py`. Regenerate with
`sh scripts/fetch_learning_commons.sh <scratch_dir>`.

Knowledge Graph is provided by Learning Commons under the CC BY 4.0 license
(https://creativecommons.org/licenses/by/4.0/). Component sources:

| File | Contents | Upstream source and license |
|---|---|---|
| `ccss_math_standards.jsonl` | 836 Common Core math standards and groupings, with grade and parent | Common Core State Standards via Common Good Learning Tools, CC BY 4.0 |
| `math_learning_components.jsonl` | 6,445 math learning components, with the CCSS standards each supports | Achievement Network and Learning Commons, CC BY 4.0 |
| `coherence_map.jsonl` | 757 `buildsTowards` and 284 `relatesTo` links between CCSS standards | Student Achievement Partners Coherence Map, CC0 |
| `eedi_constructs.jsonl` | 2,258 Eedi constructs (fine-grained skills), each with the misconceptions that hinder it | "Eedi Misconceptions Graph v1.0" (c) 2026 Eedi Ltd., CC BY 4.0 |
| `im360_curriculum.jsonl` | Illustrative Mathematics 360 courses, units, sections, lessons, positions, CCSS alignments, unit dependencies | Illustrative Mathematics, CC BY 4.0 |
| `state_crosswalk.jsonl` | State standard to CCSS standard alignments, with each side's grade | Learning Commons, CC BY 4.0 |

Note on meaning: upstream defines `buildsTowards` as "proficiency in one
supports the likelihood of success in another ... without requiring strict
prerequisite order." It is a progression link, not a prerequisite claim. This
project treats it as a benchmark, not as ground truth.
