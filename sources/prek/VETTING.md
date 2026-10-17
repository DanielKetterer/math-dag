# Pre-K sources: vetting sheet

Research step for the pre-K floor, done 2026-10-17. No nodes, edges, or model
passes were run. Subagent cost: 0 tokens.

## 1. What was gathered

| File | Source | Provenance | Items |
|---|---|---|---|
| `elof.yaml` | Head Start ELOF, Mathematics Development, preschoolers (36-60 months) | Primary, public domain | 10 goals, 30 progression steps |
| `clements_sarama.yaml` | Clements and Sarama learning trajectories, 12 trajectories | Secondary (OTF reproduction of the tables) | 103 levels, ages 1 to 7 |
| `counting_principles.yaml` | Gelman and Gallistel principles, knower-level and successor studies | Mixed: fetched, secondary, memory | 5 principles, 8 findings |

## 2. What needs your check

In order of how much a wrong source would cost later.

1. **Clements-Sarama is secondary.** Level names come from the Ontario Teachers'
   Federation reproduction; the "does" lines are paraphrases from my fetch
   tool. Two levels appear twice in the reproduction (flagged in the file).
   If you have the Routledge book or an [LT]2 login, spot-check five levels:
   Corresponder, Counter (Small Numbers), Producer, Matching Comparer,
   Conceptual Subitizer to 5+. Those five carry the most weight below.
2. **Four counting findings are from memory, not read this session**:
   `cp.knower-levels`, `cp.recite-before-meaning`, `cp.procedure-before-principle`,
   and `cp.unit-task`. They are marked `provenance: memory`. They are leads,
   not citations, until someone reads the papers.
3. **One secondary report looks inconsistent.** The successor-first view is
   attributed to Carey and Barner (2019), which sits oddly with the two-year lag
   the same source reports. Read before any edge touches the successor node.
4. **ELOF progressions are paraphrased.** Goal statements are verbatim. The
   progressions are fine as content, not as quotable wording.

## 3. Findings that change the plan

**a. The floor is a question about which competencies exist, not about ages.**
Ages and grades never go on nodes (RULES 5). So "floor at what Kindergarten
assumes" decides which competencies get nodes, and the source ages go into a
pathway file. Several trajectory levels are absences, not competencies
(Pre-Counter, Chanter, Pre-Patterner, Pre +/-, Pre-Composer, Dumper). They are
never nodes at any floor.

**b. The range-merge rule absorbs much of pre-K counting into K nodes.**
Writer rule 4 merges number-range variants unless the range changes the
mathematics. Counting 5 objects and counting 20 is the same node, so most of
the counting trajectory collapses into nodes K already needs. The range changes
the mathematics in three places only:
- exact meanings of one, two, three before the cardinal principle, versus the
  cardinal principle itself (knower levels versus CP knower);
- the memorized number words through the teens, versus the decade rule that
  generates words to 100 (K.CC.A.1);
- perceptual subitizing (up to about 4, no parts), versus conceptual
  subitizing (seeing parts, then naming the whole).

**c. The successor split has dissociation evidence.** CP-knowers often do not
know that one more object makes the next number word correct
(`cp.successor-lag`). That is the strong kind of developmental evidence: it
says cardinality and successor are separate nodes, and cardinality does not
require successor. It says nothing yet about the reverse edge.

**d. This layer fills two existing holes.** `comparing.size.direct` is
referenced 9 times and `shapes.recognize` twice, but neither is written. Both
land in the pre-K strands.

**e. Fair sharing may be a route into division.** Dealing out equal shares
(Grouper and Distributive Sharer, age 4) is a candidate second route into
`division.partitive.meaning`. Under the counterfactual test it is route-only,
not required: a learner can meet partitive division from multiplication
structure without ever dealing objects. Flag for the proposers, not a decision.

**f. ELOF has no sorting goal in its math domain.** Classifying comes only from
Clements-Sarama. K needs it (K.MD.B.3 classify and count).

## 4. Candidate inventory (for scoping the floor, not nodes)

These are the distinct competencies the sources support under the preschool-band
floor, after the merges in 3b. The writer agents produce the real nodes; this
list only shows whether 40-60 is the right size. K-level nodes from the
`counting.objects` split are listed separately because they are K work.

| Strand | Candidates | Main source ids | Flags |
|---|---|---|---|
| counting | recite number words through the teens; one word per object in a line; exact meanings of small number words; cardinality (last word tells how many); produce a set of N; count sounds or actions; read numerals 0-10; match a numeral to a quantity to 5 | elof.p-math-1, 3, 5; cs.counting.reciter-10, corresponder, counter-small, producer-small; cp.knower-levels; cp.gg.abstraction | Is "produce a set of N" its own node or the assess of cardinality? |
| subitize-compare | name a small set at a glance; make a matching set without words; see parts to name a set (conceptual); judge which of two very unequal sets has more; recognize two small sets as equal; compare by one-to-one matching; compare by counting; ordinal words first to tenth | elof.p-math-2, 4; cs.subitize.*; cs.compare.* | Counting-compare with same-size versus different-size objects: one node or two? |
| operations | add and take away very small sets without words; join and count all; separate and count what is left; small add-to and take-from word problems; whole bigger than its parts; missing part within 5; deal out equal shares; make equal groups | elof.p-math-6; cs.addsub.*; cs.compose.*; cs.muldiv.* | Equal shares as a route into division (3e) |
| measurement | length as an attribute; compare two lengths directly (`comparing.size.direct`); compare weight or capacity directly; order up to five objects by an attribute | elof.p-math-8; cs.length.* | Indirect comparison is grade 1 (1.MD.A.1): stays out |
| geometry-spatial | match shapes across size and orientation; name prototype shapes; recognize non-prototype triangles and squares (`shapes.recognize`); compare shapes as same or different; build a picture from shapes that touch; position words for one's own body; mentally turn a simple shape | elof.p-math-9, 10; cs.shapes.*; cs.compshape.*; cs.cmpshape.*; cs.spatial.* | Position words: body-referenced (pre-K) versus object-referenced (K.G.A.1) are two facets |
| classify | see objects as alike; name the attribute a group shares; sort by a given attribute | cs.classify.* | Attribute Sorter and Consistent Sorter differ in reliability, not task: one node |

Count: about 38 candidates, plus 5 if patterning is in (recognize, fill a gap,
duplicate, extend, name the repeating unit). That sits at the low end of 40-60;
the writer pass will split or merge some.

K nodes the `counting.objects` split needs, written alongside this layer:
one-to-one tagging in a count (K.CC.B.4.a), cardinality at K range
(K.CC.B.4.b, probably merged with the pre-K cardinality node under 3b),
successor (K.CC.B.4.c), and the same count regardless of order or arrangement
(K.CC.B.4.b, second clause).

## 5.  Questions:
  a. Answered
1. **Floor.** Preschool band, with the roots being rote number words, perceptual
   comparison of very unequal sets, small-set naming at a glance, shape
   matching, and seeing objects as alike.
2. **Strands.** Six (in the manifest) or two (number; space and measure)? Neither, should be one, I think you will update..
3. **Patterning.** Out.
4. **Clements-Sarama access.** Book or login available? Some sources available, see sources main folder
5. **The counting.objects split.** Do it in the same pass as the pre-K layer.

## 6. Design calls made unless you object

- Trajectory and ELOF orders go into `pathways/` as two pathway files with age
  bands. They can refute edges; they never confirm one.
- Dissociation findings (3c) go on edges and nodes as `developmental`
  evidence. Ordering findings do not.
- `schema/node.schema.json` now accepts `sources.prek: [...]` holding ids from
  these files. Writers cite those ids the way K-8 writers cite `lc` ids.

## Sources

- Head Start ELOF, math (preschool): https://headstart.gov/school-readiness/article/math-preschool
- ELOF full framework PDF: https://www.govinfo.gov/content/pkg/GOVPUB-HE23_1100-PURL-gpo65456/pdf/GOVPUB-HE23_1100-PURL-gpo65456.pdf
- Clements-Sarama trajectory tables (OTF reproduction): https://www.otffeo.on.ca/en/wp-content/uploads/sites/2/2017/05/Learning_trajectories_math.pdf
- Building Blocks counting handout: https://oldsite.earlychildhoodwebinars.com/wp-content/uploads/2013/11/Building-Blocks-Learning-Trajectories-handout-Clements-Sarama.pdf
- Counting principles summary (Stanford pre-K math): https://prek-math-te.stanford.edu/system/files/media/document/2017/The%20Principal%20Counting%20Principles.pdf
- Successor-function literature review: https://arxiv.org/html/2311.15194v2
