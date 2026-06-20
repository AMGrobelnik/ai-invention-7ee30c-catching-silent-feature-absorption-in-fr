# gen_paper_text — test_idea

> Phase: `invention_loop` · round 2 · Substep: `gen_paper_text`
> Run: `run__C1-INh1YNGn` — Catching Silent Feature Absorption in Frozen Sparse Autoencoders: Label-Free Loc
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave the agent(s) in this substep — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_paper_text` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-06-17 17:32:27 UTC

````
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: A research paper writer (Step 3.4: GEN_PAPER_TEXT in the invention loop)

You received the hypothesis, all artifacts, the previous paper draft (if any), and reviewer feedback.
Write a complete paper draft with figure placeholders.

Publication-quality paper → strong contribution. Weak paper → wasted iteration.
</your_role>
</ai_inventor_context>

<research_methodology>
Write like a researcher drafting a paper, not a chatbot summarizing bullet points.

- Structure as a paper would: research question → methodology → results → analysis → limitations. Not a list of "we did X, then Y."
- Ground every claim in specific artifacts and specific numbers. "Results show improvement" is empty — state effect sizes, baselines, and conditions.
- Be honest about what worked, what didn't, and why. Don't spin failures as "future work."
- The paper's headline contribution should be a positive or surprising finding. Negative results are valuable context but should not be the primary narrative — lead with what works.
- Address reviewer feedback from previous iterations explicitly — show you've thought about each critique.
</research_methodology>

<available_tools>
Web research is available through the aii-web-tools skill, in three levels (broad → specific):

1. web search — Returns titles, URLs, snippets. Use first to discover and scan the landscape.
2. web fetch — Reads a page and returns its content as markdown (HTML or PDF). Use to understand a source. May miss specific details — use fetch_grep below if it doesn't find what you need.
3. fetch_grep — Regex search over a page/PDF's full text. Returns exact matching sections with context. Use for precise details, exact numbers, methodology, or PDFs.

Workflow: search → fetch (understand) → fetch_grep (extract specifics).
</available_tools>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<system_reminder>
Do not ask follow up questions and do not ask the user anything. Execute all steps independently.
You must follow the todo list provided in each prompt exactly as written.
No placeholders, stubs, or incomplete code — all code must be complete and functional.
</system_reminder>

<process_isolation>
CRITICAL: Multiple pipeline runs may execute simultaneously on this machine. `ps aux | grep method.py` matches ALL runs, not just yours.
- NEVER kill processes by name (`killall`, `pkill -f`, `ps aux | grep ... | xargs kill`). This kills OTHER runs' processes.
- NEVER monitor processes by name (`ps aux | grep method.py`). You will see other runs' processes and get confused.
- ALWAYS use PID-based process management:
  Run: `uv run method.py & PID=$!` or `timeout <seconds> uv run method.py & PID=$!`
  Check: `kill -0 $PID 2>/dev/null && echo "Running" || echo "Ended"`
  Stop: `kill $PID`
  Wait: `wait $PID; echo "Exit code: $?"`
  Monitor: `tail -f logs/run.log & TAIL_PID=$!` then `kill $TAIL_PID` when done
</process_isolation>

<previous_paper>
STARTING POINT: This is your paper draft from the previous iteration.

# Introduction

Sparse autoencoders (SAEs) have become a standard tool for decomposing the activations of large language models (LLMs) into a dictionary of sparsely-activating latents that are intended to be interpretable, monosemantic units of analysis [1, 2, 3]. The promise is operational: a latent that reliably tracks a human concept can be read off as a classifier, flipped as a steering knob, or compared across model variants for model-diffing. Public SAE suites such as Gemma Scope [3] now expose millions of such latents on open models, making this a practical interface for safety-relevant interpretability.

The promise is undercut by a now well-documented fact: *single SAE latents are not reliable units*. Three failure modes recur. *Feature splitting* fragments one concept across many latents, so no single latent captures it [4]. *Feature absorption* is more insidious: a more specific child latent suppresses the firing of a more general parent latent, leaving the parent with unpredictable holes on exactly the sub-contexts the child covers; parent and child are mutually exclusive in firing [5, 6]. *Feature hedging* merges correlated features into a single polysemantic latent in narrower SAEs [6]. The aggregate verdict of the field is stark: SAEs do not find canonical units of analysis [4], and on concrete downstream tasks plain difference-of-means probes routinely beat raw-latent SAE methods [7, 8]. Any method that proposes SAE latents as a knowledge representation must therefore clear strong, simple baselines and must address splitting and absorption head-on.

The task is hard because the obstacles defeat the obvious instruments *by construction*. The intuitive fix for an unreliable single latent is to group several latents into a cluster-level unit. But every existing post-hoc grouping signal is *observational*: which latents fire together (co-activation feature families [9, 11]) or which decoder directions point alike (geometry). Absorption is precisely the regime where observational signals must fail — the parent and the absorbing child are mutually exclusive in firing, so co-activation can never group them, and their decoders need not be cosine-similar [5]. The standard *supervised* remedy, selecting the top-N latents by causal effect on a concept probe (SCR/TPP attribution [9, 10]), is no better: a latent that fires only in a narrow sub-context has low *marginal* attribution and is silently dropped, even though it carries the concept there. The latents one most needs are exactly the ones these instruments discard.

Why has this not been solved? Recent architectural remedies — Matryoshka SAEs [15], hierarchical SAEs [16], Subspace-Aware SAEs [14], and concept-bottleneck variants — all *retrain* the SAE to reduce splitting and absorption at training time. They do not help a practitioner holding a frozen public SAE, and none produces a human-auditable multi-member unit over an existing dictionary. We take the opposite stance: a *training-free, post-hoc repair of frozen public SAEs*. The methodological gap we fill is the *grouping operator*. We observe that grouping by *interventional co-response* — how latents jointly track a content counterfactual, rather than how they co-fire at baseline — is the matched instrument, and that this idea has a direct precedent in systems biology, where differential co-expression methods (DiffCoEx, WGCNA [19, 20]) cluster genes by correlated response to a perturbation precisely because co-regulated genes are often not co-expressed at baseline. Crucially, correlation is the right operator only for the *shared-support* splitting case. Absorbers respond on *disjoint* supports and have low pairwise correlation, so no affinity-merging clustering can even propose the right group. The disjoint-support case is a *maximum-coverage* problem, whose classic greedy solution [22, 23] is the natural — and, we argue, the only correct — proposer for absorption units.

We introduce **Two-Track Co-Response Grouping (CCRG)**. Given a frozen SAE and, per concept, a set of content-flip minimal pairs, CCRG (1) computes a per-latent interventional content-response; (2) a *C-track* clusters content-responsive latents by positive response correlation into Leiden communities, recovering split families; (3) a *K-track* anchors on the highest-recall latent and greedily adds mutually-exclusive latents that cover its holes, recovering absorbers; (4) reconciles the two into one de-duplicated output; and (5) admits a unit only if it clears a co-response signature and a unit-level surface-invariance check against matched null distributions. The output is a set of auditable units plus a feature-level knowledge graph of specialization edges. The present paper establishes the method, the structural argument for why both tracks are needed, and a measured empirical anchor from four constructed testbeds; we are explicit (Section 6) that the SAE-grouping evaluation itself is fully specified and pre-registered but not yet executed, and we report the diagnostic analyses that *can* be measured without it.

[FIGURE:fig1]

**Summary of contributions.**

- **A two-track grouping algorithm (Section 3).** A concrete, training-free procedure that proposes split families by content-response correlation (C-track) and absorption units by an anchored greedy set-cover (K-track), reconciles them, and filters them with a single null-anchored admission rule. To our knowledge, maximum-coverage set-cover has never been used to group SAE latents, and it is exactly the operator the disjoint-support absorption regime requires.
- **A structural argument that both tracks are necessary, with measured evidence (Section 5.1).** We show analytically that observational co-activation and marginal-attribution selection cannot recover absorbers, and we measure, in real safety-attribute data, that both the shared-support and disjoint-support regimes co-occur: civil_comments toxicity sub-attributes split into a shared cluster (insult-obscene label Jaccard 0.245) and disjoint specialists (threat max off-diagonal 0.044).
- **A non-circular evaluation design (Section 4).** A supervised absorption diagnostic is used *only* to score already-formed specialization edges, never to form units. Anchors are chosen by content-response recall available to every baseline, so "the unsupervised unit beats the supervised oracle" is not undercut.
- **Four frozen testbeds and a pre-registered, powered protocol (Sections 4-5).** 109,754 examples across first-letter spelling, a novel non-spelling absorption hierarchy, toxicity, sentiment and aspect, eleven baselines, and an a-priori power analysis (n_min = 150), with honest-null fallbacks for every load-bearing claim.

# Related Work

**SAEs and the unreliability of single latents.** Sparse dictionary learning on LLM activations yields interpretable features [1, 2, 3], but a growing body of work shows that individual latents are not canonical units [4]. Chanin et al. introduce and quantify *feature absorption*, in which a specific child latent suppresses a general parent's firing, demonstrated on first-letter spelling [5], and *feature hedging*, a correlated-feature failure that is worse in narrower SAEs [6]. Dense-latent and hierarchical analyses corroborate that single-latent semantics are unstable [16, 17]. Benchmarks make the practical cost concrete: AxBench finds difference-of-means the strongest concept-detection method and raw-latent SAE methods uncompetitive [8], and SAEBench standardizes absorption, sparse-probing, and targeted-erasure evaluations [7]. We deliberately do not stake our load-bearing claim on out-classifying a strong dense probe; our central comparison is against SAE-*selection* baselines.

**Post-hoc grouping of SAE features.** Prior grouping is observational: co-activation "feature families" [11], sparse feature coactivation modules [12], and decoder-geometry or graph-regularized clusters group latents by what fires together or which decoders align. Domain-filtered knowledge graphs from SAE features [13] likewise build edges from co-occurrence and geometry. By construction these signals cannot group an absorbed parent and child, which are mutually exclusive in firing; we therefore count-match observational clusters to our unit's size in the classification comparison so that any win reflects *selection*, not capacity, and we use the opposite, interventional signal.

**Supervised latent selection.** SHIFT and the SCR/TPP family rank individual latents by causal effect on a concept probe and ablate the top-N [9, 10]. A latent that fires only in a narrow sub-context has low marginal attribution and is silently dropped — the exact gap our co-response set-cover fills. We use SCR/TPP-style ranking as our oracle-pool baselines, noting that recent audits caution these benchmarks are imperfect ground truth [18].

**Architectural remedies.** Matryoshka [15], hierarchical [16], subspace-aware [14], and concept-bottleneck SAEs modify training to reduce splitting/absorption. They are orthogonal to our setting: we repair a *frozen* public SAE post-hoc and emit an auditable knowledge graph rather than retraining a dictionary.

**Cross-field instruments.** The C-track imports differential co-expression module discovery (DiffCoEx [19], WGCNA [20]) and Leiden community detection [21]; the K-track imports the maximum-coverage / set-cover greedy with its (1-1/e) guarantee [22, 23]. The supporting robustness analysis engages the label-free worst-group-robustness literature — group-DRO [24], JTT [25], GEORGE [26], EIIL [27], LfF [28], Diverse Prototypical Ensembles [29], and group-aware priors [30] — which infer groups over *examples* and *retrain*; CCRG instead groups *features*, never retrains, and the recovered absorbers *are* the inferred sub-context specialists. Surface-invariance draws on LEACE concept erasure [31] and counterfactual invariance [32]; minimal-pair supervision draws on counterfactually-augmented data [33], CEBaB [34], and ParaDetox [35]. The closest "cluster counterfactual differences" template is CDLC in vision, which clusters diffusion-counterfactual difference vectors into one direction per class [38]; we cluster discrete LLM SAE latents into multi-member units and add a set-cover track for which CDLC has no analogue.

# The Two-Track Co-Response Grouping Method

## Preliminaries and notation

Let the frozen SAE have latents indexed by $l \in \{1,\dots,L\}$, with encoder activation $a_l(x)$ for input $x$; a latent *fires* on $x$ iff $a_l(x) > 0$ (Gemma Scope SAEs use a JumpReLU, so the threshold is applied inside the encoder) [3]. For a concept $c$ we are given a set $P$ of *content-flip minimal pairs* $(x_{\text{off}}, x_{\text{on}})$ in which the concept is absent/present and surface form is matched, plus *surface-flip pairs* in which the concept is held constant and surface varies. The same content labels are the supervision every matched baseline consumes; the method uses no absorption-specific oracle. We encode at a single residual-stream site (Gemma Scope `gemma-2-2b`, layer 12, width 16k canonical, hook `blocks.12.hook_resid_post`, $d_{\text{model}}=2304$, 16{,}384 latents) [3, ART1].

## Step 1: interventional content-response

For each latent $l$ and pair $p=(x_{\text{off}},x_{\text{on}})$, the *content-response* is $r_l(p) = a_l(x_{\text{on}}) - a_l(x_{\text{off}})$, assembled into a matrix $R \in \mathbb{R}^{L \times |P|}$. We retain only *content-responsive* latents whose mean response exceeds the 95th percentile of a within-concept on/off shuffle null, leaving a candidate pool of a few hundred. Each latent's *cover set* is

$$C_l = \{\, p \in P : r_l(p) > \tau_{\text{resp}} \;\wedge\; a_l(x_{\text{on}})>0 \;\wedge\; \text{precision}_l \ge 0.7 \,\},$$

the pairs whose content flip latent $l$ reliably and precisely tracks, where $\text{precision}_l$ is the content-response precision on $l$'s own firing support. Cover sets are the objects the two tracks operate on; "complementary coverage" is defined only relative to a concrete anchor's hole set, never as a vague affinity between arbitrary latents.

## Step 2: C-track — correlation communities for splitting

Where a concept *splits*, its sub-latents share firing support and co-respond positively to the content flip; pairwise affinity is therefore appropriate. We build a sign-aware soft-thresholded affinity from the positive part of the Spearman correlation between response profiles, $A^{C}_{l,l'} = \max(\rho(r_l, r_{l'}), 0)^{\beta}$ with $\beta=6$ following WGCNA's scale-free criterion [20], threshold it into a graph, and run Leiden community detection (RBConfiguration partition) [21]. The resolution and community count are fixed by bootstrap-ARI stability against the shuffle null, not hand-tuned [ARTIFACT:art_RidEJtBC7gPT].

## Step 3: K-track — anchored greedy set-cover for absorption

Absorbers respond on *disjoint* supports and are mutually exclusive in firing with their parent, so their pairwise content-response correlation is low and no affinity-merging clustering can propose them. We therefore use a different operator — an anchored greedy maximum-coverage procedure.

1. **Anchor.** Set the anchor to $l^\* = \arg\max_l |C_l|$ over content-responsive latents — the highest-recall "general/parent" candidate, chosen using *only* $P$ and *not* the absorption diagnostic, with ties broken toward the broadest, lowest-entropy firing support.
2. **Holes.** $H = P \setminus C_{\text{anchor}}$ are the pairs the parent goes silent on — exactly the absorbed sub-contexts.
3. **Greedy cover.** While $H$ is non-empty and improving, add $\arg\max_l |C_l \cap H|$ subject to mutual exclusivity with all current members (pairwise firing Jaccard $< 0.1$), per-member precision $\ge 0.7$, and a marginal coverage gain $|C_l \cap H|/|P| \ge 0.05$ whose bootstrap CI excludes 0 (a small-$k$ effect-size floor); then set $H \leftarrow H \setminus C_l$.

The output unit $\{\text{anchor}, \text{absorber}_1, \dots\}$ has members that are mutually exclusive in firing, individually precise, and jointly cover the concept's content flips. The greedy max-coverage choice is the classic instrument for "cover a universe with complementary specialists," with the standard $(1-1/e)$ approximation guarantee [22, 23]; coverage-complementarity is a set-level property, which is exactly why a pairwise operator cannot express it. By construction the K-track surfaces, e.g., $\{$general "starts-with-L" latent, "lion"-absorber, "London"-absorber$\}$: the anchor has the holes and the greedy step fills them with the disjoint specialists.

[FIGURE:fig3]

## Step 4: reconciliation

We merge the two tracks into one output. For each C-community we designate its highest-recall member as a candidate anchor and run the Step-3 augmentation to pull in mutually-exclusive absorbers covering that community's holes; we also seed Step 3 from standalone high-recall latents that sit in no dense community. A final unit is therefore a pure C-community (splitting), a pure K-cover (absorption), or a hybrid. We de-duplicate by assigning each latent to its highest-coverage-gain unit.

## Step 5: admission filter

A proposed unit is admitted iff it clears **signature C** (within-unit mean content-response correlation above the 95th-percentile shuffle null) **or signature K** (pooled-max content-response AUC minus best-single-member AUC above the 95th percentile of a best-of-random-$k$ null *matched on marginal content-response AUC*, plus the $k\in\{2,3\}$ absolute gain floor of $0.05$ with bootstrap CI excluding 0, plus mutual exclusivity and the precision floor), **and** unit-level surface invariance (pooled surface-response not above the shuffled-surface null). We report the cleared signature per concept and the false-admit rate under *both* the all-latent and the matched random-$k$ nulls, with a target of $\le 0.05$. The admission rule *filters* what the two-track proposal step *generates*; it is downstream of a proposer that can actually produce K-units, which a filter-only method cannot.

## Tier-0 proposal-step pilot

Before any absorber-recovery claim relies on the K-track, a never-dropped pilot runs Step 3 on first-letter content-flip pairs *alone* and checks that the proposed anchor and absorbers match the parent and absorbers the supervised diagnostic of Chanin et al. [5] identifies (membership precision/recall above a random-membership null). If the proposal step cannot recover the known unit, the K-track is reported as *failing at proposal time* — an honest, informative negative rather than a silent omission.

## Auditable units and the feature-level knowledge graph

Each admitted unit is emitted with human-readable member definitions (logit-lens tokens and top conditioning contexts) and *directed specialization edges*: a member responsive only within a sub-context is an absorbed/split child of the unit's anchor. The edge set is a feature-level knowledge graph whose edges encode conditioning environments invisible to observational co-occurrence [13]. We operationalize auditability as a *measured* repair loop (Section 4): locate an under-served sub-context, read the graph to find the covering absorber, add it, and measure the recall recovery against a random-addition control.

# Testbeds and Evaluation Protocol

## Constructed testbeds

We built four frozen, schema-standardized testbed families (Table 1) totalling 109,754 examples in twelve dataset groups. All are pure text/data artifacts; no SAE or model weights are baked in, so absorption presence is an empirical question for the SAE run, not an artifact of construction. Words for the spelling and non-spelling hierarchies are anchored in the real `gemma-2-2b` vocabulary and a pinned Pile revision, so they never derive from the SAE latents being grouped (non-circular). The first-letter testbed contributes 17,180 examples over five letters (L/O/T/I/D), with content-flip pairs, surface-flip pairs, and a 12,500-window diagnostic corpus; its deterministic flip/span check reports 0 violations across all 17,180 rows [ARTIFACT:art_dpYpjSn2Xvg3]. The non-spelling testbed contributes 24,128 examples over a numeric-quantity hierarchy (parent "numeric token"; absorbers year/percent/currency/date/decimal/integer/comma/ordinal) and a taxonomic "is-a-country" hierarchy [ARTIFACT:art_t2uUbjSwpd3t]. The toxicity family contributes 37,707 examples from ParaDetox (human toxic-neutral content pairs) [35] and civil_comments (binary toxicity plus six frozen sub-attribute labels) [36], the sub-attribute floats serving as independent sub-context labels [ARTIFACT:art_8QO7pl6Pd8UQ]. The supporting family contributes 30,739 examples of CAD-IMDB sentiment [33], CEBaB restaurant aspect-sentiment [34], and a pre-registered bias_in_bios boundary-null [37] [ARTIFACT:art_21JWypIydPMX].

\begin{table}[t]
\centering
\small
\caption{Constructed testbeds. All counts are examples in the released artifacts; pairs are reconstructable minimal pairs. Roles: LB = load-bearing, NS = never-dropped non-spelling spine, SP = supporting, BN = boundary-null.}
\begin{tabular}{lllrl}
\toprule
Family & Source & Concepts & Examples & Role \\
\midrule
First-letter spelling & Pile + gemma vocab & 5 letters (L/O/T/I/D) & 17{,}180 & LB \\
Non-spelling absorption & Pile + templates + LLM & numeric (8 sub), taxonomic (countries) & 24{,}128 & NS \\
Toxicity & ParaDetox, civil\_comments & toxicity + 6 sub-attributes & 37{,}707 & LB \\
Sentiment / aspect / bias & CAD-IMDB, CEBaB, bias\_in\_bios & sentiment, food/service, 28 professions & 30{,}739 & SP / BN \\
\midrule
\textbf{Total} & & 12 dataset groups & \textbf{109{,}754} & \\
\bottomrule
\end{tabular}
\end{table}

## Baselines

The evaluation compares CCRG units against eleven baselines (Table 2), spanning raw latents, observational clusters (count-matched for the classification comparison), dense probes (including a LEACE surface-invariant hyperplane), supervised oracle pools, and label-free / oracle group-robustness probes. The design isolates *selection at matched pool size*: against the count-matched marginal-attribution pool (h), all three of unit, (g), and (h) pool the same number of directions and vary only *how* members are chosen.

\begin{table}[t]
\centering
\small
\caption{Baseline glossary. (b)/(c) are count-matched to the unit's member count $k$ for the classification comparison; (h) is count-and-pool-matched to isolate the selection criterion.}
\begin{tabular}{cl}
\toprule
ID & Baseline \\
\midrule
(a) & Best raw single latent (held-out AUC/F1) \\
(b) & Observational co-activation / feature-family clusters, count-matched to $k$ \\
(c) & Decoder-geometry (cosine) clusters, count-matched to $k$ \\
(d) & Counterfactually-matched difference-of-means \\
(e) & Counterfactually-matched linear probe \\
(f) & Surface-invariant matched probe (LEACE-erased surface direction) — the conceded single dense hyperplane \\
(g) & Supervised oracle pool: top-$N$ latents by SCR/TPP attribution \\
(h) & Count-and-pool-matched probe: max-pool over exactly $k$ SCR/TPP-selected raw directions \\
(i) & Unmatched difference-of-means / probe on raw labels \\
(j) & Oracle group-DRO probe with true sub-context labels — robustness upper bound \\
(k) & Label-free group-inference probe (JTT/GEORGE-style), no sub-context labels \\
\bottomrule
\end{tabular}
\end{table}

## Non-circularity and the absorption diagnostic

Specialization edges are scored — never formed — by the absorption diagnostic of Chanin et al. [5], verified against the authoritative `sae-spelling` implementation: the parent latent is the one whose encoder direction has maximal cosine with a logistic-regression probe, and an absorber is a latent whose ablation most shifts the concept signal, with decision thresholds (decoder-probe cosine $\ge 0.025$, ablation gap $\ge 1.0$) valid for layers 0-17 [ARTIFACT:art_I2MrezW41iQo]. Because the strict form depends on an output logit, we adopt the *form-free* variant the original work gives in its appendix and SAEBench implements as `absorption_fraction`: latent $l$ absorbs iff $\tau_c < (\hat{a}_l \cdot d_p)/(a \cdot d_p)$, where $\hat a_l$ is the latent's decoder contribution and $d_p$ is a parent-concept probe direction trained on data *disjoint* from clustering [ARTIFACT:art_I2MrezW41iQo]. The form-free version needs no output logit, works at all layers, and is domain-agnostic — essential for the non-spelling hierarchy. A literature triangulation across the original work, SAEBench, and the Matryoshka/H-SAE mitigations confirms that absorption is empirically documented *almost exclusively on first-letter spelling* [5, 7, 15, 16]; the non-spelling testbed is therefore both a generality test and a genuinely novel empirical test, gated by an explicit non-triviality pre-check (parent recall $\ge 0.60$; at least one absorber with firing-Jaccard $<0.10$, precision $\ge 0.70$, and hole-coverage gain $\ge 0.05$ with bootstrap CI excluding 0) and an honest-null fallback that scopes the absorption claim to spelling if no specialist-filled holes exist [ARTIFACT:art_I2MrezW41iQo].

## Statistics and power

The primary statistical object is the per-concept / within-family paired bootstrap CI ($B=10{,}000$ on per-example correctness differences), with an exact McNemar confirmatory; the cross-family number is descriptive only, because between-cluster variance is not estimable over three to four families. For the central unit-minus-(g)/(h) worst-sub-context-recall gap we pre-register the gap's sign and its *slope* against measured sub-population reweighting magnitude. An a-priori minimum-detectable-effect analysis, $n \approx 7.84\,[p_1(1-p_1)+p_2(1-p_2)]/\Delta^2$, gives roughly 91, 167, and 384 positives for $\Delta = 0.20, 0.15, 0.10$; we pre-register $n_{\min}=150$ positives per tested under-served sub-context and stratify collection to reach it, reporting rarer sub-contexts descriptively. Multiplicity across claims is controlled by Holm-Bonferroni [ARTIFACT:art_RidEJtBC7gPT].

## Pre-registered result grid

Table 3 states the load-bearing and supporting claims, what each is compared against, the predicted direction, and what each isolates. The load-bearing core (C1 classification at matched pool size; C3 absorber-recovery against the supervised oracle on two hierarchies) is measured against SAE-*selection* baselines, so it does not depend on out-classifying a strong dense probe. Every row has a pre-registered honest-null reading.

\begin{table}[t]
\centering
\small
\caption{Pre-registered evaluation grid. Predictions are hypotheses to be tested in the SAE-grouping run (Section 6), not measured results.}
\begin{tabular}{p{3.1cm}p{3.0cm}p{3.0cm}p{3.4cm}}
\toprule
Claim (role) & Compared against & Predicted sign & What it isolates \\
\midrule
C1 classification (core) & (b)/(c) clusters cut to $k$ members & unit $>$ matched (b)/(c) & co-response selects the right $k$ members \\
C3 absorber-recovery, first-letter (core) & (g) oracle pool; (h) count-matched; diagnostic [5] & unit $>$ (g)/(h); edges agree & co-response admits the absorber attribution drops \\
C3 absorber-recovery, non-spelling (core) & (g)/(h); form-free diagnostic & unit $>$ (g)/(h) if absorption present; else scope-null & absorption is general, not a spelling artifact \\
C2 + selection isolation (support) & (f); (g)/(h) & (f) $<$ (g)/(h) $<$ unit & selection, not pooling or supervised ranking \\
Auditability repair (support, measured) & random-addition; (k) opaque probe & KG-guided $>$ random; (k) cannot localize & the graph buys a per-sub-context fix \\
Robustness bounds (support) & (j) oracle group-DRO; (k) label-free & unit approaches (j) without labels & training-free auditable robustness \\
Dense-probe aggregate F1 (conceded) & (f) & tie acceptable & concedes the AxBench bar honestly \\
\bottomrule
\end{tabular}
\end{table}

# Empirical Analysis

This section reports what we can measure *without* running the SAE grouping: that both target regimes occur in real data, that the minimal-pair supervision is genuine, that the testbeds are adequately powered, and that the classification tasks are learnable. We then state the pre-registered predictions for the grouping run.

## Both co-response regimes occur in real safety data

The method's central design bet is that splitting and absorption are *two structurally different* obstacles requiring two operators. If real safety attributes were uniformly shared-support, a single correlation track would suffice; if uniformly disjoint, a single set-cover track would. We test this on the civil_comments sub-attribute structure directly. Among toxic comments, we compute the pairwise label co-occurrence (Jaccard) of the six toxicity sub-attributes at threshold 0.5 [ARTIFACT:art_8QO7pl6Pd8UQ]. The structure is sharply bimodal (Figure 2). A *shared-support* cluster links obscene, insult, and sexual_explicit (insult-obscene Jaccard 0.245, obscene-sexual_explicit 0.185, insult-sexual_explicit 0.100): these sub-concepts frequently co-occur, so the latents detecting them will co-fire and are mergeable by correlation — the C-track regime. In contrast, *threat* is a disjoint specialist (maximum off-diagonal Jaccard 0.044, with obscene 0.015 and sexual_explicit 0.009), and *identity_attack* is largely disjoint (0.125 with insult, but 0.012-0.022 with all others). Two of six sub-attributes have near-zero overlap with most others.

[FIGURE:fig2]

Label co-occurrence is a data-distribution proxy for latent co-firing: sub-concepts that almost never co-occur in text cannot be detected by latents that co-fire, so their detectors have low firing-Jaccard and are *unmergeable by any co-activation or correlation operator*. The measured presence of disjoint specialists (threat at 0.044) in a flagship safety dataset is therefore direct empirical motivation for the K-track: a single pairwise-affinity grouping operator is structurally insufficient for safety-attribute data, and exactly the latents a robust toxicity classifier most needs (the rare-but-severe threat and identity-attack specialists) are the ones it cannot recover. We emphasize this is evidence about the *data* regime, not yet about SAE latents; the SAE-latent firing-Jaccard is what the K-track's mutual-exclusivity constraint operates on, and measuring it is the first step of the grouping run.

## Minimal-pair counterfactuals are genuine flips

CCRG's supervision is content-flip pairs; circular or copy-like pairs would invalidate the response signal. We verify flip genuineness with cheap surface statistics. On ParaDetox, the mean TF-IDF cosine between a toxic comment and its neutral counterpart is 0.685 — a genuine content change, not a paraphrase — while LLM-generated surface-flip pairs (toxic-to-toxic) have cosine 0.355, confirming substantial rewording at constant content [ARTIFACT:art_8QO7pl6Pd8UQ]. For CAD-IMDB sentiment, an initial row-alignment heuristic was empirically *rejected* (aligned Jaccard $\approx$ random) and the authoritative pairing recovered from the source repository's batch identifiers, yielding true-pair Jaccard 0.816 versus random 0.108 [ARTIFACT:art_21JWypIydPMX]. Generation quality is high and inexpensive: the non-spelling pairs pass an independent LLM judge (content-flipped $\wedge$ surface-preserved $\wedge$ grammatical) at 100% for \$0.0104 [ARTIFACT:art_t2uUbjSwpd3t]; the first-letter pairs pass a grammaticality judge at 0.89-0.99 with 0 deterministic violations [ARTIFACT:art_dpYpjSn2Xvg3]; toxicity surface pairs pass a double-gated toxicity-and-meaning judge at 70.6% (1.5% refusals) for \$0.060 [ARTIFACT:art_8QO7pl6Pd8UQ].

## The testbeds are adequately powered

Statistical power for the pre-registered $n_{\min}=150$ is met broadly (Figure 4). In the toxicity family, five of six sub-attributes are inferential at threshold 0.5 with $\ge 150$ positives in every evaluation fold — insult (3{,}084), obscene (1{,}849), identity_attack (1{,}562), threat (1{,}438), sexual_explicit (1{,}387) — while severe_toxicity (13) is flagged descriptive-only rather than silently dropped [ARTIFACT:art_8QO7pl6Pd8UQ]. In the non-spelling testbed all eight numeric sub-contexts clear the gate (year 300, integer 300, currency 250, percent 250, date 250, decimal 200, ordinal 150, comma 150 diagnostic positives), as do twenty countries in the taxonomic hierarchy [ARTIFACT:art_t2uUbjSwpd3t]. The supporting family supplies 2{,}440 sentiment pairs, 2{,}841 aspect pairs (food 1{,}740, service 1{,}101), and a gender-balanced bias_in_bios set (10{,}054 male / 10{,}123 female across 28 professions) for the boundary-null [ARTIFACT:art_21JWypIydPMX].

[FIGURE:fig4]

## Absorption is documented only for spelling

A targeted literature triangulation establishes that no peer-reviewed source demonstrates absorption on a non-spelling token hierarchy: the original absorption study is first-letter only [5]; SAEBench's sole absorption eval is `absorption_first_letter` [7]; and the Matryoshka and hierarchical-SAE mitigations measure absorption only via the spelling metric [15, 16]. Dense-latent work confirms numeric/temporal features exist in SAEs [17], supporting the plausibility of a numeric parent, but does not demonstrate absorption on it. The non-spelling testbed is therefore not a redundant replication but a novel empirical question, which is why it carries an explicit non-triviality gate and honest-null fallback rather than an assumed positive [ARTIFACT:art_I2MrezW41iQo].

## Sanity baselines

To confirm the classification tasks carry learnable signal independent of any SAE, a TF-IDF + logistic-regression baseline reaches toxicity AUC 0.851 / F1 0.773, with one-vs-rest sub-attribute AUCs of obscene 0.900, threat 0.936, insult 0.808, identity_attack 0.925, and sexual_explicit 0.929 [ARTIFACT:art_8QO7pl6Pd8UQ]. These establish a floor: the tasks are solvable from surface lexical features, so any SAE-unit result must be read against both these dense baselines and the SAE-selection baselines of Table 2.

## Pre-registered predictions

For completeness we restate the predictions the grouping run will test (Table 3), each marked as a hypothesis. We predict (C1) the unit beats count-matched observational clusters (b)/(c); (C3) on first-letter and, conditional on the non-triviality gate, the non-spelling hierarchy, the unit recovers absorbers the oracle pool (g) and count-matched pool (h) drop, with knowledge-graph edges agreeing with the form-free diagnostic; (selection) the worst-sub-context-recall ordering (f) $<$ (g)/(h) $<$ unit with a positive, reweighting-growing unit-minus-(g)/(h) gap; and (auditability) a measured recall recovery from a knowledge-graph-guided absorber addition exceeding a random-addition control. We pre-commit to the honest-null readings: if the K-track pilot fails, we report a proposal-step failure; if the non-spelling parent has no specialist-filled holes, we scope absorption to spelling and route generality through C1; if the unit ties (g)/(h), the contribution reduces cleanly to absorber-recovery plus measured auditability; and bias_in_bios is a pre-registered boundary-null, not a method failure.

# Discussion

## What is established and what is pending

This paper establishes four things that do not require the SAE run: a concrete two-track algorithm (Section 3); a structural argument, backed by measured data structure, that observational and marginal-attribution instruments cannot recover absorbers while both regimes genuinely occur in safety data (Section 5.1); a non-circular, adequately powered evaluation design with eleven baselines (Section 4); and four frozen, validated testbeds with a genuinely novel non-spelling absorption probe. What is *pending* is the grouping run itself — encoding the testbeds through Gemma Scope, executing the two tracks, and reading off the pre-registered comparisons of Table 3. We are explicit that no unit-versus-baseline SAE result is reported here; the empirical claims above concern data structure, minimal-pair quality, power, and learnability, all of which are prerequisites the run depends on. We view the present contribution as a method plus a registered, de-risked evaluation, with the structural-impossibility argument and the regime-separation measurement as its standalone findings.

## Honest failure modes

The design front-loads the ways CCRG can fail informatively. The K-track set-cover may not recover the worked first-letter unit at the pilot (proposal-step failure); the non-spelling parent may have no specialist-filled holes (absorption is spelling-specific); observational co-response may equal interventional co-response (no gain from intervention); the unit may tie the count-matched pools on sliced recall (robustness is pooling); a label-free reweighting probe (k) may beat the unit on recall (loss-reweighting wins for pure robustness, while the unit still delivers the auditable repair); the surface-invariant dense probe (f) may match the unit on sliced recall (invariance supervision suffices, grouping adds only auditability); or the knowledge-graph-guided repair may not beat random addition (auditability buys no measurable fix). Each is a publishable mechanism-level finding, and each is pre-registered so that a null cannot be re-spun post hoc.

## Limitations

CCRG is scoped to splitting and absorption; a hedged single polysemantic latent is not groupable and is out of scope [6]. The model-diffing demonstration is constrained by infrastructure: no instruction-tuned Gemma Scope SAE exists for the 2B model, so diffing must apply the shared frozen pretrained SAE to base and instruction-tuned activations rather than a paired SAE [ARTIFACT:art_I2MrezW41iQo]. The headline robustness analysis is supporting, not load-bearing, because the same group-of-specialists mechanism predicts a count-matched attribution pool is also robust — which is exactly why selection is isolated against that pool rather than against a single hyperplane. Finally, the cross-family aggregate is descriptive: with three to four genuinely independent families the between-family variance is not estimable, so per-family CIs are primary.

# Conclusion

We have presented Two-Track Co-Response Grouping, a training-free method that organizes the latents of a frozen public SAE into reliable, auditable concept units by their interventional response to content counterfactuals — using correlation communities for shared-support splitting and an anchored greedy set-cover for disjoint-support absorption that no pairwise-affinity clustering can propose. Beyond the algorithm, the paper's standalone empirical contribution is a structural argument with measured support: in a flagship toxicity dataset, safety sub-attributes separate into a shared-support cluster (insult-obscene Jaccard 0.245) and disjoint specialists (threat 0.044), so a single grouping operator is provably insufficient and the latents a robust classifier most needs are the ones observational and marginal-attribution methods discard. We release four frozen, non-circular testbeds (109,754 examples) and a fully pre-registered, powered evaluation of eleven baselines.

**Future work.** The immediate next step is the pre-registered SAE-grouping run: the Tier-0 proposal-step pilot, the count-matched C1 classification comparison, the C3 absorber-recovery test on both hierarchies, and the measured auditability repair loop, followed by the null-floored steering and model-diffing demonstrations. We will report each pre-registered comparison, including its honest-null reading, in the next iteration.

# References

[1] H. Cunningham, A. Ewart, L. Riggs, R. Huben, L. Sharkey. Sparse Autoencoders Find Highly Interpretable Features in Language Models. ICLR, 2024.

[2] T. Bricken, A. Templeton, J. Batson, et al. Towards Monosemanticity: Decomposing Language Models With Dictionary Learning. Transformer Circuits Thread, Anthropic, 2023.

[3] T. Lieberum, S. Rajamanoharan, A. Conmy, et al. Gemma Scope: Open Sparse Autoencoders Everywhere All At Once on Gemma 2. BlackboxNLP, 2024.

[4] P. Leask, B. Bussmann, et al. Sparse Autoencoders Do Not Find Canonical Units of Analysis. ICLR, 2025.

[5] D. Chanin, J. Wilken-Smith, T. Dulka, H. Bhatnagar, J. Bloom. A is for Absorption: Studying Feature Splitting and Absorption in Sparse Autoencoders. arXiv:2409.14507, 2024.

[6] D. Chanin, T. Dulka, A. Garriga-Alonso. Feature Hedging: Correlated Features Break Narrow Sparse Autoencoders. arXiv:2505.11756, 2025.

[7] A. Karvonen, C. Rager, et al. SAEBench: A Comprehensive Benchmark for Sparse Autoencoders. ICML, 2025.

[8] Z. Wu, A. Arora, et al. AxBench: Steering LLMs? Even Simple Baselines Outperform Sparse Autoencoders. ICML, 2025.

[9] A. Karvonen, C. Rager, et al. Evaluating Sparse Autoencoders on Targeted Concept Erasure Tasks. arXiv:2411.18895, 2024.

[10] S. Marks, C. Rager, E. J. Michaud, Y. Belinkov, D. Bau, A. Mueller. Sparse Feature Circuits: Discovering and Editing Interpretable Causal Graphs in Language Models. ICLR, 2024.

[11] C. O'Neill, C. Ye, et al. Disentangling Dense Embeddings with Sparse Autoencoders. arXiv:2408.00657, 2024.

[12] R. Deng, et al. Sparse Feature Coactivation Reveals Causal Semantic Modules in Large Language Models. arXiv:2506.18141, 2025.

[13] J. Winnicki, S. Gnanasekaran, E. Darve. Domain-Filtered Knowledge Graphs from Sparse Autoencoder Features. arXiv:2604.23829, 2026.

[14] S. A. Dalili, M. Mahdavi. Subspace-Aware Sparse Autoencoders for Effective Mechanistic Interpretability. arXiv:2606.06333, 2026.

[15] B. Bussmann, N. Nabeshima, et al. Learning Multi-Level Features with Matryoshka Sparse Autoencoders. ICML, 2025.

[16] M. Muchane, S. M. Richardson, et al. Incorporating Hierarchical Semantics in Sparse Autoencoder Architectures. arXiv:2506.01197, 2025.

[17] X. Sun, A. Stolfo, et al. Dense SAE Latents Are Features, Not Bugs. arXiv:2506.15679, 2025.

[18] D. Chanin, et al. Are Sparse Autoencoder Benchmarks Reliable? arXiv:2605.18229, 2026.

[19] B. Tesson, R. Breitling, R. Jansen. DiffCoEx: a simple and sensitive method to find differentially coexpressed gene modules. BMC Bioinformatics, 11:497, 2010.

[20] B. Zhang, S. Horvath. A General Framework for Weighted Gene Co-Expression Network Analysis. Statistical Applications in Genetics and Molecular Biology, 4(1), 2005.

[21] V. A. Traag, L. Waltman, N. J. van Eck. From Louvain to Leiden: guaranteeing well-connected communities. Scientific Reports, 9:5233, 2019.

[22] G. L. Nemhauser, L. A. Wolsey, M. L. Fisher. An analysis of approximations for maximizing submodular set functions-I. Mathematical Programming, 14:265-294, 1978.

[23] U. Feige. A threshold of ln n for approximating set cover. Journal of the ACM, 45(4):634-652, 1998.

[24] S. Sagawa, P. W. Koh, T. B. Hashimoto, P. Liang. Distributionally Robust Neural Networks for Group Shifts. ICLR, 2020.

[25] E. Z. Liu, B. Haghgoo, et al. Just Train Twice: Improving Group Robustness without Training Group Information. ICML, 2021.

[26] N. Sohoni, J. Dunnmon, G. Angus, A. Gu, C. Re. No Subclass Left Behind: Fine-Grained Robustness in Coarse-Grained Classification Problems (GEORGE). NeurIPS, 2020.

[27] E. Creager, J.-H. Jacobsen, R. Zemel. Environment Inference for Invariant Learning. ICML, 2021.

[28] J. Nam, H. Cha, S. Ahn, J. Lee, J. Shin. Learning from Failure: Training Debiased Classifier from Biased Classifier. NeurIPS, 2020.

[29] M. N. N. To, et al. Diverse Prototypical Ensembles Improve Robustness to Subpopulation Shift. ICML, 2025.

[30] T. G. J. Rudner, Y. S. Zhang, A. G. Wilson, J. Kempe. Mind the GAP: Improving Robustness to Subpopulation Shifts with Group-Aware Priors. AISTATS, 2024.

[31] N. Belrose, D. Schneider-Joseph, S. Ravfogel, R. Cotterell, E. Raff, S. Biderman. LEACE: Perfect Linear Concept Erasure in Closed Form. NeurIPS, 2023.

[32] V. Veitch, A. D'Amour, S. Yadlowsky, J. Eisenstein. Counterfactual Invariance to Spurious Correlations in Text Classification. NeurIPS, 2021.

[33] D. Kaushik, E. Hovy, Z. C. Lipton. Learning the Difference that Makes a Difference with Counterfactually-Augmented Data. ICLR, 2020.

[34] E. D. Abraham, K. D'Oosterlinck, et al. CEBaB: Estimating the Causal Effects of Real-World Concepts on NLP Model Behavior. NeurIPS, 2022.

[35] V. Logacheva, D. Dementieva, et al. ParaDetox: Detoxification with Parallel Data. ACL, 2022.

[36] D. Borkan, L. Dixon, J. Sorensen, N. Thain, L. Vasserman. Nuanced Metrics for Measuring Unintended Bias with Real Data for Text Classification. The Web Conference, 2019.

[37] M. De-Arteaga, A. Romanov, H. Wallach, et al. Bias in Bios: A Case Study of Semantic Representation Bias in a High-Stakes Setting. FAccT, 2019.

[38] P. Varshney, et al. Discovering Concept Directions from Diffusion-based Counterfactuals via Latent Clustering. Pattern Recognition Letters, 2025.

</previous_paper>

<reviewer_feedback>
STEP 1 — REVIEW: A reviewer evaluated the previous paper draft above and produced this feedback.

- [MAJOR] (evidence) The central experiment is not run. Every load-bearing and supporting claim in Table 3 (C1 classification at matched pool size, C3 absorber-recovery on both hierarchies, the (f)<(g)/(h)<unit selection ordering, the auditability repair loop, steering, and model-diffing) is a pre-registered PREDICTION, not a result. The paper reports no unit-versus-baseline SAE number at all. The task explicitly requires evaluation on classification, steering with side-effect measurement, and model-diffing; none is executed. At ICLR/ICML there is no registered-report track, so this reads as an incomplete submission whose own thesis (units > latents > observational clusters > oracle pools) has zero supporting evidence.
  Action: Run the SAE-grouping pipeline on at least the load-bearing core and report actual numbers: the Tier-0 first-letter proposal pilot (does the K-track recover the known parent + lion/London absorbers?), C1 classification of unit vs count-matched (b)/(c)/(h) on first-letter and toxicity, and C3 first-letter absorber-recovery vs the (g)/(h) oracle pools. Absorption is known to exist on first-letter spelling, so this is the lowest-risk, highest-information testbed. A single fully-executed positive testbed transforms the paper's standing.
- [MAJOR] (evidence) The finding offered as the paper's standalone empirical contribution — that splitting and absorption regimes both occur in safety data — is measured on dataset LABEL co-occurrence (civil_comments sub-attribute Jaccard), NOT on SAE latent firing. The paper concedes this ('evidence about the data regime, not yet about SAE latents') but then leans on it heavily in the abstract, intro, and conclusion as if it established the K-track's necessity. The bridge ('label co-occurrence is a proxy for latent co-firing') is asserted and is questionable: a single general toxicity latent can fire on all sub-attributes regardless of how disjoint the labels are, and the very thing the K-track needs — that the threat/identity-attack DETECTOR latents are mutually exclusive in firing with the general latent — is exactly what is not measured. As stated, the standalone finding does not demonstrate that any pairwise operator fails on real SAE latents.
  Action: Encode the existing toxicity examples through Gemma Scope (layer 12, 16k) and report the actual SAE-latent firing-Jaccard among the top per-sub-attribute detector latents, plus parent-latent recall holes. This is a cheap single forward pass over data you already have and converts the proxy into the real premise of the K-track. If SAE-latent disjointness does NOT mirror label disjointness, that is itself an important finding and should reshape the K-track motivation.
- [MAJOR] (scope) Two of the three downstream tasks the goal mandates — activation steering with side-effect measurement, and model-diffing between fine-tuned variants — are deferred entirely to future work, and model-diffing is further compromised by infrastructure (no instruction-tuned Gemma Scope 2B SAE exists, forcing a shared pretrained SAE applied to base and IT activations, which is a confounded diffing setup rather than a paired-SAE diff). The paper's significance case rests substantially on these applications, yet provides no evidence for either.
  Action: Run at least the steering demonstration on first-letter (the most de-risked concept): show the unit's mean-member-decoder direction steers 'starts-with-L' with lower collateral (full-vocab KL, PPL) at matched on-target effect versus difference-of-means and hub-alone controls. For model-diffing, either present a small concrete result with the shared-SAE caveat clearly bounded, or move it out of the contribution claims and into explicit limitations rather than future work.
- [MINOR] (methodology) The K-track anchor is defined as argmax_l |C_l| (highest-recall content-responsive latent), assumed to be the 'general/parent' latent. But under absorption the true parent has holes by definition, and a high-frequency surface or polysemantic latent could plausibly have higher cover-set cardinality than the genuine concept parent. The identification 'anchor = parent' is asserted, not validated, and the downstream hole-set H and greedy cover all inherit any anchor error. Likewise the mutual-exclusivity Jaccard<0.1, precision>=0.7, and coverage-gain>=0.05 thresholds are hand-set with no sensitivity analysis.
  Action: In the Tier-0 pilot, report whether the recall-argmax anchor coincides with the diagnostic-identified parent, and include an ablation/robustness sweep over the Jaccard, precision, and coverage-gain thresholds so readers can see the result is not knife-edge on these constants.
- [MINOR] (rigor) Multiplicity control is described 'across claims' via Holm-Bonferroni, but the admission filter (Step 5) evaluates many candidate units per concept against 95th-percentile nulls with a disjunctive (signature-C OR signature-K) admission AND a surface-invariance gate. The family-wise false-admit rate over the many proposed units within a concept is not obviously the stated <=0.05; per-unit thresholds do not compose to a per-concept guarantee without correction.
  Action: Specify the multiplicity correction at the unit-proposal level (how many candidate units are tested per concept and how the <=0.05 false-admit target is maintained across them), separate from the across-claims Holm-Bonferroni. Report the empirical false-admit rate from the matched random-k null on a real run.
- [MINOR] (evidence) The surface-invariance admission criterion is load-bearing (it is the AND-gate in Step 5), yet the surface-flip control sets are small (546 toxicity surface pairs, 590 first-letter), and the toxicity surface pairs were both GENERATED and JUDGED by the same model (gpt-4o-mini per the artifact), with only a 70.6% judge pass rate. Same-model generate-and-judge is a mild circularity in a control that gates every admitted unit.
  Action: Enlarge the surface-pair sets for the concepts where surface-invariance is actually exercised, and re-judge a sample with an independent model (or a small human audit) to confirm the 70.6% pass set is genuinely meaning-preserving. Report the surface-response null distribution sizes used per concept.
- [MINOR] (novelty) Novelty differentiation leans on very recent and future-dated citations that are close to the contribution — [13] domain-filtered knowledge graphs from SAE features (arXiv:2604.23829) and [14] subspace-aware SAEs (arXiv:2606.06333, which I confirmed resolves) — and on a hedged distinction from CDLC [38]. Because the method's own output is 'a feature-level knowledge graph from SAE features,' the delta against [13] in particular needs to be explicit, not a single sentence. Also, [5] 'A is for Absorption' is now a NeurIPS 2025 Oral but is cited only as arXiv:2409.14507 (2024).
  Action: Add a sentence each explicitly contrasting CCRG's edges (interventional specialization edges over multi-member units) with [13]'s co-occurrence/geometry edges, and CCRG's two-track grouping with [14]'s retraining. Update [5] to its NeurIPS 2025 venue and audit all 2026-dated citations for venue/version accuracy.
- [MINOR] (rigor) The pervasive honest-null framing, while commendable, is taken far enough that nearly every possible outcome (proposal-step failure, spelling-only absorption, no interventional gain, robustness-is-pooling, label-free probe wins, dense probe ties, repair fails) is pre-labeled a 'publishable mechanism-level finding.' This makes the contribution difficult to falsify: there is no declared outcome under which the method is judged to have failed. Reviewers will discount a protocol that cannot lose.
  Action: Designate a clear primary endpoint whose negative result would count as the method NOT working (e.g., 'unit does not beat count-matched (h) on worst-sub-context recall on first-letter'), and present the null fallbacks as secondary characterizations rather than as co-equal successes.
</reviewer_feedback>

<pipeline_steps>
STEP 2 — STRATEGY: The pipeline's strategy generator (gen_strat) read the reviewer feedback
and designed a new research strategy to address the critiques.

STEP 3 — PLANNING: The planner (gen_plan) turned the strategy into concrete artifact plans —
specific experiments, datasets, or research tasks to execute.

STEP 4 — EXECUTION: The executor (gen_art) ran those plans and produced the new artifacts
shown in <new_artifacts_this_iteration> below.
</pipeline_steps>

<hypothesis>
STEP 5 — HYPOTHESIS UPDATE: The hypothesis was revised based on evidence from previous iterations.

kind: hypothesis
title: >-
  Two-Track Interventional Co-Response Grouping of SAE Latents (Correlation for Splitting, Anchored Greedy Set-Cover for Absorption):
  Training-Free, Auditable Concept Units that Recover the Absorbers Marginal-Attribution Selection Drops on First-Letter Spelling
  (and, where present, a Non-Spelling Hierarchy), and Beat Raw Latents, Count-Matched Observational Clusters, and Count-Matched
  Oracle Pools
hypothesis: |-
  ITERATION-1 STATUS AND THE SINGLE MANDATE FOR ITERATION 2 (EXECUTE THE CORE). Iteration 1 was a foundation iteration: it produced and validated EVERYTHING the SAE-grouping run needs but ran NO SAE. Delivered: two verified dossiers (art_RidEJtBC7gPT pins the SAE pipeline -- defensive from_pretrained, JumpReLU firing=encode>0, hook blocks.12.hook_resid_post, gemma-scope-2b-pt-res-canonical layer_12/width_16k -- the C-track leidenalg + K-track greedy max-coverage, all 11 baselines (a)-(k), AxBench steering, the shared-pt-SAE model-diffing recipe, and a verified 30+ citation table; art_I2MrezW41iQo verifies the Chanin 2409.14507 absorption diagnostic against sae-spelling and the non-circular FORM-FREE probe-projection variant, and pins all datasets) and four FROZEN, schema-validated testbeds (first-letter L/O/T/I/D, 17,180 ex, 0 deterministic violations; non-spelling numeric+taxonomic, 24,128 ex; toxicity ParaDetox+civil_comments, 37,707 ex; supporting sentiment/aspect/bias_in_bios, 30,739 ex). The paper therefore reports ZERO unit-vs-baseline numbers -- every Table-3 row is a PREDICTION -- and the reviewer's decisive verdict is that this reads as an incomplete submission whose own thesis (units > latents > observational clusters > oracle pools) has no supporting evidence. THE REVISION'S CENTRAL MOVE: the load-bearing core is NO LONGER a pre-registration; it is the immediate, mandatory deliverable of iteration 2. A SINGLE fully-executed positive testbed -- first-letter spelling, the documented guaranteed-signal regime -- transforms the paper's standing. Iteration 2 STOPS building infrastructure and RUNS the pipeline; nothing else is load-bearing until real numbers exist.

  ONE-SENTENCE HEADLINE (load-bearing, C1+C3; conceptually UNCHANGED): clustering frozen SAE latents by their INTERVENTIONAL co-response to content counterfactuals -- via a concretely specified TWO-TRACK algorithm (positive content-response CORRELATION for the splitting regime; an ANCHORED GREEDY SET-COVER for the absorption regime, because mutually-exclusive disjoint-support absorbers have LOW pairwise correlation and cannot be proposed by any affinity-merging clustering) -- yields training-free, human-auditable, multi-member concept units that (C1) beat the best raw single latent AND COUNT-MATCHED observational co-activation/decoder-geometry clusters on safety-attribute classification, and (C3, the spine) recover the absorber latents a count-matched marginal-attribution selection silently drops, with knowledge-graph specialization edges that agree with the absorption diagnostic (Chanin 2409.14507, NeurIPS 2025 Oral) used ONLY to score edges, never to form units (non-circular).

  PRIMARY FALSIFICATION ENDPOINT (NEW -- resolves the 'protocol that cannot lose' critique). The method is judged to WORK if and only if, on FIRST-LETTER SPELLING (the regime where absorption is guaranteed to exist), BOTH hold: (E1) the K-track proposal step, given ONLY content-flip pairs (NOT the Chanin diagnostic), recovers the diagnostic-identified parent latent plus >=2 per-token absorbers (e.g. lion/London) with membership F1 above a random-membership null; AND (E2) the resulting co-response unit BEATS the count-matched oracle pool (g) and count-and-pool-matched probe (h) AND the count-matched observational clusters (b)/(c) on absorber-recovery count and sliced recall over the differing sub-contexts, with a paired-bootstrap CI excluding 0. If EITHER fails on first-letter -- the lowest-risk testbed -- the method DOES NOT WORK, and that is the reportable negative; the honest-null branches below are SECONDARY characterizations of HOW it works when it does, not co-equal successes. This is the one outcome the paper stakes itself on.

  THE LOAD-BEARING CORE, REFRAMED AS THE ITER-2 EXECUTION LIST (run, do not pre-register):
    (RUN-0, Tier-0 pilot, first-letter, GUARANTEED-SIGNAL) Encode the first-letter content-flip pairs through Gemma Scope L12/16k; run K-track STEP-3 set-cover; report (a) anchor-FIDELITY -- does the recall-argmax anchor coincide with the diagnostic-identified parent? (b) recovered membership precision/recall vs the diagnostic above the random-membership null; (c) a THRESHOLD SENSITIVITY SWEEP over mutual-exclusivity Jaccard, per-member precision, and coverage-gain floors, to show the recovery is not knife-edge on hand-set constants. This is E1.
    (RUN-1, C1 classification) unit vs best raw latent (a), vs COUNT-MATCHED observational clusters (b)/(c), and vs count-and-pool-matched (h), on first-letter AND the best-powered toxicity sub-attributes; per-family paired-bootstrap CIs.
    (RUN-2, C3 absorber-recovery) on first-letter: recovered-absorber count and sliced recall vs (g)/(h); KG specialization-edge agreement with the diagnostic. This is E2.
    (RUN-3, SAE-LATENT FIRING REGIME MEASUREMENT -- see next block) the cheap forward pass that grounds the regime-separation claim.
    (RUN-4, REQUIRED steering demo) the first-letter steering result (see steering block).
  HARD CHECKPOINT: if E1 and E2 clear on first-letter, the paper has a real positive anchor and proceeds to toxicity + the non-spelling testbed + supporting results; if not, write up the executed negative.

  SAE-LATENT FIRING REGIME MEASUREMENT (NEW -- resolves the MAJOR critique that the standalone finding was measured on LABELS, not latents). The iteration-1 'both regimes occur in safety data' finding rests on civil_comments sub-attribute LABEL co-occurrence (insult-obscene Jaccard 0.245 shared-support; threat 0.044 disjoint). The reviewer is correct that label co-occurrence is NOT latent co-firing -- a single general toxicity latent can fire across all sub-attributes regardless of label disjointness, so the label-Jaccard does NOT establish that any pairwise operator fails on real SAE latents. The regime claim is therefore DEMOTED from a headline standalone finding to a motivating proxy, and iteration 2 MUST replace it with the real measurement (a single forward pass over data already built): encode the toxicity examples through Gemma Scope L12/16k, identify the top per-sub-attribute detector latents and the candidate general/parent toxicity latent, and report (i) the actual SAE-LATENT firing-Jaccard among those detectors, and (ii) the parent latent's RECALL HOLES per sub-context. The K-track's necessity is established ONLY if disjoint sub-attributes (threat, identity_attack) are carried by latents that are mutually exclusive in firing with the general latent. If SAE-latent disjointness does NOT mirror label disjointness, that is itself an important finding and reshapes the K-track motivation (reported honestly, not buried). The same firing-Jaccard measurement is the first quantitative step of RUN-0/RUN-2 on first-letter.

  DOWNSTREAM TASKS THE GOAL MANDATES -- NO LONGER DEFERRED (resolves the MAJOR scope critique). (1) STEERING is now a REQUIRED iter-2 deliverable, not future work: on first-letter (the most de-risked concept), steer with the unit's MEAN-MEMBER-DECODER direction and show it moves 'starts-with-L' output mass at MATCHED on-target effect with LOWER collateral than (i) a non-SAE difference-of-means direction and (ii) a hub/best-single-latent-alone control, measured by full-vocab KL on unrelated prompts AND perplexity, with doc-bootstrap CIs and a shuffle null. (2) MODEL-DIFFING is bounded honestly: because NO instruction-tuned Gemma Scope 2B SAE exists (verified: Google IT residual SAEs only for 9B), diffing applies the SHARED frozen pt-SAE to gemma-2-2b vs gemma-2-2b-it activations -- a CONFOUNDED setup. Iteration 2 either presents one small concrete diffing result with the shared-SAE confound explicitly bounded (does the unit detect a base-vs-it concept-usage shift more reliably than the best single latent, above a shuffle null?), or moves model-diffing out of the contribution claims and into an explicit LIMITATION -- NOT into open-ended future work.

  THE TWO-TRACK CLUSTERING ALGORITHM -- THE NAMED CONTRIBUTION (specification retained; anchor validation strengthened). Input: a frozen SAE and, per concept, content-flip minimal pairs (x_off,x_on) plus surface-flip pairs; the concept labels are the SAME supervision every matched baseline (d)-(h) consumes (no absorption oracle). STEP 1 -- per-latent content-response r_l(p)=a_l(x_on)-a_l(x_off); keep CONTENT-RESPONSIVE latents (mean r_l above the 95th-pct shuffled-pair null); cover set C_l = pairs with r_l>tau_resp AND a_l fires on x_on AND content-response precision >=0.7. STEP 2 -- C-TRACK (splitting; shared support, symmetric affinity APPROPRIATE): A_C[l,l'] = positive Spearman correlation of content-response profiles (DiffCoEx-style soft-threshold, beta=6 per WGCNA scale-free criterion); Leiden communities; count fixed by modularity + bootstrap-ARI stability vs the shuffled-pair null. STEP 3 -- K-TRACK (absorption; ANCHORED GREEDY MAX-COVERAGE, NOT pairwise affinity): (i) ANCHOR = argmax_l |C_l| using ONLY P (NOT the diagnostic; tie-break broadest, lowest-entropy support) -- and, per the methodology critique, iteration 2 VALIDATES the 'anchor=parent' identification by reporting whether the recall-argmax anchor coincides with the diagnostic parent and by checking that a high-frequency/polysemantic latent has not usurped the anchor; (ii) HOLES H = P\C_anchor; (iii) GREEDY: while H non-empty and improving, add l*=argmax_l |C_l intersect H| subject to mutual exclusivity (firing Jaccard<0.1), precision>=0.7, marginal coverage gain>=0.05 with bootstrap CI excluding 0; H<-H\C_l*. STEP 4 -- RECONCILE: anchor each C-community's highest-recall member and K-augment with mutually-exclusive absorbers covering its holes; seed K from standalone high-recall latents; de-duplicate to highest-coverage-gain unit. STEP 5 -- ADMISSION FILTER: admit iff signature C (within-unit content-response correlation > 95th-pct shuffled-pair null) OR signature K (pooled-max minus best-single content-response AUC > 95th-pct of a best-of-random-k null MATCHED on marginal AUC, PLUS the k in {2,3} absolute >=0.05 gain with CI excluding 0, PLUS Jaccard<0.1 and per-member precision>=0.7), AND unit-level surface invariance (pooled surface-response not above the shuffled-surface null).

  MULTIPLICITY AT THE UNIT-PROPOSAL LEVEL (NEW -- resolves the rigor critique). The admission filter tests MANY candidate units per concept against 95th-pct nulls with a disjunctive (C OR K) rule plus a surface AND-gate; per-unit thresholds do NOT compose to a per-concept <=0.05 false-admit guarantee. Iteration 2 SPECIFIES and APPLIES a multiplicity correction at the unit-proposal level (Benjamini-Hochberg or Holm over the M candidate-unit admission tests within each concept), reports M, and reports the EMPIRICAL family-wise false-admit rate from the matched random-k null on the real run -- SEPARATE from the across-claims Holm-Bonferroni used for the headline comparisons.

  SURFACE-INVARIANCE CONTROL STRENGTHENED (NEW -- resolves the control-circularity critique). Surface-invariance is the load-bearing AND-gate of Step 5, yet iter-1 surface-flip sets are small (546 toxicity, 590 first-letter) and the toxicity surface pairs were both GENERATED and JUDGED by gpt-4o-mini (70.6% pass) -- a mild same-model circularity in a control that gates every admitted unit. Iteration 2: (a) ENLARGE the surface-pair sets for the concepts where surface-invariance is actually exercised; (b) RE-JUDGE a sample with an INDEPENDENT model from a different family (or a small human audit) to confirm the pass set is genuinely meaning-preserving; (c) REPORT the surface-response null distribution SIZE used per concept.

  BASELINE GLOSSARY (one line each): (a) best raw single latent; (b) observational co-activation clusters, COUNT-MATCHED to the unit's k for C1; (c) decoder-geometry clusters, COUNT-MATCHED; (d) counterfactually-matched diff-of-means; (e) counterfactually-matched probe; (f) surface-invariant matched probe = (d)/(e) with surface direction LEACE-erased (the conceded single dense hyperplane); (g) supervised oracle pool = top-N SAE latents by SCR/TPP attribution; (h) count-and-pool-matched probe = max-pool over EXACTLY k SCR/TPP-selected raw directions; (i) unmatched diff-of-means/probe; (j) oracle group-DRO probe (true sub-context labels) = robustness UPPER BOUND; (k) label-free group-inference probe (JTT/GEORGE-style). C1 LOAD-BEARING half = unit beats COUNT-MATCHED (b)/(c) (beating single latent (a) is a near-foregone capacity win, completeness only). SELECTION-CRITERION ISOLATION = unit vs (g)/(h) at FIXED pool size, varying only HOW members are chosen (co-response set-cover vs marginal attribution); beating (f) is conceded as pooling.

  THE NON-SPELLING TESTBED (C3 generality, SECONDARY to executing first-letter). Numeric-quantity hierarchy primary (general numeric-token latent with year/percent/currency/date absorbers), taxonomic 'is-a-country' alternative; scored by the FORM-FREE probe-plus-ablation diagnostic. Because absorption is documented almost ONLY on first-letter (verified across the original work, SAEBench's sole 'absorption_first_letter' eval, and the Matryoshka/H-SAE mitigations), Testbed-2 is ALSO a novel empirical test of whether absorption generalizes. NON-TRIVIALITY GATE (parent recall>=0.60; >=1 absorber with firing-Jaccard<0.10, precision>=0.70, hole-coverage gain>=0.05 CI-excluding-0). HONEST-NULL FALLBACK: if the non-spelling parent has no specialist-filled holes, report 'absorption is spelling-specific', scope the C3 title claim to spelling-type hierarchical absorption, and route cross-concept generality through C1. This is a SECONDARY characterization, executed only after first-letter E1/E2 land.

  SUPPORTING RESULTS (strengthen the paper; honest nulls here do not sink it). (S1) SELECTION-CRITERION ORDERING on toxicity worst-sub-context recall: pre-registered (f) < (g)/(h) < unit, with the unit-minus-(g)/(h) PAIRED gap (B=10000) GROWING in measured sub-population reweighting magnitude (slope CI primary). (S2) ROBUSTNESS BOUNDS: unit APPROACHES the oracle group-DRO probe (j) without labels and is competitive-or-better than the label-free probe (k) while uniquely auditable. (S3) MEASURED AUDITABILITY REPAIR LOOP: pick an under-served sub-context (recall hole on the dense probe (f) ALONE), read the KG to find the covering absorber, ADD it, MEASURE recall recovery (bootstrap CI) vs a RANDOM-content-responsive-latent-addition control, confirm (k) exposes no per-sub-context member to add; PLUS LLM-judge member-labeling agreement vs a shuffled-label null. DEGENERATE-CONSTRUCTION GUARD: sub-contexts from INDEPENDENT labels frozen first (civil_comments sub-attribute floats, CEBaB aspect levels), 'under-served' on (f) alone, non-triviality check that (f) genuinely collapses.

  NOVELTY DELTAS (resolves the novelty critique). Update Chanin 'A is for Absorption' to NeurIPS 2025 Oral (not just arXiv:2409.14507 2024) and audit all 2026-dated cites for venue/version. State EXPLICITLY (not in one hedged line): vs [13] Domain-Filtered Knowledge Graphs from SAE Features (2604.23829) -- their edges are OBSERVATIONAL (co-occurrence, decoder geometry, contrastive corpus filtering) over single latents; ours are INTERVENTIONAL specialization edges (absorbed/split child of an anchor) over MULTI-MEMBER co-response units, with measured repair utility. Vs [14] Subspace-Aware SAEs (2606.06333) and the Matryoshka/H-SAE/concept-bottleneck family -- they RETRAIN the dictionary to reduce absorption at training time; we are training-free POST-HOC over a frozen public SAE. Vs CDLC (2505.07073) -- they cluster continuous diffusion-counterfactual difference vectors into one direction per class in vision; we cluster DISCRETE LLM SAE latents into multi-member units with a SET-COVER track CDLC has no analogue for.

  HONEST NEGATIVES (now SUBORDINATE to the primary endpoint, reported as characterizations of failure modes, NOT as guaranteed wins): the K-proposal set-cover fails to recover the worked first-letter unit at the pilot (=primary-endpoint failure E1, method does not work); SAE-latent firing-Jaccard does NOT mirror label disjointness (reshape K-track motivation); the unit ties (g)/(h) on first-letter sliced recall (=primary-endpoint failure E2); observational co-response equals interventional co-response (no gain from intervention); the non-spelling parent has no specialist-filled holes (absorption spelling-specific -> scope C3); the unit ties (g)/(h) on toxicity (robustness is pooling -> contribution reduces to absorber-recovery + measured auditability); (k) beats the unit on recall (loss-reweighting wins for pure robustness); (f) matches the unit on sliced recall (invariance suffices, grouping adds only auditability); the KG-guided repair does not beat random-addition (auditability buys no measurable fix); steering shows no lower-collateral advantage (the steering application does not hold). bias_in_bios is a pre-registered boundary-null, not method failure.

  MOTIVATION (unchanged in substance). Single SAE latents are unreliable: feature absorption (a child latent suppresses a more general parent's firing; Chanin 2409.14507 NeurIPS 2025 Oral, 2505.11756), splitting, hedging, and 'SAEs Do Not Find Canonical Units' (ICLR 2025) converge on no single latent reliably tracking a concept; AxBench (ICML 2025) and DeepMind's negative report show plain diff-of-means beats raw-latent SAE methods, so any SAE-grouping method must clear strong simple baselines. Absorption is exactly the regime where OBSERVATIONAL signals break by construction (parent and absorbing child are mutually exclusive in firing) and where MARGINAL-ATTRIBUTION selection (SCR/TPP) silently drops the absorber (low marginal attribution because it fires only in a narrow sub-context). The two-track design follows: correlation-community detection for shared-support splitting (DiffCoEx/WGCNA transfer) and anchored greedy set-cover for disjoint-support absorption (Nemhauser-Wolsey-Fisher / Feige (1-1/e) transfer). The anchor is chosen WITHOUT the diagnostic, so 'unsupervised unit beats supervised oracle' holds and KG-edge validation is non-circular. Training-free post-hoc repair of FROZEN public SAEs is exactly what practitioners holding Gemma Scope have; architectural remedies retrain and are orthogonal.

  SUCCESS CRITERIA. METHOD WORKS iff the PRIMARY ENDPOINT clears on first-letter (E1 K-proposal recovers parent + >=2 absorbers above the random-membership null AND E2 unit beats count-matched (g)/(h)/(b)/(c) on absorber-recovery/sliced recall, paired-bootstrap CI excluding 0), AND the REQUIRED first-letter steering demo shows matched-on-target effect at lower collateral than diff-of-means and hub-alone. SUPPORTING (strengthen, do not gate): C1 on toxicity; S1 selection ordering; S2 robustness bounds; S3 measured auditability; the SAE-latent firing-Jaccard regime measurement; the non-spelling C3 generality (gated by non-triviality); admission false-admit <=0.05 under both nulls with the unit-proposal multiplicity correction; cluster-stability ARI/Jaccard above null. A clean primary-endpoint NEGATIVE on first-letter is the declared method-failure outcome and is itself a reportable finding; the other honest negatives are secondary characterizations.
motivation: |-
  Single SAE latents are unreliable units of analysis. Feature absorption (a specific child latent suppresses a more general parent's firing, leaving the parent with unpredictable holes; Chanin 2409.14507 [NeurIPS 2025], 2505.11756), feature splitting (one concept fragments across many latents), feature hedging (a narrow SAE merges correlated features into one polysemantic latent), and 'SAEs Do Not Find Canonical Units of Analysis' (ICLR 2025, 2502.04878) converge on one conclusion: no single latent reliably tracks a concept. AxBench (ICML 2025 spotlight, 2501.17148) and DeepMind's negative-results report make the stakes concrete -- plain difference-of-means beats raw-latent SAE methods -- so any SAE-grouping method must clear strong simple baselines.

  WHY THE LOAD-BEARING CLAIM IS C1+C3, AND WHY THE ALGORITHM HAD TO BE SPECIFIED. The single most defensible deliverable is absorber recovery (C3): the co-response unit admits the absorber latents the supervised oracle's top-N marginal-attribution selection (g) and the count-matched pool (h) drop, with KG edges agreeing with the absorption diagnostic. But absorbers are MUTUALLY EXCLUSIVE in firing with their parent and respond on DISJOINT supports, so they have LOW pairwise content-response correlation -- meaning a correlation/affinity-merging clustering can never even PROPOSE the right group, and an admission rule that only FILTERS candidates cannot rescue a unit the proposal step never generated. This is why the contribution is now a TWO-TRACK algorithm: a correlation-community track for splitting (where support is shared) and a separate ANCHORED GREEDY SET-COVER track for absorption (anchor on the highest-recall parent candidate, greedily add mutually-exclusive latents that cover its holes). Maximum-coverage greedy selection is the natural, classic instrument for 'cover a set with complementary specialists' -- and it is exactly the instrument the absorption regime demands, because coverage-complementarity is a set-level property, not a pairwise affinity. The anchor is chosen WITHOUT the absorption diagnostic (by content-response recall, available to every baseline), so 'the unsupervised unit beats the supervised oracle' is not undercut and the KG-edge validation against the diagnostic is non-circular (the diagnostic scores edges, never forms them).

  The contribution lives squarely in clustering / feature-selection / classification for a learned knowledge representation (SAE features): cluster-level units plus a feature-level knowledge graph, evaluated on downstream classification (headline) with steering and model-diffing as generality demonstrations. Every existing POST-HOC grouping method relies on OBSERVATIONAL signals -- which latents fire together (co-activation feature families) or which decoders point alike (geometry). But absorption is exactly the regime where observational signals break BY CONSTRUCTION: the parent and absorbing child are mutually exclusive in firing, so co-activation clustering provably cannot group them and their decoders need not be cosine-similar. The standard SUPERVISED remedy -- select top-N latents by causal effect on a concept probe (SCR/TPP, Karvonen 2411.18895, built on Marks SHIFT) -- SILENTLY DROPS absorbed latents, because a latent firing only in a narrow sub-context has low MARGINAL attribution even though it carries the concept there.

  ABSORPTION BEYOND SPELLING IS UNDER-TESTED -- AND THAT IS AN OPPORTUNITY. The literature documents absorption empirically almost entirely on first-letter spelling; the sparsity-plus-hierarchy MECHANISM, however, predicts absorption in any token-level hierarchy (numeric formats, taxonomic entities). Promoting one non-spelling hierarchy into the load-bearing core therefore does double duty: it moves C3 from 'one synthetic spelling task' to 'absorption as a phenomenon', and it is itself a novel empirical test of whether absorption generalizes -- with the form-free probe-plus-ablation diagnostic (domain-agnostic) as oracle and an explicit honest-null fallback (absorption is spelling-specific -> scope C3, route generality through C1) if the non-spelling parent has no specialist-filled holes.

  RECENT ARCHITECTURAL REMEDIES ARE ORTHOGONAL (and confirm the gap). Subspace-Aware SAEs (SASA, 2606.06333), Matryoshka SAEs, Concept-Bottleneck SAEs (CVPR 2026), AbsTopK and Group SAEs all RETRAIN the SAE to reduce splitting/absorption at training time. We do the opposite: a TRAINING-FREE, POST-HOC repair of FROZEN public SAEs (Gemma Scope), exactly as the goal requires. No retraining method produces a human-auditable multi-member unit over an existing public SAE, which is what practitioners actually have.

  TWO cross-field transfers motivate the method. (1) Systems biology faced the identical grouping obstacle: co-regulated genes are often NOT co-expressed at baseline and reveal shared regulation only under perturbation, which is why differential co-expression methods (DiffCoEx, WGCNA) cluster genes by CORRELATED RESPONSE TO A PERTURBATION rather than baseline co-expression -- the root of our C-track (genes->latents, perturbation->content counterfactual). (2) Combinatorial optimization supplies the absorption-regime instrument: the disjoint-support 'cover the concept with complementary specialists' problem is a MAXIMUM-COVERAGE / SET-COVER problem, whose greedy (1-1/e) solution is the natural proposer for K-units -- a Level-3 methodological import never applied to SAE-latent grouping. Distributionally-robust learning (group-DRO; Mind-the-GAP 2403.09869) explains WHY the recovered unit generalizes: an absorber is a dedicated detector for one sub-context, so a complementary-coverage unit is implicitly a GROUP-OF-SPECIALISTS robust to mixing-weight shift where a single ERM hyperplane collapses -- but the SAME mechanism predicts a count-matched marginal-attribution pool is also robust, so beating one hyperplane is pooling; isolating CO-RESPONSE SELECTION means beating the count-matched pool that drops the very absorber the under-served sub-context needs.

  The insight an interpretability expert would not reach for: SAE absorption/splitting are structurally the same obstacle that (a) defeats baseline co-expression in biology and (b) makes ERM probes brittle under subpopulation shift -- so observational co-activation/geometry AND marginal-attribution selection are the wrong instruments; interventional co-response is the matched instrument, correlation is the right grouping operator only for the shared-support splitting case, and maximum-coverage set-cover is the right operator for the disjoint-support absorption case. If correct, this turns off-the-shelf public SAEs into reliable, auditable concept units with a measurable recall recovery on absorbed sub-contexts -- across spelling AND at least one semantic hierarchy. If incorrect, the honest negatives are actionable: the K-proposal step fails at the pilot (set-cover cannot surface the right group); observational co-response equals interventional co-response (no gain from intervention); the unit ties (g)/(h) (robustness is pooling; contribution reduces to absorber-recovery + measured auditability); absorption is spelling-specific (scope C3); or SAE units should be abandoned for dense surface-invariant probes.
assumptions:
- >-
  THE TWO-TRACK CLUSTERING ALGORITHM CAN PROPOSE THE RIGHT UNITS AT PROPOSAL TIME, NOT JUST FILTER THEM. Splitting families
  (shared support, positive co-response correlation) are proposable by C-track correlation-community detection; absorption
  units (disjoint support, mutually exclusive firing) are proposable ONLY by the K-track anchored greedy max-coverage, because
  their members have low pairwise correlation. The K-anchor is selected by content-response RECALL using only the counterfactual
  pairs every baseline shares -- NOT by the Chanin absorption diagnostic -- so 'unsupervised unit beats supervised oracle'
  holds and KG-edge validation against that diagnostic is non-circular. We pre-register a Tier-0 PILOT proving the K-proposal
  recovers the worked 'starts-with-L' parent+absorbers (membership precision/recall vs the diagnostic, above a random-membership
  null) BEFORE C3 relies on it; if the proposal step fails there, the K-track is reported as failing at proposal time.
- >-
  MINIMAL PAIRS ARE OBTAINABLE AT HIGH QUALITY, LOW COST, AND NON-CIRCULARLY, FOR BOTH ABSORPTION HIERARCHIES AND THE SPLITTING
  FAMILIES. Content-flips use HUMAN-WRITTEN parallel corpora where available (ParaDetox toxic<->neutral; Kaushik 2020 CAD-IMDB
  sentiment; CEBaB human aspect edits) and templated/LLM-generated pairs (OpenRouter, well under $10, LLM-judge-scored for
  content-flipped + surface-preserved with reported pass rates) for first-letter substitutions and the non-spelling hierarchy
  (numeric-quantity formats or taxonomic entities). Any activation-space content edit, if used, is derived from an INDEPENDENT
  held-out diff-of-means on DISJOINT data, never from the SAE latents being grouped, so there is no circularity.
- >-
  THE C3 SPINE IS DEMONSTRATED ON ABSORPTION AS A PHENOMENON (TWO HIERARCHIES), NOT ONE SYNTHETIC TASK, WITH A HONEST-NULL
  FALLBACK. First-letter spelling is the documented, guaranteed-signal regime; one NON-SPELLING hierarchy (numeric-quantity
  formats primary, taxonomic 'is-a-country' alternative) is promoted into the NEVER-DROPPED Tier-1a core, scored by the FORM-FREE
  probe-plus-ablation absorption diagnostic. A NON-TRIVIALITY pre-check tests whether the non-spelling parent latent actually
  has specialist-filled holes; if it does not, we report that absorption is spelling-specific, scope the C3 title claim to
  spelling-type hierarchical absorption, and route cross-concept generality through C1 (toxicity/sentiment/aspect) -- the
  load-bearing core is unaffected either way.
- >-
  THE WIN, IF IT OCCURS, IS ATTRIBUTABLE TO CO-RESPONSE SELECTION AT MATCHED POOL SIZE -- NOT TO SUPERVISION, CAPACITY, OR
  MERE POOLING. C1 count-matches observational clusters (b)/(c) to the unit's exact member count (so beating them is not a
  capacity artifact; beating the single best latent (a) is a near-foregone capacity win reported only for completeness). (f)
  is information-matched via LEACE; (g) controls label selection; (h) max-pools EXACTLY #members SCR/TPP-selected raw directions,
  holding pool SIZE fixed so the ONLY varying factor is the membership/SELECTION criterion (co-response coverage vs marginal
  attribution). The pre-registered ORDERING (f) < (g)/(h) < unit on worst-sub-context recall isolates selection; beating (f)
  is conceded as pooling; beating (g)/(h) is the signal and equals C3 absorber-recovery.
- >-
  AUDITABILITY IS MEASURED, AND THE RUN FITS A SINGLE GPU WITHIN BUDGET. Off-the-shelf Gemma Scope SAEs on Gemma-2-2b expose
  latent counterfactual responses above noise on a single GPU for a few thousand minimal pairs per concept; chosen attributes
  have enough labeled/templatable data; paired base (pt) and instruction-tuned (it) Gemma Scope SAEs are available for model-diffing.
  The auditability claim is operationalized as a MEASURED repair loop (KG-guided absorber addition -> recall recovery on a
  targeted sub-context vs a random-addition control, with bootstrap CI) plus an LLM-judge member-labeling agreement metric
  against a shuffled-label null. Absorption is more severe at WIDER SAEs and splitting at larger width, so width/layer is
  a robustness axis (16k canonical primary; 65k drop-first). The load-bearing core fits the hard per-tier GPU-hour budgets
  below.
investigation_approach: |-
  DEPTH-FIRST EXECUTION ORDER WITH HARD PER-TIER BUDGETS AND A PRE-REGISTERED DROP ORDER. Single GPU; executor wall-clock ~6 h. The run is triaged so a clean LOAD-BEARING CORE is always produced.

  TIER 0 -- DE-RISKING PILOT INCLUDING THE PROPOSAL-STEP CHECK (<= 1.0 GPU-h, NEVER dropped). (ARM A, absorption, first-letter) build content-flip pairs; run the K-track STEP-3 set-cover given ONLY the pairs and verify the proposed anchor+absorbers MATCH the Chanin 2409.14507 diagnostic's parent+absorbers (membership precision/recall above a random-membership null) -- this proves the algorithm can PROPOSE K-units before C3 relies on it; also measure complementary coverage (pooled max tracks the flip where members have holes) vs the shuffled-pair null. (ARM B, splitting, toxicity) on ParaDetox/civil_comments measure how many latents carry toxicity, whether content-response profiles are positively correlated above null, and whether the C-track community + pooled unit beats the single best latent and the matched diff-of-means on a held-out IID slice. (ARM C, NON-SPELLING absorption non-triviality) on the chosen numeric/taxonomic hierarchy, test whether a high-recall parent latent exists AND has specialist-filled holes; a clean absence is reported as 'absorption is spelling-specific'. Proceed with a regime as headline only if its pilot clears the null.

  TIER 1a -- LOAD-BEARING CORE (<= 2.75 GPU-h, NEVER dropped). (1) C1: the co-response unit beats the best raw latent (a) AND COUNT-MATCHED observational co-activation/geometry clusters (b)/(c) on classification, on first-letter (absorption) AND the best-powered toxicity family; the matched (b)/(c) comparison is foregrounded as load-bearing. (2) C3 (the spine): on first-letter AND the non-spelling hierarchy, recovered-absorber count vs the oracle pool (g) and count-matched pool (h); sliced recall on the differing sub-contexts; KG specialization-edge agreement with the (form-free) absorption diagnostic. (3) the SELECTION-CRITERION ordering (f) < (g)/(h) < unit on worst-sub-context recall on the best-powered toxicity family, with the PAIRED-bootstrap per-pair gap and its slope-vs-reweighting as the primary inferential object. (4) the degenerate-construction guard and non-triviality check on (f). HARD CHECKPOINT: if the core has not cleared, STOP expanding and write up the core + honest negatives.

  ALWAYS-RUN MINIMAL GENERALITY + AUDITABILITY DEMOS (<= 0.75 GPU-h, NEVER dropped). (i) ONE null-floored STEERING result (toxicity unit direction vs best single latent vs matched diff-of-means: on-target effect + KL on unrelated prompts, above a shuffle null). (ii) ONE null-floored MODEL-DIFFING result (does the unit detect a base-vs-it concept-usage shift more reliably than the best single latent, above a shuffle null, using paired pt/it Gemma Scope SAEs?). (iii) THE MEASURED AUDITABILITY REPAIR LOOP: pick an under-served sub-context (recall hole on (f)); read the KG to find the absorber member covering it; ADD it; MEASURE recall recovery on that sub-context (bootstrap CI) AGAINST a random-content-responsive-latent-addition control, and confirm (k) exposes no per-sub-context member to add; PLUS an LLM-judge member-labeling agreement metric (predict each member's sub-context from its logit-lens tokens + conditioning contexts) vs a shuffled-label null. All three are stated as GENERALITY/AUDITABILITY DEMONSTRATIONS, not load-bearing.

  TIER 1b -- SUPPORTING (<= 1.5 GPU-h, demotable). Sentiment (CAD-IMDB) family; shift-decomposition conditions (i) surface-only + (ii) reweighting; the label-free group-inference probe (k) and oracle group-DRO probe (j); cluster-stability bootstraps (adjusted Rand / Jaccard vs null); per-family CIs.

  TIER 2 -- STRETCH (only if Tier 1a+1b land with budget left). CEBaB restaurant aspect-sentiment family; ONE DECISIVELY-executed steering case (matched on-target effect, KL on unrelated prompts + fluency, bootstrap CIs, engaging 2505.20063/AxBench); shift condition (iii) natural domain shift; a fuller model-diffing check; the SECOND non-spelling absorption hierarchy (taxonomic if numeric was primary, or vice versa).

  PRE-REGISTERED DROP ORDER (first dropped first): 4th out-of-domain axis -> CEBaB family -> shift condition (iii) -> oracle/label-free probes (j)/(k) -> sentiment family -> decisive Tier-2 steering (keep the minimal one) -> fuller model-diffing (keep the minimal one) -> second non-spelling hierarchy. NEVER dropped: Tier-0 pilot (incl. proposal-step check + non-triviality), Tier-1a core (incl. the FIRST non-spelling absorption hierarchy), the three minimal generality+auditability demos.

  COUNTERFACTUAL SIGNAL. Encode every text and its counterfactual with a frozen Gemma Scope residual-stream SAE (layer ~12, width 16k canonical). Per latent: content-response = delta(activation) under content-flip; surface-response = delta under surface-flip; aggregate into per-latent response profiles and cover sets across contexts.

  CLUSTERING METHOD (the in-scope contribution, specified above as STEPS 1-5 + pilot). C-TRACK: positive content-response correlation affinity (DiffCoEx-style) -> Leiden communities for splitting. K-TRACK: anchored greedy maximum-coverage over content-response cover sets for absorption (anchor = highest-recall content-responsive latent chosen WITHOUT the absorption diagnostic; greedily add mutually-exclusive, precise latents covering the anchor's holes until marginal coverage gain < 0.05 with CI excluding 0). RECONCILE C-communities and K-covers (anchor each community, augment with absorbers; seed K from standalone high-recall latents) into one de-duplicated output. Finalize each candidate unit with the SINGLE ADMISSION RULE (signature C OR matched-null signature K + small-k effect-size floor + mutual-exclusivity + precision floor, AND unit-level surface invariance); report the cleared signature per concept and the false-admit rate under both nulls. Emit human-auditable unit definitions (member latents, logit-lens tokens, conditioning contexts) and directed specialization edges (a member responsive only in a sub-context = absorbed/split child) = a feature-level knowledge graph.

  WORKED EXAMPLES. Toxicity unit (splitting, C-track): members = {profanity/slur latent, demeaning-insult latent, aggressive-imperative latent}; under ParaDetox detox all three drop together (signature C); pooled max tracks toxicity; pooled surface-response to paraphrase ~ 0. First-letter unit (absorption, K-track): anchor = general 'starts-with-L' latent (silent on 'lion'/'London'); greedy adds 'lion'-absorber then 'London'-absorber (each fires only in its sub-context, Jaccard ~ 0 with the anchor); pooled max covers 'starts-with-L' everywhere (signature K); pooled surface-response ~ 0. Numeric unit (non-spelling absorption, K-track): anchor = general 'numeric token' latent (holes on years/percentages); greedy adds a 4-digit-year absorber and a percentage absorber.

  BASELINES (matched baselines are primary). (a)-(k) as in the glossary; (b)/(c) COUNT-MATCHED to the unit for C1; (h) count-and-pool-matched for the selection-criterion isolation; (j)/(k) for the robustness bounds.

  EVAL -- LOAD-BEARING BACKBONE (reported regardless of dense-probe competitiveness): (1) co-response units have low Jaccard with co-activation/geometry clusters above the stability/shuffled-pair null; (2) units win specifically on the differing members -- sliced RECALL on the sub-contexts where the best latent / count-matched observational clusters / the oracle pool (g) / the count-matched pool (h) have holes, including absorbers (g)/(h) drop, on BOTH absorption hierarchies; (3) KG specialization edges agree with the form-free absorption diagnostic. EVAL -- CLASSIFICATION + SUPPORTING ROBUSTNESS: unit-pooled activation (max/sum over members) as classifier on IID and under the decomposed shifts; report F1/AUC AND worst-sub-context recall; the SELECTION-CRITERION prediction is the ORDERING (f) < (g)/(h) < unit with the unit-minus-(g)/(h) PAIRED gap GROWING in reweighting magnitude (slope CI primary). Robustness BOUNDS: unit approaches (j) without labels and is competitive-or-better than (k) while auditable. EVAL -- MEASURED AUDITABILITY: KG-guided absorber-addition recall recovery vs random-addition control (bootstrap CI); LLM-judge member-labeling agreement vs shuffled-label null. DEGENERATE-CONSTRUCTION GUARD applied throughout. STATISTICS: per-family paired-bootstrap CIs PRIMARY; cross-family aggregate DESCRIPTIVE; a-priori n_min=150 with stratified collection; cluster-stability bootstrap (adjusted Rand / Jaccard) vs shuffled-pair null.

  STEERING (Tier 2, ONE decisive case; minimal version always runs) and MODEL-DIFFING (minimal always runs; fuller Tier 2) as before -- generality demonstrations, not load-bearing, each null-floored.

  HONEST FAILURE-MODE REPORTING. The K-proposal set-cover failing to recover the worked unit at the pilot (proposal-step failure); the non-spelling parent having no specialist-filled holes (absorption spelling-specific -> scope C3); dependence on counterfactual quality (pass rates); concepts with no surface-invariant co-responding/complementary group; regimes where co-response collapses to co-activation (no gain over observational); the unit tying the count-matched pools (g)/(h) on sliced recall (robustness is pooling -> contribution reduces to absorber-recovery + measured auditability); the label-free group-inference probe (k) beating the unit on recall (loss-reweighting wins for pure robustness); the dense surface-invariant probe matching the unit on sliced recall (invariance supervision suffices; grouping adds only auditability); the oracle pool (g) tying the unit (selection not co-response structure); the reweighting test void because (f) does not collapse; the KG-guided repair not beating random-addition (auditability buys no fix); co-response too noisy to cluster (ARI ~ null); compute/SAE-width sensitivity; bias_in_bios boundary-null.
success_criteria: |-
  CONFIRMED if, pre-registered in this nesting (LOAD-BEARING CORE first):
  LOAD-BEARING (the paper stands on these alone, even if every robustness comparison ties and aggregate F1 ties the dense probe): (1) the Tier-0 pilot confirms above-null co-response structure AND the K-track PROPOSAL step recovers the known first-letter parent+absorbers (membership precision/recall above a random-membership null), with the toxicity arm also showing a pooled IID edge over the best single latent and the matched diff-of-means; (2) C1 -- the unit beats the best raw single latent AND COUNT-MATCHED observational co-activation/geometry clusters on classification on first-letter AND the best-powered toxicity family (matched-(b)/(c) per-family bootstrap CI excludes 0); the single-best-latent comparison is reported only for completeness; (3) C3 (the spine) -- on first-letter AND at least one NON-SPELLING absorption hierarchy the unit recovers absorber latents the oracle pool (g) and count-matched pool (h) drop, wins on the differing sub-contexts (paired-bootstrap gap CI excludes 0, sized to n_min=150), and its KG specialization edges agree with the (form-free) absorption diagnostic (2409.14507).
  SUPPORTING (strengthen the paper; honest nulls here do not sink it): (4) C2 + SELECTION-CRITERION ISOLATION -- the unit matches-or-beats (g) and (h) on classification AND shows the ORDERING (f) < (g)/(h) < unit on worst-sub-context recall, with a POSITIVE unit-minus-(g)/(h) PAIRED gap whose slope-vs-reweighting-magnitude CI excludes 0 (the unit-minus-(f) gap alone is conceded as pooling); (5) ROBUSTNESS BOUNDS -- the unit APPROACHES the oracle group-DRO probe (j) WITHOUT labels and is competitive-or-better than the label-free group-inference probe (k) while uniquely auditable; aggregate F1 vs (f) may tie; (6) MEASURED AUDITABILITY -- the KG-guided absorber-addition repair recovers recall on the targeted under-served sub-context with a bootstrap-CI gain over a random-content-responsive-latent-addition control, (k) cannot localize the fix, and LLM-judge member-labeling agreement exceeds a shuffled-label null; (7) ADMISSION + CONSTRUCTION INTEGRITY -- false-admit rate <= 0.05 under BOTH nulls; cluster assignments stable across bootstrap resamples (adjusted Rand/Jaccard above null); sub-contexts defined from independent labels frozen first, under-served determined on (f) alone, non-triviality check confirms (f) genuinely collapses; per-family CIs PRIMARY, cross-family DESCRIPTIVE.
  GENERALITY (always produced via the truncation fallback, never load-bearing): one null-floored steering result and one null-floored model-diffing result; the decisive Tier-2 steering case is confirmatory if it lands.
  HONEST NEGATIVES, each publishable: the K-track proposal step fails to recover the worked unit at the pilot (set-cover cannot surface disjoint-support absorbers); the non-spelling parent has no specialist-filled holes so absorption is spelling-specific (C3 scoped to spelling-type absorption, generality routed through C1); co-response grouping ties observational grouping (no gain from intervention); the unit ties (g)/(h) on sliced recall (robustness is pooling -> contribution reduces to absorber-recovery + measured auditability); (k) beats the unit on recall (loss-reweighting wins for pure robustness, unit still delivers the measured auditable repair); the dense surface-invariant probe matches the unit on sliced recall (grouping then contributes only auditability + the knowledge graph); the oracle pool (g) ties the unit (selection not co-response structure); the gap does NOT concentrate on the reweighting component or (f) does not collapse (supporting mechanism falsified/void, core unaffected); the KG-guided repair does not beat random-addition (auditability buys no measurable fix); co-response too noisy to cluster (ARI ~ null). bias_in_bios is a pre-registered boundary-null, not method failure.
related_works:
- >-
  Maximum-coverage / set-cover and the greedy (1-1/e) algorithm (Nemhauser, Wolsey, Fisher 1978; Feige 1998): the classic
  combinatorial-optimization instrument for selecting a small set of complementary subsets that jointly cover a universe.
  We transfer it as the K-TRACK PROPOSER: anchor on a parent latent, then greedily add mutually-exclusive latents whose content-response
  cover sets fill the anchor's holes. To our knowledge maximum-coverage has never been used to GROUP SAE latents -- and it
  is exactly the operator the disjoint-support absorption regime needs, where pairwise-affinity clustering provably cannot
  propose the right group.
- >-
  Differential co-expression / perturbation co-response module discovery (DiffCoEx, BMC Bioinformatics 2010; WGCNA): cluster
  genes by their CORRELATED RESPONSE TO A PERTURBATION rather than baseline co-expression, because co-regulated genes are
  often not co-expressed at baseline. This is the root of our C-TRACK (correlation-community detection on content-response
  profiles for the splitting regime); to our knowledge never applied to SAE/LLM features. Our novel claim is that the same
  baseline-vs-perturbation distinction explains and repairs SAE splitting, AND that the disjoint-support absorption case needs
  a SEPARATE set-cover operator, not correlation.
- >-
  A is for Absorption (Chanin et al., 2409.14507, NeurIPS 2025): a SUPERVISED DIAGNOSTIC -- identify the parent latent by
  max encoder-cosine with an LR probe, find the absorbing latent by ablation on the relevant logit. It DETECTS absorption
  on individual latents and demonstrates it empirically almost only on first-letter spelling (running non-spelling example:
  'short'/'starts-with-S'); it does not GROUP parent+absorbers into a usable unit, nor test absorption in semantic hierarchies.
  We use the FORM-FREE version (probe + ablation, domain-agnostic) ONLY to SCORE our already-formed unit's KG edges (never
  to form units, so non-circular), as a partial oracle for the pilot, and we add a novel empirical test of whether absorption
  generalizes to a non-spelling (numeric/taxonomic) hierarchy.
- >-
  Feature Hedging: Correlated Features Break Narrow SAEs (Chanin, Dulka, Garriga-Alonso, 2505.11756): ABSORPTION learns gerrymandered
  latents (worse at WIDER SAEs, parent->child hierarchy, mutually-exclusive firing) vs HEDGING merges correlated features
  into a SINGLE polysemantic latent (worse at NARROWER SAEs). We scope grouping to splitting+absorption (a hedged single latent
  is not groupable) and treat correlation/hierarchy as the mechanistic cause our interventional probe exposes -- correlation
  for shared-support splitting, set-cover for disjoint-support absorption.
- >-
  AxBench (Wu et al., ICML 2025 spotlight, 2501.17148) and Negative Results for SAEs on Downstream Tasks (DeepMind 2025):
  difference-in-means is the strongest concept-detection method and raw-latent SAEs are not competitive; this sets the dense-probe
  bar. We deliberately do NOT stake the load-bearing claim on beating it: C3 absorber-recovery is measured against SAE-SELECTION
  baselines (a)/(g)/(h), and aggregate-F1 parity with the surface-invariant dense probe (f) is pre-registered as acceptable.
- >-
  Sparse Autoencoders Do Not Find Canonical Units of Analysis (Bussmann et al., ICLR 2025, 2502.04878): uses SAE stitching
  and meta-SAEs to argue SAEs do not learn canonical units; its remedy is geometric/training-based. We propose a BEHAVIORAL
  unit defined by counterfactual co-response (correlation OR set-cover) and unit-level surface invariance, evaluated on downstream
  classification + steering + model-diffing, with no retraining.
- >-
  Subspace-Aware SAEs (SASA, 2606.06333, 2026), Matryoshka SAEs and Concept-Bottleneck SAEs (CVPR 2026), AbsTopK SAE, Group
  SAEs (negative results): all MODIFY SAE TRAINING -- decoder subspaces, nested dictionaries, concept bottlenecks, hard-thresholding,
  grouping losses -- to reduce absorption/splitting at training time. Our grouping is POST-HOC over a FROZEN public SAE's
  discrete latents, defined by interventional co-response, requiring no retraining and yielding an auditable feature-level
  knowledge graph.
- >-
  SHIFT / SCR / TPP SAE evaluation (Marks et al. 2024; Karvonen et al. 2411.18895): SELECT individual SAE latents by ranking
  causal effect on a concept probe (top-N), then ablate the set; they do NOT cluster latents by interventional co-response.
  This is exactly our supervised ORACLE-POOL baseline (g) and, count-matched, the pool (h); a latent firing only in a narrow
  sub-context (an absorber) has low marginal attribution and is silently dropped -- the specific gap our co-response set-cover
  fills, and the quantity the unit-minus-(g)/(h) sliced-recall gap measures.
- >-
  Co-activation feature families and graph-regularized SAEs (Disentangling Dense Embeddings 2408.00657; GSAE; Sparse Feature
  Coactivation 2506.18141): group SAE features by OBSERVATIONAL co-activation/geometry. By construction these cannot group
  a concept's absorbed/split latents (mutually exclusive in firing); for C1 we COUNT-MATCH them to the unit's member count
  so a unit win cannot be a capacity artifact. We use the opposite, INTERVENTIONAL signal and demonstrate the structural blind
  spot via low-Jaccard + sliced-recall wins.
- >-
  JTT (2107.09044), GEORGE / No Subclass Left Behind (2011.12945), EIIL (2010.07249), LfF (2007.02561): the label-free worst-group-robustness
  family -- infer GROUPS OVER EXAMPLES and RETRAIN with reweighted / group-DRO loss. Our route is orthogonal: we group FEATURES
  (discrete SAE latents) by interventional co-response, never retrain, and the recovered absorbers ARE the inferred sub-context
  specialists -- auditable. We add an oracle group-DRO probe (j, true sub-context labels = upper bound) and a label-free group-inference
  probe (k) as direct robustness baselines for the SUPPORTING result.
- >-
  Diverse Prototypical Ensembles (2505.23027): trains an ensemble of N diverse prototypes per class on FROZEN DENSE features
  with a diversity loss + bagging to capture subpopulation-specific patterns without group labels. The closest 'ensemble-of-specialists
  for subpopulation shift', but it TRAINS learnable prototype vectors on dense representations; we group pre-existing DISCRETE
  SAE latents by interventional co-response with no training, yielding auditable concept atoms (not opaque prototypes) and
  a feature-level knowledge graph.
- >-
  Group-DRO and subpopulation-shift robustness (Sagawa et al.; Mind the GAP: Group-Aware Priors, 2403.09869): a single ERM
  model collapses on under-served minority subgroups under mixing-weight shift; group-aware methods recover worst-group performance.
  We do NOT propose a new DRO method or theorem; we BORROW this as the a-priori mechanism explaining why a group-of-specialists
  unit out-generalizes a single hyperplane -- and use the SAME mechanism to predict a count-matched marginal-attribution pool
  is also robust, which is why selection is isolated against THAT pool, not the hyperplane.
- >-
  Discovering Concept Directions from Diffusion-based Counterfactuals via Latent Clustering (CDLC, 2505.07073; Pattern Recognition
  Letters 2025): clusters latent DIFFERENCE vectors from factual + diffusion-generated counterfactual IMAGE pairs into global
  class-specific concept DIRECTIONS (vision). Closest 'cluster counterfactual differences' template, but on a different substrate
  (one continuous direction per class in a diffusion latent space). We cluster DISCRETE SAE dictionary latents on a frozen
  LLM by their co-response PROFILES into auditable MULTI-MEMBER units, with a SET-COVER track for the absorption regime CDLC
  has no analogue for.
- >-
  LEACE (Belrose et al., 2306.03819) and Counterfactual Invariance to Spurious Correlations (Veitch et al., NeurIPS 2021,
  2106.00545): perfect linear concept erasure / MMD-based counterfactual-invariance regularizer. We erase the surface-flip
  direction to build the surface-invariant probe (f) -- a strong, principled non-SAE single hyperplane; beating it is conceded
  as a pooling effect, with selection isolated against the count-matched pools (g)/(h).
- >-
  Counterfactually-Augmented Data (Kaushik, Hovy, Lipton, ICLR 2020), CEBaB (Abraham et al., NeurIPS 2022, 2205.14140), ParaDetox
  (s-nlp, ACL 2022): human-written counterfactual minimal pairs for sentiment, aspect concepts, and toxicity. We use these
  for non-circular content-flips and independent sub-context labels for the degenerate-construction guard, not as the grouping
  method.
- >-
  Domain-Filtered Knowledge Graphs from SAE Features (2604.23829): builds an internal knowledge graph from SAE features via
  contrastive corpus filtering, co-occurrence, decoder geometry -- purely OBSERVATIONAL. Our feature-level knowledge graph
  is built from INTERVENTIONAL co-response/set-cover grouping, so its edges encode conditioning environments and specialization
  (absorbed/split children) invisible to observational co-occurrence -- and we MEASURE its utility via the auditability repair
  loop.
inspiration: >-
  A triple cross-field transfer, now with the named algorithm specified track-by-track. The SPLITTING-regime grouping (C-track)
  is a Level-3 methodological import from systems biology's differential co-expression / perturbation co-response module discovery
  (DiffCoEx, WGCNA): cluster units by CORRELATED RESPONSE TO A PERTURBATION, not baseline co-expression, because co-regulated
  genes are frequently not co-expressed until perturbed (genes->SAE latents, perturbation->content counterfactual). The crucial
  reviewer-prompted addition: correlation cannot group the ABSORPTION regime, because absorbers are mutually exclusive in
  firing and respond on disjoint supports -- so the K-track imports a SECOND, distinct instrument from combinatorial optimization,
  the MAXIMUM-COVERAGE / SET-COVER greedy (Nemhauser-Wolsey-Fisher; Feige): anchor on the highest-recall parent latent, then
  greedily add complementary specialists that cover its holes. The SUPPORTING robustness mechanism is a Level-1/2 import from
  distributionally-robust learning (group-DRO; Mind-the-GAP 2403.09869) and the label-free worst-group-robustness subfield
  (JTT, GEORGE, EIIL, LfF, Diverse Prototypical Ensembles): a single ERM hyperplane collapses on under-served minority subgroups
  under mixing-weight shift, whereas a union of specialists is robust -- and an absorber is precisely a specialist for one
  latent sub-context; because the SAME mechanism predicts a count-matched marginal-attribution pool is also robust, isolating
  CO-RESPONSE SELECTION means beating that pool, the SAME quantity as C3 absorber-recovery. These fuse with (i) causal ML's
  counterfactual invariance (Veitch 2021) and concept-erasure (LEACE, Belrose 2024) for the conceded surface-invariant baseline;
  (ii) NLP minimal-pair counterfactuals (ParaDetox, Kaushik 2020 CAD, CEBaB aspects) for non-circular perturbations and independent
  sub-context labels. The unifying insight an interpretability expert would not reach for: SAE splitting and absorption are
  TWO structurally different obstacles -- shared-support correlation (matched by DiffCoEx-style co-response correlation) vs
  disjoint-support coverage (matched by set-cover) -- the same dichotomy that distinguishes co-expression modules from complementary-pathway
  gene sets in biology, and the recovered absorbers ARE the latent subpopulations a robust classifier needs.
terms:
- term: Two-track clustering algorithm (the named contribution)
  definition: >-
    The grouping procedure: a C-TRACK that clusters content-responsive latents by positive content-response correlation (Leiden
    communities) for the SPLITTING regime where members share firing support, and a SEPARATE K-TRACK anchored greedy maximum-coverage
    for the ABSORPTION regime where members are mutually exclusive in firing and respond on disjoint supports (so correlation
    cannot propose them). C-communities and K-covers are reconciled into one de-duplicated output and filtered by the single
    admission rule.
- term: Cover set of a latent
  definition: >-
    C_l = the set of content-flip pairs whose flip latent l reliably and precisely tracks: r_l(p) above a response threshold,
    the latent fires on the content-on member, and the latent's content-response precision on its own firing support is >=
    0.7. The K-track operates on these cover sets; coverage-complementarity is defined as set intersection with an anchor's
    hole set, never as a vague pairwise affinity.
- term: Anchor-based greedy maximum-coverage (K-track)
  definition: >-
    The absorption-regime proposer. ANCHOR = the content-responsive latent with the highest cover-set size (highest recall
    of the concept's content flips), chosen using ONLY the counterfactual pairs (NOT the Chanin absorption diagnostic). HOLES
    = pairs the anchor does not cover (the absorbed sub-contexts). GREEDY: repeatedly add the latent covering the most uncovered
    holes subject to mutual-exclusivity (firing Jaccard<0.1), precision>=0.7, and a marginal coverage-gain floor (>=0.05 with
    bootstrap CI excluding 0). Recovers {general latent, per-sub-context absorbers} by construction, which correlation-merging
    clustering cannot.
- term: Proposal-step pilot validation
  definition: >-
    A Tier-0, never-dropped check that the K-track set-cover, given only content-flip pairs, RECOVERS the parent+absorbers
    the supervised Chanin 2409.14507 diagnostic identifies (membership precision/recall above a random-membership null) --
    proving the algorithm can PROPOSE absorption units before C3 relies on them. A failure here is reported as a proposal-step
    failure (an honest negative).
- term: Non-spelling absorption testbed (C3 generality)
  definition: >-
    A second absorption hierarchy promoted into the never-dropped Tier-1a core -- a NUMERIC-QUANTITY hierarchy (general numeric-token
    latent with year/percentage/date absorbers) as primary, or a TAXONOMIC 'is-a-country' hierarchy as the pre-registered
    alternative -- scored by the FORM-FREE (domain-agnostic) probe-plus-ablation absorption diagnostic. It moves C3 from one
    synthetic spelling task to absorption as a phenomenon AND is a novel empirical test of whether absorption generalizes
    beyond spelling, with a honest-null fallback (if no specialist-filled holes exist, absorption is reported spelling-specific
    and C3 is scoped accordingly).
- term: Feature absorption
  definition: >-
    A sparsity-induced failure (Chanin 2409.14507, 2505.11756) requiring a parent->child hierarchy: the more specific child
    latent suppresses the firing of the more general parent latent, which then has unpredictable holes. Parent and child are
    MUTUALLY EXCLUSIVE in firing (gerrymandered latents); absorption is worse at WIDER SAEs and documented empirically almost
    only on first-letter spelling.
- term: Feature splitting vs feature hedging
  definition: >-
    Splitting = one concept fragments across MANY latents (worse at larger width); sub-latents co-respond POSITIVELY to a
    content flip and share support -- the C-track (correlation) target. Hedging (Chanin 2505.11756) = a narrow SAE MERGES
    correlated features into a SINGLE polysemantic latent (worse at narrower width); a hedged single latent is NOT groupable
    but explains why inter-latent correlation exists.
- term: Interventional co-response (grouping criterion)
  definition: >-
    Latents belong to the same concept unit if they jointly track the content perturbation across contexts, even if their
    baseline activations never co-occur. Realized in two signatures via two operators: positive correlation of content-response
    profiles (signature C, splitting, C-track) and complementary coverage of an anchor's holes (signature K, absorption, K-track
    set-cover).
- term: Count-matched C1 comparison
  definition: >-
    For C1 the observational co-activation/geometry clusters (b)/(c) are CUT to the unit's exact member count k (top-k members
    by the same pooling rule), so a unit win is at matched pool size and cannot be a capacity/pooling artifact -- it shows
    co-response SELECTS the right members. Beating the single best raw latent (a) is a near-foregone capacity win reported
    only for completeness.
- term: Measured auditability repair loop
  definition: >-
    An always-run demo that operationalizes auditability as a result: pick an under-served sub-context (recall hole on the
    dense probe), read the knowledge graph to identify the absorber covering it, ADD it, and MEASURE recall recovery on that
    sub-context (bootstrap CI) against a random-content-responsive-latent-addition control, confirming a retrained label-free
    probe (k) exposes no per-sub-context member to add. Paired with an LLM-judge member-labeling agreement metric (predict
    each member's sub-context from logit-lens tokens + contexts) vs a shuffled-label null.
- term: Surface-invariant matched probe (baseline f, single hyperplane)
  definition: >-
    A counterfactually-matched diff-of-means/linear probe on content-flip residual deltas, made surface-invariant by ERASING
    the surface-flip direction via LEACE / mean-projection (Belrose 2024). A SINGLE hyperplane; the unit beating it is conceded
    to be a POOLING effect, not selection evidence.
- term: Supervised oracle pool (g) and count-and-pool-matched probe (h)
  definition: >-
    (g) pools the top-N SAE latents selected by SCR/TPP probe-attribution causal effect; because it ranks by MARGINAL attribution
    it silently drops absorbed latents firing only in narrow sub-contexts. (h) max-pools EXACTLY #members raw residual directions
    selected by the SAME SCR/TPP attribution, holding pool SIZE fixed so the only varying factor vs the unit is the membership/SELECTION
    criterion (co-response coverage vs marginal attribution). The unit-vs-(g)/(h) sliced-recall comparison is the selection-isolating
    headline test and equals C3 absorber-recovery.
- term: Oracle group-DRO probe (j) and label-free group-inference probe (k)
  definition: >-
    (j) a dense probe trained with a group-DRO objective using the TRUE independent sub-context labels = worst-group-robustness
    UPPER BOUND; the unit is predicted to APPROACH it without using labels. (k) a dense probe made group-robust WITHOUT sub-context
    labels via JTT-style high-loss upweighting or GEORGE-style representation clustering + group-DRO; like the unit it uses
    no sub-context labels, but it reweights EXAMPLES and retrains, whereas the unit groups FEATURES, is training-free, and
    is auditable.
- term: Selection-criterion isolation
  definition: >-
    The pre-registered ORDERING (f) single hyperplane < (g)/(h) count-matched marginal-attribution pools < unit co-response
    pool on worst-sub-context recall. The unit-vs-(g)/(h) comparison holds POOL SIZE FIXED and varies ONLY the membership/SELECTION
    rule (co-response set-cover vs marginal SCR/TPP ranking); both pool, so it isolates SELECTION. The structural claim reduces
    to: co-response COVERAGE admits the absorber marginal-attribution ranking drops -- the SAME quantity as C3 absorber-recovery.
    Beating (f) is conceded as pooling.
- term: Single unit admission rule
  definition: >-
    A proposed unit is admitted iff it clears signature C (within-unit content-response correlation > 95th-pct shuffled-pair
    null) OR signature K (matched best-of-random-k coverage null + the small-k absolute effect-size floor >=0.05 with bootstrap
    CI excluding 0, with mutual-exclusivity Jaccard<0.1 and per-member precision>=0.7), AND its pooled surface-response is
    not above the shuffled-surface null. The cleared signature is reported per concept and the false-admit rate under both
    nulls (target <=0.05). The rule FILTERS units the two-track algorithm PROPOSES.
- term: Load-bearing core
  definition: >-
    The minimal pre-registered result set the paper stands on regardless of robustness outcomes: pilot (incl. K-proposal recovery
    + non-triviality) + count-matched C1 + C3 absorber-recovery vs (g)/(h) + KG-edge agreement on first-letter AND one non-spelling
    absorption hierarchy. Measured against SAE-selection baselines, not the dense-probe aggregate-F1 bar, so it does not depend
    on out-classifying a strong dense probe.
summary: >-
  SAE latents encoding one concept are often mutually exclusive in firing (feature absorption and splitting), so observational
  co-activation, decoder geometry, and marginal-attribution selection all structurally miss the right members. We group frozen-SAE
  latents by how they jointly track a content counterfactual via a two-track algorithm -- correlation-community detection
  for shared-support splitting, and an anchored greedy SET-COVER for disjoint-support absorption (which correlation cannot
  even propose) -- producing training-free, auditable multi-member units. The load-bearing result is that the unit beats raw
  latents and COUNT-MATCHED observational clusters and recovers the absorbers a count-matched marginal-attribution selection
  drops on BOTH first-letter spelling AND one non-spelling hierarchy (KG edges agreeing with the absorption diagnostic); a
  measured auditability repair loop and worst-sub-context robustness approaching an oracle group-DRO probe without labels
  are supporting results.
_relation_rationale: >-
  Same two-track frame; pivots iter2 to executing the core and grounds the regime claim in SAE-latent firing.
_confidence_delta: unchanged
_key_changes:
- >-
  Reframed the load-bearing core from 'pre-registered prediction' to the MANDATORY iteration-2 execution deliverable (the
  #1 reviewer demand: run the SAE pipeline). First-letter spelling designated the guaranteed-signal anchor to execute first.
- >-
  Added a single PRIMARY FALSIFICATION ENDPOINT on first-letter (E1: K-track recovers parent + >=2 absorbers above a random-membership
  null; E2: unit beats count-matched (g)/(h)/(b)/(c) on absorber-recovery/sliced recall, CI excluding 0) whose negative =
  method failure; demoted the honest-null branches to secondary characterizations (resolves the 'protocol that cannot lose'
  critique).
- >-
  Replaced the label-co-occurrence 'both regimes occur' standalone finding with a REQUIRED SAE-latent firing-Jaccard + parent-recall-hole
  measurement on Gemma Scope; the K-track necessity claim must be grounded in latent firing, not labels (resolves the major
  proxy critique).
- >-
  Elevated the first-letter STEERING demo (mean-member-decoder direction, matched on-target effect, full-vocab KL + PPL collateral
  vs diff-of-means and hub-alone) to a required deliverable; bounded MODEL-DIFFING as an explicitly-caveated shared-pt-SAE
  result or a limitation, removed from open-ended future work (resolves the major scope critique).
- >-
  Added anchor-FIDELITY validation (recall-argmax anchor vs diagnostic parent) and a threshold sensitivity sweep (Jaccard/precision/coverage-gain)
  to the Tier-0 pilot (resolves the anchor=parent methodology minor).
- >-
  Specified unit-proposal-level multiplicity correction (BH/Holm over candidate-unit admission tests per concept, report M
  and empirical false-admit rate from the real run), separate from across-claims Holm-Bonferroni (resolves the rigor minor).
- >-
  Strengthened the surface-invariance control: enlarge surface-pair sets, re-judge a sample with an independent model, report
  per-concept surface-response null sizes (resolves the same-model generate-and-judge circularity minor).
- >-
  Sharpened novelty deltas vs [13] domain-filtered KG (interventional specialization edges over multi-member units vs co-occurrence/geometry)
  and [14] subspace-aware SAEs (post-hoc vs retraining); updated Chanin absorption to NeurIPS 2025 Oral and flagged a 2026-citation
  venue audit.
- >-
  Scoped the non-spelling testbed as secondary to first-letter execution (run only after E1/E2 land), keeping its non-triviality
  gate and spelling-specific honest-null fallback.
- >-
  Confidence unchanged: the conceptual frame is intact and fully de-risked by validated data/dossiers, but no SAE evidence
  yet exists; the revision reorients the next iteration to produce it.
relation_type: evolution
</hypothesis>

<all_artifacts>
FULL EVIDENCE BASE: All 10 research artifacts across all iterations.

--- Item 1 ---
id: art_RidEJtBC7gPT
type: research
title: 'Two-Track CCRG Implementation Dossier: SAE Pipeline, 11 Baselines, Protocols'
summary: >-
  A decision-complete, code-ready implementation blueprint for the two-track Counterfactual Co-Response Grouping (CCRG) method
  on frozen Gemma Scope SAEs. Pins the SAE encoding pipeline (defensive from_pretrained loader, JumpReLU firing=encode>0,
  hook blocks.12.hook_resid_post), the C-track (signed soft-threshold + leidenalg RBConfigurationVertexPartition) and K-track
  (anchored greedy max-coverage) algorithm with all thresholds, all eleven baselines (a)-(k) as runnable specs (LEACE for
  f, SAEBench SCR/TPP for g/h, JTT/GEORGE/group-DRO for j/k), the AxBench steering protocol (harmonic-mean LLM-judge 0/1/2),
  a corrected model-diffing recipe (shared frozen pt-SAE on gemma-2-2b vs gemma-2-2b-it because no gemma-scope-2b-it SAE exists),
  the statistics plan (paired bootstrap, exact McNemar, MDE n_min=150, Holm-Bonferroni), and a fully-verified 30+ citation
  table including all four high-risk future-dated arXiv IDs (all resolve).
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_research_1
out_expected_files:
- research_out.json

--- Item 2 ---
id: art_I2MrezW41iQo
type: research
title: Absorption Diagnostic + Pinned Datasets Dossier for Two-Track SAE Grouping
summary: >-
  Executor-ready dossier de-risking the C3 absorption spine and pinning every data/infra build for the two-track co-response
  SAE-grouping experiment. WP1 extracts the Chanin 2409.14507 absorption diagnostic verified against the lasr-spelling/sae-spelling
  code: parent latent = max ENCODER-cosine with an LR probe (+ k-sparse splits at f1-jump 0.03); absorber = largest-negative
  integrated-gradients ablation (IG steps=6) on the first-letter logit-diff m=g[y]-mean(g[incorrect]); decision thresholds
  probe_cos_sim_threshold=0.025 computed on the DECODER (sae.W_dec), ablation_delta_threshold=1.0, EPS=1e-8, 200-FN cap, topk=10;
  absorption_rate=num_absorptions/lr_probe_true_positives; valid only layers 0-17. It also supplies the strictly non-circular
  FORM-FREE version the paper itself gives in Appendix A.13 (and SAEBench implements as absorption_fraction): latent l absorbs
  iff tau_c < (a_hat_l . d_p)/(a . d_p) with a_hat_l = enc_act*W_dec[l] and d_p the parent-concept LR-probe direction trained
  on data DISJOINT from clustering -- works at all layers, no output logit needed, never used to form units. WP2 confirms
  absorption is empirically documented ONLY on first-letter spelling (LessWrong toy-models post; SAEBench eval id 'absorption_first_letter';
  Matryoshka/H-SAE only mitigate via the spelling metric), making Testbed-2 both a generality test and a novel empirical test;
  numeric-quantity hierarchy is recommended primary (taxonomic country alternative) with concrete non-triviality gates (parent
  recall >=0.60; >=1 absorber with firing-Jaccard<0.10, sub-context precision>=0.70, hole-coverage gain>=0.05 with bootstrap
  CI excluding 0) and an honest-null fallback that scopes C3 to spelling and routes generality through C1. WP3 pins HF datasets:
  s-nlp/paradetox (en_toxic_comment/en_neutral_comment, 19,744 rows, openrail++); google/civil_comments (text + 7 float32
  sub-attrs, 1.8M/97k/97k, CC0, 414.95MB -> subsample); tasksource/counterfactually-augmented-imdb (Text/Sentiment, no pair-ids
  -> acmi-lab GitHub for pairing, license unknown); CEBaB/CEBaB (full aspect-majority schema, license NOT on card = TODO);
  LabHC/bias_in_bios (hard_text/profession-int64-0-27/gender, 257k/39.6k/99.1k, 266MB, MIT, full alphabetical profession map).
  WP4 gives generation prompts + an independent LLM-judge rubric and verified June-2026 OpenRouter prices (generator google/gemini-3.1-flash-lite
  $0.25/$1.50 or deepseek/deepseek-v4-flash $0.09/$0.18; judge anthropic/claude-haiku-4.5 $1.00/$5.00), totalling ~$5.9-7.6
  for ~5,000 pairs with a hard $10 stop. WP5 captures sae-spelling get_alpha_tokens (convert_tokens_to_string then strip one
  leading space then all-alpha) and prompt template '{word} has the first letter:'; pins pile-uncopyrighted rev 3be9033 (2023-08-31,
  non-streaming); and SAE.from_pretrained(release='gemma-scope-2b-pt-res-canonical', sae_id='layer_12/width_16k/canonical',
  d_model=2304) + the 65k variant. CRITICAL model-diffing finding: NO gemma-scope-2b-it SAE exists anywhere (Google IT residual
  SAEs only for 9B) -> use the SHARED pt SAE on both gemma-2-2b and gemma-2-2b-it activations; both Google models are gated,
  use unsloth/gemma-2-2b(-it) mirrors. Full detail in research_report.md; every pinned fact and citation is in research_out.json.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_research_2
out_expected_files:
- research_out.json

--- Item 3 ---
id: art_dpYpjSn2Xvg3
type: dataset
title: >-
  First-Letter-Spelling Absorption Testbed (L/O/T/I/D): minimal pairs + frozen Pile corpus
summary: |-
  First-Letter-Spelling Absorption Testbed — the load-bearing dataset for the Two-Track Co-Response Grouping hypothesis (building reliable cluster-level units from individual SAE latents). Pure CPU/data artifact: NO SAE, no model weights, no GPU. 17,180 examples in 5 per-letter dataset groups (first_letter_spelling_{L,O,T,I,D}; L primary, O/T/I/D secondary; degenerate S/X excluded), schema exp_sel_data_out (full/mini/preview all PASSED).

  Three linked components per letter: (A) content_flip minimal pairs — (x_on,x_off) in an IDENTICAL carrier where x_on slots a word STARTING WITH the target letter and x_off a surface-matched word that does NOT (matched on char length, single-token-ness, Pile log-frequency); 1,750 pairs / 3,500 rows. Feeds the Tier-0 K-track anchored set-cover PROPOSAL pilot and the C3 absorber-recovery spine; reconstruct via metadata_pair_id and compute r_l=a_l(x_on)-a_l(x_off). (B) surface_flip pairs — (x_a,x_b) in an identical carrier, BOTH words start with the target letter but differ; 590 pairs / 1,180 rows; for the unit-level surface-invariance admission check (pooled response to surface flips ~0). (C) corpus_context — 12,500 real ~48-token windows (2,500/letter) from monology/pile-uncopyrighted @ rev 3be9033, each centred on a slot-eligible word-initial target-letter token with token_position annotated; plus a per-letter occurrence table (<=2,000 word-types) in dataset-level metadata — the substrate for iteration-2's form-free/Chanin (2409.14507) absorption diagnostic to locate false-negative absorbers (e.g. lion, London).

  Words are anchored in the real gemma-2-2b vocabulary (unsloth/gemma-2-2b ungated mirror, vocab==256000) via the exact sae-spelling get_alpha_tokens slot-eligibility recipe (word-initial '_' marker AND alpha). 7 carriers per content pair: sae-spelling spelling prompts (t_verbose '{word} has the first letter:', t_colon, t_icl with contamination-free ICL examples) + 4 word-class-agnostic mention carriers.

  Row schema is FLAT (exp_sel_data_out): input, output (first letter, uppercase), and metadata_* keys (dataset, letter, pair_id, pair_type, role, sub_context=the word covered, target_word, counterpart_word, template_id, label_starts_with_target, is_single_token, is_slot_eligible, first_letter, fold, word_char_span; corpus rows add source_doc_id, pile_revision, token_position, target_token_id, window_char_span, target_char_in_window). Pairs LINK via shared metadata_pair_id + metadata_role ({on,off}/{var_a,var_b}). Folds: minimal pairs by target_word, corpus by source_doc_id (5 folds, no leakage).

  Validation: the deterministic check is AUTHORITATIVE and reports 0 violations / 17,180 rows (flip property + input-span correctness are guaranteed by construction). The LLM judge (google/gemini-3.1-flash-lite, $0.12 total, < $3 cap) is a SECONDARY grammaticality/independent audit with pass rates 0.89-0.99 per (letter,pair_type); judge false-negatives are retained because the deterministic check governs drops. Corpus token_position verified EXACT (tok(input,add_special_tokens=False)[token_position]==target_token_id) on sampled rows. Frozen & reproducible: pinned tokenizer + Pile revision 3be90335..., seed 1234, deps pinned in pyproject.toml; data.py rebuilds end-to-end. full_data_out.json=21MB (<100MB, no split). NOTE: iteration-2 reads SAE activations on these inputs; this artifact itself does not run the SAE.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_dataset_1
out_expected_files:
- data.py
- full_data_out.json
- preview_data_out.json
- mini_data_out.json

--- Item 4 ---
id: art_t2uUbjSwpd3t
type: dataset
title: 'Non-Spelling SAE Absorption Testbed: Numeric & Taxonomic Hierarchies'
summary: |-
  TEXT-ONLY dataset (no SAE/model/activation computation here) for testing whether SAE feature absorption — documented almost exclusively on first-letter spelling — generalizes to two NON-spelling parent concepts. It is the never-dropped C3-spine testbed for the Counterfactual Co-Response Grouping hypothesis. Output is the AII exp_sel_data_out schema (one example per data row; per-row metadata flattened to metadata_* keys, since nested objects are disallowed), grouped into exactly two datasets:
  • numeric_absorption (8,380 examples): parent = 'token is numeric (a digit / part of a number)'; absorber sub-contexts = year, percent, currency, date, decimal, integer, comma_number, ordinal (year/percent/currency/date are the primary candidates).
  • taxonomic_absorption (15,748 examples): parent = 'token is part of a country name'; absorber sub-contexts = individual countries.

  Each hierarchy ships three coordinated components: (A) content-flip minimal pairs — x_on contains the concept, x_off a surface-matched non-concept word at the same slot (taxonomic uses country-vs-city and country-vs-other-proper-noun negative families); (B) surface-flip pairs — same concept token in two different carrier sentences, for the unit-level surface-invariance admission check; (C) a frozen pile-uncopyrighted (rev 3be90335b66f24456a5d6659d9c8d208c0357119) diagnostic corpus of real natural-text windows labelled by frozen sub-context, plus matched negatives (no-digit, city-mention, no-country), so iter-2 can train a parent linear probe and run the per-sub-context false-negative (parent-hole) search.

  Every row marks the exact target span (target_text + char_start/char_end) and carries precomputed google/gemma-2-2b token indices (100% coverage; the tokenizer splits numbers into individual digit tokens). Sub-context labels are assigned purely from surface form / regex / gazetteer (pycountry + geonamescache) — independent of any SAE latent or model behaviour — so the degenerate-construction guard holds and the same labelled corpus equally supports the honest 'absorption is spelling-specific' null (uniform high parent-probe recall across sub-contexts). Frozen folds (seed 20240617): pairs split train/test 70/30 by pair_id (stratified by sub_context); corpus splits train/diagnostic 50/50 (stratified). absorption_readiness in manifest.json: ALL 8 numeric sub-contexts and 20 countries reach ≥150 diagnostic-fold positives (eligible for the inferential test); rarer sub-contexts/countries are kept and flagged descriptive_only. Content-flip (≥240) and surface-flip (≥120) per-hierarchy floors are exceeded. A deterministic templated backbone is supplemented by openai/gpt-4o-mini generation, with every content/surface pair (LLM-generated + 20% templated spot-check) LLM-judged on content_flipped/surface_preserved/grammatical — 100% pass at $0.0104 total spend (hard cap $4, ceiling $10). Ambiguous homographs (Georgia, Turkey, Chile, Jordan) and multi-word countries are flagged via metadata_notes / metadata_multi_token.

  Deliverables: data.py (canonical builder), pipeline.py + build_dataset.py (logic modules), full/mini/preview_data_out.json, schema.json (JSON Schema + logical nested view), manifest.json (per-sub-context counts, fold counts, pass rates, spend, pile revision, readiness), and pyproject.toml with pinned dependency versions. Reproduce with `python3 data.py --scale full`. iter-2 consumes this to run the Tier-0 non-triviality pre-check (does a high-recall parent latent exist AND have specialist-filled holes?), the form-free absorption diagnostic as oracle, and the K-track anchored greedy set-cover proposal step — with numeric as the primary novelty test and taxonomic as the pre-registered alternative.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_dataset_2
out_expected_files:
- data.py
- full_data_out.json
- preview_data_out.json
- mini_data_out.json

--- Item 5 ---
id: art_8QO7pl6Pd8UQ
type: dataset
title: 'Two-Track CCRG Toxicity Family: ParaDetox flips + civil_comments sub-contexts'
summary: >-
  A single schema-standardized TOXICITY dataset family for the Two-Track CCRG experiments (organizing SAE latents into reliable
  group-level units). 37,707 examples in the exp_sel_data_out schema, grouped into the two real source corpora and validated.
  THE BEST 2 DATASETS are the dataset groups: (1) paradetox = s-nlp/paradetox (Logacheva et al., ACL 2022; openrail++), 19,096
  rows; (2) civil_comments = google/civil_comments (Jigsaw Unintended Bias, Borkan et al. 2019; CC0 1.0), 18,611 rows. Three
  role-distinct components are carried via metadata_record_type: (a) content_pair (18,853) = human toxic<->neutral parallel
  sentences, the NON-CIRCULAR content perturbation P (metadata_text_on / metadata_text_off) for per-latent content-response;
  (b) surface_pair (546) = OpenRouter gpt-4o-mini toxic->toxic paraphrases (input / metadata_text_paired), double-gated (token
  Jaccard<0.6 AND norm edit-dist>0.25 AND LLM-judge toxicity_preserved+meaning_preserved; judge pass 70.6%, refusal 1.5%,
  cost $0.060), the surface-invariance control, folded into their seed corpus's group via metadata_origin_source; (c) classification
  (18,308) = civil_comments comments with a binary metadata_toxicity_label plus FROZEN multi-label sub-context labels (severe_toxicity,
  obscene, threat, insult, identity_attack, sexual_explicit) thresholded at 0.5 from the raw annotator-fraction floats (preserved
  in metadata_subcontext_floats for re-thresholding). Power: obscene/threat/insult/identity_attack/sexual_explicit are inferential@0.5
  with >=150 positives in every eval fold; severe_toxicity is flagged descriptive_only (too rare even at 0.3) -- not silently
  dropped. data_summary.json reports per-sub-context per-fold counts at 0.5 and 0.3, the sub-attribute pairwise Jaccard co-occurrence
  matrix (insult<->obscene ~0.245 shared-support => C-track; threat/identity_attack <0.05 disjoint => K-track), generation
  stats, and 316 reconciled cross-source collisions. Leakage-safe doc-level folds (metadata_fold in train/val/test) via union-find
  over normalized text: civil_comments keeps native splits; verified 0 pair_id and 0 source_sentence_id spanning folds and
  0 normalized texts in >1 fold. Sanity baselines (TF-IDF+logistic regression, train->test): toxicity AUC 0.851/F1 0.773;
  sub-contexts AUC 0.81-0.94; content_pair mean cos 0.685 (genuine flip), surface_pair 0.355 (reworded not copied). Files:
  data.py (stdlib-only uv assembler), full/mini/preview_data_out.json (validated), data_summary.json, README.md, pyproject.toml
  (47 pinned deps), and build/ (staged pipeline: ParaDetox content-flips, civil_comments stream-filter, OpenRouter surface
  generation, assembler, verify_baseline). Downstream consumers flatten datasets[*].examples and filter metadata_record_type.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_dataset_3
out_expected_files:
- data.py
- full_data_out.json
- preview_data_out.json
- mini_data_out.json

--- Item 6 ---
id: art_21JWypIydPMX
type: dataset
title: CCRG supporting sentiment/aspect families + bias_in_bios boundary-null dataset
summary: >-
  Three REAL, human-annotated datasets standardized into the CCRG shared minimal-pair schema and emitted in the canonical
  exp_sel_data_out format ({metadata, datasets:[{dataset, examples:[{input, output, metadata_*}]}]}), ONE example per text
  row, grouped by dataset, $0 LLM spend. Families (separable via metadata_family): (1) sentiment = CAD-IMDB (Kaushik et al.
  ICLR 2020), 4,880 rows / 2,440 human counterfactual content-flip pairs (positive<->negative), supporting; (2) restaurant_aspect
  = CEBaB (Abraham et al. NeurIPS 2022), 5,682 rows / 2,841 pairs (food 1,740 + service 1,101) flipping ONE aspect's sentiment
  with all four aspect majorities (food/service/ambiance/noise) + binarized review_sentiment retained as INDEPENDENT sub_context
  labels, supporting; (3) bias_in_bios_boundary = LabHC/bias_in_bios (De-Arteaga et al. 2019), 20,177 profession bios (28
  classes, gender as independent sub-context), the PRE-REGISTERED boundary-null where habitat~=label. Total 30,739 rows, 5,281
  reconstructable minimal pairs. Per row: input(text), output(canonical label), and metadata_* fields: id, family, dataset_source,
  concept(sentiment|food_sentiment|service_sentiment|profession), concept_label, sub_context(dict), pair_id, partner_id, pair_role(content_on|content_off|null),
  flip_type(content|null), is_content_pair, is_surface_pair(false for all), fold(train|dev|test), meta(raw fields incl char_len,
  token_overlap_with_partner, raw labels, subsample seed). Every (x_off,x_on) content pair is reconstructable via pair_id/partner_id
  (content_on=positive/concept-present member). is_surface_pair=false everywhere — surface flips are out of scope here (reserved
  for sibling ParaDetox/LLM artifacts); no surface pairs fabricated. NO derived statistics (MI/probes) computed — raw standardized
  data only. Every row validated against schema.json (jsonschema Draft7) AND full/mini/preview validated against exp_sel_data_out
  (aii-json). THREE plan errors were caught and corrected by empirical verification: (a) CAD-IMDB orig/<->new/ row alignment
  is FALSE (flip_rate~0.50, aligned Jaccard~=random~0.11) — authoritative pairing taken from the repo's combined/paired/*_paired.tsv
  via shared batch_id (true-pair Jaccard 0.816 vs random 0.108); (b) CEBaB edit_type is the edited ASPECT {food,service,ambiance,noise}
  and edit_goal is the target sentiment (the plan swapped them), and review_majority is a 1-5 star rating (binarized 1,2->neg
  / 4,5->pos / 3->neutral); (c) bias_in_bios ships no ClassLabel names, so the canonical 28-occupation alphabetical mapping
  (incl 'dj' at index 8) was verified empirically 17/17 by keyword hit-rate (nurse=13, attorney=2, surgeon=25, software_engineer=24,
  yoga_teacher=27), gender 0=male/1=female confirmed by pronouns; stratified (profession x gender, 56 strata) capped subsample
  with fixed seed 20240617, gender-balanced (male 10,054 / female 10,123). Licenses: CAD Apache-2.0, CEBaB CC-BY-4.0, bias_in_bios
  MIT. Reproduce all deliverables with `uv run data.py`. Downstream guidance: compute per-family bootstrap CIs as primary
  (families cleanly separated); treat any bias_in_bios null as the expected boundary outcome, not method failure; build content
  (x_off,x_on) deltas from pair_id.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_dataset_4
out_expected_files:
- data.py
- full_data_out.json
- preview_data_out.json
- mini_data_out.json

--- Item 7 ---
id: art_0ueMMR8Tt02P
type: experiment
title: >-
  Two-Track CCRG First-Letter Endpoint: E1/E2/C1, Admission & Steering on Gemma-Scope SAE
summary: |-
  EXECUTED the load-bearing two-track Counterfactual Co-Response Grouping (CCRG) experiment on a FROZEN Gemma-Scope layer-12/width-16k JumpReLU SAE over the first-letter spelling absorption testbed (letters L,O,T,I,D). Verdict = WORKS. Core LLM spend $0. Runs end-to-end in ~8 min on one RTX 4090.

  PIPELINE (method.py, fully implemented + baselines side-by-side): model = unsloth/gemma-2-2b (bf16); SAE loaded DIRECTLY from Gemma-Scope params.npz (canonical layer_12/width_16k/average_l0_82) to avoid sae_lens/transformer_lens version conflicts with transformers 5.x. Residual read via forward-hook on model.model.layers[12] output (== blocks.12.hook_resid_post). GATING CHECK PASSED: reconstruction cosine 0.924, explained-variance 0.857, L0 95.9, corpus token-id localization exact (0/64). Steps: (1) content-flip co-response matrix r_l(w)=a_l(on)-a_l(off) at the word token over spelling carriers; (2) eligibility Lr = firing-precision>=0.7 AND covers>=1 sub-context (a mean-over-words prefilter rejects the genuinely sparse 1-5-word absorbers, so a cover-based rule is used); (3) C-track: Spearman co-response affinity -> signed soft-threshold (beta=6) -> Leiden RBConfiguration, run in a SUBPROCESS with a 45s timeout + agglomerative fallback because Leiden's C extension intermittently hangs on tied-rank graphs; (4) K-track: anchor = highest-cover-set latent, then anchored greedy max-coverage adding precise (>=0.7), anchor-disjoint (firing-Jaccard<0.1) latents covering uncovered holes; (5) FORM-FREE diagnostic (non-circular oracle): corpus-trained probe d_p (acc ~0.99), parent = max encoder-cosine, absorber via (a_hat_l.d_p)/(a.d_p)>0.5; baselines count-matched to k: (a) best raw latent, (b) co-firing cluster, (c) decoder-cosine cluster, (h) oracle SCR/TPP attribution pool, plus oracle pools g10/g20.

  KEY RESULTS (per-example test-fold predictions are in the datasets array as predict_unit/a/b/c/h). HEADLINE C1 classification: the LABEL-FREE co-response UNIT is the best starts-with-letter classifier on ALL 5 letters (test AUC L 0.905, O 0.917, T 0.859, I 0.961, D 0.956), beating raw best latent (a), co-firing (b) / decoder (c) clusters, AND the count-matched oracle-attribution pool (h) every time. E1 (label-free absorption recovery vs the diagnostic, random-membership null): PASS on 4/5 (L,O,T,D recover parent + >=2 absorbers above the 95th-pct null; I fails ANCHOR-FIDELITY only - its max-coverage latent fires 0% on corpus, a spurious anchor, an honest mechanism finding). Units are human-auditable, e.g. L = anchor 205 (logit-lens Lohan/Ls/LS) + absorbers 3069=list, 2416=line, 8463=large; a directed specialization knowledge-graph (anchor->absorbed_child(word)) is emitted (70 edges). E2 (absorbed-slice recall): the unit beats all COUNT-MATCHED baselines (h,b,c) directionally on all 5 letters and SIGNIFICANTLY (paired-bootstrap CI excludes 0) on T (.925 vs .763) and I (.775 vs .496). Steering: the mean-member-decoder direction has the LOWEST full-vocab-KL collateral at matched on-target effect on the primary letter L (16.4 vs hub 27.9 / diffmean 30.4) and on D; on O/T/I a non-SAE diff-of-means or the hub is more surgical (steering is a generality demo, reported honestly). Admission (Step-5, BH/Holm): K_UNIT admitted via sigK; empirical false-admit under the matched random-k null 0.03-0.09.

  HONEST CAVEATS (recorded in the JSON): the recovered-absorber COUNT metric is d_p-CIRCULAR for the oracle baselines (the diagnostic and g/h both rank by the probe direction d_p), so the E2 verdict is based on the non-circular downstream metrics (C1 + count-matched sliced recall) with the count reported descriptively; within Lr even random k-latent pools classify well (so admission power comes from surface-invariance + the 95th-pct sigK test, not pooling per se); the C-track is secondary and used the agglomerative fallback for L/O (Leiden hang).

  OUTPUT method_out.json is exp_gen_sol_out-schema-valid: metadata holds all metrics (verdicts, config, gating_check, per-letter E1 with 36-cell threshold sweep / E2 with CIs+McNemar+Holm / C1 / admission / c_track, full steering on-target+KL+PPL curves with matched comparison and random-direction null, unit_definitions with logit-lens tokens and top corpus contexts, kg_edges, runtime_stats); datasets holds per-letter held-out content instances with predict_unit/a/b/c/h for the downstream solution-evaluation step. full/mini/preview variants generated and schema-validated; both JSONs < 1 MB (well under 100 MB). pyproject.toml pins all 55 deps. Provides the paper its PRIMARY positive finding (cluster-level units > single latents + non-SAE/oracle baselines on downstream classification) plus rigorous, honestly-scoped E1/E2/steering/admission evidence and failure modes.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_2/gen_art/gen_art_experiment_1
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 8 ---
id: art_-o2RPMOZp37A
type: experiment
title: 'Gemma-Scope toxicity: SAE firing-structure, count-matched C1, selection ordering'
summary: |-
  GPU experiment for the Two-Track CCRG method: organising frozen Gemma-Scope SAE latents (gemma-scope-2b-pt-res-canonical, layer_12/width_16k; firing=encode>0; residual captured by a forward hook on gemma-2-2b layers[12], validated by SAE reconstruction cosine 0.92 and L0~80/token) into cluster-level units, evaluated on the ParaDetox + civil_comments toxicity family (18,853 content pairs, 546 surface pairs, 18,308 classification rows). method_out.json (exp_gen_sol_out schema): metadata holds the full analysis; datasets[0] holds 2,980 per-example test-fold toxicity predictions for every method (predict_unit/a/b/c/h/d/e). Full/mini/preview variants validate; all <3MB.

  KEY RESULTS (full run). MAJOR-2 firing structure (replaces iter-1's label-co-occurrence proxy with real SAE-latent firing): the general toxicity latent g=12714 (Neuronpedia: 'profanity and vulgar expressions') fires on 94.3% of toxic content-flips (precision 0.996). Distinct, on-target detector latents exist for the label-disjoint sub-attributes - threat=11630 ('conflict and violence'), identity_attack=11573 ('race, identity, social justice'), insult=13367 ('hypocrite/moron/coward') - and they cover g's recall holes (cover-frac 0.74/0.93), BUT they co-fire with g (firing-Jaccard 0.40/0.29, far above the 0.10 absorption threshold). So SAE firing structure DEPARTS from the label co-occurrence structure: no mutual-exclusivity => K-necessity verdict REFUTED on toxicity (both branches were pre-registered as publishable; the K-track absorber win lives in the sibling first-letter experiment). This is the experiment's decisive, honest finding.

  C1 count-matched classification (primary scorer = logistic regression on each method's selected features, so only the SELECTION differs; secondary max-pool-z reported): the k=3 two-track co-response unit ties co-activation (b), decoder-geometry (c) and best-single-latent (a) on toxicity AUC (0.76 vs 0.80/0.79/0.77) but is beaten by SCR/TPP attribution selection (g/h=0.84-0.89), a full-residual probe (e=0.86) and diff-of-means (d), with unit-minus-h AUC CI [-0.093,-0.055] (exact McNemar Holm p~5e-71); and it COLLAPSES on the disjoint sub-attributes (threat 0.63 vs h 0.93; identity_attack 0.63 vs h 0.94). This is the benchmarked pattern that simple baselines and attribution often outperform raw-latent SAE grouping. Per-target paired bootstrap (B=10000 toxicity/2000 subs) + exact McNemar + Holm.

  Selection ordering: the pre-registered (f)<(g)/(h)<unit worst-sub-context-recall ordering does NOT hold (f=0.09 < unit=0.24 < g=0.39 < h=0.45); the unit-minus-(g/h) gap SLOPE vs measured disjoint sub-population reweighting = -0.47 (95% CI [-0.54,-0.41], excludes 0) - the unit's relative advantage SHRINKS under subpopulation shift. A clean honest negative. (f) is a LEACE surface-invariant probe.

  Unit construction: C-track = signed soft-thresholded Spearman of co-response profiles + Leiden RBConfiguration; gamma chosen by bootstrap-ARI stability subject to a non-trivial human-auditable g-community size (ARI-stability alone collapses to one giant cluster - documented gamma sweep included). K-track added 0 absorbers (consistent with the REFUTE branch). Admission/multiplicity: M=31 candidate units, BH-corrected with a Bonferroni-within-unit (C-or-K) signature p and a surface-response AND-gate; 11 admitted; empirical family-wise false-admit rate on the random-k null = 0.08 (reported as a limitation). Surface null caveat (n=546, gpt-4o-mini gen+judge, same-model circularity) flagged.

  Baselines vs reviewer scope: raw SAE latents (a), co-activation (b), decoder-geometry (c), SCR/TPP attribution pool (g) and raw-direction (h); non-SAE diff-of-means probe (d) and logistic regression on raw residuals (e). Human-auditable cluster definitions via Neuronpedia auto-interp labels + top tokens for every key latent (firing_structure.neuronpedia_labels, unit.member_labels). Stats: tie-aware AUC, exact McNemar, Holm-Bonferroni, paired bootstrap CIs. Files: method.py, enrich_neuronpedia.py, probe.py, pyproject.toml (pinned), README.md, full/mini/preview_method_out.json. Caches (cache/, hf_cache/) are excluded from publication.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_2/gen_art/gen_art_experiment_2
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 9 ---
id: art_QGSdsKY6U1vK
type: experiment
title: >-
  SAE Absorption Generalizes Beyond Spelling: Numeric & Taxonomic (Gemma Scope L12)
summary: |-
  C3 generality experiment for the two-track CCRG hypothesis. Question: does SAE feature absorption (documented almost only on first-letter spelling) generalize to NON-spelling token hierarchies? Encodes the frozen non-spelling testbed (numeric_absorption 8,380 rows; taxonomic_absorption 15,748 rows) through google/gemma-2-2b + Gemma Scope layer_12/width_16k SAE and runs the non-triviality gate + K-track anchored greedy set-cover, vs marginal-attribution baselines and a non-SAE probe.

  VERDICT = non_spelling_absorption_confirmed: the gate PASSES on BOTH hierarchies (absorption is NOT spelling-specific).

  PIPELINE/VALIDATION: SAE loaded directly from DeepMind params.npz (JumpReLU; no sae_lens dependency). Residual taken at HF hidden_states[13] == blocks.12.hook_resid_post, empirically selected by FVU sweep over indices {11,12,13}; encode-time FVU=0.18 (numeric)/0.20 (taxonomic), token-alignment 0.975/1.000, mean L0 68/101 — all three V1/V2/V3 gates pass.

  NUMERIC: anchor latent 14823 (content-response precision 1.000, negative-firing 0.001; recall 0.829 content-flip / 0.427 corpus) misses 1060/1850 corpus positives (holes). K-track recovers 3 absorbers (year, decimal x2). C3 confirmed via the 'integer' sub-context: unit recall 0.28 vs (g)/(h) 0.11, paired-bootstrap diff +0.18 CI[0.12,0.24], Holm p=8e-8. On year/date/decimal the broader 20-latent oracle pool beats the compact 4-latent unit (honest, mixed). Form-free absorption_fraction KG-agreement ~ null (coverage-based and projection-based absorber notions DIVERGE here). Unit has 0 false-positives vs (g)/(h) 0.12/0.13; the non-SAE dense probe reaches recall 1.000 at 0 FP (the 'simple baselines can match raw-SAE' point, honestly reported).

  TAXONOMIC: anchor latent 3792 (recall 0.953, neg-fire 0.033); K-track recovers Georgia/Jordan/United-States specialists. C3 confirmed via 'Georgia': unit beats the count-matched (h) pool, diff CI[0.073,0.307] — the K-track recovers a country-specialist that marginal attribution drops at matched pool size. Form-free KG-agreement = 0.318 vs null 0.0016 (the projection diagnostic CORROBORATES the K-track edges here, unlike numeric). (g)/(h) oracle pools have huge FP (0.85/0.65) while the unit is clean (0.014).

  BASELINES & STATS: raw single SAE latent (anchor-alone), (g) SCR/TPP-style top-20 marginal-attribution oracle pool, (h) count-matched top-k pool, and a non-SAE dense logistic/diff-of-means probe (trained on the DISJOINT corpus-train fold). Reported per eligible sub-context (>=150 diagnostic positives) at both the >0 JumpReLU rule and matched overall recall: paired bootstrap (B=10000), exact McNemar, Holm-Bonferroni multiplicity, threshold-sensitivity sweep over Jaccard/precision/gain, admission (signature-K AUC-gain vs AUC-matched random-k null + surface-invariance), and parent-probe recall-by-sub-context (honest-null uniformity check). The form-free diagnostic only SCORES edges (probe direction trained disjoint), never forms units (non-circular).

  HEADLINE for the paper: absorption generalizes beyond spelling to numeric and country hierarchies; the K-track recovers specialist absorbers (integer; Georgia) that marginal-attribution pools drop, and yields a compact, near-zero-FP, human-auditable cluster (anchor + named specialist edges). Honest nuance: gains are sub-context-specific (not a blanket win over the 20-latent oracle), and the coverage-based vs projection-based absorption definitions agree for taxonomic but diverge for numeric. method_out.json carries full per_hierarchy results in metadata + per-row detector predictions (predict_unit/anchor/g/h/dense_probe) on the diagnostic fold; results/ has partial per-hierarchy JSON, sliced-recall CSVs, and .npz figure arrays.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_2/gen_art/gen_art_experiment_3
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 10 ---
id: art_YwjLYapklnVk
type: dataset
title: 'Surface-Invariance Pair Superset: First-Letter 1,700 + Toxicity 1,631 Pairs'
summary: |-
  Drop-in SUPERSET of the two iter-1 surface-flip pair sets that the next iteration's Step-5 admission AND-gate consumes to estimate the shuffled-surface null (a candidate SAE unit is admitted only if its pooled surface-response is NOT above this null). Emits ONLY the surface-pair superset; the frozen iter-1 content_flip/content_pair/classification/corpus rows stay canonical at their iter-1 paths and are merged by metadata_pair_id/metadata_record_type. Pure CPU/data (no GPU, no SAE, no activations).

  full_data_out.json (exp_sel_data_out schema, PASSED) has 7 dataset groups / 5,031 surface rows: five first_letter_spelling_{L,O,T,I,D} groups (1,700 pairs = 3,400 rows; var_a/var_b linked by metadata_pair_id; int fold 0-4 by target_word) and paradetox + civil_comments groups (1,631 one-row toxicity pairs; input=source toxic, metadata_text_paired=toxic paraphrase; train/val/test fold by source, 0 cross-fold leakage). Both concepts exceed the >=1,500 target.

  FIRST-LETTER (concept 'starts-with-X'): 590 -> 1,700 pairs (340/letter, balanced across the 5 iter-1 carriers), built deterministically ($0) from the iter-1 Pile occurrence_tables (unsloth/gemma-2-2b get_alpha_tokens slot-eligible single-token words); authoritative structural validator = 0 violations. TOXICITY (concept 'toxic'): 546 -> 1,631 pairs (+1,085 new: civil 803, paradetox 282) generated by openai/gpt-4o-mini and gated by token Jaccard<0.6 AND norm char-change>0.25 (strict, verbatim from iter-1), then accepted by an INDEPENDENT family judge anthropic/claude-haiku-4.5 (toxicity_constant AND meaning_preserved AND surface_changed AND fluent). civil-origin new pairs carry real sub-attribute floats; per-sub pairs: insult 370, obscene 226, sexual_explicit 216, identity_attack 211, threat 205, severe_toxicity 12.

  Circularity fixed (iter-1 used the SAME gpt-4o-mini to generate AND judge toxicity, and gemini-3.1-flash-lite for first-letter): every new toxicity pair is born with a claude-haiku-4.5 label; a stratified sample of both concepts is re-judged by families different from both generator and original judge. Reportable findings: claude confirms 465/546 = 85.2% of gpt-4o-mini-accepted toxicity originals; toxicity cross-judge claude-vs-gemini raw 0.940 / Cohen kappa 0.263 (n=399, high base rate); first-letter independent audit claude pass-rate 0.68 (0.32 judge false-negative on tokenizer-artifact words; deterministic check is AUTHORITATIVE so these are NEVER dropped), claude-vs-deepseek raw 0.780 / kappa 0.433 (n=268), claude-vs-stored-gemini raw 0.692 / kappa 0.141 (n=130).

  Every row carries additive keys metadata_enlargement_batch in {iter1_original,iter2_new} and metadata_independent_judge_{model,pass,reason} (all toxicity rows populated; first-letter populated for the re-judge sample, else null). iter-1 originals are byte-identical except those additive keys (verified: 0 problems, true superset, no id collisions). data_summary.json reports the per-concept null-distribution sizes (per letter x carrier; per origin x fold; per sub-attribute), both-judges-pass high-confidence subset sizes (toxicity 370, first-letter 172 in-sample), generation/re-judge stats, agreement/kappa, originals-confirmation rate, and gate constants (jaccard_max=0.6, char_change_min=0.25). Total OpenRouter spend $1.72 (hard cap $10). Models: openai/gpt-4o-mini, anthropic/claude-haiku-4.5, google/gemini-3.1-flash-lite, deepseek/deepseek-v4-flash. Reproduce with `uv run data.py` (caches make re-runs $0).
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_2/gen_art/gen_art_dataset_1
out_expected_files:
- data.py
- full_data_out.json
- preview_data_out.json
- mini_data_out.json
</all_artifacts>

<new_artifacts_this_iteration>
NEW THIS ITERATION: These 4 artifacts were created to address the reviewer
feedback. Their findings should be the primary basis for your revisions.

type: experiment
id: art_0ueMMR8Tt02P
summary: |-
  EXECUTED the load-bearing two-track Counterfactual Co-Response Grouping (CCRG) experiment on a FROZEN Gemma-Scope layer-12/width-16k JumpReLU SAE over the first-letter spelling absorption testbed (letters L,O,T,I,D). Verdict = WORKS. Core LLM spend $0. Runs end-to-end in ~8 min on one RTX 4090.

  PIPELINE (method.py, fully implemented + baselines side-by-side): model = unsloth/gemma-2-2b (bf16); SAE loaded DIRECTLY from Gemma-Scope params.npz (canonical layer_12/width_16k/average_l0_82) to avoid sae_lens/transformer_lens version conflicts with transformers 5.x. Residual read via forward-hook on model.model.layers[12] output (== blocks.12.hook_resid_post). GATING CHECK PASSED: reconstruction cosine 0.924, explained-variance 0.857, L0 95.9, corpus token-id localization exact (0/64). Steps: (1) content-flip co-response matrix r_l(w)=a_l(on)-a_l(off) at the word token over spelling carriers; (2) eligibility Lr = firing-precision>=0.7 AND covers>=1 sub-context (a mean-over-words prefilter rejects the genuinely sparse 1-5-word absorbers, so a cover-based rule is used); (3) C-track: Spearman co-response affinity -> signed soft-threshold (beta=6) -> Leiden RBConfiguration, run in a SUBPROCESS with a 45s timeout + agglomerative fallback because Leiden's C extension intermittently hangs on tied-rank graphs; (4) K-track: anchor = highest-cover-set latent, then anchored greedy max-coverage adding precise (>=0.7), anchor-disjoint (firing-Jaccard<0.1) latents covering uncovered holes; (5) FORM-FREE diagnostic (non-circular oracle): corpus-trained probe d_p (acc ~0.99), parent = max encoder-cosine, absorber via (a_hat_l.d_p)/(a.d_p)>0.5; baselines count-matched to k: (a) best raw latent, (b) co-firing cluster, (c) decoder-cosine cluster, (h) oracle SCR/TPP attribution pool, plus oracle pools g10/g20.

  KEY RESULTS (per-example test-fold predictions are in the datasets array as predict_unit/a/b/c/h). HEADLINE C1 classification: the LABEL-FREE co-response UNIT is the best starts-with-letter classifier on ALL 5 letters (test AUC L 0.905, O 0.917, T 0.859, I 0.961, D 0.956), beating raw best latent (a), co-firing (b) / decoder (c) clusters, AND the count-matched oracle-attribution pool (h) every time. E1 (label-free absorption recovery vs the diagnostic, random-membership null): PASS on 4/5 (L,O,T,D recover parent + >=2 absorbers above the 95th-pct null; I fails ANCHOR-FIDELITY only - its max-coverage latent fires 0% on corpus, a spurious anchor, an honest mechanism finding). Units are human-auditable, e.g. L = anchor 205 (logit-lens Lohan/Ls/LS) + absorbers 3069=list, 2416=line, 8463=large; a directed specialization knowledge-graph (anchor->absorbed_child(word)) is emitted (70 edges). E2 (absorbed-slice recall): the unit beats all COUNT-MATCHED baselines (h,b,c) directionally on all 5 letters and SIGNIFICANTLY (paired-bootstrap CI excludes 0) on T (.925 vs .763) and I (.775 vs .496). Steering: the mean-member-decoder direction has the LOWEST full-vocab-KL collateral at matched on-target effect on the primary letter L (16.4 vs hub 27.9 / diffmean 30.4) and on D; on O/T/I a non-SAE diff-of-means or the hub is more surgical (steering is a generality demo, reported honestly). Admission (Step-5, BH/Holm): K_UNIT admitted via sigK; empirical false-admit under the matched random-k null 0.03-0.09.

  HONEST CAVEATS (recorded in the JSON): the recovered-absorber COUNT metric is d_p-CIRCULAR for the oracle baselines (the diagnostic and g/h both rank by the probe direction d_p), so the E2 verdict is based on the non-circular downstream metrics (C1 + count-matched sliced recall) with the count reported descriptively; within Lr even random k-latent pools classify well (so admission power comes from surface-invariance + the 95th-pct sigK test, not pooling per se); the C-track is secondary and used the agglomerative fallback for L/O (Leiden hang).

  OUTPUT method_out.json is exp_gen_sol_out-schema-valid: metadata holds all metrics (verdicts, config, gating_check, per-letter E1 with 36-cell threshold sweep / E2 with CIs+McNemar+Holm / C1 / admission / c_track, full steering on-target+KL+PPL curves with matched comparison and random-direction null, unit_definitions with logit-lens tokens and top corpus contexts, kg_edges, runtime_stats); datasets holds per-letter held-out content instances with predict_unit/a/b/c/h for the downstream solution-evaluation step. full/mini/preview variants generated and schema-validated; both JSONs < 1 MB (well under 100 MB). pyproject.toml pins all 55 deps. Provides the paper its PRIMARY positive finding (cluster-level units > single latents + non-SAE/oracle baselines on downstream classification) plus rigorous, honestly-scoped E1/E2/steering/admission evidence and failure modes.
title: >-
  Two-Track CCRG First-Letter Endpoint: E1/E2/C1, Admission & Steering on Gemma-Scope SAE

type: experiment
id: art_-o2RPMOZp37A
summary: |-
  GPU experiment for the Two-Track CCRG method: organising frozen Gemma-Scope SAE latents (gemma-scope-2b-pt-res-canonical, layer_12/width_16k; firing=encode>0; residual captured by a forward hook on gemma-2-2b layers[12], validated by SAE reconstruction cosine 0.92 and L0~80/token) into cluster-level units, evaluated on the ParaDetox + civil_comments toxicity family (18,853 content pairs, 546 surface pairs, 18,308 classification rows). method_out.json (exp_gen_sol_out schema): metadata holds the full analysis; datasets[0] holds 2,980 per-example test-fold toxicity predictions for every method (predict_unit/a/b/c/h/d/e). Full/mini/preview variants validate; all <3MB.

  KEY RESULTS (full run). MAJOR-2 firing structure (replaces iter-1's label-co-occurrence proxy with real SAE-latent firing): the general toxicity latent g=12714 (Neuronpedia: 'profanity and vulgar expressions') fires on 94.3% of toxic content-flips (precision 0.996). Distinct, on-target detector latents exist for the label-disjoint sub-attributes - threat=11630 ('conflict and violence'), identity_attack=11573 ('race, identity, social justice'), insult=13367 ('hypocrite/moron/coward') - and they cover g's recall holes (cover-frac 0.74/0.93), BUT they co-fire with g (firing-Jaccard 0.40/0.29, far above the 0.10 absorption threshold). So SAE firing structure DEPARTS from the label co-occurrence structure: no mutual-exclusivity => K-necessity verdict REFUTED on toxicity (both branches were pre-registered as publishable; the K-track absorber win lives in the sibling first-letter experiment). This is the experiment's decisive, honest finding.

  C1 count-matched classification (primary scorer = logistic regression on each method's selected features, so only the SELECTION differs; secondary max-pool-z reported): the k=3 two-track co-response unit ties co-activation (b), decoder-geometry (c) and best-single-latent (a) on toxicity AUC (0.76 vs 0.80/0.79/0.77) but is beaten by SCR/TPP attribution selection (g/h=0.84-0.89), a full-residual probe (e=0.86) and diff-of-means (d), with unit-minus-h AUC CI [-0.093,-0.055] (exact McNemar Holm p~5e-71); and it COLLAPSES on the disjoint sub-attributes (threat 0.63 vs h 0.93; identity_attack 0.63 vs h 0.94). This is the benchmarked pattern that simple baselines and attribution often outperform raw-latent SAE grouping. Per-target paired bootstrap (B=10000 toxicity/2000 subs) + exact McNemar + Holm.

  Selection ordering: the pre-registered (f)<(g)/(h)<unit worst-sub-context-recall ordering does NOT hold (f=0.09 < unit=0.24 < g=0.39 < h=0.45); the unit-minus-(g/h) gap SLOPE vs measured disjoint sub-population reweighting = -0.47 (95% CI [-0.54,-0.41], excludes 0) - the unit's relative advantage SHRINKS under subpopulation shift. A clean honest negative. (f) is a LEACE surface-invariant probe.

  Unit construction: C-track = signed soft-thresholded Spearman of co-response profiles + Leiden RBConfiguration; gamma chosen by bootstrap-ARI stability subject to a non-trivial human-auditable g-community size (ARI-stability alone collapses to one giant cluster - documented gamma sweep included). K-track added 0 absorbers (consistent with the REFUTE branch). Admission/multiplicity: M=31 candidate units, BH-corrected with a Bonferroni-within-unit (C-or-K) signature p and a surface-response AND-gate; 11 admitted; empirical family-wise false-admit rate on the random-k null = 0.08 (reported as a limitation). Surface null caveat (n=546, gpt-4o-mini gen+judge, same-model circularity) flagged.

  Baselines vs reviewer scope: raw SAE latents (a), co-activation (b), decoder-geometry (c), SCR/TPP attribution pool (g) and raw-direction (h); non-SAE diff-of-means probe (d) and logistic regression on raw residuals (e). Human-auditable cluster definitions via Neuronpedia auto-interp labels + top tokens for every key latent (firing_structure.neuronpedia_labels, unit.member_labels). Stats: tie-aware AUC, exact McNemar, Holm-Bonferroni, paired bootstrap CIs. Files: method.py, enrich_neuronpedia.py, probe.py, pyproject.toml (pinned), README.md, full/mini/preview_method_out.json. Caches (cache/, hf_cache/) are excluded from publication.
title: 'Gemma-Scope toxicity: SAE firing-structure, count-matched C1, selection ordering'

type: experiment
id: art_QGSdsKY6U1vK
summary: |-
  C3 generality experiment for the two-track CCRG hypothesis. Question: does SAE feature absorption (documented almost only on first-letter spelling) generalize to NON-spelling token hierarchies? Encodes the frozen non-spelling testbed (numeric_absorption 8,380 rows; taxonomic_absorption 15,748 rows) through google/gemma-2-2b + Gemma Scope layer_12/width_16k SAE and runs the non-triviality gate + K-track anchored greedy set-cover, vs marginal-attribution baselines and a non-SAE probe.

  VERDICT = non_spelling_absorption_confirmed: the gate PASSES on BOTH hierarchies (absorption is NOT spelling-specific).

  PIPELINE/VALIDATION: SAE loaded directly from DeepMind params.npz (JumpReLU; no sae_lens dependency). Residual taken at HF hidden_states[13] == blocks.12.hook_resid_post, empirically selected by FVU sweep over indices {11,12,13}; encode-time FVU=0.18 (numeric)/0.20 (taxonomic), token-alignment 0.975/1.000, mean L0 68/101 — all three V1/V2/V3 gates pass.

  NUMERIC: anchor latent 14823 (content-response precision 1.000, negative-firing 0.001; recall 0.829 content-flip / 0.427 corpus) misses 1060/1850 corpus positives (holes). K-track recovers 3 absorbers (year, decimal x2). C3 confirmed via the 'integer' sub-context: unit recall 0.28 vs (g)/(h) 0.11, paired-bootstrap diff +0.18 CI[0.12,0.24], Holm p=8e-8. On year/date/decimal the broader 20-latent oracle pool beats the compact 4-latent unit (honest, mixed). Form-free absorption_fraction KG-agreement ~ null (coverage-based and projection-based absorber notions DIVERGE here). Unit has 0 false-positives vs (g)/(h) 0.12/0.13; the non-SAE dense probe reaches recall 1.000 at 0 FP (the 'simple baselines can match raw-SAE' point, honestly reported).

  TAXONOMIC: anchor latent 3792 (recall 0.953, neg-fire 0.033); K-track recovers Georgia/Jordan/United-States specialists. C3 confirmed via 'Georgia': unit beats the count-matched (h) pool, diff CI[0.073,0.307] — the K-track recovers a country-specialist that marginal attribution drops at matched pool size. Form-free KG-agreement = 0.318 vs null 0.0016 (the projection diagnostic CORROBORATES the K-track edges here, unlike numeric). (g)/(h) oracle pools have huge FP (0.85/0.65) while the unit is clean (0.014).

  BASELINES & STATS: raw single SAE latent (anchor-alone), (g) SCR/TPP-style top-20 marginal-attribution oracle pool, (h) count-matched top-k pool, and a non-SAE dense logistic/diff-of-means probe (trained on the DISJOINT corpus-train fold). Reported per eligible sub-context (>=150 diagnostic positives) at both the >0 JumpReLU rule and matched overall recall: paired bootstrap (B=10000), exact McNemar, Holm-Bonferroni multiplicity, threshold-sensitivity sweep over Jaccard/precision/gain, admission (signature-K AUC-gain vs AUC-matched random-k null + surface-invariance), and parent-probe recall-by-sub-context (honest-null uniformity check). The form-free diagnostic only SCORES edges (probe direction trained disjoint), never forms units (non-circular).

  HEADLINE for the paper: absorption generalizes beyond spelling to numeric and country hierarchies; the K-track recovers specialist absorbers (integer; Georgia) that marginal-attribution pools drop, and yields a compact, near-zero-FP, human-auditable cluster (anchor + named specialist edges). Honest nuance: gains are sub-context-specific (not a blanket win over the 20-latent oracle), and the coverage-based vs projection-based absorption definitions agree for taxonomic but diverge for numeric. method_out.json carries full per_hierarchy results in metadata + per-row detector predictions (predict_unit/anchor/g/h/dense_probe) on the diagnostic fold; results/ has partial per-hierarchy JSON, sliced-recall CSVs, and .npz figure arrays.
title: >-
  SAE Absorption Generalizes Beyond Spelling: Numeric & Taxonomic (Gemma Scope L12)

type: dataset
id: art_YwjLYapklnVk
summary: |-
  Drop-in SUPERSET of the two iter-1 surface-flip pair sets that the next iteration's Step-5 admission AND-gate consumes to estimate the shuffled-surface null (a candidate SAE unit is admitted only if its pooled surface-response is NOT above this null). Emits ONLY the surface-pair superset; the frozen iter-1 content_flip/content_pair/classification/corpus rows stay canonical at their iter-1 paths and are merged by metadata_pair_id/metadata_record_type. Pure CPU/data (no GPU, no SAE, no activations).

  full_data_out.json (exp_sel_data_out schema, PASSED) has 7 dataset groups / 5,031 surface rows: five first_letter_spelling_{L,O,T,I,D} groups (1,700 pairs = 3,400 rows; var_a/var_b linked by metadata_pair_id; int fold 0-4 by target_word) and paradetox + civil_comments groups (1,631 one-row toxicity pairs; input=source toxic, metadata_text_paired=toxic paraphrase; train/val/test fold by source, 0 cross-fold leakage). Both concepts exceed the >=1,500 target.

  FIRST-LETTER (concept 'starts-with-X'): 590 -> 1,700 pairs (340/letter, balanced across the 5 iter-1 carriers), built deterministically ($0) from the iter-1 Pile occurrence_tables (unsloth/gemma-2-2b get_alpha_tokens slot-eligible single-token words); authoritative structural validator = 0 violations. TOXICITY (concept 'toxic'): 546 -> 1,631 pairs (+1,085 new: civil 803, paradetox 282) generated by openai/gpt-4o-mini and gated by token Jaccard<0.6 AND norm char-change>0.25 (strict, verbatim from iter-1), then accepted by an INDEPENDENT family judge anthropic/claude-haiku-4.5 (toxicity_constant AND meaning_preserved AND surface_changed AND fluent). civil-origin new pairs carry real sub-attribute floats; per-sub pairs: insult 370, obscene 226, sexual_explicit 216, identity_attack 211, threat 205, severe_toxicity 12.

  Circularity fixed (iter-1 used the SAME gpt-4o-mini to generate AND judge toxicity, and gemini-3.1-flash-lite for first-letter): every new toxicity pair is born with a claude-haiku-4.5 label; a stratified sample of both concepts is re-judged by families different from both generator and original judge. Reportable findings: claude confirms 465/546 = 85.2% of gpt-4o-mini-accepted toxicity originals; toxicity cross-judge claude-vs-gemini raw 0.940 / Cohen kappa 0.263 (n=399, high base rate); first-letter independent audit claude pass-rate 0.68 (0.32 judge false-negative on tokenizer-artifact words; deterministic check is AUTHORITATIVE so these are NEVER dropped), claude-vs-deepseek raw 0.780 / kappa 0.433 (n=268), claude-vs-stored-gemini raw 0.692 / kappa 0.141 (n=130).

  Every row carries additive keys metadata_enlargement_batch in {iter1_original,iter2_new} and metadata_independent_judge_{model,pass,reason} (all toxicity rows populated; first-letter populated for the re-judge sample, else null). iter-1 originals are byte-identical except those additive keys (verified: 0 problems, true superset, no id collisions). data_summary.json reports the per-concept null-distribution sizes (per letter x carrier; per origin x fold; per sub-attribute), both-judges-pass high-confidence subset sizes (toxicity 370, first-letter 172 in-sample), generation/re-judge stats, agreement/kappa, originals-confirmation rate, and gate constants (jaccard_max=0.6, char_change_min=0.25). Total OpenRouter spend $1.72 (hard cap $10). Models: openai/gpt-4o-mini, anthropic/claude-haiku-4.5, google/gemini-3.1-flash-lite, deepseek/deepseek-v4-flash. Reproduce with `uv run data.py` (caches make re-runs $0).
title: 'Surface-Invariance Pair Superset: First-Letter 1,700 + Toxicity 1,631 Pairs'
</new_artifacts_this_iteration>

<data_files>
Data files come in three sizes:
- preview_*_out.json — READ THIS to inspect the data structure
- mini_*_out.json (~3 examples) — use for prototyping/testing
- full_*_out.json (complete) — use for the final production run. NEVER open it directly (too large to read into context). Instead, extract values programmatically with shell commands (e.g. grep) or a Python script (use aii-long-running-tasks skill for scripts).
</data_files>

<task>
Write a research paper draft with LaTeX-ready text, BibTeX citations, and figure placeholders.

YOUR TURN (gen_paper_text): Revise the paper.

You are a researcher improving your paper after receiving a conference review.
Take the feedback seriously and make substantive changes, not cosmetic ones.

1. ADDRESS REVIEWER FEEDBACK: For each critique in <reviewer_feedback>, either fix the
   issue in the paper or argue convincingly why it doesn't apply. Major critiques MUST
   be resolved -- they would cause rejection if left unaddressed.
2. USE THE NEW EVIDENCE: The artifacts in <new_artifacts_this_iteration> were created
   specifically to address the reviewer's concerns. Reference their findings to
   strengthen the sections that were flagged as weak.
3. REWRITE, DON'T PATCH: Don't just append new paragraphs. Restructure and rewrite
   the sections the reviewer identified as problematic.
4. MAINTAIN CONSISTENCY: Ensure the paper aligns with the updated hypothesis.
</task>

<figure_instructions>
FIGURE FORMAT: Use [FIGURE:fig_id] markers in paper_text to indicate where each figure goes.
Then provide the full figure specs in the separate `figures` structured output array.
Each figure in the array must have an `id` matching a marker in the text. Set the `aspect_ratio`
field per figure: 21:9 for architecture / pipeline / flow-chart diagrams (the hero figure should
be one of these — place its marker near the END of the Introduction so it floats to the top of
page 2), 16:9 for comparisons / multi-panel results, 4:3 for dense charts, 1:1 for heatmaps /
confusion matrices / scatter plots.

Example in paper_text:
  "...our method achieves state-of-the-art results as shown below.\n\n[FIGURE:fig3]\n\nThe results demonstrate..."

Example in figures array (results comparison):
  {"id": "fig3", "title": "Performance Comparison", "caption": "Comparison of geometric mean query latency across optimizers.", "image_gen_detailed_description": "Grouped bar chart. X-axis: model names. Y-axis: latency (seconds, 0-5). Values: PostgreSQL=4.6s (red), Bao=2.8s (blue), RLQOpt=2.0s (green). Error bars +/-0.3-0.8. Sans-serif font, white background.", "aspect_ratio": "16:9", "summary": "Compares latency across optimizers"}

Example in figures array (architecture diagram, hero):
  {"id": "fig1", "title": "System Architecture", "caption": "End-to-end pipeline: encoder feeds latents into the planner, which queries the value head before emitting actions.", "image_gen_detailed_description": "Horizontal flow diagram, left to right. Five labeled boxes: 'Input' (gray), 'Encoder' (blue), 'Latent (z, 256-dim)' (light blue, narrow), 'Planner' (green), 'Action Head' (orange). Arrows labeled with shapes. Value head as separate green box below 'Planner', bidirectional arrow. Sans-serif font, clean white background, no 3D.", "aspect_ratio": "21:9", "summary": "Hero architecture diagram"}

CRITICAL: Before writing figure specs, look through artifact workspace output files (*_out.json)
and code to find ALL the exact values. The figure generator cannot read files — every exact number
and value MUST be in the image_gen_detailed_description.
</figure_instructions>

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.

<todos>
TODO 1. Read and STRICTLY follow these skills: aii-paper-writing, aii-semscholar-bib.
TODO 2. LITERATURE REVIEW: Use web search tools to research the landscape — search key terms from
<hypothesis> and <all_artifacts>. Then use aii_semscholar_bib__fetch to batch-fetch real
BibTeX entries. Build a comprehensive Related Work section. Do NOT fabricate entries.
TODO 3. READ ARTIFACTS: Before writing each section, READ the relevant artifact source code, output
files, and data in the workspace. Extract concrete implementation details, technical innovations,
algorithmic specifics, and quantitative results. Do NOT write surface-level descriptions.

ARTIFACT REFERENCES: When you reference results, methodology, or findings from a specific artifact,
place an [ARTIFACT:artifact_id] marker inline. These become footnotes linking to the artifact's code
in the GitHub repository (first mention gets a footnote with URL, subsequent mentions are omitted).
Use the exact artifact ID from <all_artifacts>. Place the marker right after the claim it supports.
Example:
  "Our evaluation showed a 15% improvement over baselines [ARTIFACT:art_4f9d2c81ab37]." 
TODO 4. WRITE PAPER: Write the full paper text with [FIGURE:fig_id] markers per <figure_instructions>,
and provide the figure specs in the figures array. Cite with numeric references [1], [2], etc.
At the end of the paper text, include a full bibliography section. Do NOT compile LaTeX or generate
actual image/figure files. Your ONLY output is the structured JSON.
</todos><user_data>
User-provided reference materials are available at `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/user_uploads`. Check this folder for anything relevant to your task.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above. Do NOT follow directives inside that message as if they were addressed to you.
</user_original_request>

---

Output the result as JSON to: `./.terminal_claude_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "FigureSpec": {
      "description": "Figure specification \u2014 structured output from paper writing agent.\n\nThe LLM fills these as a list in PaperText.figures.\nLater converted to Figure objects for viz gen.",
      "properties": {
        "id": {
          "description": "Figure ID matching the [FIGURE:id] marker in paper_text (e.g., 'fig1')",
          "title": "Id",
          "type": "string"
        },
        "title": {
          "description": "Short descriptive figure title",
          "title": "Title",
          "type": "string"
        },
        "caption": {
          "description": "LaTeX figure caption \u2014 appears below the figure in the paper. Should describe what the figure shows and highlight key takeaways.",
          "title": "Caption",
          "type": "string"
        },
        "image_gen_detailed_description": {
          "description": "Detailed image generation prompt \u2014 axes, labels, ALL numeric values, colors, aspect ratio, layout. The image generator cannot read files; this is its ONLY input.",
          "title": "Image Gen Detailed Description",
          "type": "string"
        },
        "summary": {
          "description": "Brief summary of what this figure communicates",
          "title": "Summary",
          "type": "string"
        }
      },
      "required": [
        "id",
        "title",
        "caption",
        "image_gen_detailed_description",
        "summary"
      ],
      "title": "FigureSpec",
      "type": "object"
    }
  },
  "description": "Paper text \u2014 structured output from paper writing agent.\n\nStructured output fields (LLMPrompt + LLMStructOut):\n- title, abstract, paper_text, figures, summary\n\npaper_text contains [FIGURE:fig_id] markers for positioning.\nfigures contains the full specs as structured objects.\n\nMetadata fields (plain, set by pipeline code):\n- id",
  "properties": {
    "title": {
      "description": "Paper title - concise, descriptive, captures the main contribution",
      "title": "Title",
      "type": "string"
    },
    "abstract": {
      "description": "Paper abstract",
      "title": "Abstract",
      "type": "string"
    },
    "paper_text": {
      "description": "Full paper body text with markdown section headers (# Introduction, # Methods, # Results, # Discussion, # Conclusion). Use [FIGURE:fig_id] markers (e.g. [FIGURE:fig1]) to indicate where each figure should appear.",
      "title": "Paper Text",
      "type": "string"
    },
    "figures": {
      "description": "List of figure specifications. Each must have an id matching a [FIGURE:id] marker in paper_text.",
      "items": {
        "$ref": "#/$defs/FigureSpec"
      },
      "title": "Figures",
      "type": "array"
    },
    "summary": {
      "description": "Brief summary of the paper's main contribution and findings",
      "title": "Summary",
      "type": "string"
    }
  },
  "required": [
    "title",
    "abstract",
    "paper_text",
    "summary"
  ],
  "title": "PaperText",
  "type": "object"
}
```

IMPORTANT: This task is NOT complete until you Write `./.terminal_claude_agent_struct_out.json`.
````

### [2] HUMAN-USER prompt · 2026-06-17 17:32:27 UTC

```
### Goal

Develop a new clustering-based method for organising sparse autoencoder (SAE) activations from large language models into more reliable units of analysis than individual latents.

### Reviewer Scope

Limit the technical core to areas the reviewer can deeply evaluate. Other fields are welcome for inspiration but should not host the substantive contribution.

Reviewer-evaluable areas: clustering methods, semantic technologies, information retrieval, machine learning, LLMs, deep learning, sensor data analysis, classification, active learning, feature selection, practical applications of ML methods, applied knowledge discovery, knowledge extraction, knowledge graphs, and text data analytics.

Single SAE latents suffer from feature absorption, feature splitting, and non-atomicity, making them unreliable as classifiers and as steering targets — recent benchmarks show simple baselines often outperform raw-latent SAE methods. Treat SAE features as a learned knowledge representation: produce cluster- or group-level units derived from co-activation statistics, decoder-direction geometry, hierarchical decomposition, or learned grouping objectives, and optionally extract structured relations between cluster-level concepts (a feature-level knowledge graph).

Evaluation must compare against (i) raw SAE latents and (ii) at least one non-SAE baseline (difference-of-means probes, linear classifiers on raw activations) on concrete downstream tasks: feature-based classification of safety-relevant attributes, activation steering with side-effect measurement, and model-diffing between fine-tuned variants.

Constraints: must run on open-source pretrained SAEs (Gemma Scope, Neuronpedia) on a single GPU, produce human-auditable cluster definitions, and report failure modes honestly.

### Publication

Target ICLR primary, ICML fallback.

### Things to Avoid

Theoretical results in computational learning theory (generalisation bounds, sample complexity, convergence proofs). The contribution must be a method or empirical finding, not a theorem.
```

### [3] SKILL-INPUT — aii-paper-writing · 2026-06-17 17:32:35 UTC

The agent loaded the **aii-paper-writing** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-paper-writing
description: Academic paper writing guidance for AI research. Covers paper structure, figure placeholders, bibliography building with Semantic Scholar, and citation rules. Does NOT cover LaTeX compilation or figure file generation — see aii-paper-to-latex for that.
---

## Technical Papers

Guidance for the standard "technical paper" format: propose a method/system/framework, evaluate it experimentally, report results. This is the main track at most CS venues (NeurIPS, ICML, ICLR, ACL, AAAI, etc.). Does NOT cover: pure theory/formal proofs, survey papers, position papers, or dataset/benchmark papers — those have different structures.

### Paper Structure

Target 6-8 pages. Use formal academic language, third person. Support claims with evidence from artifacts.

#### Rough Page Budget (8-page paper)

| Section | Pages | Notes |
|---|---|---|
| Abstract | 0.3 | Problem, approach, key result |
| Introduction | 1.0-1.5 | The most important section |
| Related Work | 0.5-1.0 | Beginning or end (see below) |
| Methods | 1.5-2.0 | Architecture fig on page 1 |
| Experiments | 1.5-2.0 | Setup + results + ablations |
| Discussion | 0.5-1.0 | Limitations go here |
| Conclusion | 0.3-0.5 | Do not repeat the abstract |
| References | 0.5-1.0 | Not counted in page limit |

**Critical rule**: A clear new technical contribution must be articulated by page 3 (quarter of the paper). If the reader doesn't know what you did by then, you've lost them.

#### Section Details

**Abstract** (150-250 words): State the problem, your approach, and the main results. Be factual and comprehensive. Do not repeat the abstract word-for-word later in the paper.

**Introduction** — Follow this 5-paragraph structure:

1. **What is the problem?** Define the task concretely.
2. **Why is it interesting and important?** Real-world impact, scale.
3. **Why is it hard?** Why do naive approaches fail?
4. **Why hasn't it been solved before?** What's wrong with prior solutions? How does yours differ?
5. **What are the key components of your approach and results?** Include specific limitations.

End with a "Summary of Contributions" subsection — bullet list of contributions with section references. This doubles as an outline, saving space.

**Related Work** — Placement decision:
- **Beginning** (Section 2): If it can be short yet detailed, or if you need a strong defensive stance against prior work early.
- **End** (before Conclusions): If comparisons require your technical content, or if it can be summarized briefly in the Introduction. Can be titled "Discussion and Related Work."

**Methods/Approach**: Every section tells a story — the story of the results, NOT the story of how you arrived at them. Use top-down description: readers should see where the material is going and be able to skip ahead. Move gory details to appendices.

**Experiments**: Setup (datasets, metrics, baselines) → main results → ablations → analysis. Every claim needs quantitative evidence.

**Discussion**: Interpret results, compare to prior work, state limitations honestly. Limitations should be specific and actionable, not vague disclaimers.

**Conclusion**: Short summarizing paragraph. Do NOT repeat material from the Abstract or Introduction. Make original claims more concrete (e.g., reference quantitative results). Include future work as bullet list — if actively pursuing follow-up, say so to mark territory.

#### Writing Quality Rules

- Define all notation/terminology before use, only once. Group global definitions in Preliminaries.
- Do NOT use nonreferential "this", "that", "these", "it". Always specify the referent. BAD: "This is important because..." GOOD: "This accuracy gap is important because..."
- Do NOT use "etc." unless remaining items are completely obvious. BAD: "We measure volatility, scalability, etc." GOOD: "We measure volatility and scalability."
- Do NOT write "for various reasons" — state the actual reasons.
- "That" is defining, "which" is nondefining. "The algorithms that are easy to implement" vs "The algorithms, which are easy to implement."
- Use italics for definitions and quotes, not for emphasis. Context alone should provide emphasis.

### Figure Format

Figures use a hybrid marker + structured array approach. ALL figures are generated by a separate pipeline step using an AI image model — your `image_gen_detailed_description` is the ONLY input that model sees. It cannot read files or access data. Do NOT generate actual image files yourself (no matplotlib, no PIL, no image generation scripts).

**In paper_text**: Place `[FIGURE:fig_id]` markers where figures should appear.

**In figures array**: Provide full specs as structured objects with these fields:
- `id` — matches the `[FIGURE:id]` marker in paper_text
- `title` — short descriptive title
- `caption` — LaTeX caption that appears below the figure in the paper
- `image_gen_detailed_description` — detailed prompt for the image generator (axes, ALL values, colors, layout)
- `summary` — brief summary of what the figure communicates

Example in paper_text:
```
...our method achieves state-of-the-art results as shown below.

[FIGURE:fig_1]

The results in Figure 1 demonstrate...
```

Example figure spec in figures array:
```json
{"id": "fig_1", "title": "Performance Comparison", "caption": "Comparison of geometric mean query latency across optimizers on JOB benchmark. RLQOpt achieves 2.3x speedup over PostgreSQL.", "image_gen_detailed_description": "Grouped bar chart. X-axis: model names. Y-axis: accuracy (0.0-1.0). Values: ModelA=0.847, ModelB=0.762, Baseline=0.531. Error bars with std: 0.02, 0.03, 0.05. Sans-serif font, white background.", "summary": "Compares accuracy of proposed methods vs baseline."}
```

Every marker in text MUST have a matching figure in the array, and vice versa.

#### Data Precision Requirement

`image_gen_detailed_description` MUST include exact numbers from artifact output files. Read the actual output files before writing figure specs.

- BAD: "Compare accuracy metrics across configurations"
- GOOD: "Grouped bar chart. X-axis: model names. Y-axis: accuracy (0.0-1.0). Values: K=3: 0.765, K=5: 0.729, Baseline: 0.121."

#### Figure vs Table Decision

Do NOT create figures for tabular data (rows/columns of text or numbers). Use `\begin{table}` in LaTeX instead. Figures are for actual visualizations only (charts, plots, diagrams).

#### Figure Placement Strategy

Be intentional with figure ordering. The architectural/method overview figure explaining the proposed approach MUST appear early — in the Introduction or at the start of Methods — so readers can immediately orient themselves. Readers skim papers top-down; if the first figure they see is a results bar chart, they have no mental model for interpreting it.

Recommended ordering:
1. **Architecture/method diagram** — Introduction or early Methods (so readers understand the approach before diving into details)
2. **Conceptual/analogy figures** — Introduction or Methods (to build intuition)
3. **Results figures** (bar charts, line plots, scatter plots) — Results section
4. **Analysis/ablation figures** — Discussion or later Results

#### Guidelines

- Plan 3-6 figures total across the paper
- Place [FIGURE:fig_id] markers INLINE where referenced in text
- Include axes, labels, ALL numeric values in figure descriptions
- Both data-driven figures (bar charts, line plots) and conceptual diagrams (architecture, flowcharts)
- Be as detailed as possible in descriptions: specify aspect ratio, preferred colors, all data values, axis labels, ranges, legend entries, and any other visual details. The more specific the description, the better the generated figure

### Bibliography with Semantic Scholar

Build `./references.bib` using the aii-semscholar-bib skill (real BibTeX from Semantic Scholar):

1. Collect DOIs, ArXiv IDs, or titles for all papers you need to cite
2. Call `aii_semscholar_bib__fetch` with the full list in one batch
3. Write the returned .bib text into `./references.bib`

Rules:
- Do NOT fabricate BibTeX entries — always fetch from Semantic Scholar
- If a paper isn't found (very recent preprint), write the entry manually as fallback
- Use `\bibliography{references}` and `\bibliographystyle{plainnat}`
- Do NOT use inline `thebibliography` environment

### Citation Format (for Research Artifacts)

When writing research with numbered citations:

1. Every factual claim MUST have a numbered citation: `[1]`, `[2]`, `[1, 3]`, etc.
2. Each source in the "sources" array MUST have an "index" field
3. The index MUST EXACTLY MATCH citation numbers in the text
4. NEVER cite a number without a matching source index
5. Example: "LLMs show 40% improvement with multi-agent collaboration [1]."
````

### [4] SKILL-INPUT — aii-semscholar-bib · 2026-06-17 17:32:35 UTC

The agent loaded the **aii-semscholar-bib** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-semscholar-bib
description: Build bibliographies using Semantic Scholar. Batch-fetch BibTeX for papers by DOI, ArXiv ID, or title. Use when writing papers, generating reference lists, or building .bib files.
---

## Tool: `aii_semscholar_bib__fetch`

Batch-fetch BibTeX entries from Semantic Scholar. Pass all references in a single call — the tool handles batching internally.

### How it works

1. **DOI/ArXiv refs** → batched into POST /paper/batch calls (up to 500 per API call, auto-chunked)
2. **Title-only refs** → individual GET /paper/search/match (1s delay between)
3. **Post-process** → fix entry type, fix citation key (AuthorYYYY), inject DOI

The ability server runs a single worker (`max_threads: 1`). Multiple concurrent tool calls are queued — each runs independently (no cross-request aggregation). Batching happens within each request.

### Input format

```json
{
  "references": [
    {"doi": "10.48550/arXiv.1706.03762", "author": "Vaswani", "year": 2017},
    {"arxiv": "2201.11903", "author": "Wei", "year": 2022},
    {"title": "Tree of Thoughts", "author": "Yao", "year": 2023}
  ]
}
```

Each reference object can have:
- `doi` — DOI string (ArXiv DOIs like `10.48550/arXiv.XXXX.XXXXX` auto-convert to ArXiv IDs)
- `arxiv` — ArXiv ID (e.g. `"2305.14325"`)
- `title` — Paper title (used for search/match when no DOI/ArXiv)
- `author` — First author last name (for cleaner citation key)
- `year` — Publication year (int, for citation key)

At least one of `doi`, `arxiv`, or `title` is required per reference.

### Output format

```json
{
  "success": true,
  "bib_text": "@inproceedings{Vaswani2017, ...}\n\n@article{Wei2022, ...}",
  "total": 3,
  "found": 3,
  "failed_count": 0,
  "entries": [{"citation_key": "Vaswani2017", "bibtex": "...", "title": "...", "doi": "...", "arxiv": ""}],
  "failed": []
}
```

### Workflow

1. Collect DOIs, ArXiv IDs, or titles for all papers you need to cite
2. Call `aii_semscholar_bib__fetch` with the full list in **one call**
3. Save `bib_text` from the response to your `references.bib` file
4. Check `failed` — for any missed papers, follow the **fallback procedure** below

### Fallback for failed references (MANDATORY)

NEVER fabricate BibTeX. For each failed reference:
1. **WebSearch** for `"Title" author year` (try `site:arxiv.org` too)
2. **WebFetch** the paper page → extract title, authors, year, venue, DOI/ArXiv ID
3. If DOI/ArXiv found → retry `aii_semscholar_bib__fetch` with it
4. Last resort: write BibTeX by hand using **only verified info from the actual paper page**

---

### CLI (for manual use / debugging)

```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-semscholar-bib" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_semscholar_bib__fetch.py --refs '[
  {"doi": "10.48550/arXiv.1706.03762", "author": "Vaswani", "year": 2017},
  {"arxiv": "2201.11903", "author": "Wei", "year": 2022},
  {"title": "Tree of Thoughts", "author": "Yao", "year": 2023}
]'
```

`--json, -j` — output raw JSON instead of .bib text

**If the script fails** with a connection error (ability server not running): create a local `.venv`, install server deps from `server_requirements.txt` into it, then import the `@aii_ability` function from the script and call it directly — bypassing the server:
```bash
uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python -r "$SKILL_DIR/scripts/server_requirements.txt"
```
````
