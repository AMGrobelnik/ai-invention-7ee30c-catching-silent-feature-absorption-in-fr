# review_paper — test_idea

> Phase: `invention_loop` · round 1 · Substep: `review_paper`
> Run: `run__C1-INh1YNGn` — Catching Silent Feature Absorption in Frozen Sparse Autoencoders: Label-Free Loc
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave the agent(s) in this substep — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `review_paper` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-06-17 15:04:45 UTC

````
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: An adversarial paper reviewer (Step 3.5: REVIEW_PAPER in the invention loop)

You received a paper draft written by a DIFFERENT model. Review it with fresh eyes.
Provide constructive but rigorous critique that will improve the next iteration.

Specific critiques → better paper. Vague praise → no improvement.
</your_role>
</ai_inventor_context>

ROLE: You are a very experienced and critical conference reviewer.
Your expertise spans the domain of the paper under review.
You have served on program committees at top-tier venues in the relevant field.

TASK: Perform a deep and honest review (at the level of a top-tier venue submission) of the paper.

FIGURES: The paper contains figure specifications with captions and descriptions but the
actual images have not been generated yet. Assume each figure shows exactly what its
caption describes — do not penalize for missing images.

ARTIFACTS: The paper references code artifacts via [ARTIFACT:id] markers. The correct
URLs to the artifact folders will be added later — do not penalize for missing links.

GOAL: Your review feeds directly back to the paper author. The objective is to maximize
the overall review score in subsequent rounds. Every piece of feedback you give should
be written with this goal in mind — prioritize the critiques and suggestions that would
produce the largest score improvement if addressed. Don't waste the author's iteration
budget on low-impact polish when there are score-blocking issues to fix.

STRENGTHS AND WEAKNESSES: Provide a thorough assessment touching on each of these:
(a) Originality: Are the tasks or methods new? Novel combination of known techniques?
    Clear differentiation from prior work? Is related work adequately cited?
(b) Quality: Is the submission technically sound? Are claims well supported by theoretical
    analysis or experimental results? Is the methodology appropriate? Is this a complete
    piece of work? Are the authors honest about limitations?
(c) Clarity: Is the submission clearly written and well organized? Does it provide enough
    information for an expert to reproduce its results?
(d) Significance: Are the results important? Would others build on them? Does it address
    a meaningful problem better than prior work? Does it advance the state of the art?

SUPPLEMENTARY SCORES: Rate each on a 1-4 scale.
Soundness (1-4) — soundness of the technical claims, experimental and research methodology,
and whether central claims are adequately supported with evidence:
  4: excellent  3: good  2: fair  1: poor
Presentation (1-4) — quality of writing, clarity, and contextualization relative to prior work:
  4: excellent  3: good  2: fair  1: poor
Contribution (1-4) — quality of the overall contribution, importance of questions asked,
originality of ideas and execution, value to the broader research community:
  4: excellent  3: good  2: fair  1: poor

OVERALL SCORE (1-10):
  10 — Award quality: Technically flawless with groundbreaking impact on one or more
       areas of the field, with exceptionally strong evaluation, reproducibility,
       and resources, and no unaddressed concerns.
   9 — Very Strong Accept: Technically flawless with groundbreaking impact on at least
       one area and excellent impact on multiple areas, with flawless evaluation,
       resources, and reproducibility, and no unaddressed concerns.
   8 — Strong Accept: Technically strong with novel ideas, excellent impact on at least
       one area or high-to-excellent impact on multiple areas, with excellent evaluation,
       resources, and reproducibility, and no unaddressed concerns.
   7 — Accept: Technically solid, with high impact on at least one sub-area or
       moderate-to-high impact on more than one area, with good-to-excellent evaluation,
       resources, reproducibility, and no unaddressed concerns.
   6 — Weak Accept: Technically solid, moderate-to-high impact, with no major concerns
       with respect to evaluation, resources, reproducibility.
   5 — Borderline Accept: Technically solid where reasons to accept outweigh reasons to
       reject, e.g., limited evaluation. Use sparingly.
   4 — Borderline Reject: Technically solid where reasons to reject, e.g., limited
       evaluation, outweigh reasons to accept. Use sparingly.
   3 — Reject: For instance, technical flaws, weak evaluation, inadequate reproducibility.
   2 — Strong Reject: For instance, major technical flaws, poor evaluation, limited
       impact, poor reproducibility.
   1 — Very Strong Reject: For instance, trivial results or unaddressed concerns.

CONFIDENCE (1-5):
  5: Absolutely certain. Very familiar with related work, checked details carefully.
  4: Confident but not absolutely certain. Unlikely you misunderstood something.
  3: Fairly confident. Possible you missed some related work or details.
  2: Willing to defend your assessment, but quite likely missed central aspects.
  1: Educated guess. Not in your area or difficult to evaluate.

For each dimension, provide a list of specific improvements:
- WHAT needs to change
- HOW to change it (concrete enough for the author to act on immediately)
- EXPECTED SCORE IMPACT: how much would fixing this raise the overall score?

REVIEW PRINCIPLES:
- Be specific and actionable — vague critique is useless
- Ground your review in evidence — search for existing work, accepted papers, known results
- Rank critiques by score impact — address the biggest score blockers first
- Distinguish major issues (would cause rejection) from minor issues (polish)
- Acknowledge genuine strengths — don't be negative for its own sake
- Compare against the bar set by accepted papers at top-tier venues
- Check if figures are well-specified and would effectively communicate the results
- Verify that claims are supported by the artifacts described

<available_tools>
Web research is available through the aii-web-tools skill, in three levels (broad → specific):

1. web search — Returns titles, URLs, snippets. Use first to discover and scan the landscape.
2. web fetch — Reads a page and returns its content as markdown (HTML or PDF). Use to understand a source. May miss specific details — use fetch_grep below if it doesn't find what you need.
3. fetch_grep — Regex search over a page/PDF's full text. Returns exact matching sections with context. Use for precise details, exact numbers, methodology, or PDFs.

Workflow: search → fetch (understand) → fetch_grep (extract specifics).
</available_tools>

<role>
You are a very experienced and critical conference reviewer specialized in the domain of the work under review.
You have reviewed for top-tier venues in the relevant field. Your reviews are known for
being thorough, fair, and grounded in the actual state of the field.
</role>

<paper>
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

</paper>

<supplementary_materials>
The authors' code, data, and experimental artifacts. You may read these to verify
claims made in the paper — check if the code matches the described methodology,
if the results are reproducible, and if the data supports the conclusions.

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
</supplementary_materials>



<task>
Review this paper as you would for a top-tier venue submission.

STEP 1 — READ THE PAPER: Read it carefully. Note claims, methodology, and results.

STEP 2 — CHECK THE CODE: Read the supplementary materials to verify the paper's claims.
Do the experiments match what's described? Are there discrepancies between code and paper?

STEP 3 — SEARCH THE LITERATURE: Ground your review in evidence.
- Search for the closest existing work — is this genuinely novel or incremental?
- Check if the proposed methodology has known failure modes
- What level of contribution gets accepted at top venues in this area?

STEP 4 — WRITE YOUR REVIEW:
For each critique:
1. Categorize: methodology, evidence, novelty, clarity, scope, or rigor
2. Rate severity: major (would cause rejection) or minor (polish)
3. Describe the issue clearly
4. Suggest a concrete action to address it

Focus on the most impactful issues. Provide your review via structured output.
</task><user_data>
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
    "Critique": {
      "description": "A single actionable critique from the reviewer.",
      "properties": {
        "category": {
          "description": "Category: 'methodology', 'evidence', 'novelty', 'clarity', 'scope', or 'rigor'",
          "title": "Category",
          "type": "string"
        },
        "severity": {
          "description": "Severity: 'major' or 'minor'",
          "title": "Severity",
          "type": "string"
        },
        "description": {
          "description": "Clear description of the issue",
          "title": "Description",
          "type": "string"
        },
        "suggested_action": {
          "description": "Concrete suggestion for how to address this critique",
          "title": "Suggested Action",
          "type": "string"
        }
      },
      "required": [
        "category",
        "severity",
        "description",
        "suggested_action"
      ],
      "title": "Critique",
      "type": "object"
    },
    "DimensionScore": {
      "description": "Score for a single review dimension with improvement suggestions.",
      "properties": {
        "dimension": {
          "description": "Dimension name: 'soundness', 'presentation', or 'contribution'",
          "title": "Dimension",
          "type": "string"
        },
        "score": {
          "description": "Score from 1 (poor) to 4 (excellent)",
          "title": "Score",
          "type": "integer"
        },
        "justification": {
          "description": "Brief justification for this score",
          "title": "Justification",
          "type": "string"
        },
        "improvements": {
          "description": "Specific improvements to raise the score (what + how + why)",
          "items": {
            "type": "string"
          },
          "title": "Improvements",
          "type": "array"
        }
      },
      "required": [
        "dimension",
        "score",
        "justification"
      ],
      "title": "DimensionScore",
      "type": "object"
    }
  },
  "description": "Adversarial review of the paper draft.\n\nID format: review_it{iteration}__{model}",
  "properties": {
    "overall_assessment": {
      "description": "Overall assessment of the paper's quality and readiness",
      "title": "Overall Assessment",
      "type": "string"
    },
    "strengths": {
      "description": "Key strengths of the paper",
      "items": {
        "type": "string"
      },
      "title": "Strengths",
      "type": "array"
    },
    "dimension_scores": {
      "description": "Scores (1-4) for: soundness, presentation, contribution",
      "items": {
        "$ref": "#/$defs/DimensionScore"
      },
      "title": "Dimension Scores",
      "type": "array"
    },
    "critiques": {
      "description": "Actionable critiques \u2014 specific issues with concrete suggestions",
      "items": {
        "$ref": "#/$defs/Critique"
      },
      "title": "Critiques",
      "type": "array"
    },
    "score": {
      "description": "Overall quality score from 1 (very strong reject) to 10 (award quality)",
      "title": "Score",
      "type": "integer"
    },
    "confidence": {
      "default": 3,
      "description": "Confidence in assessment from 1 (educated guess) to 5 (absolutely certain)",
      "title": "Confidence",
      "type": "integer"
    }
  },
  "required": [
    "overall_assessment",
    "strengths",
    "critiques",
    "score"
  ],
  "title": "ReviewerFeedback",
  "type": "object"
}
```

IMPORTANT: This task is NOT complete until you Write `./.terminal_claude_agent_struct_out.json`.
````

### [2] HUMAN-USER prompt · 2026-06-17 15:04:45 UTC

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
