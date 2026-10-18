# A Diagnostic Frontier for Mathematics Learning
## Architecture and research proposal

**Status:** proposal, not an implemented feature  
**Scope:** an evidence-based diagnostic layer built on the math-dag knowledge graph  
**Intended learners:** primarily elementary and middle-school learners, with the architecture extendable across pre-K–12  
**Core question:** Given what a learner has demonstrated so far, what mathematical capability is plausibly within reach next, what may be blocking it, and what evidence would help us tell?

---

## 1. Executive summary

math-dag currently aims to represent school mathematics as an explicit, inspectable structure: what there is to learn, which capabilities may be prerequisites for others, why each dependency is proposed, and how particular curricula order the material. This proposal describes a separate diagnostic layer that uses that graph to estimate a learner's present capabilities and identify a **learning frontier**.

The frontier is not a grade level, a single score, or a claim that a graph can infer a child's mind. It is a ranked but uncertainty-aware set of candidate targets, possible prerequisite gaps, and useful next observations. It should distinguish:

1. **Likely-ready targets:** capabilities the learner has not yet demonstrated but whose prerequisite conditions appear supported.
2. **Blocked targets:** desired capabilities for which one or more plausible prerequisite gaps remain.
3. **Ambiguous diagnoses:** cases where multiple explanations fit the available response evidence.
4. **Partial or representation-specific mastery:** capabilities demonstrated in some forms, contexts, or levels of formality but not others.

The proposal separates five layers:

1. **Knowledge graph:** claims about mathematics and prerequisite routes.
2. **Assessment model:** tasks and the capabilities or misconceptions their responses can help distinguish.
3. **Learner state:** evidence-backed estimates of what this learner can do, including uncertainty.
4. **Frontier engine:** candidate next targets, likely blockers, and the best next diagnostic question.
5. **Validation layer:** tests of whether the graph and diagnosis predict responses and help instruction.

The central architectural rule is non-negotiable:

> Mathematical dependency, demonstrated learner performance, inferred readiness, and recommended instruction must remain separate objects.

The graph may propose that capability A supports capability B. It cannot, by itself, establish that a particular child has A, lacks A, is ready for B, or will benefit from a particular lesson. Those conclusions require evidence and must remain open to correction.

The recommended first implementation is narrow: use a manually reviewed slice of the graph, a small item bank, and transparent learner-state estimates to test whether graph-guided diagnosis adds value. Do not begin by training a large opaque model or by collecting extensive data about children.

## 2. Why a formal graph may make diagnosis better

A conventional quiz reports which answers were right and wrong. A curriculum map reports topics and a possible order. A diagnostic frontier would connect these into a falsifiable explanation:

- Which mathematical capability does a task actually test?
- Which different capabilities could explain the observed response?
- What evidence supports or weakens each explanation?
- Which other tasks should be affected if an explanation is correct?
- What is the smallest plausible gap that blocks a particular target?
- What question would best distinguish competing explanations?
- After instruction, did the expected capability change, and did downstream predictions hold?

Formal representation is useful because it forces these claims to be named and related. It can support traceable inferences across concepts, procedures, representations, facets, and levels of formality. It can also expose places where a diagnosis rests on a disputed edge, an underspecified node, or an assessment item that tests several things at once.

This is a hypothesis about the value of the architecture, not a result already established by math-dag. The project should test whether explicit graph structure improves diagnostic quality over simpler alternatives such as raw item scores, a topic checklist, or a teacher's unaided judgment.

## 3. Terminology and formal objects

The first design task is to keep five objects distinct.

### 3.1 Mathematical knowledge graph

Let the knowledge graph be \(G=(V,E)\). A node \(v\in V\) represents a defined mathematical capability: for example, interpreting a denominator as the number of equal parts, locating a fraction on a number line, carrying out a procedure, or justifying why that procedure works.

An edge records a proposed dependency and the part of the target it supports. Nodes may differ by concept, facet, level, and type. The graph's existing OR-of-AND prerequisite structure should be retained: one target may have several sufficient prerequisite routes, and each route may require several capabilities jointly.

The graph represents claims about mathematics and learning requirements. It does not store whether an individual learner has mastered a node.

### 3.2 Assessment item model

An assessment item is an observable prompt or activity with a defined purpose. It records what the learner was asked to do, the response evidence available, the capabilities the item is intended to probe, and the limitations of the inference that can be drawn from the response.

An item may provide evidence about more than one capability, but that mapping must be explicit. A wrong answer should not automatically be treated as proof that every mapped capability is absent. Reading demand, unfamiliar notation, working memory, ambiguity, guessing, carelessness, language, accessibility, and strategy choice can affect performance.

### 3.3 Learner state

Let \(K_t\) denote the learner's latent or only partly observed state at time \(t\). It is not necessarily a single set of mastered/not-mastered nodes. A capability may be stable in one representation and fragile in another, available only with prompts, or demonstrated procedurally without conceptual explanation.

The system maintains an estimate of that state using evidence \(D_t\) collected so far. In a probabilistic formulation, it could maintain a posterior distribution \(P(K_t\mid D_t)\). A first prototype need not implement a sophisticated Bayesian model; it must, however, represent uncertainty and distinguish direct observations from inferences.

### 3.4 Readiness

For a target node \(v\), let \(\mathcal C(v)\) be its accepted prerequisite clauses. Each clause is one sufficient route. In a simple known-state model, target readiness can be defined as:

\[
R(v,K)=\mathbf 1\{\exists C\in\mathcal C(v): C\subseteq K\}.
\]

This says the target is structurally ready if at least one accepted route has its required capabilities. Under uncertainty, estimate:

\[
P(R(v,K)=1\mid D_t).
\]

This probability is meaningful only to the extent that the prerequisite clauses, item-to-capability mappings, and learner-state model are credible. It must not be presented as a calibrated fact unless calibration has been empirically tested.

The formula is not permission to multiply estimated mastery probabilities as if all capabilities were independent. Dependencies between skills and between test responses may be substantial. Compute readiness over plausible joint learner states, or begin with transparent qualitative confidence labels until a defensible joint model exists.

### 3.5 Learning frontier

The learning frontier is a set of candidate unmastered capabilities selected from the graph in relation to a learner state and a declared goal. It includes more than nodes whose prerequisites appear complete. It should expose uncertainty, possible blockers, alternative routes, and the evidence that would change the recommendation.

The frontier is not an intrinsic boundary inside the child. It is a model-based, revisable description of the next plausible instructional opportunities under the tasks, representations, and supports considered so far.

## 4. The five-layer architecture

### Layer 1 — Knowledge graph

**Purpose:** represent the mathematical territory and the project's claims about dependencies.

**Responsibilities**

- Define capabilities at an assessable grain.
- Preserve distinctions between concepts, procedures, facts, representations, justifications, and applications.
- Represent facets such as part-whole, measure, quotient, ratio, and operator interpretations of fractions.
- Distinguish concrete, representational, symbolic, and justified levels where those distinctions are mathematically meaningful.
- Encode multiple sufficient prerequisite routes instead of forcing one universal sequence.
- Give every prerequisite edge a specific rationale and identify the part of the target it supports.
- Track source, reviewer decision, confidence or evidential status, and disputed claims.
- Preserve related-but-not-prerequisite relationships separately.
- Keep curricular order and grade placement in pathways rather than treating them as properties of mathematical knowledge itself.

**Required discipline**

An edge is a hypothesis with a scope, not a general statement that one topic is useful before another. A requirement may be definitional, procedural, representational, or justificatory; a requirement imposed by a particular word problem or test format should be marked as task-specific. Evidence that a learner can acquire or demonstrate a target without a proposed prerequisite should trigger review of the edge, the node's grain, or a missing alternative route.

**Output:** a versioned graph in which each candidate diagnosis can point to the exact nodes, clauses, and edges on which it depends.

**Not this layer's job:** estimate individual mastery, rank lessons, or diagnose misconceptions from response data.

### Layer 2 — Assessment model

**Purpose:** connect observable tasks to the capabilities they can provide evidence about.

An assessment item should have a stable identifier and a specification containing:

- **Prompt and materials:** text, visual model, objects, notation, response mode, and any supports.
- **Target capability:** the node or nodes the item is designed to probe.
- **Evidence mapping:** which aspects of a response are informative about which capabilities, and how direct that evidence is.
- **Scoring rule:** what counts as correct, partially correct, incorrect, ambiguous, or not interpretable.
- **Response categories:** meaningful error patterns and strategies, not merely right/wrong, when those can be identified reliably.
- **Competing interpretations:** plausible reasons for a response, including non-mathematical sources of difficulty.
- **Prerequisite assumptions:** demands intentionally included by the item, including reading or notation demands that may confound the mathematical inference.
- **Representational variants:** concrete, visual, number-line, verbal, symbolic, or applied forms, as appropriate.
- **Evidence and review:** author, reviewer, pilot evidence, known limitations, and revision history.
- **Administration notes:** accessibility, language burden, prompting, time, and whether the item can be repeated without a practice effect.

Items should be mapped to the exact capability level and facet they probe, not just a broad concept label. For example, a symbolic fraction-comparison item may probe symbolic comparison and depend on notation interpretation; it does not automatically establish a learner's ability or inability to compare fraction magnitudes using visual models.

**Item-design rule:** whenever possible, pair a broad screening item with a follow-up item that discriminates between plausible explanations. The aim is not to make a child answer many questions. It is to ask the smallest useful set of questions that can support a responsible inference.

**Output:** an item bank whose claims about what each task measures are themselves reviewable and testable.

**Not this layer's job:** infer a complete learner profile from one response or treat a misconception label as a certain diagnosis.

### Layer 3 — Learner state

**Purpose:** represent what is currently supported by evidence about a particular learner.

The learner state must preserve at least these distinctions:

- observed response versus inferred capability;
- demonstrated mastery versus uncertain evidence;
- capability versus representation or context in which it was demonstrated;
- independent performance versus performance after prompting or scaffolding;
- current estimate versus historical evidence;
- an absent observation versus evidence of inability;
- a stable pattern versus one potentially noisy response.

The state should be updated as new evidence arrives. A robust system may need to revise earlier inferences when later evidence contradicts them. Mastery should not be permanent by default: evidence can become stale, and durable retention should be tested where relevant.

A simple implementation can start with categories such as **demonstrated**, **probable**, **uncertain**, **not yet demonstrated**, and **contradictory evidence**. These are evidence statuses, not permanent labels attached to a child. “Not yet demonstrated” is deliberately different from “does not know.”

A later implementation can estimate \(P(K_t\mid D_t)\) or use a cognitive diagnostic model. Such a model requires an explicit mapping between items and the underlying attributes they diagnose, adequate response data, and empirical checks of fit and classification quality. A sophisticated model is not automatically a better model.

**Learner privacy and boundaries**

- Store learner-specific evidence separately from the shared knowledge graph.
- Use pseudonymous learner identifiers in any research dataset and avoid placing names or sensitive records in the public repository.
- Collect the minimum information required for the stated diagnostic purpose.
- Provide a way to inspect, correct, export, and delete learner records in a deployed system.
- Do not use this prototype for high-stakes placement, special-education eligibility, grading, or other consequential decisions.
- Do not label children as inherently weak, low-ability, or incapable on the basis of the model.
- Any real study with children should use appropriate consent, privacy, safeguarding, and institutional review procedures.

**Output:** a timestamped, evidence-linked estimate of the learner's current mathematical capabilities and remaining uncertainty.

**Not this layer's job:** determine what a child ought to learn or make a diagnosis from the graph alone.

### Layer 4 — Frontier engine

**Purpose:** use the knowledge graph and learner state to generate explainable candidates for the next useful learning or diagnostic step.

For each target, the engine should consider:

1. Is the target already demonstrated?
2. Which prerequisite clauses are available in the graph?
3. Which prerequisite capabilities are demonstrated, uncertain, or not yet demonstrated?
4. Does at least one accepted route appear supported?
5. If not, what are the minimal missing capability sets across plausible routes?
6. Which missing capability explains the largest number of current difficulties without relying on weak or disputed edges?
7. What question could most efficiently distinguish the remaining hypotheses?
8. Is the target appropriate to the learner's goal, context, and attention—not merely reachable in the graph?

The engine should output a **frontier report**, not just a ranked list. Each candidate should include:

- target node and plain-language description;
- frontier category;
- prerequisite route or routes being considered;
- evidence supporting each relevant learner-state estimate;
- missing, uncertain, or conflicting prerequisite evidence;
- dependency-edge status, including any disputed or merely proposed edge;
- reason for surfacing this candidate;
- one or more next assessment prompts or instructional experiments;
- what outcomes would support or weaken the current explanation;
- a confidence description and the main reasons for uncertainty.

#### 4.1 Frontier categories

Use a modest, explicit vocabulary:

- **Likely ready to explore:** the target is unmastered and at least one accepted prerequisite route has adequate support.
- **Likely blocked:** a goal-relevant target lacks support for every currently accepted route, with one or more plausible gaps identified.
- **Needs discrimination:** several learner-state explanations remain plausible and a targeted question could separate them.
- **Partial or context-dependent mastery:** performance supports the capability in one facet, representation, level, or support condition but not another.
- **Graph uncertain:** the diagnosis depends on unresolved, disputed, or poorly evidenced prerequisite claims.
- **Insufficient evidence:** the system lacks enough reliable evidence to classify the target responsibly.

These labels must not be collapsed into a hidden score that appears more certain than the underlying evidence.

#### 4.2 Minimal prerequisite gaps

For a target with alternative OR-of-AND clauses, a minimal gap is a smallest set of currently missing or unsupported capabilities whose resolution would make at least one plausible route available. This identifies alternative ways forward rather than implying that there is only one remediation path.

Do not define a “best” gap solely as the node with the most descendants. A widely connected node may be useful, but instructional choice must also account for the learner's goal, the target task, evidence strength, effort, and the possibility that the graph is wrong.

#### 4.3 Selecting the next question

When the state is ambiguous, choose a question for its expected diagnostic usefulness, not just its difficulty. The ideal item separates plausible explanations and avoids loading too many unrelated demands into one response.

A later probabilistic version could select an item expected to reduce uncertainty across candidate learner states. In a first version, a transparent decision table is preferable: list the hypotheses, the response patterns that would favor each, and the follow-up that best distinguishes them.

#### 4.4 Instruction and diagnosis are distinct

An assessment item is not necessarily a lesson; a reachable target is not necessarily the best teaching choice. The engine may suggest a short instructional experiment, but should present the rationale as a hypothesis. It should update its learner-state estimate after the next observation rather than declaring its recommendation successful in advance.

**Output:** an explainable frontier of targets, gaps, and evidence-gathering opportunities tailored to the learner's current state and stated goal.

**Not this layer's job:** independently invent prerequisite claims, hide uncertainty, or make a consequential decision without human judgment.

### Layer 5 — Validation and monitoring

**Purpose:** determine whether the graph, item mappings, learner-state estimates, and frontier recommendations actually work.

Validation is not one metric. It has several levels:

1. **Graph validity:** Are the represented capabilities and edges mathematically and pedagogically defensible? Are alternative routes missing? Are nodes too broad or redundant?
2. **Item validity:** Do tasks elicit evidence about the capabilities they claim to measure? Can the item distinguish the intended hypotheses?
3. **State validity:** Do estimates of mastery agree with independent demonstrations and repeated observations?
4. **Diagnostic validity:** Do proposed causes predict performance on new, deliberately chosen tasks?
5. **Instructional utility:** Does acting on the diagnostic report help a learner more than a credible baseline approach?
6. **Operational and ethical validity:** Are the tool's outputs understandable, accessible, appropriately uncertain, and safe for the context of use?

A graph can pass structural checks while containing incorrect dependencies. An item bank can score consistently while measuring the wrong construct. A learner model can predict responses but still recommend inefficient instruction. Each layer needs evidence of its own.

Validation should include blinded human review of sampled edges, multiple independent reviewers where feasible, agreement and disagreement reporting, item pilots, held-out tasks, and comparison against plausible baselines. For an instructional trial, define the outcome and analysis plan before seeing the results. Avoid evaluating the system only on the same source maps or responses used to design it.

Report uncertainty, subgroup limitations, missing data, model failures, and cases where teacher judgment overrides the system. A “successful” pilot is not one in which the system always produces an answer; it is one that makes calibrated claims and exposes its own failure conditions.

## 5. Worked example: diagnosing fraction comparison

Suppose a learner answers the symbolic question “Which is larger, 1/6 or 1/8?” by selecting 1/8 and explaining that eight is greater than six.

A simple score records one wrong answer. A frontier-based system records the observation, then keeps multiple explanations alive:

- The learner may interpret the denominator as the size of the fraction rather than the number of equal parts.
- The learner may know how to partition a whole but not infer the relative size of one of its parts.
- The learner may understand the magnitude visually but not transfer it to symbolic notation.
- The response may reflect a temporary misreading, an unfamiliar prompt, or another source of noise.

The system should not immediately declare any one of these explanations true.

It could next ask the learner to compare one of six equal pieces and one of eight equal pieces of identically sized wholes, using a visual or physical model. It might then ask the learner to place 1/6 and 1/8 on a number line. Finally, if the responses support it, it returns to the symbolic comparison.

Illustrative patterns:

| Observed pattern | Plausible interpretation | Next useful step |
|---|---|---|
| Selects the larger piece correctly in a visual model but reverses the symbolic comparison | Possible transfer or notation difficulty | Compare visual, verbal, and symbolic forms while holding the mathematical relation fixed |
| Chooses the eighth as larger in both visual and symbolic forms | Possible difficulty relating the number of equal parts to part size | Explore partitioning the same whole into different numbers of equal parts |
| Answers inconsistently across repeated or equivalent tasks | Evidence is too unstable for a confident diagnosis | Use a simpler prompt, check task comprehension, and gather another independent observation |
| Answers correctly and explains why more equal parts make smaller pieces | Original response may not represent a stable misconception | Revise the earlier estimate; check retention or generalization only if useful |

These interpretations are examples, not validated diagnostic rules. A pilot should determine whether the tasks and response categories actually distinguish the proposed explanations.

The graph helps in two ways. It gives each hypothesis a distinct mathematical capability and describes which other tasks should depend on that capability. This enables a counterexample test: if a capability is reported missing, but the learner repeatedly succeeds at tasks that truly require it, the system must reconsider the learner estimate, the item mapping, the node definition, or the prerequisite edge.

## 6. Data boundaries and proposed repository structure

The public repository should contain the shared mathematical ontology, assessment specifications, schemas, synthetic examples, validation code, and aggregate research results—not identifiable child records or raw response logs.

A possible future structure is:

    diagnostics/
      README.md
      design/
        item-design.md
        learner-state.md
        frontier-rules.md
        validation-plan.md
      items/
        fractions/
          fraction-comparison-001.yaml
          fraction-unit-size-001.yaml
      examples/
        synthetic-fraction-case.yaml
      protocols/
        pilot-protocol.md
    schema/
      diagnostic-item.schema.json
      learner-state.schema.json
      frontier-report.schema.json
    tools/
      validate_diagnostic_items.py
      frontier.py
      evaluate_diagnostics.py
    tests/
      test_frontier.py
      fixtures/

This is a proposed destination, not a requirement to create all of these files at once. The first deliverable should be the design document and a small set of reviewed, synthetic examples. The main graph schema should not be changed merely to accommodate learner-specific data. Learner state should be linked to graph node identifiers and a graph version, allowing a diagnosis to be reconstructed against the exact dependency claims used at the time.

Every frontier report should record:
- graph version or commit;
- item versions and response evidence IDs;
- learner-state estimates used;
- routes and edges that affected the result;
- engine version and configuration;
- output label and explanation;
- later human corrections or outcomes, with appropriate access controls.

For public examples, use synthetic learners and invented responses. Do not commit identifiable profiles or real student records into this repository.

## 7. A staged implementation plan

### Phase 0 — Define the diagnostic contract

**Goal:** agree on what the tool is allowed to claim.

Deliverables:
- a one-page definition of frontier categories;
- explicit distinction between observed, inferred, and recommended information;
- a minimal schema for item specifications and response evidence;
- rules for disputed prerequisites and insufficient evidence;
- a statement that the prototype is not for high-stakes decisions.

**Exit criterion:** two reviewers can read the same synthetic case and identify what the system knows, what it infers, and what remains unresolved.

### Phase 1 — Build a narrow fraction pilot

**Goal:** test the architecture on a coherent, bounded region rather than the entire graph.

Choose a small set of fraction nodes covering at least two facets or representations and several genuine alternative routes. Review the relevant prerequisite edges before using them for diagnosis. Create a small set of items that distinguish specific hypotheses rather than merely sampling many curriculum topics.

Deliverables:
- reviewed node and edge subset;
- item-to-capability mappings with rationales;
- synthetic learner cases with varied evidence patterns;
- hand-constructed expected frontier reports;
- unit tests for readiness and minimal-gap logic.

**Exit criterion:** the engine produces traceable reports matching the declared rules on synthetic cases, including ambiguous cases and cases where all available edges are disputed or unreviewed. Passing these tests shows implementation consistency, not educational validity.

### Phase 2 — Implement transparent state and frontier logic

**Goal:** make the inference reproducible and inspectable before adding statistical complexity.

Begin with categorical evidence states or a transparent scoring table. Each inference must show which observations support it and which assumptions it uses. Keep graph structure, response data, and instructional recommendations separate.

Deliverables:
- learner-state update rules;
- frontier calculation over OR-of-AND routes;
- explicit handling for missing, uncertain, conflicting, and stale evidence;
- readable explanations and tests for each frontier category;
- a way for a reviewer to challenge a state estimate or prerequisite edge.

**Exit criterion:** no output calls an unobserved capability absent solely because there is no record for it; no target is called ready when the only available route relies on an unresolved prerequisite claim without disclosure.

### Phase 3 — Item and reviewer pilot

**Goal:** test whether the proposed items elicit the evidence their specifications predict.

Have independent reviewers inspect a sample of items and response interpretations. Pilot the tasks in a suitable, consented setting before drawing conclusions about children. Record administration conditions and alternative explanations for errors. Where feasible, compare items that target the same capability through different representations.

Deliverables:
- item review results and revisions;
- inter-reviewer agreement with disagreements documented;
- preliminary response-pattern analysis;
- examples where the model changed its initial hypothesis;
- an error taxonomy for ambiguous or uninterpretable responses.

**Exit criterion:** no key diagnosis depends entirely on a single untested item interpretation; limitations are documented and the next study has an explicit question.

### Phase 4 — Validate diagnoses on new tasks

**Goal:** determine whether diagnoses predict performance beyond the tasks that generated them.

For each diagnosis, pre-specify the responses expected on one or more held-out or newly designed tasks. Compare the model's predictions with observations. Include cases that challenge the graph's assumptions, not only cases that confirm them.

Compare at minimum against:
- raw accuracy or a topic checklist;
- a baseline prerequisite model with simpler assumptions;
- independent educator judgment, collected without exposing the model output where feasible.

Report calibration where probabilistic estimates are made, false positive and false negative diagnoses, uncertainty, and the proportion of cases in which the correct result is “insufficient evidence.” If the system confidently predicts prerequisite gaps that do not appear on independent tasks, revisit the graph and item mappings.

**Exit criterion:** the proposed diagnostic layer demonstrates incremental predictive value or the project narrows its claims accordingly.

### Phase 5 — Test instructional utility

**Goal:** establish whether using the frontier helps a learner, not merely whether the model can label responses.

Compare graph-guided instruction with a credible alternative, such as a teacher's normal diagnostic process or a conventional item-score report. Choose outcomes in advance: improvement on target tasks, transfer to new tasks, retention after a delay, time to mastery, or another justified measure. Consider the burden on teachers and learners as well as learning outcomes.

Do not claim instructional effectiveness from a demonstration, a few success stories, or a higher predicted readiness score. A learner can improve for reasons unrelated to the graph; the evaluation design must support the claimed conclusion.

**Exit criterion:** evidence shows an educational benefit, or a clear reason why the system should be redesigned before broader use.

### Phase 6 — Expand carefully

Only after the narrow pilot performs well should the system expand to more topics, representations, age ranges, or adaptive item selection. Broader coverage adds complexity: a larger graph can introduce more disputed edges, item mappings, and interaction effects, not merely more opportunities for useful diagnosis.

Expansion should be governed by observed reliability and utility, not by node count.

## 8. Validation metrics

Use several metrics and always state which layer each metric evaluates.

### Graph and item quality
- proportion of sampled prerequisite edges accepted, revised, disputed, or rejected by blinded reviewers;
- reviewer agreement and the substantive reasons for disagreement;
- frequency of missing alternative routes and overly broad or redundant nodes;
- item review results and consistency of response interpretation;
- evidence that items differentiate intended competing hypotheses.

### Learner-state quality
- agreement with independent demonstrations of the same capability;
- stability across comparable tasks and reasonable time intervals;
- sensitivity to representation, context, prompting, and item difficulty;
- false mastery claims and false gap claims;
- calibration and uncertainty quality if probabilistic estimates are reported.

### Frontier quality
- proportion of proposed ready targets for which the learner succeeds on independent target tasks;
- proportion of identified gaps supported by follow-up evidence;
- accuracy of predicted response patterns on held-out tasks;
- frequency of appropriate abstentions or “insufficient evidence” reports;
- value of the next selected question, measured by whether it actually reduces ambiguity.

### Instructional utility
- gains on target skills and transfer tasks compared with a baseline;
- retention after a defined interval;
- time and number of items required to reach a reliable diagnosis;
- teacher and learner usability;
- equity and accessibility checks, with subgroup conclusions made only when sample size and study design support them.

No single composite score should conceal trade-offs. In particular, a system that recommends many targets may appear useful while creating excessive false-ready predictions; a system that abstains on every difficult case may avoid errors but offer little value.

## 9. Risks and design constraints

### The graph may encode an incorrect prerequisite

A logically neat graph is not necessarily a valid account of how children learn. Keep prerequisite status and evidence strength visible. Use independent review and counterexample tests; allow the system to say that the graph is uncertain.

### Assessment tasks can confound several capabilities

A word problem may require reading comprehension, contextual knowledge, notation, and arithmetic. The model must not interpret every failure as a mathematical deficit. Include task demands and plausible non-target explanations in the item specification.

### Binary mastery is often too crude

Success is affected by context and support. A node may need separate facets, levels, or representation-specific variants. Split nodes when that changes a meaningful instructional decision, but do not proliferate nodes just to fit every item.

### A readiness prediction is not a promise of learning

The graph may suggest that prerequisites are available; it cannot guarantee that the learner will understand the target without instruction. Readiness is a reason to try an instructional step, not a certification that it will work.

### Adaptive testing can become overconfident

A system that chooses only questions consistent with its current diagnosis may reinforce its own mistakes. Deliberately sample disconfirming evidence, keep some independent checks, and permit a human to request another route or representation.

### Optimization can harm the learning process

Maximizing the number of unlocked nodes may push toward narrow test performance at the expense of explanation, curiosity, confidence, or productive exploration. The frontier should be a decision aid, not an automatic curriculum or a measure of a child's worth.

### Bias and accessibility require active testing

Items and response interpretations may behave differently across language backgrounds, disabilities, familiarity with classroom conventions, and access to materials. The project should measure these effects where appropriate and avoid making claims for populations not represented in validation.

### Explanations must reveal evidence, not just graph paths

“B is recommended because A is a prerequisite” is inadequate if the learner has not been assessed on A or if the edge is disputed. Reports should say whether A was observed, inferred, or not observed, and disclose how strongly the edge is supported.

## 10. Success criteria and explicit non-goals

The project succeeds initially if it can:

1. Generate reproducible candidate frontiers from a reviewed graph and a transparent learner state.
2. Explain each recommendation in terms of exact prerequisites, clauses, evidence, and uncertainty.
3. Distinguish absence of evidence from evidence of absence.
4. Produce a useful follow-up question when multiple explanations remain plausible.
5. Identify cases where the graph itself—not the learner—is the likely source of a bad inference.
6. Predict independent task performance better than a simple baseline, once that claim is tested.
7. Eventually demonstrate that graph-guided diagnosis improves instructional decisions or learning outcomes.

The initial project is **not** intended to:
- determine a child's ability or potential;
- assign an immutable developmental stage;
- infer a grade level from isolated responses;
- prescribe a fixed curriculum for every learner;
- replace teachers, tutors, or professional assessment;
- use an unvalidated model for high-stakes decisions;
- treat curriculum order as proof of mathematical necessity;
- treat a passing structural checker as evidence of pedagogical correctness.

## 11. Immediate next actions

The next practical work should be deliberately small:

1. **Freeze a fraction diagnostic slice.** Select a manageable set of reviewed nodes and prerequisite clauses, and record unresolved edge claims rather than silently treating them as true.
2. **Define five to ten assessment items.** Each item should target a clear capability and be chosen to discriminate among a short list of plausible hypotheses.
3. **Write synthetic cases first.** Include clear mastery, partial mastery, contradictory responses, representation-specific competence, and insufficient evidence.
4. **Specify expected reports manually.** Before implementing the engine, write what a responsible diagnostic report ought to say for each synthetic case.
5. **Build rule-based frontier logic.** Calculate supported routes and minimal gaps, trace every conclusion to its evidence, and test the edge cases.
6. **Invite independent review.** Ask reviewers to challenge both the prerequisite claims and the inferences from item responses.
7. **Pilot and evaluate before expanding.** Treat the first data as a test of the design, not as proof of the system.

### First concrete deliverable

A small, auditable demo should take as input:
- a pinned version of a reviewed math-dag subgraph;
- one synthetic learner's observations on the fraction item set;
- the item-to-node mappings and scoring rules.

It should return:
- demonstrated and uncertain capabilities;
- a frontier with clear categories;
- candidate prerequisite gaps and alternative routes;
- the next question most useful for distinguishing remaining hypotheses;
- the exact evidence and graph claims behind each result;
- a list of conditions under which the system should abstain or revise its diagnosis.

This is enough to test the architecture without prematurely committing to a large adaptive platform or an elaborate statistical model.

## 12. The governing principle

The frontier should not be conceived as a line the child is either behind or ahead of. It is a set of evidence-supported opportunities, blocked paths, and unresolved questions.

The graph contributes a formal map of possible mathematical dependencies. The assessment model turns responses into bounded evidence. The learner state tracks what that evidence supports. The frontier engine uses these pieces to propose next steps. Validation determines whether those proposals deserve trust.

Keep these roles separate, and the system can make claims that are traceable and falsifiable. Collapse them, and the system risks turning a graph of mathematical ideas into an unjustified story about a child's mind.

The research question is therefore not simply whether mathematics can be represented as a graph. It is whether a reviewed graph, joined to carefully designed assessment evidence, can identify the next useful learning opportunity more accurately, efficiently, and transparently than simpler diagnostic approaches.

That is the claim this proposal recommends testing.
