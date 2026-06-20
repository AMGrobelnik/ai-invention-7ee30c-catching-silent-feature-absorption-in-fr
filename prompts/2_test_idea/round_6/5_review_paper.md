# review_paper — test_idea

> Phase: `invention_loop` · round 6 · `review_paper`
> Run: `run__C1-INh1YNGn` — Catching Silent Feature Absorption in Frozen Sparse Autoencoders: Label-Free Loc
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `review_paper` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-06-18 07:37:25 UTC

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

Sparse autoencoders (SAEs) decompose the activations of large language models (LLMs) into a dictionary of sparsely-activating latents intended to be interpretable, monosemantic units of analysis \citep{Cunningham2023, Bricken2023, Templeton2024}. The appeal is operational: a latent that reliably tracks a human concept can be read off as a classifier, flipped as a steering knob, or compared across model variants. Public SAE suites such as Gemma Scope \citep{Lieberum2024} expose millions of such latents over open models, making this a practical interface for safety-relevant interpretability.

This appeal is undercut by a now well-documented fact: \emph{single SAE latents are not reliable units} \citep{Leask2025}. Two failure modes recur. \emph{Feature splitting} fragments one concept across many latents, so no single latent captures it. \emph{Feature absorption} is more insidious: a more specific child latent suppresses the firing of a more general parent, leaving the parent with unpredictable holes on exactly the sub-contexts the child covers; parent and child become \emph{mutually exclusive in firing} \citep{Chanin2024}. (A related failure, \emph{feature hedging}, merges correlated features into one polysemantic latent in narrow SAEs \citep{Chanin2025}; a hedged latent is not groupable and is out of scope.) On concrete downstream tasks the cost is stark: difference-of-means probes are the strongest concept detectors and raw-latent SAE methods are uncompetitive \citep{Wu2025, Kantamneni2025}, while standardized suites quantify absorption, sparse probing, and targeted erasure \citep{Karvonen2025}. Any method proposing SAE latents as a knowledge representation must clear strong simple baselines and address splitting and absorption head-on.

The task is hard because the obstacles defeat the obvious instruments \emph{by construction}. The intuitive fix for an unreliable single latent is to group several latents into a cluster-level unit. But every existing post-hoc grouping signal is \emph{observational}: which latents fire together (co-activation feature families \citep{ONeill2024, Deng2025}) or which decoder directions point alike. Absorption is precisely the regime where observational signals must fail---the parent and the absorbing child are mutually exclusive in firing, so co-activation can never group them, and their decoders need not be cosine-similar \citep{Chanin2024}. The standard \emph{supervised} remedy, selecting the top-$N$ latents by causal effect on a concept probe (SCR/TPP attribution \citep{Karvonen2024, Marks2024}), is no better: a latent that fires only in a narrow sub-context has low \emph{marginal} attribution and is silently dropped, even though it carries the concept there. The latents one most needs are exactly the ones these instruments discard.

Why has this not been solved post-hoc? Recent architectural remedies---Matryoshka SAEs \citep{Bussmann2025}, hierarchical SAEs \citep{Muchane2025}, and subspace-aware SAEs \citep{Dalili2026}---all \emph{retrain} the SAE to reduce splitting and absorption at training time, and do not help a practitioner holding a frozen public SAE. We take the opposite stance: a \emph{training-free, post-hoc} method over frozen public SAEs. The methodological gap we fill is the \emph{grouping operator}. Grouping by \emph{interventional co-response}---how latents jointly track a content counterfactual, rather than how they co-fire at baseline---is the matched instrument, with a direct precedent in systems biology, where differential co-expression methods (DiffCoEx \citep{Tesson2010}, WGCNA \citep{Zhang2005}) cluster genes by correlated response to a perturbation precisely because co-regulated genes are often not co-expressed at baseline. Crucially, correlation is the right operator only for the \emph{shared-support} splitting case. Absorbers respond on \emph{disjoint} supports and have low pairwise correlation, so no affinity-merging clustering can even \emph{propose} the right group. The disjoint-support case is a \emph{maximum-coverage} problem, whose classic greedy solution \citep{Nemhauser1978, Feige1998} is the natural---and, we argue, the only correct---proposer for absorption units.

We introduce \textbf{Two-Track Co-Response Grouping (CCRG)} and execute it on a frozen Gemma Scope SAE. We deliberately do not stake the contribution on out-classifying a strong dense probe, because on aggregate detection no raw-latent SAE method does \citep{Wu2025}; our own results confirm this on every task we measure. Instead, the contribution is what the method \emph{discovers and can do}: a training-free, label-free discovery procedure that surfaces the single precise absorber latent a marginal-attribution ranking drops, a feature-level knowledge graph (KG) whose edges carry \emph{measured} localized repair utility, and---the headline---an edit through one discovered absorber that produces a \emph{better downstream outcome than a sub-context-targeted dense baseline}.

[FIGURE:fig1]

\paragraph{The headline: a discovered single absorber beats a \emph{sub-context-targeted} dense direction.}
A prior version of this work compared the KG edit only against a \emph{whole-parent} erasure (erase the ``is-a-country'' or ``starts-with-L'' direction), which by construction over-shoots a single sub-context---a near-tautological comparator, as a reviewer rightly observed. We close that gap decisively. The decisive comparator is now a \emph{sub-context-targeted} dense direction $u_{\text{sub}} = \text{diff-of-means}(\text{target sub-context}, \text{sibling sub-contexts in the same parent context})$, built from the very per-sub-context labels the evaluation already uses, erased via the identical operator $h \leftarrow h - \beta (h\cdot u_{\text{sub}})\,u_{\text{sub}}$ and swept to matched forget-quality. $u_{\text{sub}}$ \emph{is} a single dense hyperplane and \emph{does} localize to the sub-context (its sub-probe AUC is $\approx 1.0$); we therefore retire the false claim that ``a single dense hyperplane structurally cannot localize.'' At \emph{matched} forget, ablating the single KG-named absorber, gated by its own sparse firing ($h \leftarrow h - \lambda\, z_l\, W_{\text{dec}}[l]$), still beats $u_{\text{sub}}$ on a joint (retain-utility $\times$ fluency) outcome from an AxBench-style LLM judge: forgetting that ``Georgia'' is a country ($\Delta_{\text{joint}} = +0.561$, CI $[0.318,0.811]$) and forgetting the spelling sub-context of \texttt{large} under ``starts-with-L'' ($\Delta_{\text{joint}} = +1.000$, CI $[0.796,1.213]$), each with a second different-family judge CI also excluding $0$ and curve-dominance on the full achievable forget range [ARTIFACT:art_3WXWsaSoGMnK]. The edge is not that the dense direction cannot localize---it can---but that the absorber fires \emph{sparsely}, so its gated edit touches almost no retain/unrelated tokens (token footprint $0.01$--$0.03$), whereas the continuous $u_{\text{sub}}$ projection perturbs the residual at every token. This is, to our knowledge, the first demonstration that a \emph{discovered single SAE feature} beats a \emph{sub-context-labeled} dense direction on a parent-preserving sub-context-removal task.

\paragraph{The significance ceiling, reported honestly: safety-relevant absorption is homograph-confined.}
The goal asks for reliability gains on safety-relevant attributes. We searched for one. Screening four identity hierarchies (religion, race/ethnicity, orientation/gender, nationality) built from the full \texttt{civil\_comments} corpus ($1.76$M rows), of $44$ eligible safety identity groups \emph{exactly two} exhibit the absorption signature (a parent recall hole $>0.5$ with a firing-disjoint specialist): \texttt{white} and \texttt{straight}---and both are \emph{lexical homographs}. The other $42$ descriptive identity terms (Muslim, Hindu, gay, lesbian, Mexican, Chinese, $\dots$) show \emph{no} parent recall hole; the general identity parent fires reliably on them [ARTIFACT:art_yAQgbq5Wgymx]. Absorption tracks \emph{lexical polysemy}, not safety semantics. Worse, structure does not imply leverage: the two structured safety groups do not yield a robust unlearning win (\texttt{straight} wins under the primary judge only; \texttt{white}'s absorber has \emph{no on-target effect}). We therefore report \textbf{SAFETY\_ABSORPTION\_FOUND\_NO\_WIN}: the downstream win lands on non-safety homograph/spelling sub-contexts (Georgia, \texttt{large}), and the honest, capping finding is that the absorption phenomenon CCRG repairs is confined to homograph/polysemy tokens, not to the demographic attributes a safety practitioner most wants to control.

\paragraph{Three further findings.}
(i) The auditability spine is real and multiplicity-controlled: $30$ KG repairs over $22$ distinct recall holes survive Benjamini--Hochberg FDR across spelling, taxonomic, and numeric families, beating a random single-latent-addition control, and the single-absorber surgical edit reaches a median $1262\times$ (mean $1452\times$) selectivity over collateral on the $n{=}6$ absorption cases at $16$k width [ARTIFACT:art_sxwT7hK6YFEA] [ARTIFACT:art_0CZwPjG2YMCf] [ARTIFACT:art_w7p8du2N1f0Y]. (ii) The auditability spine replicates on a $4\times$-wider ($65$k) SAE---with \emph{more} absorption, as the literature predicts \citep{Karvonen2025, Chanin2025}---and partially across a layer, where the absorbed token shifts; we also correct a prior divide-by-$\epsilon$ selectivity artifact ($16$k and $65$k are \emph{comparably} surgical, not $2000\times$ apart) [ARTIFACT:art_4L1MZxvWYlGd]. (iii) The one-forward-pass recall-hole \emph{router} is derivation-perfect (balanced accuracy $1.0$) but, on a deliberately enlarged prospective set ($34$ homograph entities, $5.6\times$ the prior set), its discriminative absorption stratum does \emph{not} validate (Wilson CIs include $0.5$); we honestly \emph{demote} it to an exploratory diagnostic and report a systematic breadth count---of $64$ homograph entities only three (the months March, June, February) are absorption-structured, with zero of $22$ cities, $20$ given-names, and $10$ brands [ARTIFACT:art_F_-HUhl0NR_i].

\paragraph{Summary of contributions.}
\begin{itemize}
\item \textbf{A stronger downstream win} (\S\ref{sec:unlearn}): ablating one \emph{discovered} absorber beats a \emph{sub-context-targeted} dense direction $u_{\text{sub}}$ (not merely whole-parent erasure) on a joint collateral+fluency outcome at matched forget, with CIs excluding $0$ under two judges and curve-dominance on $2/2$ clean absorption cases; the edge is sparse-firing gating, and we retire the false ``cannot localize'' framing.
\item \textbf{An honest safety scoping result} (\S\ref{sec:safety}): a screen of $44$ safety identity groups shows absorption is \emph{homograph-confined} (two homograph groups, no robust safety win); the positive-control non-safety win (Georgia) is confirmed against $u_{\text{sub}}$ under both judges. This caps the contribution and is our headline limitation.
\item \textbf{A two-track grouping algorithm reframed as a discovery procedure} (\S\ref{sec:method}): correlation communities (C-track) for splitting and a precision-gated anchored greedy set-cover (K-track) for absorption that pairwise affinity provably cannot propose; its demonstrated value is \emph{proposing} the single precise absorber, with multi-member grouping a secondary product (\S\ref{sec:unlearn}, M7).
\item \textbf{Measured auditability and cross-dictionary replication} (\S\ref{sec:audit}, \S\ref{sec:crossdict}): an FDR-controlled KG repair loop, a corrected surgical-selectivity account, LLM-auditable members, and a full-spine replication on a wider SAE.
\item \textbf{An honestly-demoted router and four/six frozen testbeds} (\S\ref{sec:router}, \S\ref{sec:negatives}): an enlarged prospective router test that does not validate, a systematic homograph breadth count, and a dedicated account of failure modes.
\end{itemize}

# Related Work
\label{sec:related}

\paragraph{SAEs and the unreliability of single latents.} Sparse dictionary learning on LLM activations yields interpretable features \citep{Cunningham2023, Bricken2023, Templeton2024, Lieberum2024}, but a growing body of work shows individual latents are not canonical units \citep{Leask2025}. \citet{Chanin2024} introduce and quantify \emph{feature absorption}---a specific child latent suppresses a general parent's firing---demonstrated on first-letter spelling, and \citet{Chanin2025} characterize \emph{hedging} and give the two-sided width law (absorption worsens as the SAE widens, hedging as it narrows). Benchmarks make the practical cost concrete: AxBench finds difference-of-means strongest and raw-latent SAE methods uncompetitive \citep{Wu2025}; a sparse-probing case study reaches the same conclusion \citep{Kantamneni2025}; and SAEBench standardizes absorption, sparse-probing, and erasure evaluations and reports that ``absorption scores worsen with increased dictionary size'' and that unlearning effectiveness varies by layer \citep{Karvonen2025}. We adopt this as our honest bar and as the \emph{signed prediction} for our cross-dictionary test (\S\ref{sec:crossdict}).

\paragraph{SAE unlearning, concept removal, and the dense comparator.} Our headline edit lives in the unlearning/concept-removal literature, so we position it carefully and narrowly. The canonical SAE-unlearning study finds that intervening with multiple SAE features unlearns topics ``with similar or larger unwanted side-effects'' than the fine-tuning baseline RMU \citep{Farrell2024}; AxBench reaches the analogous conclusion for steering \citep{Wu2025}. Recent work contests this for \emph{whole concepts}: CRISP reports utility-preserving SAE-unlearning \citep{Ashuach2025}, and SAEs are useful for editing diffusion models \citep{Cywinski2025}. We make \emph{no} general claim that SAE interventions beat dense baselines. Crucially, the decisive dense comparator is \emph{not} a whole-concept eraser. A sub-context-targeted difference-of-means direction $u_{\text{sub}}$ is itself a single dense hyperplane that \emph{localizes} to the sub-context, and a labeled dense direction can be removed while preserving task-relevant covariance \citep{Holstege2025} and overall utility \citep{KarvonenMarks2025}; label-free erasure can even match label-based debiasing \citep{Shao2026}. We therefore retire the earlier (false) claim that a dense hyperplane ``structurally cannot localize'' and compare against $u_{\text{sub}}$ directly; the defensible contribution is that the absorber is \emph{discovered} label-free---directly answering the ``use SAEs to \emph{discover}, not to \emph{act} on, known concepts'' position \citep{Peng2025}---and that its sparse-firing gating beats $u_{\text{sub}}$ at matched forget. The whole-concept dense direction (LEACE-style erasure \citep{Belrose2023}) is retained only as a clearly-labeled secondary reference; SAE-TS \citep{Chalnev2024} and SRS \citep{He2025} select a whole \emph{concept} feature, not a sub-context absorber. We map the outcome onto the established forget-quality / retain-utility / fluency triad \citep{Li2024, Shi2024}.

\paragraph{Safety/identity debiasing and editing.} SAE-based debiasing edits or suppresses \emph{whole} bias-correlated features, often in vision-language models \citep{Sasse2024}; the closest near-miss steers a single race-correlated SAE latent in clinical LLMs but that latent \emph{co-fires} (on ``African American'' and ``incarceration''), i.e.\ it is entangled, not an absorber with a clean parent recall hole, and the authors concede SAE steering is ``of marginal utility for realistic tasks'' \citep{Ahsan2025}. Model-editing for stereotype \citep{Xu2025} and neural-collapse fairness fine-tuning \citep{Xu2024} edit a whole stereotype association; affine concept-erasure edits a whole protected-attribute direction while preserving utility \citep{KarvonenMarks2025, Holstege2025}. None discovers an SAE absorber for a \emph{single} identity sub-context, preserves the parent and sibling sub-contexts on the same hierarchy, and scores against $u_{\text{sub}}$. Our safety finding is, accordingly, a \emph{measured scoping null}: identity attributes are predominantly co-firing/entangled (consistent with \citet{Ahsan2025}), and absorption-structured identity tokens are confined to homographs (\S\ref{sec:safety}).

\paragraph{Post-hoc grouping and supervised selection.} Prior grouping is observational: co-activation ``feature families'' \citep{ONeill2024} and sparse feature coactivation modules \citep{Deng2025}, and the closest feature-level KG \citep{Winnicki2026} builds edges from corpus co-occurrence, transcoder pathways, and decoder geometry---none interventional. By construction, such edges cannot express CCRG's central relation: a country anchor joined to a Georgia specialist that is \emph{mutually exclusive in firing} with it (firing-Jaccard $<0.05$). SHIFT and the SCR/TPP family rank individual latents by causal effect and ablate the top-$N$ \citep{Marks2024, Karvonen2024}; a latent firing only in a narrow sub-context has low marginal attribution and is silently dropped---the exact gap our co-response set-cover fills. PS-Eval \citep{Minegishi2025} asks whether SAE features separate word senses; it never studies a suppressed parent or a recall hole, a clean cite-and-distinguish.

\paragraph{Architectural remedies and cross-field instruments.} Matryoshka \citep{Bussmann2025}, hierarchical \citep{Muchane2025}, and subspace-aware \citep{Dalili2026} SAEs modify \emph{training} to reduce splitting/absorption; their dictionary-size dependence is exactly why our cross-dictionary replication matters. The C-track imports differential co-expression module discovery \citep{Tesson2010, Zhang2005} and Leiden community detection \citep{Traag2018}; the K-track imports the maximum-coverage greedy with its $(1-1/e)$ guarantee \citep{Nemhauser1978, Feige1998}. The robustness framing engages label-free worst-group robustness---group-DRO \citep{Sagawa2019}, JTT \citep{Liu2021}, GEORGE \citep{Sohoni2020}, EIIL \citep{Creager2020}, LfF \citep{Nam2020}, group-aware priors \citep{Rudner2024}, diverse prototypical ensembles \citep{To2025}---which infer groups over \emph{examples} and \emph{retrain}; CCRG groups \emph{features}, never retrains, and the recovered absorbers \emph{are} the inferred sub-context specialists. Surface invariance draws on LEACE \citep{Belrose2023} and counterfactual invariance \citep{Veitch2021}; label-free SAE steering on the principle that latents need no concept supervision \citep{Chatzoudis2025}; minimal-pair supervision draws on counterfactually-augmented data \citep{Kaushik2019}, CEBaB \citep{Abraham2022}, and ParaDetox \citep{Logacheva2022}. The closest ``cluster counterfactual differences'' template is CDLC in vision \citep{Varshney2025}, which clusters one continuous direction per class; we cluster \emph{discrete} SAE latents and add a set-cover track for which CDLC has no analogue.

# Two-Track Co-Response Grouping: A Label-Free Discovery Procedure
\label{sec:method}

We frame CCRG primarily as a \emph{discovery procedure}: its demonstrated job is to surface the single precise absorber latent that marginal attribution drops, from which the KG, the repair, and the surgical edit follow. Multi-member units are a secondary product, real where the data support them (first-letter pools; the rebuilt Georgia unit) but not the source of the downstream wins (\S\ref{sec:unlearn}).

[FIGURE:fig2]

\paragraph{Preliminaries.} Let the frozen SAE have latents $l \in \{1,\dots,L\}$ with encoder activation $a_l(x)$; a latent \emph{fires} on $x$ iff $a_l(x) > 0$ (Gemma Scope uses a JumpReLU, so the threshold is inside the encoder \citep{Lieberum2024}). For a concept $c$ we are given \emph{content-flip minimal pairs} $(x_{\text{off}}, x_{\text{on}})$ in which the concept is absent/present at matched surface form, plus \emph{surface-flip pairs} in which the concept is held constant and surface varies. Content labels are the supervision every matched baseline consumes; the method uses no absorption-specific oracle. The primary run encodes at one residual-stream site (\texttt{gemma-2-2b}, layer 12, width 16k canonical; $d_{\text{model}}=2304$, $16{,}384$ latents); \S\ref{sec:crossdict} re-runs at width $65$k and at layer $9$.

\paragraph{Step 1: interventional content-response and cover sets.} For each latent $l$ and pair $p$, the \emph{content-response} is $r_l(p) = a_l(x_{\text{on}}) - a_l(x_{\text{off}})$. A latent's \emph{cover set} $C_l$ is the set of pairs whose content flip it tracks reliably ($r_l(p)>\tau_{\text{resp}}$ and $a_l(x_{\text{on}})>0$) and precisely (firing-precision $\geq 0.7$ on its own support). Because absorbers fire on only a handful of words, a mean-over-pairs prefilter would discard them; eligibility is therefore \emph{cover-based}, retaining the genuinely sparse absorbers.

\paragraph{Step 2: C-track --- correlation communities for splitting.} Where a concept \emph{splits}, sub-latents share firing support and co-respond positively, so pairwise affinity is appropriate. We build a sign-aware soft-thresholded affinity from the positive part of the Spearman correlation between response profiles, $A^{C}_{l,l'} = \max(\rho(r_l, r_{l'}), 0)^{\beta}$ with $\beta=6$ (WGCNA's scale-free criterion \citep{Zhang2005}), and run Leiden community detection (RBConfiguration partition \citep{Traag2018}), with resolution fixed by bootstrap-ARI stability against a shuffle null.

\paragraph{Step 3: K-track --- precision-gated anchored set-cover for absorption (the discovery step).} Absorbers respond on \emph{disjoint} supports and are mutually exclusive in firing with their parent, so their pairwise correlation is low and no affinity-merging clustering can propose them. We use an anchored greedy maximum-coverage procedure. \textbf{(1) Anchor:} $l^{*} = \arg\max_l |C_l|$, the highest-recall ``parent'' candidate, chosen using \emph{only} the pairs and \emph{not} the absorption diagnostic. An \emph{unsupervised parent-validation} step requires the anchor to fire on the held-out corpus above a floor ($5\%$); this rejects a spurious high-cover-set latent that fires $0\%$ on the corpus. \textbf{(2) Holes:} $H = P \setminus C_{\text{anchor}}$, the pairs the parent goes silent on. \textbf{(3) Greedy cover:} while $H$ is non-empty and improving, add $\arg\max_l |C_l \cap H|$ subject to mutual exclusivity (firing-Jaccard $<0.1$ with members), per-member precision $\geq 0.7$ on a held-out fold, and a marginal-coverage-gain floor $\geq 0.05$ whose bootstrap CI excludes $0$. A pure max-coverage objective would prefer a high-coverage low-precision latent over a high-precision specialist; we therefore add a \emph{per-sub-context precision gate} (a precision-weighted coverage objective), so the selected absorber is the precise specialist rather than the broad latent. The greedy max-coverage choice is the classic instrument for ``cover a universe with complementary specialists'' \citep{Nemhauser1978, Feige1998}; coverage-complementarity is a set-level property a pairwise operator cannot express.

\paragraph{Step 4: reconciliation.} For each C-community we designate its highest-recall member as a candidate anchor and run Step 3 to pull in mutually-exclusive absorbers covering its holes; we also seed Step 3 from standalone high-recall latents in no dense community. A final unit is a pure C-community (splitting), a pure K-cover (absorption), or a hybrid; we de-duplicate by highest coverage gain.

\paragraph{Step 5: admission filter with multiplicity control.} A proposed unit is admitted iff it clears \textbf{signature C} (within-unit content-response correlation above the 95th-percentile shuffle null) \textbf{or signature K} (pooled-max minus best-single content-response AUC above the 95th percentile of a best-of-random-$k$ null \emph{matched on marginal AUC}, plus the $k\in\{2,3\}$ absolute gain floor of $0.05$ with bootstrap CI excluding $0$, plus mutual exclusivity and the precision floor), \textbf{and} unit-level surface invariance. Because many candidate units are tested per concept, we control multiplicity at the \emph{unit-proposal} level (Bonferroni-within-unit over the disjunctive signature, then Benjamini--Hochberg across the $M$ candidate units), reporting $M$ and the empirical family-wise false-admit rate under the matched random-$k$ null.

\paragraph{Non-circular diagnostic and auditable graph.} Specialization edges are \emph{scored}, never formed, by the absorption diagnostic of \citet{Chanin2024}. Because the strict form needs an output logit, we use the domain-agnostic \emph{form-free} variant (the probe-projection implemented in SAEBench as \texttt{absorption\_fraction}): $l$ absorbs iff $\tau_c < (\hat{a}_l \cdot d_p)/(a \cdot d_p)$, with $d_p$ a parent-concept probe trained on data \emph{disjoint} from clustering. The anchor is chosen by recall available to every baseline, so a label-free unit beating a supervised oracle is not undercut. Each admitted unit is emitted with logit-lens tokens and top conditioning contexts, plus directed anchor$\to$child specialization edges---a feature-level knowledge graph.

\paragraph{Editable graph operators and the decisive dense comparator.} Two operators act through a named anchor$\to$absorber edge. \emph{Repair} adds the absorber to the suppressed parent ($\max$-pool) to recover the parent's recall hole. \emph{Surgical edit / unlearning} ablates the single absorber, $h \leftarrow h - \lambda\, z_l\, W_{\text{dec}}[l]$, gated by the latent's own sparse firing $z_l$. The decisive dense comparator is the \emph{sub-context-targeted} direction $u_{\text{sub}} = \text{diff-of-means}(\text{target-sub-context-positive}, \text{sibling-positive in the same parent context})$, fit on a fold disjoint from evaluation and erased via $h \leftarrow h - \beta (h\cdot u_{\text{sub}})\,u_{\text{sub}}$. We retain whole-parent erasure $h \leftarrow h - \beta (h\cdot u)\,u$ only as a secondary ``naive over-shoot'' reference. For the downstream task (\S\ref{sec:unlearn}) we sweep $\lambda$ and $\beta$ to \emph{match} forget-quality across operators, then generate under each edit hook and score.

\paragraph{The a-priori router (an exploratory diagnostic).} Before any grouping, one forward pass yields two label-free signals per concept: the parent's per-sub-context recall holes and the positive-only firing-Jaccard between each per-sub-context detector and the parent. The screening rule predicts the \emph{absorption regime} (grouping helps) iff the parent has a recall hole (corroborated by low firing-Jaccard) and the \emph{co-firing regime} otherwise. We report this as an exploratory diagnostic, because it does not validate out-of-sample (\S\ref{sec:router}).

# Testbeds, Baselines, and Protocol
\label{sec:setup}

\paragraph{Constructed testbeds.} We built six frozen, schema-standardized families (Table~\ref{tab:testbeds}). All are pure text/data artifacts, so absorption presence is an empirical question for the SAE run, not a construction artifact. Words for the spelling and non-spelling hierarchies are anchored in the real \texttt{gemma-2-2b} vocabulary and a pinned Pile revision. The first-letter testbed contributes $17{,}180$ examples over five letters [ARTIFACT:art_dpYpjSn2Xvg3]; the non-spelling testbed contributes $24{,}128$ examples over numeric and is-a-country hierarchies [ARTIFACT:art_t2uUbjSwpd3t]; the toxicity family contributes $37{,}707$ examples \citep{Logacheva2022, Borkan2019} [ARTIFACT:art_8QO7pl6Pd8UQ]; a supporting family contributes $30{,}739$ examples of CAD-IMDB sentiment \citep{Kaushik2019}, CEBaB aspect-sentiment \citep{Abraham2022}, and a bias\_in\_bios boundary-null \citep{DeArteaga2019} [ARTIFACT:art_21JWypIydPMX]; a homograph-entity testbed (cities, months, given-names, brands) supplies prospective router candidates [ARTIFACT:art_2xQn686KUmV5]; and a new safety-identity testbed (nationality, religion, ethnicity, named-entity; $36{,}448$ examples) hosts the safety screen [ARTIFACT:art_KNPsfjByyxiS].

\begin{table}[t]
\centering
\small
\caption{Constructed testbeds. Counts are released examples. LB = load-bearing, NS = non-spelling spine, SP = supporting, RT = router prospective, SF = safety screen.}
\label{tab:testbeds}
\begin{tabular}{lllrl}
\toprule
Family & Source & Concepts & Examples & Role \\
\midrule
First-letter spelling & Pile + gemma vocab & 5 letters (L/O/T/I/D) & 17{,}180 & LB \\
Non-spelling absorption & Pile + templates + LLM & numeric, countries & 24{,}128 & NS \\
Toxicity & ParaDetox, civil\_comments & toxicity + 6 sub-attrs & 37{,}707 & LB \\
Sentiment / aspect / bias & CAD-IMDB, CEBaB, bias\_in\_bios & sentiment, food/service, 28 professions & 30{,}739 & SP \\
Homograph entities & Pile + gazetteers & 23 cities, 12 months, 34 names, 24 brands & --- & RT \\
Safety identity & civil\_comments + Pile & nationality, religion, ethnicity, entity & 36{,}448 & SF \\
\bottomrule
\end{tabular}
\end{table}

\paragraph{Baselines.} We compare CCRG units against fifteen baselines spanning raw latents, observational clusters (count-matched), dense probes, supervised oracle pools, label-free/oracle group-robustness probes, a random-eligible-$k$ pool, and three non-random label-free selectors (S-rec, S-prec, S-mag) that isolate the set-cover-specific selection rule (Table~\ref{tab:baselines}). For the downstream edit (\S\ref{sec:unlearn}), the \emph{decisive} comparator is the sub-context-targeted dense direction $u_{\text{sub}}$ (baseline f$'$); whole-parent erasure (f) is demoted to a secondary reference.

\begin{table}[t]
\centering
\small
\caption{Baseline glossary. (b)/(c) count-matched to the unit's member count $k$; (h) count-and-pool-matched; (RE-$k$) random-eligible floor; (S-$\cdot$) non-random label-free selectors. \textbf{(f$'$) is the decisive dense comparator for the edit.}}
\label{tab:baselines}
\begin{tabular}{cl}
\toprule
ID & Baseline \\
\midrule
(a) & Best raw single latent (held-out AUC/F1) \\
(b)/(c) & Observational co-activation / decoder-geometry clusters, count-matched to $k$ \\
(d)/(e) & Counterfactual difference-of-means / linear probe on raw residual \\
(f) & Whole-parent diff-of-means / LEACE erasure (\emph{secondary} edit reference) \\
\textbf{(f$'$)} & \textbf{Sub-context-targeted dense direction $u_{\text{sub}}$ (decisive edit comparator)} \\
(g)/(h) & Supervised SCR/TPP oracle pool / count-and-pool-matched probe \\
(i) & Unmatched difference-of-means / probe on raw labels \\
(j)/(k) & Oracle group-DRO probe / label-free group-inference probe (JTT/GEORGE) \\
(RE-$k$) & Random-eligible-$k$ pool, max-pooled \\
(S-rec)/(S-prec)/(S-mag) & Top-$k$ by content-flip recall / firing precision / response magnitude \\
\bottomrule
\end{tabular}
\end{table}

\paragraph{Statistics.} The primary object is the per-concept paired bootstrap of the AUC or outcome difference ($B=10{,}000$, resampling whole content-flip pairs or held-out prompts as clusters on the held-out fold), with exact McNemar confirmatory tests and Holm--Bonferroni across headline claims; any accuracy comparison uses a comparison-matched Youden threshold. Encoding, gating, and software pins are in Appendix~\ref{sec:repro}.

# A Discovered Absorber Beats a Sub-Context-Targeted Dense Direction
\label{sec:unlearn}

The reliability gain CCRG delivers is localization through a \emph{sparsely-firing} handle. The decisive question, sharpened from the prior draft, is whether ablating one discovered absorber beats a dense baseline that \emph{also localizes to the sub-context}---not merely a whole-concept eraser that over-shoots by construction.

\paragraph{The task and the corrected comparator.} The goal is to make the model forget \emph{one} sub-context---``Georgia is a country,'' or the spelling of \texttt{large} under starts-with-L---while preserving the parent concept (other countries; other L-words) and fluency on unrelated text. The decisive dense comparator is $u_{\text{sub}} = \text{diff-of-means}(\text{target-sub-context-positive}, \text{sibling-positive})$ inside the same parent context, fit on a disjoint fold from the per-sub-context labels the testbed already carries. We verified $u_{\text{sub}}$ is a competent localizer: its sub-context probe AUC is $\approx 1.0$, and over the achievable dense forget range it has strictly lower collateral than whole-parent erasure on both clean cases [ARTIFACT:art_3WXWsaSoGMnK]. We therefore \emph{delete} the earlier structural claim that a dense hyperplane cannot localize; the open question is whether the discovered sparse handle still wins.

\paragraph{Protocol: matched forget-quality, two judges.} We compare KG-ABL (ablate the KG-named absorber, gated by its own firing) against DENSE-SUB-ABL (erase $u_{\text{sub}}$; baseline f$'$), with DENSE-WHOLE-ABL (erase the whole-parent direction; baseline f, secondary), RAND, and NOOP as references. We sweep $\lambda,\beta$, define $\mathrm{forget}(\text{op})$ as mean next-token KL on held-out FORGET windows at the target token, set the matched target to $0.8 \cdot \min(\max_\lambda\mathrm{forget}_{\text{KG}}, \max_\beta\mathrm{forget}_{\text{SUB}})$, and pick the scales reaching it. At matched forget we generate a $40$-token greedy continuation under each edit hook on held-out RETAIN (sibling + parent-positive) and UNRELATED prompts and score it with an AxBench-style judge (\texttt{claude-haiku-4.5}, temp $0$): $\text{utility}=\text{harmonic\_mean}(\text{fluency},\text{content\_pres})\in[0,2]$. The headline statistic is $\Delta_{\text{joint}}=\text{paired\_bootstrap\_diff}(\text{util}_{\text{KG}},\text{util}_{\text{SUB}},B{=}10{,}000)$. We additionally require a \emph{second different-family judge} (\texttt{gpt-4o-mini}) CI to exclude $0$, report curve-level dominance and model-internal corroboration (retain next-token KL, continuation PPL), and run a deterministic \$0 human-proxy check that KG-ABL preserves sibling tokens that whole-parent erasure corrupts. Total judge spend was \$0.53 over $1459$ calls with zero failures [ARTIFACT:art_3WXWsaSoGMnK].

\paragraph{Result: KG-ABL beats $u_{\text{sub}}$ on the two clean absorption cases.}
Table~\ref{tab:unlearn} reports the four cases. On both \emph{clean absorption} cases the KG edit wins the joint outcome with both judges' CIs excluding $0$ and curve-dominance $1.0$. For Georgia, KG-ABL holds retained utility $1.73/2$ vs.\ $u_{\text{sub}}$'s $1.17/2$ ($\Delta_{\text{joint}}+0.561$, CI $[0.318,0.811]$; second judge $+0.465$, CI $[0.289,0.658]$), with retain next-token KL $3.4\times10^{-5}$ (KG) vs.\ $0.078$ ($u_{\text{sub}}$) vs.\ $0.102$ (whole). For \texttt{large} the gap is starker: $u_{\text{sub}}$ at matched forget drops utility to $0.87/2$ while KG-ABL holds $1.87/2$ ($\Delta_{\text{joint}}+1.000$, CI $[0.796,1.213]$; second judge $+0.574$); whole-parent erasure collapses to $0.0/2$. The human-proxy confirms KG preserves $8/8$ sibling continuations while whole-parent erasure corrupts $6/8$ (Georgia) and $8/8$ (\texttt{large}). We report one honest caveat: for \texttt{large} the noisier \$0 model-internal joint is inconclusive (CI includes $0$) even though both LLM judges agree, so the verdict rests on the pre-registered judged outcome.

[FIGURE:fig3]

\begin{table}[t]
\centering
\small
\caption{Selective sub-concept unlearning at matched forget-quality: KG-named single-absorber ablation (KG-ABL) vs.\ the \emph{sub-context-targeted} dense direction $u_{\text{sub}}$ (DENSE-SUB-ABL, f$'$) and whole-parent erasure (f, secondary). $\Delta_{\text{joint}} = \text{util}_{\text{KG}}-\text{util}_{\text{SUB}}$ (paired bootstrap $B{=}10{,}000$); util $=$ harmonic mean of judged fluency and content-preservation $\in[0,2]$. fp $=$ KG token footprint. All four cases have a primary-judge $\Delta_{\text{joint}}$ CI excluding $0$; $^\ast$ marks the \emph{clean absorption wins} counted toward the gate (both-judge CIs exclude $0$, curve-dominance $1.0$, footprint $<0.05$). The co-firing cases are excluded for mechanistic reasons (see text), not for a failed CI.}
\label{tab:unlearn}
\begin{tabular}{llcccccl}
\toprule
Case (absorber) & regime & util$_{\text{KG}}$ & util$_{\text{SUB}}$ & util$_{\text{whole}}$ & $\Delta_{\text{joint}}$ [95\% CI] & fp & verdict \\
\midrule
taxonomic/Georgia (16009) & absorption & 1.73 & 1.17 & 1.33 & $+0.561\ [0.318,0.811]^\ast$ & 0.014 & \textbf{KG\,$\succ$\,$u_{\text{sub}}$} \\
first-letter/\texttt{large} (8463) & absorption & 1.87 & 0.87 & 0.00 & $+1.000\ [0.796,1.213]^\ast$ & 0.030 & \textbf{KG\,$\succ$\,$u_{\text{sub}}$} \\
taxonomic/United States (846) & co-firing & 1.74 & 1.30 & 1.40 & $+0.439\ [0.242,0.644]$ & 0.017 & router false-neg \\
toxicity/\texttt{insult} (13367) & co-firing & 1.19 & 0.83 & 0.98 & $+0.352\ [0.065,0.639]$ & 0.166 & judge-only (excl.) \\
\bottomrule
\end{tabular}
\end{table}

\paragraph{Why KG wins: sparse-firing gating, not a localization failure.} The mechanism is now precise. $u_{\text{sub}}$ localizes in concept space, but the erasure hook subtracts a continuous projection at \emph{every} token, so even a well-targeted direction perturbs the residual on retain/unrelated text and accumulates collateral at matched forget. The absorber fires only on its sub-context (firing-Jaccard $0.0019$--$0.013$, token footprint $0.014$--$0.03$), so gating by $z_l$ drives the edit footprint toward zero off-target. The contribution is therefore a \emph{discovery-then-act}: the grouping discovers the sparse handle label-free, and the handle's sparsity is what beats the labeled dense direction.

\paragraph{The win traces to the single absorber (M7).} Ablating the full multi-member K-track unit instead of the single absorber strictly \emph{lowers} retained utility (Georgia: single $1.73$ vs.\ unit $1.16$, single$-$unit $\Delta_{\text{joint}}+0.568$ CI $[0.341,0.811]$; \texttt{large}: single $1.87$ vs.\ unit $1.38$, $+0.491$ CI $[0.315,0.676]$) [ARTIFACT:art_3WXWsaSoGMnK]. The multi-member unit only adds collateral here; the two-track algorithm's value is as the \emph{discovery procedure} that proposes the precise single absorber, consistent with our reframing of the grouping contribution (\S\ref{sec:method}).

\paragraph{Co-firing cases, honestly excluded.} United States and toxicity/\texttt{insult} are co-firing, not absorption, and are \emph{not} counted toward the gate. US is a router false-negative: its specific absorber $846$ has a low footprint ($0.017$) but the aggregate parent recall hole is small ($0.197<0.5$), so the router correctly flags co-firing while a precise specialist still exists inside the aggregate (\S\ref{sec:router}, M5). Toxicity/\texttt{insult} co-fires hard (firing-Jaccard $0.882$, footprint $0.166$, no recall hole); it registers a judge-level $\Delta_{\text{joint}}>0$ but the collateral CI \emph{includes} $0$ and the model-internal joint does not corroborate it, so we report it as a weak judge-only edge, not a surgical win. Both behave exactly as the firing-Jaccard/recall-hole regime split predicts.

# The Significance Ceiling: Safety-Relevant Absorption Is Homograph-Confined
\label{sec:safety}

The stated goal asks for reliability on safety-relevant attributes. We tested whether the absorption signature that makes one KG-named latent a surgical handle (established for Georgia and \texttt{large}) extends to identity attributes, and report the result honestly as the contribution's ceiling.

\paragraph{A \$0 absorption screen over four identity hierarchies.} From the full \texttt{civil\_comments} corpus ($1{,}756{,}346$ rows, CC0) we build gazetteer-matched windows and content-flip templates for four identity hierarchies---religion, race/ethnicity, orientation/gender, nationality---with group labels assigned by surface form only (never the model, never Jigsaw identity columns). Per hierarchy we identify a firing-floor-validated content-responsive parent latent and screen every group for the Georgia signature (recall hole $>0.5$, firing-disjoint absorber Jaccard $<0.1$, precision $\geq 0.7$, $\geq 150$ eligible, hole-coverage gain CI excluding $0$), corroborating each flag with the non-circular form-free absorption-fraction oracle [ARTIFACT:art_yAQgbq5Wgymx].

[FIGURE:fig4]

\paragraph{Finding: of $44$ eligible safety groups, exactly two are absorption-structured---and both are homographs.} The positive control reproduces (Georgia recall hole $0.76$, Jordan $0.66$). Among the $44$ eligible \emph{safety} identity groups, only \texttt{white} (race; recall hole $0.63$, Jaccard $0.019$, oracle $0.46$) and \texttt{straight} (orientation; recall hole $0.72$, Jaccard $0.009$, oracle $0.26$) exhibit the absorption signature, and both are lexical homographs. The remaining $42$---Muslim, Hindu, Catholic, gay, lesbian, Asian, Mexican, Chinese, Canadian, and so on---show \emph{no} parent recall hole: the general identity parent fires reliably on them (Table~\ref{tab:safety}). Absorption tracks lexical polysemy, exactly as for Georgia/Jordan, not safety semantics.

\paragraph{Structure does not imply leverage.} On the conditional downstream test (KG-ABL vs.\ $u_{\text{sub}}=\text{diff-of-means}(\text{target group}, \text{sibling groups})$, two judges), the non-safety positive control Georgia is a clean win ($\Delta_{\text{joint}}+0.743$, CI $[0.528,0.958]$, both judges, retain collateral KG $3.4\times10^{-5}$ vs.\ $u_{\text{sub}}$ $0.078$, curve-dominance $1.0$, selectivity $1542\times$). But the two structured \emph{safety} groups do not transfer: \texttt{straight} wins under the primary judge only ($+0.20$, CI $[0.042,0.383]$) with a borderline second judge ($+0.117$, CI $[0.0,0.267]$, includes $0$) and a tiny matched-forget magnitude ($0.0012$, selectivity $<1$); \texttt{white}'s oracle-confirmed absorber has \emph{no on-target effect} ($\Delta_{\text{joint}}+0.058$, CI $[-0.1,0.2]$, curve-dominance $0.0$). The overall verdict is \textbf{SAFETY\_ABSORPTION\_FOUND\_NO\_WIN}: the absorption \emph{structure} exists for two homograph safety tokens, but the \emph{unlearning leverage} does not robustly follow.

\begin{table}[t]
\centering
\small
\caption{Safety absorption screen. ``struct.'' = groups with the absorption signature (recall hole $>0.5$ and firing-disjoint specialist). Only homograph tokens are structured; no safety group yields a robust downstream win. Taxonomic (Georgia) is the non-safety positive control.}
\label{tab:safety}
\begin{tabular}{lrrrl}
\toprule
Hierarchy & eligible & struct. & no-hole & structured groups \\
\midrule
taxonomic (control) & 20 & 1 & 19 & Georgia (homograph) \\
religion & 11 & 0 & 11 & --- \\
race/ethnicity & 8 & 1 & 7 & \texttt{white} (homograph) \\
orientation/gender & 5 & 1 & 4 & \texttt{straight} (homograph) \\
nationality & 20 & 0 & 20 & --- \\
\midrule
\textbf{safety total} & \textbf{44} & \textbf{2} & \textbf{42} & all structured are homographs \\
\bottomrule
\end{tabular}
\end{table}

\paragraph{What this means for the contribution.} This is the honest answer to ``is the method safety-relevant?'' The reliability gain CCRG delivers---a discovered, addable, ablatable single-sub-context handle that beats $u_{\text{sub}}$---is real but lands on homograph/polysemy and spelling sub-contexts, because those are where the absorption signature occurs; the demographic attributes a safety practitioner most wants to control are predominantly co-firing/entangled, consistent with \citet{Ahsan2025}. We present the homograph confinement of absorption as a measured scoping result and the headline limitation of the work, alongside the existing $0/28$-profession and toxicity-co-firing negatives (\S\ref{sec:negatives}).

# Measured Auditability and Cross-Dictionary Replication
\label{sec:audit}
\label{sec:crossdict}

The downstream win rests on the KG's localization; here we measure that the graph's edges are correct and that the spine is not an artifact of one dictionary.

\paragraph{KG-guided recall repair, honestly counted.} For every eligible under-served sub-context the KG names a covering absorber on a selection split and adds it to the anchor; recall recovery on a disjoint held-out split must exceed the $95$th/$99$th percentile of a \emph{random single content-responsive-latent addition} control (paired bootstrap, $B=10{,}000$). Across spelling, taxonomic, and numeric families, $69$ repair variants over $54$ candidate holes enter one Benjamini--Hochberg family; \textbf{$30$ survive FDR $\leq 0.05$}, spanning \textbf{$22$ distinct suppressed-parent recall holes} ($22 = 30 - 6$ coincident k-track/diagnostic variants naming the identical latent $- 2$ non-hole survivors), by family spelling $13$, homograph-taxonomic $3$ (Georgia $0.13\!\to\!1.00$, Jordan $0.25\!\to\!1.00$, United States $0.77\!\to\!0.99$), numeric $6$ [ARTIFACT:art_sxwT7hK6YFEA] [ARTIFACT:art_w7p8du2N1f0Y]. The control is cleared by $28/28$ surviving holes at the $95$th percentile and $23/28$ at the $99$th. We flag numeric as \emph{below-gate} (digit-token reconstruction cosine $0.876<0.9$). A dense label-free probe (k) classifies the holes but its decoder-projection argmax is always the \emph{parent}, never an absorber---it exposes no addable per-sub-context latent, whereas the KG names exactly one.

\paragraph{A KG-localized surgical edit, with the selectivity artifact corrected.} The mechanism underlying the downstream win is a surgical single-absorber ablation. Measuring on-target next-token KL at the edited token and collateral on siblings, surgical selectivity ($=$ on-target/collateral at matched effect) over the $n{=}6$ absorption cases at $16$k has \textbf{mean $1452\times$ and median $1262\times$}; restricting to the $n{=}5$ cleanly-surgical cases gives median $1722\times$ (Georgia $16009$ $1722\times$, Jordan $540$ $2722\times$, Jordan $8347$ $3247\times$, US $846$ $214\times$, \texttt{large} $8463$ $802\times$) [ARTIFACT:art_0CZwPjG2YMCf] [ARTIFACT:art_w7p8du2N1f0Y]. We do \emph{not} claim ``precision predicts surgicality'': it holds within the taxonomic family (Spearman $\rho=0.90$, $p=0.037$) but breaks across families (\texttt{large}/precision $0.571$ reaches $802\times$, exceeding US-$4760$/precision $0.709$ at $7.8\times$). The regime map is clean: the co-firing toxicity pole collapses to $2.4\times$ with footprint $0.117$, a $\sim\!600\times$ split the router predicts from one forward pass.

\paragraph{Members are human/LLM-auditable.} Describing each of $89$ unit members by its logit-lens top-10 tokens and top-5 activating windows with the sub-context label withheld, an ensemble LLM judge names the sub-context with agreement $0.730$ versus a shuffle null of $0.096$ (gap $0.634$, CI $[0.545,0.724]$). Absorbers are named at $0.756$ while anchors are named at only $0.43$ (the judge over-specifies the parent's mixed windows, an honest caveat).

\paragraph{The wider SAE fully replicates---and absorbs more.} On the $4\times$-wider $65$k canonical SAE (same model+layer, gating cosine $0.928$, FVU $0.170$) all four spine pieces replicate [ARTIFACT:art_4L1MZxvWYlGd]: the homograph holes recur (Georgia recall $0.13$, hole $0.87$, firing-Jaccard $0.004$, AUC $0.995$; Jordan hole $0.75$), the FDR repair loop yields \emph{more} survivors ($52$ distinct holes vs.\ $22$ at $16$k, spelling $29$/taxonomic $8$/numeric $15$---directly consistent with ``wider absorbs more'' \citep{Karvonen2025, Chanin2025}), the Georgia surgical edit reproduces, and the frozen recall-hole router transfers at balanced accuracy $1.0$.

\paragraph{Correcting the selectivity artifact.} A prior draft reported the $65$k Georgia edit at ``$3.7\times10^{6}$ selectivity.'' This is a \emph{divide-by-$\epsilon$ artifact}: the $65$k Georgia absorber has KG collateral $0.0$ exactly, so the ratio is on-target$/\epsilon$ ($\epsilon=10^{-8}$); the regime-mean ``$466997\times$'' is dominated by the same artifact and a NO\_ON\_TARGET\_EFFECT case [ARTIFACT:art_w7p8du2N1f0Y]. Excluding floor-limited and no-on-target cases, the corrected $65$k absorption selectivity is \textbf{mean $722\times$, median $676\times$} ($n{=}4$). The $16$k Georgia edit ($1722\times$, collateral $2.9\times10^{-5}$) and the $65$k Georgia edit (collateral below numerical precision; floor-bound $\geq 1290\times$ referenced to the $16$k collateral) are therefore \emph{comparably} surgical---not one being $2000\times$ better. The second \emph{layer} (layer 9, gating cosine $0.93$) replicates only partially and informatively: Georgia loses its hole ($0.003$; the layer-9 parent already covers it) while Jordan gains one ($0.536$) with a confirmed surgical edit ($2376\times$). The mechanism and its edits replicate; \emph{which} homograph is absorbed is a property of the (layer, width) dictionary.

[FIGURE:fig5]

# When and Where Does Grouping Help? A Demoted Router and a Breadth Count
\label{sec:router}

The contribution is regime-scoped, so its value depends on telling, before grouping, which regime a concept is in. We ran the strongest available test of the router and report its honest failure.

\paragraph{Derivation-perfect, out-of-sample-unvalidated.} The recall-hole-alone rule (predict absorption iff the parent's per-sub-context recall hole $>\tau_h=0.779$) separates the $12$ derivation concepts perfectly (balanced accuracy $1.0$, leave-one-out $0.833$), and firing-Jaccard is a corroborating signal only [ARTIFACT:art_F_-HUhl0NR_i]. To test it out-of-sample we \emph{enlarged} the prospective set with the homograph-entity testbed---$34$ eligible entities ($18$ cities, $12$ months, $3$ given-names, $1$ brand), a $5.6\times$ expansion. The frozen rule reproduces exactly ($\tau_h=0.7795$, drift $\approx 0$). It validates on the base-rate co-firing direction (co-firing-predicted $29/30$, Wilson CI $[0.833,0.994]$), but the \emph{discriminative} absorption-predicted stratum does not: homograph $2/4$ (Wilson $[0.15,0.85]$), homograph$+$spelling $5/10$ (Wilson $[0.237,0.763]$)---both CIs include $0.5$---and recall-hole$=1.0$ over-predicts absorption on new spelling letters F/M/W, which measure co-firing. We therefore \emph{demote} the router to an exploratory diagnostic, not a validated a-priori predictor.

\paragraph{A breadth count that bounds the phenomenon.} The same run answers the ``absorption is $n{=}1$--$2$'' critique with a systematic count [ARTIFACT:art_F_-HUhl0NR_i]. Of $64$ homograph entities with a stable estimate, only \textbf{three} are absorption-structured (recall hole $>0.5$ and firing-Jaccard $<0.1$)---and all three are \emph{months}: March ($0.997$), June ($0.947$), February ($0.573$), \emph{new} named suppressed-parent homographs beyond Georgia/Jordan. Zero of $22$ cities, $20$ given-names, and $10$ brands are structured; the month parent fires on only $0.62$ of month mentions versus $0.94$/$0.92$/$0.95$ for cities/names/brands, so only months leave holes. Structure and downstream leverage diverge once more: the strongest downstream-confirmed case is the month \texttt{May} (label-free unit AUC $0.95$ vs.\ best raw latent $0.79$, $\Delta+0.160$, CI $[0.123,0.198]$)---absorbed by the modal verb---even though \texttt{May} is not ``structured'' ($J=0.434$). The homograph phenomenon recurs but is confined to homograph/polysemy tokens, corroborating the safety screen.

# Within-SAE Selection and the Scope of Absorption
\label{sec:selection}

Where the signature holds, the unit recovers absorbers a count-matched marginal-attribution selection drops; where it does not, the method correctly degenerates.

\paragraph{Absorption is a homograph-polysemy phenomenon, not broad taxonomy.} Across all $52$ countries the absorption signature holds for \emph{exactly two}, Georgia and (descriptive) Jordan [ARTIFACT:art___vgSpUe6wAF]; United States is co-firing. A clean profession is-a hierarchy ($28$ professions over $13{,}843$ bias\_in\_bios bios) shows uniform-high parent recall ($0.88$--$1.00$, max hole $0.116$) and \textbf{$0/28$} absorption [ARTIFACT:art_Iy77UHoNaIhS]. So non-spelling absorption is polysemy-specific, not broad is-a generalization.

\paragraph{Where the signature holds, set-cover selection wins.} On the Georgia slice ($150$ positives vs.\ $2{,}100$ negatives) the precision-gated rebuild recovers the diagnostic-corroborated specialist $16009$ (held-out precision $0.955$) and drops the high-coverage low-precision $4697$ ($0.335$); the rebuilt unit $[3792,16009,540,846]$ reaches AUC $0.995$ and beats every label-free selector with AUC-difference CIs excluding $0$: S-rec $+0.307$, S-prec $+0.416$, S-mag $+0.294$, RE-$k$-anchored $+0.082$, and the supervised pools (g) $+0.577$ and (h) $+0.612$ (both below chance---the absorption signature) [ARTIFACT:art_Iy77UHoNaIhS]. The discriminating case is S-prec: the globally most-precise latents are not Georgia-specific, so a precision ranking collapses to AUC $0.579$, exactly where set-cover \emph{coverage} wins. By contrast, on the profession \texttt{model} slice (no hole) the unit degenerates to the bare parent (AUC $0.308$) and loses to (g) $0.544$ and a dense probe $0.961$---the honest contrast that bounds scope. A non-SAE dense probe still edges the Georgia unit ($1.000$ vs.\ $0.995$, $-0.005$): the contribution is auditable within-SAE selection, not out-classifying a dense probe.

\paragraph{First-letter spelling: set-cover isolated against non-random selectors.} On first-letter spelling the unit attains the highest held-out AUC on every letter (L $0.905$, O $0.917$, T $0.858$, I $0.983$, D $0.956$) and beats the count-matched attribution pool (h) [ARTIFACT:art_JMA2gBvnakAm]. The set-cover-specific win (beats (h) \emph{and} all three S-selectors) holds on I and D ($2/5$); on L/O/T the strong S-rec matches the unit. The compact named unit ($k\approx5$) is significantly below the $\sim\!15$-member wide pool (AUC difference $-0.056$ to $-0.200$): human-auditable compactness costs AUC, a trade-off we report rather than hide.

# Honest Negatives and Limitations
\label{sec:negatives}

We collect the method's failures in one place, each with its statistic.

\paragraph{No dense-probe out-classification.} On every task the best non-SAE dense probe matches or beats the unit (Georgia $0.995$ vs.\ $1.000$; numeric \texttt{integer} $0.635$ vs.\ $1.000$; toxicity loses to a residual probe). The contribution is auditable within-SAE repair and a regime-scoped edit, not aggregate classification.

\paragraph{The safety ceiling.} Safety-relevant absorption is homograph-confined: $2/44$ safety groups structured (both homographs), no robust safety downstream win (\S\ref{sec:safety}). The confirmed downstream wins are non-safety (Georgia, \texttt{large}).

\paragraph{Downstream win is regime-bounded.} KG-ABL beats $u_{\text{sub}}$ on the two clean absorption cases under both judges; the co-firing cases (US, toxicity) are not surgical wins. We do not beat dense on aggregate unlearning, consistent with \citet{Farrell2024}.

\paragraph{Router is exploratory; absorption is narrow.} The router's discriminative prospective stratum does not exclude chance even after a $5.6\times$ expansion (\S\ref{sec:router}); absorption recurs only on homograph/polysemy tokens ($3/64$ entities, $0/28$ professions). Toxicity is a clean co-firing negative.

\paragraph{Grouping is a discovery procedure, not a multi-member win.} The downstream wins and surgical edits trace to individual discovered absorbers ($16009$, $8463$, $846$), not to multi-member units; the C-track ties weak baselines (toxicity AUC $0.762$ vs.\ (a) $0.765$), and set-cover-specific selection appears on only three slices (Georgia, I, D) [ARTIFACT:art_w7p8du2N1f0Y].

\paragraph{Replication is layer-conditional; numeric is below-gate; steering and model-diffing are demos.} Cross-dictionary replication is full at $4\times$ width but partial across a layer (the absorbed token shifts); numeric digit-token reconstruction is cosine $0.876<0.9$. Steering with the unit's mean-member direction is most surgical on L and D but a diff-of-means/hub direction is more surgical on O/T/I [ARTIFACT:art_0ueMMR8Tt02P]. For model-diffing, no instruction-tuned Gemma Scope SAE exists for the 2B model; the shared-SAE base-vs-IT shift is detectable but \emph{not concept-specific} (control-subtracted genuine shift $+0.000$, CI $[-0.009,0.007]$), a confound-bounded null [ARTIFACT:art_jI2KIJotjzIU].

# Discussion
\label{sec:discussion}

\paragraph{What is established.} Executed on a frozen Gemma Scope SAE, CCRG is a training-free, label-free discovery procedure that surfaces the single precise absorber a marginal-attribution ranking drops, and emits a feature knowledge graph whose edges carry measured utility. The headline is that ablating one discovered absorber, gated by its own sparse firing, beats a \emph{sub-context-targeted} dense direction $u_{\text{sub}}$---not merely a whole-concept eraser---at matched forget on a joint collateral+fluency outcome (two-judge CIs excluding $0$, curve-dominance, on the two clean absorption cases). The edge is sparse-firing gating, not a localization failure of the dense direction, which we explicitly retire. The supporting spine---$22$ FDR-controlled recall repairs, a median $1262\times$-selective surgical edit, LLM-auditable members---replicates on a $4\times$-wider SAE (with more absorption) and partially across a layer, and we correct a prior divide-by-$\epsilon$ selectivity artifact.

\paragraph{A regime-scoped, discovery-then-act contribution with an honest ceiling.} The most useful lesson is that latent grouping is not a universal repair, and that the regime where it helps---homograph-polysemy absorption with a suppressed parent---is \emph{narrow} and, crucially, does \emph{not} coincide with the safety-relevant attributes the goal targets. A direct screen of $44$ safety identity groups finds absorption confined to two homograph tokens and no robust safety win. This positions the method precisely against the ``discover, don't act'' critique \citep{Peng2025}: CCRG discovers the sub-context handle through interventional grouping and acts through it where the handle is sparse, while we are candid that the handle exists for lexical-polysemy tokens, not demographic semantics.

\paragraph{Honest failure modes.} (1) No SAE unit out-classifies a dense probe on any task. (2) Safety absorption is homograph-confined; no robust safety win. (3) The downstream win is regime-bounded (two clean absorption cases). (4) The router is an exploratory diagnostic (prospective CI includes $0.5$). (5) Absorption is narrow ($3/64$ homograph entities, $0/28$ professions). (6) The wins trace to single absorbers, not multi-member grouping. (7) Cross-layer replication is partial; numeric is below-gate; model-diffing is a confound-bounded null. Each is reported with its statistic, not spun as future work.

# Conclusion
\label{sec:conclusion}

We presented Two-Track Co-Response Grouping, a training-free, label-free \emph{discovery procedure} that organizes the latents of a frozen public SAE by their interventional response to content counterfactuals---correlation communities for shared-support splitting and a precision-gated anchored set-cover for disjoint-support absorption that no pairwise-affinity clustering can propose. The durable contribution is the demonstration that a single \emph{discovered} absorber, ablated through a sparse-firing-gated edit, beats a \emph{sub-context-targeted} dense direction (not just whole-parent erasure) on a joint collateral+fluency outcome at matched forget---two-judge CIs excluding $0$ and curve-dominance on the two clean absorption cases (Georgia, \texttt{large})---because the absorber's sparsity drives its off-target footprint toward zero. We frame this honestly: the safety-relevant reach is bounded, because a direct screen finds absorption confined to homograph tokens ($2/44$ safety groups, no robust safety win), and the absorption regime is narrow ($3/64$ homograph entities, $0/28$ professions). The auditability spine---$22$ FDR-controlled recall repairs, a median $1262\times$-selective surgical edit, LLM-auditable members---replicates on a $4\times$-wider SAE and partially across a layer, and the one-forward-pass router is demoted to an exploratory diagnostic after an enlarged prospective test fails to exclude chance.

\paragraph{Future work.} Search wider entity vocabularies for additional suppressed-parent homographs beyond Georgia/Jordan/months; characterize \emph{which} representational structure (beyond lexical homography) yields a sparse single-feature handle, since safety attributes do not; harden the router only if a prospective set that excludes chance can be assembled; and revisit model-diffing if a paired instruction-tuned SAE becomes available.

# Appendix: Reproducibility
\label{sec:repro}

\paragraph{Encoding and gating.} SAEs are loaded directly from Gemma Scope \texttt{params.npz} (primary: canonical \texttt{layer\_12/width\_16k}, \texttt{average\_l0\_82}, JumpReLU, $d_{\text{model}}=2304$; cross-dictionary: \texttt{layer\_12/width\_65k/average\_l0\_72} and \texttt{layer\_9/width\_16k/average\_l0\_73}); the residual is captured by a forward hook on \texttt{model.layers[L]} output (\texttt{hidden\_states} index $L{+}1$). Each run gates on reconstruction fidelity before analysis: the unlearning and safety runs gate at cosine $0.919$ (L0 $\approx 88$); the $65$k and layer-9 runs gate at cosine $0.928$/$0.930$ (FVU $0.170$/comparable). Numeric digit-token reconstruction is $0.876<0.9$ and flagged below-gate. Word-token positions are recovered via the tokenizer offset map; corpus windows are drawn from a pinned Pile revision; surface-flip nulls use an independently re-judged $1{,}700$-pair superset [ARTIFACT:art_YwjLYapklnVk].

\paragraph{Models, edits, and software.} Model \texttt{google/gemma-2-2b} (and \texttt{-2b-it} for model-diffing) via ungated mirrors, bf16, eager attention; SAE \texttt{google/gemma-scope-2b-pt-res}. The unlearning experiment (\S\ref{sec:unlearn}, \S\ref{sec:safety}) reuses the surgical-edit code path verbatim (\texttt{JumpReLUSAE}, \texttt{ModelBundle}, \texttt{make\_edit\_hook}, \texttt{side\_effects}, \texttt{paired\_bootstrap\_diff}) and adds forget-matching, generation under the edit hook, the $u_{\text{sub}}$ comparator, two LLM judges, the joint composite, curve-dominance, and the deterministic human-proxy check. KG/units are taken from the iter-3 unit/KG artifact (taxonomic anchor $3792$, Georgia$\to$$16009$, first-letter L $8463$$\to$\texttt{large}). LLM judging/labeling uses \texttt{claude-haiku-4.5} (primary, temp $0$) and \texttt{gpt-4o-mini} (second judge); total spend was \$0.53 (unlearning, $1459$ calls, $0$ failures) and \$0.30 (safety), all under budget; all other compute is \$0 on a single NVIDIA L4 (23\,GB). Citation venues follow a verified audit (e.g.\ \citet{Chanin2024} NeurIPS 2025; \citet{Wu2025}, \citet{Karvonen2025} ICML 2025; \citet{Leask2025} ICLR 2025; \citet{Farrell2024} NeurIPS 2024 Safe-GenAI Workshop) [ARTIFACT:art_3zaa2xXEp8Az].

\bibliographystyle{plainnat}
\bibliography{references}

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

--- Item 11 ---
id: art_8AwUJK9qOwX_
type: experiment
title: >-
  Iter-3 CCRG Re-Run: Random-Eligible-k Baseline, AUC-Difference CIs, Verdict Reconciliation
summary: >-
  Decisive iter-3 re-run of the two-track CCRG first-letter-spelling pipeline (frozen Gemma-Scope L12/16k JumpReLU SAE on
  gemma-2-2b), reusing iter-2's method.py verbatim and surgically adding three fixes. M1 (decisive): a RANDOM-ELIGIBLE-k (RE-k)
  baseline drawing k=|unit| latents uniformly at random from the cover-eligible set Lr, max-pooled identically to the unit/(h)/(b)/(c),
  so unit-minus-RE-k isolates two-track SELECTION from cover-based eligibility+pooling; added to C1 and E2. The single most
  decisive number is frac_rek_ge_unit (one-sided permutation p: fraction of random eligible pools matching/beating the unit).
  M2: replaces the iter-2 accuracy-as-margin artifact with threshold-free AUC POINTS plus bootstrap AUC-DIFFERENCE CIs (B>=10,000,
  content-flip pair-cluster resampling on the held-out test fold) for unit vs (a)/(b)/(c)/(h)/(RE-k) per letter, a pooled-across-letters
  stratified-bootstrap + inverse-variance meta-analysis, and a Youden-threshold accuracy table (no predict-all-positive collapse;
  the F1-threshold artifact is retained and flagged). M3: computes primary_endpoint from the stated falsifier (E1 AND unit-AUC-significantly-above-BOTH-(h)-AND-(RE-k)
  on >=3/5 letters => ABSORPTION_REPAIR_SELECTION_CONFIRMED; else REFRAMED_TO_ELIGIBILITY_POOLING; else SELECTION_NOT_ESTABLISHED),
  reporting E1 and E2 transparently and never dropping E2 from the conjunction. Reproduction is verified: gating cosine 0.924,
  deterministic baselines reproduce iter-2 (h-AUC 0.795 vs 0.794), E1_PASS and E2_PASS patterns match; the greedy set-cover
  unit AUC drifts within ~0.03 because iter-2's torch 2.6+cu126 cannot run on this RTX 5090 (Blackwell sm_120), requiring
  torch 2.8+cu128 (all other deps pinned identically). On L the unit significantly beats RE-k (frac_rek_ge_unit~0.009, diff
  +0.24 CI excludes 0) but ties the oracle attribution baseline h (CI includes 0) — the pre-registered expectation. All analysis
  is under metadata.* (per_letter, verdicts, pooled_across_letters, endpoint_reconciliation_note, admission on the 1,700-pair
  surface superset, config, gating_check); datasets carry per-letter held-out test-fold rows with predict_unit/a/b/c/h/REk
  (Youden-thresholded). Output validates against exp_gen_sol_out.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_3/gen_art/gen_art_experiment_1
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 12 ---
id: art_P8-3ipCuQwVY
type: experiment
title: >-
  Non-Spelling SAE Absorption: RE-k Selection-Isolation, AUC-Diff CIs, Router Inputs
summary: |-
  Iteration-3 re-analysis of the executed iter-2 non-spelling SAE-absorption experiment. It reuses the frozen Gemma-Scope layer_12/width_16k SAE encodings (cached CSR latents + fp16 residuals) and the same two-track K-track unit/anchor/(g)/(h)/dense-probe, then adds the three iter-3-mandate analyses on the NON-SPELLING slices (taxonomic countries; numeric quantity types). Runs CPU-only via cache reuse (the RTX 5090 sm_120 is unsupported by torch 2.6.0+cu124, so the script auto-falls-back to CPU; the GPU re-encode path exists only for a cache miss, which never occurs). VERDICT = taxonomic_selection_established.

  M1 (selection isolation): adds a RANDOM-ELIGIBLE-k pool baseline (RE-k) and an anchor-fixed variant (RE-k-anchored) that separate the two-track set-cover SELECTION from cover-based eligibility+pooling. Rule selection_established(s) = (unit AUC > RE-k-anchored 95th pct) AND (paired AUC-difference CI vs RE-k-anchored mean excludes 0). TAXONOMIC Georgia: True (unit-RE-k-anchored = +0.099 [+0.085,+0.113], unit at 100th pct of draws). NUMERIC integer: False (unit-RE-k-anchored = +0.029 [-0.006,+0.062] includes 0) -> non-spelling numeric is eligibility+pooling, not set-cover selection.

  M2 (AUC + AUC-difference CIs): point AUC plus stratified paired-bootstrap AUC-DIFFERENCE CIs (B=10,000) for unit vs (g)/(h)/RE-k/RE-k-anchored/dense-probe on the defining absorbed slices (Georgia, integer), all 20 eligible countries / 8 numeric sub-contexts, and descriptive subs (Jordan, United States, decimal, year), replacing iter-2's mislabelled matched-recall-accuracy deltas. Georgia headline (pos=150 Georgia tokens vs 2100 taxonomic negatives): unit AUC=0.989, g=0.418, h=0.383 (below chance = absorption signature), RE-k=0.906, RE-k-anchored=0.890, dense-probe=1.000; unit-h=+0.606 [+0.570,+0.642] confirms a genuine AUC-rank effect (the R1 honesty fix), unit-dense=-0.011 [-0.015,-0.008] (the non-SAE probe slightly edges the unit but the unit is the best SAE detector). A comparison-matched Youden accuracy table is added so NO baseline is forced to predict-all (the artefact that made (h) look degenerate in iter-2).

  M7/M4 (router inputs): per-hierarchy firing-Jaccard(parent, top per-sub-context detector) on positives + parent per-sub-context recall holes + per-slice form-free KG top1, emitted as inputs for the M4 prediction-vs-outcome router table. absorption_type (parent hole>0.5 AND Jaccard<0.10) is True for exactly two countries -- Georgia (J=0.059, KG top1=1.0) and Jordan (n=124<150 descriptive, KG top1=0.95), the ambiguous homographs where the parent country-latent has a genuine recall hole; all other countries have parent_recall_hole~=0. Numeric integer router J=0.256 (co-firing, not mutually exclusive), KG mean top1=0.0. M7 framing: taxonomic = diagnostic_corroborated LEAD; numeric = suggestive_diagnostic_unconfirmed (dense-probe AUC=1.000 dominates, KG top1=0.0) and is NOT promoted.

  Deliverables: method.py (single pipeline = iter-2 core + iter-3 phases D-H), method_out.json / full|mini|preview_method_out.json (exp_gen_sol_out schema, PASSED, 8.5MB < 100MB; metadata.per_hierarchy carries auc_point, auc_diff_ci, rek_distribution, selection_established, youden tables, router+regime, generalization_status, honest_notes; datasets[].examples carry per-row diagnostic predictions predict_{unit,anchor,g,h,dense_probe,rek}), results/ (partial_{taxonomic,numeric}_iter3.json, results.json, auc_diff/router/sliced_recall CSVs, arrays npz), pyproject.toml (21 pinned deps), RESULTS_SUMMARY.md. Downstream GEN_PAPER_TEXT consumes this for the M1/M2/M7 non-spelling tables: taxonomic Georgia is the established selection win (and the only AUC-rank win that survives the anchor-fixed random control), numeric is honestly demoted to suggestive, and the router rows feed the M4 absorption-vs-splitting regime map.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_3/gen_art/gen_art_experiment_2
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 13 ---
id: art_lvYKkaolutJG
type: experiment
title: >-
  Measured Auditability of Two-Track CCRG SAE Units: KG Repair Loop + LLM Member-Labeling
summary: |-
  Executes the two previously-dropped, now load-bearing M5 AUDITABILITY results for the two-track Counterfactual Co-Response Grouping (CCRG) units on a frozen Gemma-Scope L12/16k JumpReLU SAE (gating cosine 0.919, token localization exact, hidden_states[13]). Canonical units/KG are READ from the deterministic iter-2 outputs (first-letter exp_1, taxonomic exp_3) and re-derived as a cross-check (responsive set 682 vs iter-2 684; anchor 3792 matches). It converts the iter-2 'we emit a 70-edge graph' ASSERTION into MEASURED numbers.

  M5a KG-GUIDED REPAIR LOOP (load-bearing): for each under-served sub-context (recall hole where the anchor/parent latent goes silent) the KG names a covering absorber; we ADD it to the anchor (max-pool) and measure recall recovery on HELD-OUT corpus windows (selection split disjoint from eval split: taxonomic train->diagnostic; first-letter folds 0-3 -> fold 4) vs a control that adds the full population of other content-responsive latents, with a paired-bootstrap CI (B=10,000). Result: 8 measured successful repairs whose KG-minus-random gain CI excludes 0 -- taxonomic Georgia (anchor recall 0.20 -> 1.00, gain 0.80, 99.4th pct vs random, CI [0.70,0.82]), Jordan (0.29 -> 1.00/0.935), United States (0.77 -> 0.99/0.97), plus first-letter O/'our' and D/'day' (0.00 -> 1.00). BOTH the K-track edge (4697/9339/8442) and the higher-precision diagnostic-corroborated absorber (16009/540/846) are significant. Honest negatives: first-letter L ('list','line',...) and T ('type','things',...) candidate words tie the random-addition control (too few held-out windows / no extra localization) -- reported verbatim.

  M5a(k) LOCALIZATION-FAILURE CHECK: the label-free group-inference probe (k) (JTT: ERM -> upweight hardest/error set -> retrain) yields a dense hyperplane whose decoder-projection argmax is the PARENT 3792 (top |cos|=0.44, does not dominate; KG absorbers rank 2269/58/5964, never argmax). (k) classifies the holes (recall 1.0 on Georgia/Jordan/US) but exposes NO addable per-sub-context latent -- whereas the KG names exactly one. Country is linearly separable so the JTT error set is empty and we upweight the lowest-margin 20%; the structural conclusion is unchanged.

  M5b LLM-JUDGE MEMBER-LABELING (load-bearing): 67 unit members (anchor + absorbers across taxonomic + L/O/T/D) each described by logit-lens top-10 tokens + top-5 raw activating corpus windows with the sub-context label WITHHELD (non-leaky); anthropic/claude-haiku-4.5 (temp 0, forced-choice) names the sub-context. Agreement 0.716 vs shuffle null 0.090 (analytic chance 0.087); gap 0.627, bootstrap CI [0.522,0.731] excludes 0. Per-role: absorbers 0.76 accuracy, anchors 0.20 (judge over-specifies the parent's mixed-country/word windows -- honest caveat). 84 calls, 0 errors, total LLM spend $0.047 (<<$3 target).

  VERDICT: kg_utility_measured=True, member_labeling_above_null=True, replaces_iter2_assertion=True. Output method_out.json (exp_gen_sol_out-schema-valid, full/mini/preview all <100MB) stores per-sub-context repair stats (recall_anchor, recall_anchor_plus_kg, gain_kg, kg_percentile_vs_random, random_gain percentiles, paired_bootstrap_CI, k-track + diagnostic variants, honest_negatives), the (k) decoder-projection check, full member evidence + judge choices + scoring (gap CI, per-role accuracy, confusion), and a datasets block (kg_repair_loop rows; member_labeling rows with predict_judge) for downstream solution evaluation. This provides the paper's auditability section: the emitted feature knowledge-graph carries MEASURED localization utility and the cluster-level units are human/LLM-auditable, while example-reweighting baselines provide no addable per-feature unit.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_3/gen_art/gen_art_experiment_3
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 14 ---
id: art_07ju05r0onqB
type: experiment
title: >-
  Firing-Structure Router (M4): firing-Jaccard predicts when grouping beats attribution
summary: |-
  This experiment promotes the SAE-latent firing-Jaccard to a headline, a-priori router (M4) and validates it PROSPECTIVELY on a frozen Gemma-Scope SAE (google/gemma-scope-2b-pt-res, layer_12/width_16k/average_l0_82; model unsloth/gemma-2-2b; hook blocks.12.hook_resid_post; firing := encode>0; gating reconstruction-cosine 0.927, L0 median 70). method.py runs ONE uniform pipeline over 15 concepts: 12 ESTABLISHED (spelling L/O/T/I/D; numeric; taxonomic; toxicity threat/identity_attack/insult/obscene/sexual_explicit) used to DERIVE the rule, and 3 PROSPECTIVE (CAD-IMDB sentiment; CEBaB food/service aspect) predicted BEFORE their outcome is revealed. Per concept it (1) identifies a content-responsive parent latent on content-flip pairs (an unsupervised positive-firing-floor validation fixes the letter-I spurious-anchor bug), (2) finds per-sub-context detector latents + parent recall holes, (3) computes positive-only firing-Jaccard(detector,parent) over the concept's positives, and (4) measures a downstream OUTCOME: a LABEL-FREE CCRG K-track-lite unit (parent anchor + firing-disjoint, hole-covering absorbers) versus three required baselines at MATCHED pool size k -- (a) the best single raw SAE latent, (h) a supervised SAE standardized diff-of-means attribution pool (AxBench/SCR-TPP proxy), and (d) a non-SAE diff-of-means probe on the raw layer-12 residual -- scored by a held-constant logistic head on a held-out test fold with paired-bootstrap CIs (B=10000).

  KEY RESULTS: firing-Jaccard cleanly separates the regime EXTREMES -- spelling is firing-disjoint (Jaccard L=0.017, O=0.039, T=0.003, I=0.008, D=0.017, all <0.1; reproduces iter-2) and cluster-level grouping helps; toxicity co-fires (~0.69) so a single specialist latent wins. The primary router (predict absorption iff Jaccard<tau*) yields tau*=0.05, balanced accuracy 0.917 on the 12 established concepts; leave-one-concept-out accuracy 0.733; prospective out-of-sample accuracy 0.333 (sentiment HIT, predicted+measured co_firing; aspect_food/service MISS -- predicted co_firing but showed small absorption deltas +0.034/+0.071).

  HONEST FINDINGS (load-bearing for the paper): (i) firing-Jaccard ALONE is insufficient -- the TAXONOMIC counterexample has LOW Jaccard (0.056) yet a co_firing OUTCOME because the parent already has ~0.95 recall (no holes to fill); accordingly a recall-hole-only router (hole>0.777) reaches balanced accuracy 1.0 on established concepts, and a 2-signal router (low-Jaccard AND high-recall-hole) is also reported, supporting the refined rule 'grouping helps only when disjoint specialists AND parent recall holes co-occur'. (ii) The supervised baselines (h)/(d) frequently MATCH or beat the label-free unit on raw AUC (consistent with 'simple baselines are strong on raw-latent SAE tasks'); the unit's contribution is being LABEL-FREE while still beating the best single latent (a) in the absorption regime. (iii) numeric is reported honestly as suggestive/diagnostic-unconfirmed (absorption is documented empirically only on spelling).

  DELIVERABLES: method.py (self-contained, single-GPU, $0 LLM spend) and method_out.json with full/mini/preview variants (exp_gen_sol_out schema, all schema-PASSED, each <0.4MB). The output carries metadata with the prediction_vs_outcome_table (parent, jaccard min/median/max, recall_hole_max, predicted vs ground-truth regime, per-baseline AUCs auc_unit/auc_a/auc_h/auc_d, deltas with paired-bootstrap CIs, hit), per_concept_firing_jaccard (per-sub-context detector + bootstrap CIs), the router block (tau-sweep, regime separation, LOO per-concept, prospective table, plus strict-CI / recall-hole-only / combined router variants), a reproduction_check (spelling all <0.1 = True; toxicity references), and honest_notes. Expensive SAE forward passes are cached under cache/ (excluded from the published repo). Downstream GEN_PAPER_TEXT can use this as the M4 'when does cluster-level grouping help vs marginal attribution' router result and its honestly-reported boundary (firing-disjointness must co-occur with parent recall holes).
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_3/gen_art/gen_art_experiment_4
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 15 ---
id: art_jI2KIJotjzIU
type: experiment
title: >-
  M6 Model-Diffing: Shared pt-SAE Co-Response Unit vs Best Latent, gemma-2-2b vs -it
summary: >-
  Delivers the M6 (model-diffing) downstream task for the Two-Track CCRG hypothesis: a single frozen Gemma-Scope layer-12/width-16k
  JumpReLU pretrained SAE (loaded directly from params.npz; reconstruction cosine 0.925 base / 0.913 IT, matching iter-2 ~0.92)
  applied to layer-12 residual activations of gemma-2-2b (base) vs gemma-2-2b-it (instruction-tuned), both unsloth ungated
  mirrors. METHOD = the iter-2 co-response UNIT (toxicity members {1920,12714,14630}; spelling-L 15-member anchor+absorber
  unit, anchor 205; both READ from iter-2 method_out.json). BASELINE = best single latent (toxicity anchor 12714) plus a descriptive
  oracle best-member. For 1200 toxic (civil_comments) and 1200 spelling-L corpus texts, it computes BOS-excluded max-pooled
  unit and single-latent responses on base vs IT, then base-vs-IT separability AUC, paired Cohen's d_z, a 2000x paired sign-flip
  shuffle null, and 2000x doc-bootstrap CIs. CONFOUND BOUNDING is load-bearing: B1 reconstruction parity (IT cosine 0.913
  not catastrophic, so the shared-base-SAE recipe is viable here); B2 control-concept floor (genuine toxicity shift = toxicity
  AUC-departure MINUS spelling-control departure); B3 residual-norm / norm-matched re-analysis (IT residual-stream norm 1.11x
  base). RESULT (verdict = clean-null-limitation, an explicitly valid M6 deliverable): a base-vs-IT shift IS detectable above
  the shuffle null for the toxicity unit (AUC 0.438, departure 0.062, p<1e-3, direction IT>base), but it is NOT concept-specific.
  The spelling control shows the SAME direction and an identical 0.062 departure, so the confound-controlled genuine toxicity
  shift is +0.000 (95% CI [-0.009, 0.007], includes 0); the norm-matched genuine shift is a small +0.027 (CI [0.021, 0.033])
  but still IT>base, OPPOSITE the naive detox prediction, i.e. generic OOD/norm drift rather than a concept-specific reduction
  in toxicity-feature usage. A within-model sanity check confirms the unit IS a genuine toxicity detector (toxic-vs-neutral
  AUC 0.71 base / 0.73 IT). The co-response UNIT does NOT detect the shift more reliably than the best single latent (abs-AUC-deviation
  difference CI includes 0; unit_wins=false), reported honestly. The result is stable across the gradual-scaling smoke/100/1200
  runs (toxicity unit AUC 0.459 -> 0.443 -> 0.438; genuine departure -> 0), evidence of a genuine null not noise. Honest framing:
  no gemma-scope-2b-it SAE exists, so this is an INFRASTRUCTURE-BOUNDED diffing result; the B1/B2/B3 bounds make the shared-SAE
  OOD confound explicit rather than leaving it as future work (cf. crosscoders, Anthropic 2024; Latent-Scaling misattribution
  risk, arXiv 2504.02922). Outputs: method.py (memory-safe one-model-at-a-time GPU pipeline), method_out.json + full/mini/preview
  variants (all validate against exp_gen_sol_out schema, all <1.7MB), and a results/per_text_arrays.npz sidecar of paired
  per-text arrays. Pure SAE/model inference; $0 LLM spend.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_3/gen_art/gen_art_experiment_5
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 16 ---
id: art_i-tkvFCKneA-
type: research
title: >-
  CCRG Citation Audit: Chanin NeurIPS-2025 Fix, Muchane Resolved, Winnicki Contrast
summary: >-
  Closes the iteration-3 M8 novelty/citation minors for the two-track CCRG paper (pure web research). THREE DELIVERABLES.
  (A) A drop-in Winnicki-2026 contrast: arXiv:2604.23829 (Winnicki, Gnanasekaran, Darve; Stanford ICME; arXiv preprint, no
  venue) builds feature-level KG edges PURELY OBSERVATIONALLY (corpus co-occurrence graph weighted by Jaccard over binary
  presence matrices + transcoder cross-layer mechanism graph of source->target sparse latent pathways); a full-text grep finds
  ZERO occurrences of 'interventional/counterfactual/intervention', so it provably cannot draw CCRG's interventional anchor-205
  -> absorber-3069('list') edge (firing-Jaccard<0.1, never co-fire) nor the taxonomic 3792 -> Georgia/Jordan edges (diagnostic
  KG-agreement 0.318 vs 0.002 null; Jordan 0.99). 2-3 sentence + long paragraph versions provided. (B) Corrected citation
  table. CRITICAL FIX: Chanin 'A is for Absorption' (2409.14507) = NeurIPS 2025 ORAL (Dec 4 2025; forum R73ybUciQF; 6 authors
  incl. Golechha), NOT the dossier's 'NeurIPS 2024' (which is the separate NeurIPS-2024 Workshop version, forum Wzav8fesTL,
  5 authors, '...in Spelling Tasks'). Muchane2025 RESOLVES to arXiv:2506.01197 (Muchane/Richardson/Park/Veitch) -- no removal
  needed. Benchmark audit 2605.18229 is SOLE-authored by David Chanin (key 'Chanin2026' VALID). SASA 2606.06333 confirmed
  (Dalili & Mahdavi). AxBench 2501.17148 = ICML 2025 (not ICLR); SAEBench 2503.09532 = ICML 2025; CanonicalUnits 2502.04878
  = ICLR 2025; MindTheGAP 2403.09869 = AISTATS 2024. DPE 2505.23027 and SCR/TPP 2411.18895 have NO venue in arXiv metadata
  -> cite as preprints. SparseCoactivation 2506.18141 title is now '...Causal Semantic Modules...' (was 'Composable'). Full
  table + corrections diff + BibTeX in research_report.md. (C) Three-axis novelty confirmation -- interventional co-response
  grouping, set-cover-for-SAE-grouping, a-priori firing-structure router -- ALL HOLD, with cite-and-distinguish one-liners
  for the four near-misses (Winnicki 2604.23829; Deng 2506.18141 observational coactivation; CDLC 2505.07073 vision/diffusion
  analog; Kantamneni 2502.16681 post-hoc, not a-priori). Outputs: research_out.json {answer, sources(19), follow_up_questions(5)}
  + research_report.md.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_3/gen_art/gen_art_research_1
out_expected_files:
- research_out.json

--- Item 17 ---
id: art_sxwT7hK6YFEA
type: experiment
title: >-
  Expanded KG-Repair + Member-Labeling Auditability Spine for SAE-Latent Cluster Units
summary: >-
  Expands the iter-3 measured-auditability result into the paper's load-bearing spine on a frozen Gemma-Scope L12/16k JumpReLU
  SAE over gemma-2-2b (gating cosine 0.9189 @ hidden_states[13], align 1.000; always gated on taxonomic country tokens because
  numeric digit tokens reconstruct at 0.8911<0.9 yet the SAE/layer mapping is global). FOUR measured pieces. (M1a) BROAD K-track
  KG: for EVERY eligible sub-context X a covering absorber is named purely on the selection split (argmax recall over content-responsive
  latents with firing-Jaccard<0.10 and sub-context precision>=0.70 vs the anchor), then ADDED to the parent/anchor and tested
  on held-out eval windows against a random-addition control of every other content-responsive latent, with paired-bootstrap
  CI (B=10000) AND a one-sided bootstrap p. (Multiplicity) Benjamini-Hochberg FDR<=0.05 across ALL 69 repair variants of all
  three families (hand-rolled BH cross-checked against statsmodels): 30 survive — homograph-taxonomic 6 (Georgia +0.80, Jordan
  +0.65, United States +0.21; k-track AND diagnostic; reproduces iter-3 exactly), numeric 10 (date +0.68, ordinal +0.53, decimal
  +0.45, year +0.35, comma_number +0.24, currency +0.14 — a NEW result showing absorption-repair generalises beyond spelling),
  spelling 14 (T that/their/there/then/those/three/through +1.0; O our +1.0, one +0.96; L like +1.0, law +0.78). 9 honest
  negatives emitted verbatim: numeric integer ties random (+0.007), first-letter O/on,out,over,own and T/this,think,time tie
  random; letter I anchor (1227) fires 0% on corpus -> auto-flagged spurious, repair N/A. (M1a-k) JTT label-free group-inference
  probe run per concept: its decoder-dictionary projection argmax is NEVER a KG absorber (kg_absorber_is_argmax=False everywhere)
  and on taxonomic/L/O/T/D is the PARENT anchor at rank 1 — (k) classifies holes but exposes no addable per-sub-context latent,
  whereas the KG names exactly one. (M7) Ensemble member-labeling (J=3 forced-choice claude-haiku-4.5 calls with shuffled
  candidate order to kill position bias) over 89 unit members INCLUDING all 15 of every first-letter max-pool: agreement 0.730
  vs shuffle null 0.096, gap 0.634, bootstrap CI [0.545,0.724] excludes 0, 0 parse-fails; per-role absorbers 0.756 / anchors
  0.43 (honest over-specification caveat). 15-wide confident-label fraction per letter L 0.87 / O 0.80 / T 0.93 / I 0.87 /
  D 0.67 (confident-and-correct ~0.60-0.73). LLM spend $0.194 (target <$1). Deliverables: method.py (full pipeline, reuses
  iter-3 SAE loader/encoder/repair_loop/k_localization_check, adds broad-KG derivation, one-sided p + BH, generalized (k),
  ensemble labeling + confident-fraction, disk-cached encodings), method_out.json (exp_gen_sol_out schema PASSED) with datasets
  kg_repair_loop (69 rows) and member_labeling (89 rows, predict_judge), README.md, fully-pinned pyproject.toml. Verdict:
  kg_utility_measured=True, n_survive_FDR05=30, member_labeling_above_null=True, fifteen_wide_confident_fraction_reported=True.
  Downstream paper-writing should headline the cross-family BH-surviving repairs + the (k)-cannot-localize contrast + the
  15-wide auditability fraction, and report numeric-integer/sparse-first-letter ties as honest negatives.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_4/gen_art/gen_art_experiment_1
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 18 ---
id: art_0CZwPjG2YMCf
type: experiment
title: KG-Localized Surgical Sub-Concept SAE Edit with Side-Effect Measurement (M1b)
summary: |-
  M1b is the unique-capability downstream task for the auditability-first two-track CCRG units: using the emitted feature knowledge-graph (KG), edit EXACTLY ONE sub-context by ablating its single NAMED absorber latent, and show high on-target effect with near-zero collateral on sibling sub-contexts and a tiny token footprint -- a capability the standard non-SAE handle (a dense parent direction) structurally cannot provide. This directly supplies the goal's 'activation steering with side-effect measurement' and 'feature-based classification of safety-relevant attributes' evaluation on a frozen Gemma-Scope L12/16k JumpReLU SAE + gemma-2-2b (edit/read at blocks.12.hook_resid_post; gating cosine 0.919, L0 88, matching iter-3), $0 LLM, single GPU.

  OPERATORS (forward hooks on the edit layer): KG-ABL = single named-absorber ablation h-=lambda*z_l*W_dec[l] (gated by the latent's own sparse firing); DENSE-ABL = diff-of-means parent erasure h-=beta*(h.u)u (baseline f, the non-SAE difference-of-means / logistic probe direction); RAND = random firing-rate-matched content latent; KG-ADD = steering-toward; (k) = label-free JTT probe (structural: no per-sub-context latent to edit). PRIMARY measure is behavioral: per-context next-token KL divergence at the edited token's position (steering-with-side-effects). A frozen dense parent probe (logistic + diff-of-means, fit on a DISJOINT diagnostic fold) is the secondary instrument; because country/letter membership is redundantly encoded, its margin is huge & broad under DENSE-ABL but insensitive to single-latent edits -- which is WHY behavioral KL is the primary on-target signal. Selectivity = on_target/collateral at matched effect, with B=10,000 paired bootstrap CIs on on-target, collateral, and the dense-minus-kg collateral difference; a graded verdict separates a CLEAN surgical edit (selectivity>=20, off-target footprint<5%, dense>kg collateral CI excludes 0) from a partial/co-firing edit.

  RESULTS (method_out.json, 7 cases, 5 SURGICAL_EDIT_CONFIRMED): taxonomic Georgia->16009 selectivity ratio 1722x (on-target KL 0.0216, KG collateral 3e-5, dense collateral 0.0496, KG footprint 0.0015 vs dense 1.0, dense-kg collateral CI [0.036,0.066]); Jordan->540 (2722x) & 8347 (3247x); United States->846 (214x); first-letter large->8463 (802x). The low-precision US absorber 4760 is only PARTIAL_SURGICAL (7.8x) -- absorber precision predicts surgicality (honest negative). TOXICITY negative pole (insult->13367) is PARTIAL_CO_FIRING_AS_PREDICTED: firing-Jaccard 0.878, parent recall-hole 0.0, selectivity 2.4x, footprint 0.117 -- single-latent ablation is NOT cleanly surgical because the sub-attribute co-fires with the parent, exactly as the firing-Jaccard/recall-hole router predicts. The regime router map cleanly splits absorption (n=6: mean selectivity 1452x, jaccard 0.014, footprint 0.0036) from co-firing (selectivity 2.4x, jaccard 0.878, footprint 0.117) -- a ~600x split. RAND raw-latent on-target ~0 (cannot reach matched); the (k) probe's decoder-projection argmax is the parent latent, never a KG absorber (no per-sub-context handle).

  OUTPUT DATASETS (exp_gen_sol_out, 409 examples, every example has predict_* per method): (1) edit_locality_per_context (402 rows) -- one labeled held-out context each: output=ON_TARGET (an X-context the edit SHOULD change) vs OFF_TARGET_SIBLING (a sibling it should NOT), with predict_kg_abl / predict_dense_abl / predict_rand = AFFECTED/UNAFFECTED from each operator's behavioral KL at full edit (lambda=1/beta=1); KG-ABL marks 0 of N siblings AFFECTED while DENSE-ABL marks nearly all (the collateral signature), RAND ~0 everywhere; (2) kg_surgical_edit_per_case (7 rows) -- output=SURGICAL_EXPECTED/NON_SURGICAL_EXPECTED by regime, predict_kg_abl=verdict, predict_dense_abl=HIGH/LOW_COLLATERAL, predict_*_selectivity. Rich aggregates live in metadata (per_case curves/matched/selectivity_CIs, summary.regime_router_map, k_localization_check, honest_negatives).

  DELIVERABLES: method.py (self-contained; reuses iter-2/iter-3 JumpReLUSAE/ModelBundle/encode_rows/k_localization_check/bootstrap + canonical units/KG read from iter-3 method_out.json; genuinely-new code = edit operators + behavioral side-effect measurement + per-context prediction rows); method_out.json + full/mini/preview_method_out.json (all schema-valid against exp_gen_sol_out, <500KB each); README.md; pyproject.toml (exact pinned versions, torch 2.6.0+cu124). Downstream paper can cite the surgical-edit ratios, the dense-baseline per-context collateral, the (k) no-handle result, and the firing-Jaccard router map as the auditability headline's concrete downstream payoff.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_4/gen_art/gen_art_experiment_2
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 19 ---
id: art___vgSpUe6wAF
type: experiment
title: 'Taxonomic SAE Unit/Specialist Conflation Fix: Precision-Gated K-Track Rebuild'
summary: |-
  Re-analysis (no new data) of the frozen Gemma-Scope L12/16k taxonomic absorption testbed, reusing the iter-2/3 cached CSR latents + fp16 residuals (CPU; no GPU re-encode). Fixes the iter-3 conflation where the two-track K-track classification unit's Georgia member was the high-coverage/low-precision latent 4697 (sub-context firing precision 0.35), not the diagnostic-corroborated specialist 16009 (0.96).

  CORE FIX (M2): the anchored greedy max-coverage is run in three objective variants on a SELECTION (train) fold and reported on a disjoint HELD-OUT (diagnostic) fold (M7): `original` (raw coverage; reproduces 4697), `gated` (+ hard per-sub-context FIRING-precision gate >=0.70 -> recovers 16009, drops 4697), and `weighted` (precision*coverage -> also 16009). Headline = gated unit [3792(anchor), 16009(Georgia .97/.96 sel/held-out), 540(Jordan), 846(United States)]. All 3 absorbers pass held-out subctx precision >=0.70 (fraction 1.0); member-labeling agrees.

  VERDICT taxonomic_setcover_isolated. On the held-out Georgia slice (150 pos vs 2100 neg, paired bootstrap B=10000) the unit AUC=0.995 beats every comparator with CIs excluding 0: vs (g) +0.577, (h) +0.612 (g/h below chance = the absorption signature), RE-k-anchored +0.082, and the three NEW non-random label-free count-matched selectors S-rec (+0.307), S-mag (+0.294), and the discriminating S-prec (+0.416; the globally most-precise latents are not Georgia-specific so S-prec misses 16009 -> AUC 0.579) => set_cover_established=True. A non-SAE dense probe still slightly edges the unit (-0.005, honest negative): the contribution is auditable WITHIN-SAE precision-gated selection + the homograph router, not out-classifying a dense probe.

  M3 homograph scope: a homograph x absorption-type cross-tab over all 52 countries shows absorption_type (parent recall-hole>0.5 AND specialist firing-Jaccard<0.10) is True for EXACTLY {Georgia, Jordan} - both documented homographs whose general parent latent is suppressed (hole 0.80/0.71). Chile/Turkey are homographs but their parent COVERS them (hole ~0) -> not absorption; United States is non-homograph co-firing/splitting (fj 0.20); 48 non-homographs have hole~0. The hardcoded homograph set equals the dataset's metadata_notes=='ambiguous_homograph' flag (no discrepancy).

  HONEST NUANCE (per-edge form-free KG, M2 Phase 4): the form-free absorption_fraction is a MAGNITUDE oracle and on Georgia holes picks the high-coverage LOW-precision latent 1966 (precision 0.34), not the precise member 16009 (they co-fire, Jaccard 0.34) -> per-edge top-1 agreement with 16009 is 0. Corroboration therefore rests on the PRECISION diagnostic (non-triviality) + the router recall-hole signal, all of which 16009/540/846 pass; the magnitude oracle is precision-blind (reported separately, not a 3-edge mean). The precision rebuild buys AUDITABILITY (a Georgia-pure member), not raw AUC (all 3 Georgia absorbers reach recall 1.0 / ~0 FP so AUC is ~identical across variants).

  Numeric is the contrast: verdict numeric_suggestive_diagnostic_unconfirmed, set_cover_established=False (integer is co-firing/splitting J=0.256, no precision-passing integer specialist; dense probe AUC 1.0 dominates the unit's 0.635).

  DELIVERABLES: method.py (single pipeline; copied & edited from iter-3 method, +run_greedy 3-variant K-track, fold split, M5 selectors, M3 cross-tab, ablation, transparency). full/mini/preview_method_out.json (schema exp_gen_sol_out, all PASS; full 10.9MB <100MB) with metadata.per_hierarchy.{taxonomic,numeric} carrying rebuilt_units, precision_objective_ablation, auc_point + auc_diff_ci (S-rec/S-prec/S-mag + RE-k-anchored + g/h/dense), kg_agreement (per-edge + formfree_magnitude_top), formfree_magnitude_tension, homograph_crosstab, router_all, selection_isolation, rebuilt_unit_transparency; datasets[].examples carry predict_{unit,anchor,g,h,dense_probe,rek,S_rec,S_prec,S_mag,original,weighted}. results/*.csv (auc_diff +S-* cols, router_all +homograph col, ablation, per_edge_kg). All JSON-vs-CSV internal-consistency cross-checks PASS. cache/ (124MB reused encodings) is upload-ignored.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_4/gen_art/gen_art_experiment_3
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 20 ---
id: art_JMA2gBvnakAm
type: experiment
title: >-
  Two-Track CCRG Selection Isolation: Non-Random Selectors, Firing-Floor, Compact Unit
summary: |-
  Iter-4 re-runs the frozen-SAE first-letter two-track Counterfactual Co-Response Grouping (CCRG) pipeline (Gemma-Scope L12/16k JumpReLU SAE on unsloth/gemma-2-2b, hook blocks.12, gating cosine 0.924 / EV 0.857) verbatim from iter-3 and adds three honest-scoping deltas; $0 LLM spend, B=10,000, ~14 min on one GPU. Method = K-track anchored greedy set-cover unit (anchor + per-token absorbers). Baselines held constant: raw single latent (a), co-fire/decoder clusters (b,c), oracle attribution top-k (h), and the demoted random-eligible-k floor (RE-k). M5 (decisive new core): three NON-RANDOM, label-free, count-matched-to-k selectors over the SAME cover-eligible set Lr -- S_rec (top-k by content-flip recall), S_prec (top-k by firing precision), S_mag (top-k by mean magnitude) -- max-pooled identically to the unit, so unit-minus-each isolates the set-cover SELECTION rule from sensible label-free selection; reported as paired-bootstrap AUC-difference CIs (pair-cluster resampling). M4: an unsupervised firing-floor anchor validation (a valid parent anchor must fire >=5% on held-out corpus) plus a per-letter JOINT (E1 AND selection) and a renamed verdict. M7: the compact named unit (anchor + diagnostic-corroborated absorbers, cap 5) vs the full 15-wide max-pool, with an AUC-difference CI, an anchor_only floor, and an AUC-vs-cumulative-k curve.

  RESULTS (L,O,T,I,D). primary_endpoint = REFRAMED_TO_ELIGIBILITY_AND_SENSIBLE_SELECTION (n_E1_pass=5, n_joint=2, n_selection_vs_M5=2, n_eligibility_only=2). M4 firing-floor RECOVERED letter I: its recall-argmax anchor 1227 fires 0% on corpus; the validated anchor 1634 (fires 20.6%) IS the form-free-diagnostic parent, so E1 now PASSES for I (5/5 overall, up from iter-3's 4/5); L/O/T/D anchors unchanged (already fire >0.26). M5 selection isolation: the set-cover-specific selection is established only on I and D (unit beats h AND all three non-random selectors, CIs exclude 0); on L/O/T the strong S_rec (top-k by recall, which picks the anchor + highest-coverage latents) matches the unit, so the win there is cover-based eligibility + sensible selection, not set-cover-specific. Per-letter unit AUC (vs h): L .905(.795) O .917(.819) T .858(.647) I .983(.735) D .956(.727). Pooled across letters the unit beats h by 0.188 (CI .148-.223), S_rec by 0.109 (.077-.143), S_prec by 0.273, S_mag by 0.120 (all pooled CIs exclude 0), but per-letter S_rec is significant on only 2/5. M7: the compact named unit (k=5) is SIGNIFICANTLY BELOW the 15-wide pool on every letter ( delta AUC -0.056 to -0.200, CIs exclude 0) -- the diagnostic-uncorroborated absorbers carry real classification signal, so human-auditable compactness costs AUC; reported, not hidden. E2 (absorbed-slice recall) passes only on T. The iter-3 over-aggregating rule (E1 AND unit>h AND RE-k on >=3/5) would have declared ABSORPTION_REPAIR_SELECTION_CONFIRMED (RE-k is an easy floor: median draw AUC 0.63-0.69, frac_rek>=unit <=0.008); this is recorded under legacy_iter3_verdict and contrasted.

  FAITHFULNESS/HARDWARE: this run is on RTX 2000 Ada (sm_89); iter-3 ran on RTX 5090 (sm_120). The UNMODIFIED iter-3 method.py was re-run on this host and produced numbers IDENTICAL to this iter-4 run for L (unit AUC 0.905, K_UNIT ending in latent 1566, RE-k mean 0.651), confirming the additive M4/M5/M7 code does not perturb the pipeline (M5/M7 use separate child rngs; the firing-floor corpus encode consumes no shared rng). Differences from the stored iter-3 anchors (L unit 0.876, member 1362) are bf16 hardware numerics breaking a discrete greedy set-cover tie at L's 15th member -- documented in metadata.repro_appendix.

  OUTPUT (schema exp_gen_sol_out, {metadata, datasets}, all variants <0.7MB). metadata.per_letter[X] carries anchor_validation, E1, E2, C1 (per_method AUC for unit/a/b/c/h/REk/S_rec/S_prec/S_mag/unit_compact/unit_15wide/anchor_only + auc_diff CIs), selection_isolation, compact_vs_wide (auc_by_k curve, compact_minus_15wide CI), admission, kg_edges, unit_definition. metadata.verdicts carries primary_endpoint, per_letter_joint, set_cover_isolation_table, compact_vs_wide_table, letter_I_annotation, legacy_iter3_verdict, and pooled_across_letters (unit_vs_h/REk/S_rec/S_prec/S_mag stratified-bootstrap + inverse-variance meta). datasets = one group per letter of held-out test-fold rows with predict_{unit,a,b,c,h,REk,S_rec,S_prec,S_mag,unit_compact,unit_15wide,anchor_only}. For the paper: the headline is the honest reframe (cluster-level units beat raw latents and attribution and a random-eligible floor, but the set-cover-SPECIFIC win over strong non-random selectors holds only on 2/5 letters), plus the M4 firing-floor anchor fix and the M7 auditability-vs-AUC tradeoff.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_4/gen_art/gen_art_experiment_4
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 21 ---
id: art_GTc_f26dMzFs
type: experiment
title: >-
  A-priori SAE firing-structure router as a screening heuristic with measured error
summary: >-
  method.py implements an a-priori SAE firing-structure ROUTER on the frozen Gemma-Scope L12/16k JumpReLU SAE over unsloth/gemma-2-2b
  (layer-12 residual hook; firing := encode>0; SEED=1234; $0 LLM). From ONE forward pass it reads two label-free signals per
  concept — the firing-Jaccard between per-sub-context detector latents and the broad parent latent, and the parent's recall-hole
  — and combines them into a screening rule: predict ABSORPTION-regime iff (firing-Jaccard < tau_J) AND (recall-hole > tau_h),
  else CO-FIRING. Absorption => the label-free CCRG K-track unit (parent anchor + firing-disjoint hole-covering absorbers)
  beats the best single RAW SAE latent (a); co-firing => a single specialist already wins. The experiment's contribution is
  methodological honesty: (1) DERIVATION vs TRULY-PROSPECTIVE separation — 12 derivation concepts (spelling L/O/T/I/D, numeric,
  taxonomic, 5 toxicity sub-attributes) fit the thresholds, single-signal ablations, and leave-one-out; they are NEVER counted
  as prospective. (2) An EXPANDED, truly-held-out prospective set predicted with the FROZEN rule before measurement: sentiment,
  CEBaB aspect_food/service, ~8 bias_in_bios profession concepts (pre-registered boundary-null), and civil_comments severe_toxicity
  (descriptive_only). Prospective hit-rate + Wilson CI = the MEASURED error, framed as a screening heuristic, not a validated
  oracle. Each concept reports the held-out-test outcome of the label-free unit vs three supervised baselines at matched pool
  size: (a) best raw SAE latent, (h) standardized diff-of-means SAE attribution pool, (d) non-SAE residual diff-of-means probe;
  paired-bootstrap delta CIs (B_BOOT=4000); PRIMARY regime = sign(auc_unit-auc_a), SECONDARY vs (h). KEY VERIFIED RESULT (reproduced
  exactly in the run logs at full scale): spelling firing-Jaccard 0.017/0.039/0.003/0.009/0.017 (all absorption), numeric
  0.285 with recall-hole 0.800 (absorption), toxicity ~0.69 (co_firing); the COMBINED rule achieves balanced-accuracy 1.0
  on derivation at tau_J~0.30, tau_h~0.78 — strictly dominating jaccard-alone (0.917) and tying recall-hole-alone (1.0, the
  strongest single separator) — with derivation leave-one-out ~0.83 (misses only the boundary concepts numeric+taxonomic).
  Counterexamples justify the conjunction: numeric has HIGH jaccard yet is absorption; taxonomic has LOW jaccard yet co_firing
  (parent already ~full recall). Outputs (exp_gen_sol_out): method_out.json + full/mini/preview, one router-decision card
  per concept with metadata mirroring derivation_table, prospective_table (vs-a AND vs-h), single_signal_ablations, loo, prospective_hitrate
  (existing-3 / new-only / combined-all + Wilson CIs), reproduction_check, and honest_notes. IMPORTANT STATUS: the currently-emitted
  JSON is a small placeholder from the --smoke run because a co-tenant job held the shared single GPU continuously for >2.5h,
  blocking the full-scale pass; method.py is complete, correct, and validated (gating recon-cos 0.927, BOS token-id mismatches
  0), and its self-healing launcher (run_full.sh) is wired to overwrite the output with the full 24-concept result the instant
  the GPU frees. Reproduce: uv run method.py --scale full.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_4/gen_art/gen_art_experiment_5
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 22 ---
id: art_QBxBPF-9Ldxe
type: research
title: >-
  CCRG iter-4: Homograph-Absorption Novelty, KG-Surgical-Edit Distinctness, Locked Citations
summary: >-
  Finalizes positioning + citations for the auditability-first CCRG (Counterfactual Co-Response Grouping) paper, building
  on the iter-3 audit (art_i-tkvFCKneA-) without re-doing settled entries. FOUR deliverables (pure web research, $0): (A)
  Homograph/polysemy absorption framing = NOVEL: documented feature absorption is empirically first-letter-spelling-only (Chanin
  2409.14507 'short'/'starts-with-S'; SAEBench 2503.09532 absorption metric is built on Chanin's first-letter task) and mechanistically
  tied to sparsity+hierarchy+dictionary-size (Chanin; Matryoshka 2503.17547), NOT to homograph/polysemous tokens with a suppressed
  parent on a semantic hierarchy. The key near-miss PS-Eval (Minegishi et al., 2501.06254, ICLR 2025) evaluates SAE word-SENSE
  separation and a full-text grep finds it NEVER mentions absorption/recall-hole/router/spelling/suppressed-parent (only hit
  = JumpReLU 'suppresses small activations'). Provides short+long positioning paragraphs + a one-line PS-Eval cite-and-distinguish;
  framing guardrail = 'absorption recurs on polysemous tokens, predicted by the recall-hole signal' NOT 'broad taxonomic generalization'.
  (B) KG-localized single-absorber surgical sub-concept edit = DISTINCT: no SAE/LLM steering/erasure method edits a single
  absorber latent NAMED by an interventional feature-KG edge to change/recover ONE sub-context while preserving the parent,
  measured as recall-recovery vs random-addition control + side-effect KL. SAE-TS (2411.02193) and SRS (2503.16851) select
  a CONCEPT feature (effect-approximator / contrastive-KL) with a coefficient; SALVE (2512.15938) is VISION (ResNet-18/ViT-B/16);
  LEACE (2306.03819, NeurIPS 2023) is dense whole-concept erasure that cannot localize to a sub-context; SAeUron/SAEmnesia/SNCE
  are text-to-image DIFFUSION erasure (modality distinguisher). AxBench (2501.17148, ICML 2025) is the side-effect/fluency
  LLM-judge eval bar AND the honest concession (diff-of-means beats SAEs on aggregate steering) -> CCRG scopes the edit as
  an auditability DEMONSTRATION. Cite-and-distinguish table + M1 positioning paragraph + honest-scope note provided. (C) Locked
  2025/2026 citation table: PS-Eval=ICLR2025; SALVE=ICLR2026 Trustworthy-AI Workshop(vision); SAE-TS=arXiv2024; SRS=arXiv2025;
  LEACE=NeurIPS2023; SAeUron=ICML2025(diffusion); SAEmnesia/SNCE=2025 preprints(diffusion). TWO upgrades vs iter-3: DPE 2505.23027
  -> ICML 2025 (poster 43937/OpenReview qUTiOeM57J); SCR/TPP 2411.18895 -> NeurIPS 2024 ATTRIB Workshop. BibTeX block + corrections
  diff + unresolved flags (SAEmnesia/SNCE author lists to verify at bib-time; do not invent). (D) Presentation-strip checklist
  for GEN_PAPER_TEXT (strip iteration/rebuttal/infra scaffolding; move SAE-IDs/seeds/env to appendix; lead with measured auditability;
  dedicated honest-negatives subsection; use locked table). Outputs research_out.json {title, summary, answer, 23 sources,
  4 follow_ups} + research_report.md (sections A-D with drop-in paragraphs, full table, BibTeX, checklist). Both novelty claims
  HOLD; adversarial disprove-searches found no precedent.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_4/gen_art/gen_art_research_1
out_expected_files:
- research_out.json

--- Item 23 ---
id: art_9muVcI4tkqJf
type: experiment
title: KG-Localized Absorber Unlearning Beats Dense Parent Erasure on a Joint Outcome
summary: |-
  M1 LOAD-BEARING DOWNSTREAM WIN for the two-track CCRG units: it converts iter-4's 'surgical selectivity' capability into a BETTER RESULT than the dense baseline on selective sub-concept UNLEARNING. Task: at MATCHED forget-quality, ablate ONE KG-named absorber latent (KG-ABL: h-=lambda*z_l*W_dec[l], gated by the latent's own sparse firing) vs erase the dense diff-of-means parent direction (DENSE-ABL, baseline f; for a binary parent ~ LEACE 1-D erasure). WIN <=> KG-ABL has strictly LOWER sibling+parent collateral AND BETTER fluency than DENSE-ABL, with a KG-minus-dense paired-bootstrap CI (B=10000) on the JOINT (retain-quality x fluency) outcome excluding 0.

  RESULT (method_out.json, full run): 4 cases, 2 DOWNSTREAM_WIN_CONFIRMED => the M1 gate is PASSED. (i) taxonomic/Georgia (absorber 16009): joint Delta=+0.423 [0.274,0.571], retain next-token KL KG=3e-5 vs DENSE=0.102, KG utility 1.75 vs 1.33, footprint 0.014 vs 1.0; collateral AND fluency CIs each exclude 0. (ii) first-letter/large (8463): joint Delta=+1.646 [1.479,1.799]; the dense 'starts-with-L' erasure at matched forget collapses to utility 0.17 while KG stays 1.82 (it wrecks fluency on every token; KG does not). (iii) taxonomic/United States (846): PARTIAL_WIN -- joint CI excludes 0 and collateral favors KG, but fluency CI includes 0 (weaker, multi-token absorber). (iv) toxicity/insult (13367) is the declared honest co-firing negative pole: insult sub-attributes co-fire with the toxic parent (firing-Jaccard 0.882, no parent recall-hole), the single latent fires on 16.6% of tokens, and the joint CI INCLUDES 0 [-0.035,0.451] -> EXPECTED_LOSS_ROUTER_CONSISTENT, exactly as the firing-Jaccard router predicts in advance. Curve-level dominance = 1.00 for every case (KG strictly lower collateral at every achievable forget level), so the win is robust to the single matched point. The REGIME SPLIT (absorption Jaccard 0.002-0.04 -> clean win; co-firing Jaccard 0.88 -> no win) is the contribution.

  METHOD/BASELINES: forget-matching via a lambda/beta sweep (next-token KL on held-out FORGET windows); generation under each edit hook (greedy, 40 tokens); an AxBench-style OpenRouter LLM judge (anthropic/claude-haiku-4.5, temp 0, utility=harmonic_mean(fluency,content_pres) in [0,2]); plus a model-internal joint (high-n retain next-token KL + continuation perplexity) as corroboration and explicit fallback. Required baselines covered: (ii) non-SAE = dense diff-of-means/LEACE parent probe (DENSE-ABL); raw-latent SAE contrast = RAND (firing-rate-matched random latent, ~no effect). SAE google/gemma-scope-2b-pt-res layer_12/width_16k (JumpReLU, d_model 2304); model google/gemma-2-2b bf16; edit+read at blocks.12.hook_resid_post (gating cosine 0.919). Canonical units/KG from iter-3 (taxonomic.anchor=3792, Georgia->16009, L 8463->large); insult latent re-found by max-AUC among toxic rows (13367, matching iter-4). $0 model-internal + $0.4367 LLM judge (876 calls, 0 fail/refusal; target $2, hard cap $10).

  REUSE: core.py = iter-4 gen_art_experiment_2/method.py verbatim (only WORK path repointed): JumpReLUSAE, load_sae, ModelBundle, ParentProbe (logistic probe AND diff-of-means dense direction u_t), make_edit_hook, side_effects, forward_pos_logprobs/kl_rows/behavioral_curve, paired_bootstrap_diff, bootstrap_mean_ci, _scale_for_on_target, pick_random_latents, content_responsive, load_*, NEUTRAL_TEXT, read_canonical_units, save_json. method.py adds the new pieces.

  OUTPUTS: datasets[0]='unlearn_per_prompt' (292 rows: one per (case, held-out prompt); input=prefix, output=role FORGET/RETAIN/UNRELATED, predict_kg_abl/predict_dense_abl/predict_rand/predict_noop = generated continuations + per-op metadata_fluency/content_pres/utility and model-internal last-token KL + continuation PPL). datasets[1]='kg_vs_dense_per_case' (4 rows: output=WIN_EXPECTED/LOSS_EXPECTED, predict_kg_abl=win_verdict, all collateral/joint CIs + firing-Jaccard + curve-dominance in metadata_*). metadata holds gating, judge spend, per_case curves/matched-scales/CIs/judged-forget-confirmation, summary, and honest_negatives verbatim. Concrete worked example in the data: on a sibling context naming 'United States', KG-ABL preserves it (content_pres 2) while DENSE-ABL corrupts 'United States'->'surrounding areas' (content_pres 1). All outputs validate against exp_gen_sol_out and are < 0.5 MB.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_experiment_1
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 24 ---
id: art_4L1MZxvWYlGd
type: experiment
title: >-
  Cross-Dictionary Replication of the SAE Auditability Spine on a 65k Gemma-Scope SAE
summary: |-
  M2 re-runs iter-4's four-piece auditability spine on a SECOND Gemma-Scope SAE dictionary of the SAME frozen gemma-2-2b, to separate model+method findings from one-dictionary artifacts. PRIMARY = width-65k canonical at layer-12 (average_l0_72, d_sae=65536, resolved as closest-to-100 from {21,38,72,141,297}); SECONDARY (reduced) = layer-9 width-16k (average_l0_73). The decisive design point: latent indices are dictionary-specific, so anchors AND per-sub-context absorbers are RE-DERIVED on each dictionary (16k Georgia->16009/Jordan->540 do not carry over). Anchor re-derivation = highest content-flip-coverage content-responsive latent with sub-context precision>=0.70, validated by an unsupervised corpus firing-floor>=0.01; absorbers via the K-track greedy (firing-Jaccard<0.10, precision>=0.70) and, independently, a form-free probe-projection diagnostic. method.py is one file parametrized over the SAE config; it reuses iter-4 exp1 (broad KG-repair + random-single-latent control + one-sided bootstrap p + Benjamini-Hochberg FDR, statsmodels-crosschecked), iter-4 exp2 (KG-ABL/DENSE-ABL/RAND edit operators + next-token-KL on_target/collateral run_case), iter-3 exp4 (firing_jaccard, recall-hole, derive_1d router). Core is $0 LLM.

  HEADLINE: cross_dictionary_replicates = full. 65k (layer-12) gives overall=full with ALL four pieces REPLICATES: (A) homograph holes reappear (Georgia recall-hole 0.873/jaccard 0.0038; Jordan 0.746/0.097; re-derived anchor 31478, corpus-fire 0.916); (B) 55/154 KG-repairs survive BH FDR<=0.05 (spelling 29 / homograph-taxonomic 11 / numeric 15, deltas +15/+5/+5 vs 16k's 14/6/10 = the predicted wider-SAE-absorbs-more signal; 52 distinct holes); (C) Georgia single-absorber (46143) ablation is SURGICAL_EDIT_CONFIRMED at selectivity ratio 3.7M (KG-collateral 0 vs DENSE 0.037), plus US/`layer`/`did`; (D) the FROZEN 16k recall-hole threshold (tau_h=0.7774) transfers at balanced-accuracy 1.0. Clean regime split: absorption mean selectivity 466997x vs co-firing toxicity-insult 1.99x (jaccard 0.837), confirming the router on the new dictionary. SECONDARY layer-9 gives overall=partial and shows absorption is LAYER-specific: a cleaner layer-9 parent (corpus-fire 0.987) means Georgia loses its hole (0.003) while Jordan keeps its hole (0.536) and a confirmed surgical edit (2376x); the multi-concept router transfer is NOT_RUN in the reduced taxonomic-only run. Honest nulls reported verbatim (re-derived Jordan/`on`/`take` absorbers fire but ablation has no on-target effect). Gating: 65k cosine 0.9280 (>0.9, +0.009 vs 16k), hidden_states[13]; numeric digit-token cosine 0.876 recorded descriptively (not gate-failed); all anchors firing-floor-validated, none spurious.

  OUTPUT (exp_gen_sol_out, schema-valid): metadata.replication_tables[dict] (per-piece recall_hole/jaccard, per-family FDR survivors+deltas+distinct count, surgical CIs/footprint, frozen-vs-refit router balanced-accuracy, regime_split, per_piece_verdicts, overall_verdict), metadata.router_transfer, metadata.verdict.cross_dictionary_replicates, plus datasets cross_dictionary_replication (one row per dictionary x piece x sub_context), kg_repair_loop, edit_locality_per_context. Downstream (paper) gets a precise, honest characterization of when the absorption/KG-repair/surgical-edit story is dictionary- and layer-dependent. cache/ (encoding npz, ~400MB) is excluded from upload. NOTE: repatch_verdicts.py re-assembles the verdict tables from the saved run via the same method.py functions (no model re-run); a fresh `uv run method.py --dicts 65k,l9_16k` reproduces method_out.json identically.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_experiment_2
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 25 ---
id: art_4q5Om8wdqZuz
type: experiment
title: >-
  A-priori SAE firing-structure router: recall-hole screens cluster-vs-latent reliability
summary: >-
  method.py FULLY RUNS (scale=full, 31 concepts) an a-priori SAE firing-structure ROUTER on the frozen Gemma-Scope L12/16k
  JumpReLU SAE over unsloth/gemma-2-2b (layer-12 residual hook; firing := encode>0; SEED=1234; $0 LLM; single GPU; gating
  recon_cos_mean=0.9269 (>0.80), encode_token token-id mismatches 0). From ONE forward pass it reads label-free firing-structure
  signals per concept and predicts the regime: ABSORPTION (the label-free CCRG K-track unit = parent anchor + firing-disjoint
  hole-covering absorbers BEATS the best single raw SAE latent) vs CO-FIRING (a single specialist already wins). M6b REFRAME
  (recommended): RECALL-HOLE-ALONE = predict absorption iff the parent latent's per-sub-context recall-hole > tau_h_alone=0.779;
  on the 12 derivation concepts this is the strongest single separator (balanced-acc=1.0, NO counterexample). Firing-Jaccard-alone
  reaches only balanced-acc=0.917 (demoted to a CORROBORATING signal); the combined conjunction (firing-Jaccard<0.31 AND recall-hole>0.78)
  also reaches 1.0 on derivation but its out-of-sample prospective hit-rate does NOT exceed recall-hole-alone (conjunction_beats_primary_out_of_sample=False),
  so recall-hole-alone stays the recommendation by parsimony. Two honest counterexamples justify recall-hole over firing-Jaccard-alone:
  numeric (firing-Jaccard 0.285 HIGH yet ground-truth absorption) and aggregated taxonomic (firing-Jaccard 0.058 LOW yet co_firing
  because the parent already has near-full recall / ~0 hole). EVALUATION compares the label-free unit against (a) best single
  raw SAE latent, (h) supervised standardized diff-of-means SAE-attribution pool, and (d) a non-SAE residual diff-of-means
  probe, all at MATCHED pool size with a held-constant LR head (only SELECTION differs); paired-bootstrap delta CIs (B_BOOT=4000);
  ground-truth regime = sign(auc_unit-auc_a). INTEGRITY: 12 DERIVATION concepts (spelling L/O/T/I/D, numeric, taxonomic, 5
  toxicity sub-attributes) fit thresholds/ablations/leave-one-out (LOO acc 0.833; misses ONLY the boundary numeric+taxonomic)
  and are NEVER counted as prospective. M6c: the truly-held-out PROSPECTIVE set is predicted with the FROZEN rule BEFORE its
  outcome is measured ('logged BEFORE outcome measurement') and spans BOTH regimes: 7 internally-built NEW first-letter spelling
  concepts (B,C,F,M,P,R,W; 250 content pairs + 300 real Pile-window corpus positives each, from_templates=False; derived from
  the gemma vocab get_alpha_tokens recipe) supply ABSORPTION-regime concepts alongside CO-FIRING concepts (sentiment, CEBaB
  aspect food/service, 8 bias_in_bios professions, civil_comments severe_toxicity). M6d DECISIVE deliverable - prospective
  hit-rate STRATIFIED by predicted regime, each with a Wilson 95% CI (the MEASURED error of a screening heuristic, not a validated
  oracle): absorption_predicted 3/6=0.50 [0.19,0.81], cofiring_predicted 8/12=0.67 [0.39,0.86], combined_all 11/18=0.61 [0.39,0.80].
  The router is genuinely WRONG IN BOTH DIRECTIONS: new letters F/M/W are predicted absorption (recall-hole=1.0) but measure
  co_firing (unit ties (a)) = false-absorption misses, while C/P/R are correct absorption wins (delta_vs_a +0.05 to +0.07,
  sig). Honest reproduction: derivation spelling firing-Jaccard stays low (L .017 .. D .016) but several new letters are higher
  (B .10, F .089, M .087, R .09) so spelling<0.05 is False (reported, not hidden); recomputed toxicity firing-Jaccard (threat
  .69, identity_attack .11, insult .69) differs from the prior reference and is reported as an honest discrepancy. Outputs
  (exp_gen_sol_out, all PASSED, <100MB): method_out.json + full/mini/preview, 31 router-decision cards (metadata_role, metadata_predicted_regime
  [PRIMARY recall-hole-alone] + _combined/_jaccard ablations, ground-truth regimes, recall_hole_max, jaccard_median, outcome
  auc_unit/a/h/d + delta CIs, is_prospective_hit, power_flag, per_subcontext) mirroring top-level derivation_table, prospective_table,
  single_signal_ablations (recall_hole_alone PRIMARY), ablation_combined, loo, counterexamples, prospective_hitrate_primary
  + ablation hitrates, reproduction_check, honest_notes, new_letter_report. self_check.py: ALL CHECKS PASSED. Reproduce: uv
  run method.py --scale full.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_experiment_3
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 26 ---
id: art_Iy77UHoNaIhS
type: experiment
title: >-
  M7: Second SAE Absorption Case Beyond Georgia — Profession Is-A Hierarchy + Homograph Scan
summary: |-
  Executes M7 on the FROZEN Gemma-2-2b / Gemma-Scope layer_12/width_16k JumpReLU SAE to test whether the iter-4 non-spelling absorption/set-cover result (effectively n=1, Georgia; 1-2 with descriptive Jordan) corroborates on a SECOND suppressed-parent case. VERDICT = `absorption_remains_narrow` (the expected, publishable honest negative).

  PART 1 (NEW science, fresh GPU whole-text encode): the bias_in_bios PROFESSION is-a hierarchy. 13,843 bios (cap 500/profession, gender-stratified) + 5,000 non-bio negatives (movie+restaurant reviews, same corpus file) encoded by mean-residual / max-latent over all non-special tokens (per-token FVU=0.173, meanL0=76.9 — pipeline correct). 50/50 selection/diagnostic split, stratified by profession. Corpus-only parent = latent 12692 (discriminative bio-vs-review, content-style precision 0.906, held-out recall 0.973, firing-floor pass). The 28-profession HOLE TABLE (held-out) is the headline: every profession has parent recall 0.88-1.00 (max hole 0.116 on 'model'), 0/28 `absorption_type` => `uniform_high_parent_recall_no_absorption`: a general occupation parent fires on ~all professions with NO suppressed hole for a specialist to fill => absorption does NOT generalize to a clean is-a hierarchy. Baseline comparison on the largest-hole profession 'model' (one-vs-rest, DESCRIPTIVE): the set-cover unit degenerates to the bare parent (AUC 0.308) and is BEATEN by g=top-20 marginal-attr (0.544) and the non-SAE dense difference-probe (0.961); set_cover_established=False — the honest contrast showing the two-track method only helps when an absorption signature exists.

  PART 2 (CPU, iter-4 taxonomic cache): re-running reproduces iter-4 EXACTLY. `absorption_type` (parent recall-hole>0.5 AND specialist firing-Jaccard<0.10) is True for exactly {Georgia, Jordan}, both suppressed-parent homographs; {Chile,Turkey} are homographs the parent covers; 48 non-homograph countries (incl. United States = co-firing/splitting) are not. Entity-token scan over 20 country-mention surfaces with >=150 occurrences: only Georgia qualifies (Jordan n=124<150) => no new case; coverage-limited (testbed labels per-country not per-city).

  PART 3 (CPU): Jordan-beside-Georgia side-by-side. Georgia (n=150, eligible, hole 0.80, J=0.059, unit AUC 0.995, set_cover_established=True) beats every label-free/attribution baseline with paired-bootstrap AUC-diff CIs (B=10,000) excluding 0: S-rec +0.307[0.267,0.348], S-prec +0.416[0.382,0.448], S-mag +0.294[0.254,0.334], RE-k-anch +0.082, g +0.577, h +0.612; non-SAE dense probe still slightly edges it (-0.005[-0.008,-0.003], honest). Jordan (n=124, descriptive, hole 0.71, J=0.021, AUC 0.957). United States (n=150, J=0.204, hole 0.23, NOT absorption).

  BASELINES held side-by-side in one pipeline: two-track set-cover UNIT vs raw-SAE {anchor, g top-20 marginal-attr, h count-matched, S_rec/S_prec/S_mag label-free selectors, RE-k-anchored} vs non-SAE {dense difference-of-means probe}. Result reproduced deterministically across two runs (cache-reuse re-run identical).

  DELIVERABLES: method.py (orchestrator + baselines), profession_absorption.py (Part 1: whole-text encoder, corpus-only parent ID, 28-profession hole table, per-profession set-cover/selection-isolation), engine.py (iter-4 method reused verbatim for the taxonomic cache path). method_out.json (+ full/mini/preview) validate against exp_gen_sol_out (all PASS, 2.85 MB <100 MB); metadata.per_family.{professions,taxonomic} carries the full 28-row hole table, parent, set-cover with CIs, homograph cross-tab, entity scan, side_by_side, honest_negatives; datasets[].examples carry per-row predict_{unit,anchor,g,h,dense_probe,rek,S_rec,S_prec,S_mag} (2,750 profession one-vs-rest rows + 424 Georgia/Jordan/US rows). results/*.csv (hole_table_professions, setcover_auc_diff_model, side_by_side_jordan_georgia, homograph_crosstab). FOR DOWNSTREAM PAPER: this corroborates that SAE feature absorption is specific to suppressed-parent homograph polysemy, NOT a general is-a/taxonomic phenomenon; affirmative non-spelling set-cover evidence remains ONE eligible slice (Georgia), 1-2 counting descriptive Jordan — report as a scoped, honest finding. SAE: gemma-scope-2b-pt-res-canonical layer_12/width_16k/canonical (avg L0 82), seed 20240617, GPU NVIDIA L4 (sm_89); re-runs GPU-free (encodings cached).
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_experiment_4
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 27 ---
id: art_-k4Yg-l4NaNO
type: evaluation
title: >-
  M3/M4/M5/M8 honest-counting, selectivity, control & transparency consolidation eval
summary: |-
  Pure-analysis ($0, CPU-only, no LLM/GPU) read-only evaluation that recomputes the four iter-4 reviewer-flagged headline numbers directly from the stored experiment JSONs (D1 art_sxwT7hK6YFEA, D2 art_0CZwPjG2YMCf, D3 art___vgSpUe6wAF, D4 art_JMA2gBvnakAm) and serializes them as drop-in, cross-checked statements. eval.py loads each full_method_out.json, traverses defensively, and emits eval_out.json (schema exp_eval_sol_out PASSED; 91KB) with metrics_agg (25 scalars), 5 datasets (M3 survivor_table 30, M4 cases 7, M5 percentile_evidence 28, M8 first-letter 5 + taxonomic 4), and rich M3/M4/M5/M8 + cross_checks blocks under metadata.

  KEY CORRECTED NUMBERS (every value COMPUTED then compared to stored expectations; mismatches reported, never overwritten). M3 honest counting: 69 repair variants tested, 30 survive BH-FDR<=0.05, spanning 22 DISTINCT recall holes (NOT 23) = 30 - 6 double-count-redundant - 2 non-hole survivors; reconciliation balances. The 6 identical-latent double-counts are exactly Georgia/16009, Jordan/540, United States/846, date/8684, decimal/7983, ordinal/13658 (kg_ktrack==kg_diagnostic). HONEST DEVIATION from plan: there are 2 non-hole survivors, not 1 — numeric/percent (lat 9112) AND L/layer (lat 2378, anchor already recalls 'layer' at 1.0 on the selection fold), so per-family distinct holes are spelling 13 (not 14), taxonomic 3, numeric 6. M4 selectivity: absorption set n=6 mean=1452.5x / median=1262.2x; cleanly-surgical set n=5 (excludes partial-surgical US-4760 at 7.8x) median=1722.5x — the draft's '1452x median' is the MEAN of the n=6 set. Spearman precision-vs-selectivity: all-7 rho=0.679, absorption-6 rho=0.714, within-taxonomic-5 rho=0.900 (p=0.037) — NOT 1.0, because US-846 (prec 0.973) has lower selectivity (213.5) than Georgia (prec 0.955 -> 1722.5); the softened verdict and paper_wording use the actual 0.90. Cross-family counterexample confirmed: spelling large (prec 0.571 -> 802x) beats taxonomic US-4760 (prec 0.709 -> 7.8x). M5 control wording: implemented control is a random SINGLE content-responsive-latent addition (method.py lines 617-621: ctrl_detect=base[:,None]|ctrl_fire is per-latent; pct=(ctrl_gain<gain_kg).mean()); no union/max-pool exists. All 28 surviving hole-variants clear the single-latent p95 (frac 1.0); 23/28 clear p99 (frac 0.821); Georgia pct=0.9939. The misleading docstring phrase 'every OTHER content-responsive latent (the full random-addition population)' at lines 19-20 is flagged for removal. M8 transparency: first-letter compact-vs-15-wide AUC deltas -0.056..-0.200 (all CIs exclude 0 = auditability cost); 15-wide confident-fraction L .867/O .8/T .933/I .867/D .667; taxonomic held-out per-member precision with gate-fold=selection/report-fold=heldout (16009 .968/.955, 540 .992/.975, 846 .993/.973, all pass >=0.70 heldout); member-labeling agreement 0.730 vs shuffle null 0.096, gap 0.634 CI [0.545,0.724]; characterized-subset fractions per letter scope the auditability claim.

  cross_checks: 35/38 pass; the 3 'fails' are the honest expected-vs-actual discrepancies (n_distinct_holes 22 vs ~23, non_hole_survivors 2 vs 1, taxonomic rho 0.90 vs 1.0), each carrying an explanatory note — this is the integrity-lock working as designed, surfacing that the iter-4 draft framing needs these exact edits. Outputs: eval.py, eval_out.json + full/mini/preview_eval_out.json (all schema-valid), pinned pyproject.toml (numpy==2.1.3, scipy==1.14.1, loguru==0.7.2). Paper-writing can drop the M3/M4/M5/M8 paper_wording strings in verbatim to preempt the reviewer minors.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_evaluation_1
out_expected_files:
- eval.py
- full_eval_out.json
- mini_eval_out.json
- preview_eval_out.json

--- Item 28 ---
id: art_y_5u-bfJOq3V
type: research
title: >-
  CCRG iter-5: M1 Unlearning Positioning, M2 Absorption Width-Dependence, Locked Cites
summary: >-
  Positions the two new iteration-5 results of the Counterfactual Co-Response Grouping (CCRG) paper against the right literatures
  and finalizes the venue-locked citation set for GEN_PAPER_TEXT. Pure web research, $0, no code; builds on iter-3 (art_i-tkvFCKneA-)
  and iter-4 (art_QBxBPF-9Ldxe) without re-doing settled entries. THREE deliverables. (A) M1 = a KG-named single-ABSORBER
  edit claimed to beat a dense diff-of-means / LEACE whole-concept-erasure baseline on a joint within-hierarchy-collateral
  + fluency metric at matched on-target (forget) effect. VERDICT: DISTINCT but must be framed NARROWLY. The broad claim 'an
  SAE-feature intervention can beat a dense baseline on unlearning/steering' is CONTESTED, not unprecedented: Farrell/Lau/Conmy
  (2410.19278, NeurIPS-2024 Safe-GenAI Workshop) report multi-feature SAE unlearning has side-effects >= RMU and that SAE
  quality must improve to match fine-tuning, and AxBench/Kantamneni concede dense beats SAEs on aggregate -- BUT CRISP (2508.13650,
  ACL 2026), SAUCE (ICCV 2025, VLM), SSPU (2505.24428, EMNLP 2025) and SRMU (2512.16297) all claim utility-preserving SAE-unlearning
  wins on WHOLE concepts. The defensible novelty is the CONJUNCTION none combine: (1) regime = single SUB-CONTEXT removal
  WITH PARENT preservation on the SAME hierarchy (where a dense whole-concept direction structurally over-shoots); (2) unit
  = ONE KG-NAMED absorber latent DISCOVERED (not pre-known) -- directly answering the 'Use SAEs to Discover, not Act' framing
  threat (2506.23845, Peng et al.); (3) metric = within-hierarchy sibling+parent collateral mapped onto the established forget-quality/retain-utility/fluency
  Pareto triad (WMDP=ICML2024, TOFU=COLM2024, MUSE=ICLR2025, RWKU=NeurIPS2024-D&B, SHRED 'new Pareto frontier' 2605.07482,
  survey 2601.13264). Three adversarial disprove searches returned only whole-concept removal (SAUCE/SAeUron/CRISP/Harry-Potter-ablation)
  and non-archival single-feature steering near-misses (GDM anger feature; ETH SAE-vs-MeanActDiff) -- no archival precedent
  for the conjunction. Honest concession + scope guardrail + 'if it fails reframe to auditability' contingency provided. (B)
  M2 = cross-dictionary (65k-width and/or second-layer) replication is the literature-PREDICTED robustness axis with a SIGNED
  prediction: SAEBench (2503.09532) states verbatim 'Feature Absorption ... scores degrade at larger widths' and 'Absorption
  scores worsen with increased dictionary size for all architectures except Matryoshka' and 'Unlearning effectiveness is best
  at earlier layers and varies significantly by layer' (width series 4k/16k/65k at layers [5,12,19]); Feature Hedging (2505.11756)
  gives the two-sided law (absorption worse WIDER, hedging worse NARROWER, 'width is not a neutral hyperparameter'); Matryoshka
  (2503.17547) gives the dictionary-size law + a non-spelling 'Lily/female-names' absorption hole. So 16k->65k should show
  MORE absorption (the CCRG phenomenon stronger), making replication the expected outcome and non-replication itself a publishable
  dictionary-dependence finding. Feasibility confirmed: Gemma-Scope has 65k residual SAEs at ALL gemma-2-2b layers (Neuronpedia)
  + width series at layers 5/12/19; numeric-digit reconstruction <0.9 caveat has NO literature basis -> gate the numeric arm
  on measured cosine. (C) Citation finalization: carries forward every iter-3/iter-4 lock; adds 13 verified M1/M2 cites with
  IDs/venues/authors; KEY CORRECTION: SAUCE arXiv 2503.14530 is WITHDRAWN but an ICCV 2025 CVF camera-ready exists -> cite
  CVF; CRISP UPGRADED to ACL 2026; SSPU=EMNLP 2025; Farrell=NeurIPS 2024 Safe-GenAI Workshop; possible Deng NeurIPS-2025 upgrade
  flagged (verify track); BibTeX block + corrections diff + extended presentation-strip checklist provided. Outputs research_out.json
  + research_report.md (sections A-D).
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_research_1
out_expected_files:
- research_out.json

--- Item 29 ---
id: art_2xQn686KUmV5
type: dataset
title: >-
  Homograph/Polysemy Entity Absorption Testbed (cities, months, given-names, brands)
summary: |-
  A pure CPU/text artifact: a FOUR-hierarchy homograph/polysemy entity absorption testbed, built as a strict structural drop-in extension of the iter-1 non-spelling absorption testbed (art_t2uUbjSwpd3t). It is explicitly a NEXT-ITERATION BUILDING BLOCK (not consumed by this iteration's parallel experiments): it supplies breadth of suppressed-parent candidates so the persistent single-slice taxonomic critique (Georgia-only) can be answered with many homograph cases.

  Four `dataset`s, one per is-a hierarchy, whose surface tokens carry a strong competing NON-target sense (the competition that produces feature absorption / a suppressed-parent recall hole):
    1. city_homograph_absorption  (parent = is-a-city): Phoenix, Mobile, Reading, Bath, Nice, Buffalo, Paris, Mercury, Jackson, Columbus, Cleveland, Florence, ... (23 entities).
    2. month_name_absorption (parent = is-a-month): all 12 calendar months; homograph-strong May/March/August/April/June.
    3. given_name_absorption (parent = is-a-given-name): Grace, Hope, Mark, Will, Rose, Frank, Faith, Joy, Dawn, Jack, ... (34 entities).
    4. brand_homograph_absorption (parent = is-a-brand): Apple, Amazon, Shell, Target, Orange, Gap, Tide, Visa, Subway, Java, ... (24 entities).

  Each hierarchy ships the SAME three coordinated components as dataset_2: (A) content-flip minimal pairs (parent present vs absent, surface-matched), (B) surface-flip pairs (concept fixed, surface varied; both positive, for the unit-level surface-invariance check), and (C) a frozen monology/pile-uncopyrighted diagnostic corpus (pinned rev 3be90335b66f24456a5d6659d9c8d208c0357119) of real windows labelled by frozen, model-independent sub-context. The NEW homograph_competitor negative family (the same surface token in its non-target sense, e.g. lowercase 'apple'/'will'/'march', 'Joaquin Phoenix', 'Christopher Columbus') is the matched hard control that makes a suppressed parent visible.

  On-disk format is the AII exp_sel_data_out schema: {metadata, datasets:[{dataset, examples:[{input, output, metadata_*}]}]} with FLAT metadata_* keys (no nested objects). New/extended fields vs iter-1: metadata_hierarchy (city|month|given_name|brand), metadata_entity (canonical surface), metadata_target_sense (city|month|given_name|brand|competitor|null), metadata_competitor_sense (gloss of competing sense), metadata_homograph_strength (wordfreq Zipf of the lowercase competitor), and metadata_neg_family expanded to include homograph_competitor / other_place / other_time / other_person_ref / other_company_ref / easy. Fold semantics are unchanged (pairs 70/30 train/test by pair_id stratified by sub_context; corpus 50/50 train/diagnostic stratified), gemma-2-2b offset-mapping token anchoring is reused (metadata_target_token_indices), and the downstream K-track + form-free absorption diagnostic pipeline runs unchanged except for the new enum values.

  Labels are assigned PURELY from surface form / regex / gazetteer (geonamescache for cities) / disambiguating local context — never from a model — so the degenerate-construction guard holds and absorption presence/absence stays a future-iteration EMPIRICAL finding: the corpus equally supports the 'absorption is spelling-specific' null and a positive homograph-absorption finding. Corpus target-sense labels use high-precision case-aware cues; an LLM-judged stratified sample MEASURES per-hierarchy target-sense precision (reported in manifest.json, target >=0.9; it does not relabel the corpus). manifest.json carries per-(hierarchy,entity) absorption_readiness with diagnostic_positives counts and status (eligible if >=150 diagnostic-fold positives, else descriptive_only), eligible_entities_per_hierarchy, per-component counts, source/pile-set counts, llm_pair_pass_rate, llm_corpus_sense_precision, llm_cost_breakdown, city geonames provenance, and cross-hierarchy collision notes (Dawn, Chase, Jordan, Mercury, Paris). Deliverables: data.py, build_dataset.py, pipeline.py, schema.json, manifest.json, and full/mini/preview_data_out.json (validated against exp_sel_data_out, each <100MB). Reproducible via fixed seed 20240617 and pinned pile revision; total LLM spend well under $1.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_dataset_1
out_expected_files:
- data.py
- full_data_out.json
- preview_data_out.json
- mini_data_out.json

--- Item 30 ---
id: art_3WXWsaSoGMnK
type: experiment
title: 'M1'': KG single-absorber unlearning vs a sub-context-targeted dense baseline'
summary: >-
  M1' replaces the near-tautological WHOLE-PARENT dense comparator of iter-5 with a STRONGER, sub-context-targeted dense baseline
  u_sub = diff-of-means(target-sub-context-positive, sibling-positive in the same parent context), fit on a DISJOINT fold
  from the per-sub-context labels the testbeds carry. The decisive downstream test is selective sub-concept UNLEARNING: at
  MATCHED forget-quality (next-token KL on held-out FORGET windows, matched_target = 0.8*min(maxKG,maxSUB)), it compares KG-ABL
  (ablate one KG-named absorber, h -= lambda*z_l*W_dec[l], gated by the latent's own sparse firing) against the DECISIVE DENSE-SUB-ABL
  (erase u_sub) and a clearly-labeled SECONDARY DENSE-WHOLE-ABL (erase the whole-parent diff-of-means), plus RAND and (M7)
  KG-ABL-UNIT. The joint (retain-utility x fluency) outcome is scored by an AxBench-style OpenRouter judge (anthropic/claude-haiku-4.5)
  with paired-bootstrap KG-vs-SUB CIs (B=10000), curve-dominance, and model-internal corroboration (continuation PPL + retain
  next-token KL). Per-case FORK verdict: KG_BEATS_USUB (joint CI excl 0 favoring KG AND a 2nd-family judge CI also excl 0),
  KG_MATCHES_USUB_LABEL_FREE (CI includes 0 - KG matches u_sub WITHOUT needing the labels), or KG_LOSES_TO_USUB. RESULTS (full
  run, both judges, $0.53/1459 calls): GATE PASSED. The two ABSORPTION cases are both KG_BEATS_USUB - taxonomic Georgia(16009)
  and first_letter large(8463) - each with u_sub localizing better than whole-parent and the M7 win tracing to the SINGLE
  discovered absorber (the multi-member K-track unit only adds collateral); human-proxy spot-checks pass. Folded-in modules:
  (M1') u_sub localization validation is CURVE-BASED over the achievable dense forget range (the KG-pinned matched point is
  tiny because KG single-latent next-token KL has a small ceiling, so a single-point check is mis-specified) - this DELETES
  the false 'a single dense hyperplane cannot localize' framing and reframes KG's edge as sparse-firing GATING (token footprint
  -> 0 for absorption), NOT the dense direction failing to localize; (M5) United States(846) is a ROUTER FALSE-NEGATIVE reclassified
  to co-firing - its absorber footprint is low/surgical-looking but the small parent recall-hole (0.197) flags co-firing,
  so it is moved out of the absorption gate; (M6) a second different-family judge (openai/gpt-4o-mini) with Cohen kappa +
  Pearson/Spearman utility correlation keeps a KG win only if its CI also excludes 0, plus a deterministic $0 human-proxy
  check that KG-ABL preserves sibling tokens while DENSE-WHOLE corrupts them; (M7) unit-vs-single ablation. Toxicity_insult
  is the co-firing case where KG is NOT surgical (footprint 0.166, firing-Jaccard 0.882, no recall-hole - the regime mechanism
  holds); it registers KG_BEATS_USUB on the LLM-judge joint but the $0 model-internal joint does NOT corroborate it (CI includes
  0) and u_sub itself fails to localize in co-firing, so it is reported as a weak judge-only edge, not a surgical win, and
  is not counted toward the gate. A per-case mi_corroborates_fork flag is reported (Georgia/US True; large/toxicity False
  - the noisier model-internal proxy is inconclusive there even though both LLM judges agree). Reuses the iter-4/iter-5 Gemma-Scope
  L12/16k JumpReLU engine via core.py (only the multi-latent abl_latent generalization for M7 + WORK repoint). Single GPU
  (NVIDIA L4); $0 model-internal, <$2 LLM judges (hard cap $10). All outputs validate against exp_gen_sol_out: unlearn_per_prompt
  (per (case,role,prompt) with predict_kg_abl / predict_dense_sub_abl / predict_dense_whole_abl / predict_rand / predict_noop
  continuations + both judges' utilities) and kg_vs_dense_per_case (fork verdicts + all decisive CIs).
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_6/gen_art/gen_art_experiment_1
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 31 ---
id: art_yAQgbq5Wgymx
type: experiment
title: >-
  Safety-Attribute SAE Absorption Screen + Sub-Context Dense-Direction Unlearning Test
summary: |-
  M2' answers whether the feature-absorption signature that makes one KG-named SAE latent a SURGICAL unlearning handle (established for the entity homograph Georgia->16009 and first-letter spelling) extends to SAFETY-RELEVANT identity attributes. Two parts, both reusing iter-5 core.py VERBATIM (JumpReLU Gemma-Scope L12/16k SAE d_model=2304, edit hooks, behavioral_curve, paired_bootstrap_diff, _scale_for_on_target) on a single L4 GPU.

  (1) $0 ABSORPTION SCREEN (always emitted). For 4 identity hierarchies (religion / race_ethnicity / orientation_gender / nationality) we build candidate slices INLINE from the FULL google/civil_comments (1.76M rows, CC0) gazetteer-matched windows + deterministic content-flip templates; group labels are surface-form only (never the model, never Jigsaw identity columns). Per hierarchy we find a firing-floor-validated content-responsive PARENT latent and screen every group for the Georgia signature via a vectorised K-track-lite absorber search (firing-disjoint Jaccard<0.1 + hole-covering + precision>=0.7), flagging absorption_structured = recall-hole>0.5 AND Jaccard<0.1 AND >=150 eligible AND precision>=0.7 AND hole-coverage-gain>=0.05 (CI excl 0). Each flagged edge is corroborated by a NON-CIRCULAR form-free absorption-fraction oracle (SAEBench/Chanin-A.13: decoder contribution projected onto a parent LR-probe direction trained on disjoint data; never used to flag).

  HEADLINE FINDING: safety-attribute SAE absorption is HOMOGRAPH-CONFINED. Of 44 eligible safety groups, only 2 are absorption-structured -- white (race; hole .63, Jaccard .019, oracle .46) and straight (orientation; hole .72, Jaccard .009, oracle .26) -- and BOTH are lexical homographs. The other 42 (Muslim/Hindu/Catholic, gay/lesbian/Asian, Mexican/Chinese/Canadian, ...) show NO parent recall-hole: the general identity parent reliably fires on them. Absorption tracks LEXICAL POLYSEMY (like Georgia/Jordan), NOT safety semantics. Positive control reproduces: Georgia recall-hole .76 (flagged), Jordan .66.

  (2) CONDITIONAL DOWNSTREAM (M1', $0.30 of $10 cap). At MATCHED forget-quality, ablating one KG absorber (KG-ABL) vs erasing the SUB-CONTEXT-targeted dense direction u_sub=diff-of-means(target-group, SIBLING-group) -- a sharper comparator than the whole-parent direction iter-5 M1 already beat -- scored on a joint retain-utility x fluency outcome with TWO judges (claude-haiku-4.5 + gemini-2.5-flash), paired-bootstrap Delta_joint CI B=10000, plus a $0 model-internal selectivity/curve-dominance track. overall_verdict = SAFETY_ABSORPTION_FOUND_NO_WIN: the single-absorber surgical win is DECISIVE for the entity homograph Georgia (DOWNSTREAM_WIN_CONFIRMED: retain-collateral KL 3e-5 vs u_sub .078, curve-dominance 1.0, Delta_joint [.53,.96] under BOTH judges) but does NOT robustly transfer to safety -- straight wins under the PRIMARY judge only (small-magnitude matched-forget .0012; second judge borderline, CI incl 0), and white has NO_ON_TARGET_EFFECT (its oracle-confirmed absorber gives no unlearning leverage). Structure != leverage.

  DELIVERABLES: method.py (driver), safety.py (gazetteers, identify_parent, screen_subcontexts, absorption_fraction_oracle), core.py (iter-5 verbatim), prefetch.py, finalize.py, README.md, pyproject.toml (48 pinned deps). method_out.json validates against exp_gen_sol_out: dataset safety_screen (one row per (hierarchy,group), predict_absorption in {ABSORPTION_STRUCTURED, CO_FIRING, NO_HOLE, DESCRIPTIVE_ONLY}, metadata_is_homograph + metadata_absorption_fraction_oracle) and downstream_subcontext (per (candidate,prompt) KG/u_sub/NOOP continuations + per-candidate summary rows). metadata carries overall_verdict, scoping_summary (homograph-confinement), positive_control_reproduced, screens, per_candidate_downstream, honest_negatives, llm_cost_usd. All honest negatives reported verbatim (homograph confinement, straight judge-fragility, white no-leverage, Jordan weak case). Gating reconstruction cosine 0.919.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_6/gen_art/gen_art_experiment_2
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 32 ---
id: art_KNPsfjByyxiS
type: dataset
title: >-
  Safety Identity SAE Absorption Testbed: nationality/religion/ethnicity/named-entity
summary: >-
  Four-hierarchy SAFETY-RELEVANT identity feature-absorption testbed, a strict structural drop-in of the iter-1 taxonomic
  testbed (gen_art_dataset_2) and the iter-5 homograph testbed, so the downstream K-track set-cover + form-free Chanin absorption
  diagnostic + recall-hole router pipeline runs UNCHANGED. exp_sel_data_out format: top-level {metadata, datasets:[{dataset,
  examples}]}; output is the PARENT binary label (positive=parent identity concept present at the target token, negative=absent);
  all per-row metadata flattened to metadata_<key>. FOUR datasets (36,448 examples): nationality_absorption (14,028), religion_absorption
  (6,055), ethnicity_identity_absorption (7,777), named_entity_safety (8,588). Each hierarchy has the same THREE coordinated
  components as dataset_2: (A) content-flip minimal pairs (x_on/x_off), (B) surface-flip pairs (surface_a/surface_b) for the
  surface-invariance admission, (C) a FROZEN diagnostic corpus of REAL Pile-uncopyrighted windows (pinned rev 3be90335...)
  labelled PURELY by surface form/gazetteer + per-token high-precision INCLUDE/EXCLUDE disambiguators, with a matched hard-negative
  family (other_group, non_identity, homograph_distractor=same token in its competing non-identity sense, easy). Labels are
  MODEL-INDEPENDENT and NON-CIRCULAR, so the corpus equally supports the honest 'no safety attribute is absorption-structured'
  null and a positive finding (degenerate-construction guard preserved). 56 sub-contexts reach >=150 diagnostic-fold positives
  = 'eligible' in the absorption_readiness manifest (far exceeding the >=4 target), including homograph-sense identity tokens
  Black/White/Asian/Native/Polish/Turkish/Indian/Apple/Amazon/Bush/Cook/King most likely to be absorption-structured. Target
  tokens anchored in the real google/gemma-2-2b vocab with precomputed metadata_target_token_indices via offset_mapping (add_special_tokens=False;
  token_indices_present=True; multi_token flagged). Sources: 35,430 pile_uncopyrighted + 922 templated + 96 llm_generated.
  LLM augment (openai/gpt-4o-mini) + independent judge (anthropic/claude-haiku-4.5, sense_correct rubric): pair pass 0.55;
  corpus sense precision nationality 0.935 / religion 1.0 / ethnicity 0.909 / named_entity 0.672; total spend $0.13 (under
  $3 target, $10 cap). Frozen folds (seed 20240617): pairs 70/30 by pair_id stratified by sub_context, corpus 50/50 by doc
  — the diagnostic fold is where iter-6 runs the form-free parent-hole search. Cross-hierarchy collisions documented (Jewish=ethnicity
  canonical, Indian/Arab notes). Validates PASSED against exp_sel_data_out; full=61MB, mini/preview ~20KB, all <100MB. Stamped
  NEXT-ITERATION (M2') building block — NOT consumed by this iteration's parallel experiments. Deliverables: data.py, build_dataset.py,
  pipeline.py, schema.json, manifest.json (counts/folds/sources/pass-rates/cost/absorption_readiness), pyproject.toml, full/mini/preview_data_out.json.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_6/gen_art/gen_art_dataset_1
out_expected_files:
- data.py
- full_data_out.json
- preview_data_out.json
- mini_data_out.json

--- Item 33 ---
id: art_F_-HUhl0NR_i
type: experiment
title: 'M4 Recall-Hole Router: Homograph Prospective Expansion + M7 Absorption Breadth'
summary: |-
  Executes M4 + M7 on the homograph/polysemy entity testbed (art_2xQn686KUmV5), reusing the iter-5 a-priori SAE firing-structure router VERBATIM as core.py and adding a thin method.py (homograph hierarchy loader + per-entity predict-then-measure router + Wilson-CI verdict + breadth count). SAE = google/gemma-scope-2b-pt-res L12/16k JumpReLU on unsloth/gemma-2-2b; SEED=1234; single GPU (NVIDIA L4); $0 LLM. The homograph dataset shipped builder-only (no full_data_out.json), so it was deterministically rebuilt in homograph_build/ (pipeline.py --scale full --no-llm, 34,357 rows, $0).

  INTEGRITY: the FROZEN recall-hole-alone rule, fit ONLY on the 12 derivation concepts (spelling L/O/T/I/D, numeric, taxonomic, 5 toxicity sub-attrs), reproduces iter-5 EXACTLY: tau_h_alone=0.7795 (drift 0.0000), derivation balanced_acc=1.000, LOO=0.833, gating recon-cos=0.927. Every entity regime is PREDICTED and LOGGED before its outcome is measured (predict-then-measure audit trail). Ground-truth regime PRIMARY = sign(auc_unit - auc_a); baselines (a) best raw latent, (h) supervised attribution pool, (d) non-SAE residual probe are reported per entity.

  M4 VERDICT = ROUTER_DEMOTED (honest negative). 34 eligible entities (>=150 diagnostic positives: city 18 / month 12 / given-name 3 / brand 1) — a 5.6x expansion of the iter-5 6-concept set. The router validates on the base-rate co-firing direction (co-firing-predicted 29/30, Wilson95 [0.833,0.994] excludes 0.5) but the DISCRIMINATIVE absorption-predicted stratum does NOT: homograph 2/4 [0.15,0.85]; homograph+7-spelling-letters 5/10 [0.237,0.763] — both include 0.5. So as an a-priori predictor of WHERE label-free grouping helps it is an exploratory diagnostic, not validated. This is the acceptable/publishable negative the plan anticipated and matches the iter-6 consolidation memo's M4 DEMOTE.

  M7 BREADTH (answers the 'absorption is n=1-2' critique with a systematic count): of 64 homograph entities with a stable estimate (n_all>=30), only 3 are absorption-structured (recall-hole>0.5 AND firing-Jaccard<0.1) — ALL months (cities 0/22, given-names 0/20, brands 0/10). NEW named suppressed-parent homographs (beyond Georgia/Jordan, which live in the taxonomic derivation set): March (recall-hole 0.997), June (0.947), February (0.573). The month parent fires on only 0.623 of month mentions vs 0.94/0.92/0.95 for city/given-name/brand, so only months leave holes. STRUCTURAL != DOWNSTREAM: the strongest downstream-confirmed absorption (label-free unit actually beats best raw latent) is month/May, delta_vs_a=+0.160 (the is-a-month parent misses 98% of 'May' mentions, absorbed by the modal verb), even though May is NOT 'structured' (jaccard 0.434); the structurally-shaped months are co-firing downstream. Documented counterexamples re-confirmed: numeric (high Jaccard yet absorption), taxonomic (low Jaccard yet co-firing), spelling F/M/W (recall-hole~1.0 over-predicts absorption).

  DELIVERABLES: method_out.json (+ full/mini/preview, all validate against exp_gen_sol_out, each <0.4MB) with 111 cards (12 derivation + 7 spelling-prospective + 92 homograph entities), each card = {input: router-decision string, output: ground_truth_regime, predict_router: predicted_regime, metadata_*: recall_hole, jaccard, predicted/ground-truth regimes, auc_unit/a/h/d, deltas+CIs, eligibility, absorption_structured, is_prospective_hit}. Rich metadata: frozen_rule, reproduction_check, router_verdict(+rationale), all prospective hitrate strata (primary/combined-with-spelling/ablations/vs-h) with Wilson CIs, absorption_breadth (per-hierarchy + new-suppressed + downstream-confirmed), hierarchy_parents, entity_table, honest_notes. NOTE: two surgical numerical-stability patches over core (NaN/inf-safe residual probe and auc — Gemma massive-activation residual dims overflow float16) and B_BOOT=2000 (plan allows >=2000; CI-width only, point estimates/tau unaffected); core.py stays verbatim. For GEN_PAPER_TEXT: this gives an honest validate-or-demote result + a breadth count that directly rebuts the single-slice critique and names new homograph cases (May the downstream winner).
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_6/gen_art/gen_art_experiment_3
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 34 ---
id: art_w7p8du2N1f0Y
type: evaluation
title: >-
  Integrity-Lock Eval: 65k Selectivity Fix, Router Wilson-CI, Honest-Counting Drop-in
summary: |-
  Pure CPU-only ($0, no GPU/encoding/LLM) integrity-lock re-analysis (eval.py) over four frozen JSONs (D1 iter5-exp2 65k cross-dict, D2 iter4-exp2 surgical 16k, D3 iter5-exp3 router, D4 iter5-eval template). Every headline value is COMPUTED then COMPARED to source; mismatches are reported with notes (44 cross-checks, 43 pass; the one mismatch is the intentional honest correction m3_n_floor_limited=2 vs the plan's anchor of 1). Labels mapped by CONTENT, not by D4's differing internal label numbers.

  M3 (NEW, load-bearing): the stored 65k 'absorption mean selectivity 466996.718x' and 'Georgia 3.7e6x' are divide-by-epsilon artifacts (kg_collateral==0 -> ratio=on_target/1e-8; recomputed mean reproduces 466996.718 exactly, confirming the artifact). Excluding floor-limited (kg_coll==0: Georgia/46143, Jordan/60904) and NO_ON_TARGET_EFFECT (60904, on/54546, take/26458) cases, the CORRECTED 65k absorption mean = 721.72x / median 676.33x (n=4 PRIMARY); the lenient rule that excludes only the two artifacts gives 483.06x / 184.61x (n=6 SECONDARY). 65k Georgia (on_target 0.03711 = dense_collateral; floor-limited >= ~371x at 1e-4, or >= ~1290x referenced to the 16k 2.876e-5 collateral) is COMPARABLY surgical to 16k Georgia (1722.46x), NOT ~2000x better. Honest layer-9 note: Georgia loses its hole (0.003) while Jordan keeps it (0.536) with a 2376x surgical edit.

  M4 (NEW): prospective Wilson CIs INCLUDE 0.5 -> absorption-predicted 3/6=0.50 [0.188,0.812], cofiring 8/12=0.667 [0.391,0.862], combined 11/18=0.611 [0.386,0.797]; the vs-h 14/19=0.737 [0.512,0.882] (excludes 0.5) is flagged SECONDARY/non-primary (unit-beats-h ground truth). recall-hole=1.0 over-predicts absorption on new letters F/M/W (which measure co-firing); C/P/R are correct wins -> router is WRONG IN BOTH DIRECTIONS. Run-tree scan found no iter-6 expansion experiment with a CI excluding 0.5 -> DEMOTE to exploratory diagnostic (derivation balanced-acc 1.0, tau_h_alone 0.77949 kept separate).

  M8 (carry D4, RE-VERIFY selectivity from D2): 22 distinct holes = 30 FDR survivors - 6 double-counts - 2 non-hole; per-family distinct 13/3/6, survive-FDR 14/6/10; absorption-6 mean 1452.47x / median 1262.21x (the draft's '1452 median' is the MEAN); surgical-5 median 1722.46x; within-taxonomic Spearman rho=0.90 (NOT 1.0, p 0.037), cross-family counterexample (large prec 0.571 -> 802x beats US-4760 prec 0.709 -> 7.8x); random SINGLE-latent control 28/28 > p95, 23/28 > p99; member-labeling gap 0.6344 [0.545,0.724]; numeric flagged below-gate (digit cosine 0.876 < 0.90). M5: US = CO-FIRING (aggregate recall-hole 0.20-0.23 < tau_h 0.78) yet absorber 846 = 214x surgical -> router FALSE-NEGATIVE (jaccard 0.04 specific vs 0.20 aggregate). M7: two-track = TRAINING-FREE LABEL-FREE DISCOVERY of the single absorber (16009/8463/846), not multi-member grouping; C-track ties weak baselines (toxicity 0.762 vs 0.765); set-cover-specific only on I/D/Georgia.

  Output eval_out.json (exp_eval_sol_out schema, all variants validate, <100MB): metadata blocks M3_selectivity_artifact / M4_router_ci / M8_honest_counting / M5_us_consistency / M7_grouping_reframe / cross_checks, a flat numeric metrics_agg (62 scalars incl. all corrected means, includes_half flags, n_cross_checks/pass), and 5 datasets (M3_selectivity_cases 16, M4_router_prospective_strata 4, M4_new_letter_directionality 7, M8_distinct_hole_survivors 30 reused from D4, M8_selectivity_reverify 7), each example carrying predict_* strings. Provides GEN_PAPER_TEXT with trustworthy, cross-checked drop-in paper_wording for the cross-dictionary and auditability spines.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_6/gen_art/gen_art_evaluation_1
out_expected_files:
- eval.py
- full_eval_out.json
- mini_eval_out.json
- preview_eval_out.json

--- Item 35 ---
id: art_3zaa2xXEp8Az
type: research
title: 'CCRG iter-6: Safety-Identity Absorption & u_sub Label-Efficiency Positioning'
summary: >-
  Positions the two new load-bearing iter-6 gates of the Counterfactual Co-Response Grouping (CCRG) paper and refreshes the
  venue-locked citation set for GEN_PAPER_TEXT. Pure web research, $0 LLM spend, no code; builds on iter-4 (art_QBxBPF-9Ldxe)
  and iter-5 (art_y_5u-bfJOq3V) without re-doing settled entries. THREE deliverables. (A) M2' SAFETY-RELEVANT IDENTITY ABSORPTION:
  a cite-and-distinguish block over FIVE sub-literatures never previously surveyed -- SAE debiasing (debiaSAE 2410.13146 VLM/COLM-under-review;
  Ahsan&Wallace 2511.00177 ICLR2026 healthcare; SteerRM 2603.12795 reward-model; DeBiasLens 2602.24014 VLM/CVPR2026-flag),
  model-editing for stereotype (BiasEdit 2503.08588 TrustNLP@NAACL2025; Collapsed-LMs 2410.04472 ICLR2025), fairness/concept-erasure
  editing (Karvonen&Marks 2506.10922 NeurIPS2025 Mech-Interp-WS affine edit; SPLINCE 2506.10703 NeurIPS2025; H-SAL 2606.12088),
  identity/entity/PII unlearning (Entity-Level-Unlearning COLING2025; Not-Every-Token 2506.00876; DFSU 2601.15595), and example-reweighting
  debiasing (JTT/GEORGE/EIIL/LfF, carried). VERDICT: CCRG's three-part conjunction -- a DISCOVERED single absorber latent
  for ONE identity sub-context + a PARENT-preserving sub-context edit + scoring vs a SUB-CONTEXT-targeted dense direction
  u_sub -- is distinct from all five (each edits a WHOLE attribute/entity/example-set and preserves UNRELATED material; closest
  near-miss Ahsan&Wallace steers a single race-latent that CO-FIRES with 'incarceration' = entanglement not absorption, and
  concedes SAE steering is 'of marginal utility for realistic tasks'). Both-branches honest-null framing supplied (safety-WIN
  vs absorption-not-exhibited NULL bounded to the auditable edit primitive, connected to the existing 0/28-professions + toxicity-co-firing
  negatives). (B) M1' u_sub LABEL-EFFICIENCY: RETIRES the now-FALSE 'a single dense hyperplane structurally cannot localize
  to a sub-context / erasing the is-a-country direction removes all countries' argument -- u_sub IS a dense hyperplane and
  DOES localize, the testbed already carries its labels, and SPLINCE (preserves covariance with target label), Karvonen&Marks
  (affine edit, bias <2.5%, perf maintained) and H-SAL (label-free matches label-based) externally prove a labeled dense direction
  localizes/preserves utility. Supplies an exact DELETE/REPLACE list + BOTH M1' fork paragraphs (FORK-WIN: discovered single
  feature beats sub-context-labeled dense; FORK-MATCH: matches u_sub WITHOUT sub-context labels = label-efficiency/discovery,
  grounded in Peng 'Discover-not-Act' 2506.23845 verbatim thesis + label-free SAE 2506.01247) + an honest cost note (counterfactual-pair
  cost of grouping vs sub-context-label cost of u_sub). (C) CITATION REFRESH: 14 new grep-verified entries + carry-forward
  flags RESOLVED (Deng 2506.18141 UPGRADE->ACL2026; SAEmnesia 2509.21379 UPGRADE->ICML2026; SNCE 2509.21008 authors confirmed;
  Muchane 2506.01197 keep-preprint), BibTeX, corrections diff, unresolved-flags list, and an updated presentation-strip checklist.
  Outputs research_out.json + research_report.md (sections A-D).
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_6/gen_art/gen_art_research_1
out_expected_files:
- research_out.json
</supplementary_materials>

<previous_review>
Your review from the previous iteration. Check which critiques have been addressed
in the revised paper. Do NOT re-raise critiques that have been adequately fixed.
Only re-raise if the fix is insufficient.

- [MAJOR] (rigor) The headline downstream win compares KG-ABL only against a WHOLE-PARENT dense erasure. I verified in the code (core.py ParentProbe fits diff-of-means on parent-positive vs negatives; method.py lines 454 and 535 set fit_pos = all-countries / all-L-words, fit_neg = non-country / non-L) that the dense direction u is the country-vs-non-country (or L-vs-not-L) direction. The paper's load-bearing structural argument—'a single dense hyperplane structurally cannot localize to a sub-context' (§related) and 'erasing the is-a-country direction removes all countries' (§unlearn)—is false: a diff-of-means computed on Georgia-in-country-contexts vs other-countries-in-country-contexts (or large vs other L-words) is also a single dense hyperplane, and it localizes to the sub-context. The testbed carries the per-sub-context labels needed to build it (the same labels used to define the forget/retain/sibling eval sets). Worse, the matched-forget protocol cranks beta until the whole-parent direction forgets the target token, which by construction nukes sibling countries—so high collateral for the dense baseline is guaranteed, making the win near-tautological. As stated, 'the first demonstration that a discovered single SAE feature beats a dense baseline on a sub-concept removal task' is not established; only 'beats whole-parent erasure' is.
  Action: Add a sub-context-targeted dense baseline: u_sub = diff-of-means(target-sub-context-positive, sibling-positive), erased via the same h <- h - beta(h.u_sub)u_sub operator, swept to matched forget-quality, and scored with the identical judge. Report the joint outcome KG vs this stronger dense baseline. If KG still wins, the contribution is dramatically stronger; if not, reframe the result as 'KG-ABL matches a sub-context dense direction without needing sub-context labels' (a discovery/label-efficiency claim) and drop the false 'structurally cannot localize' argument.
- [MAJOR] (scope) Demonstrated significance against the stated goal remains the ceiling. The goal asks for cluster-level units that are more reliable on concrete downstream tasks (safety-relevant classification, steering with side-effects, model-diffing). The paper itself concedes: (i) no SAE unit out-classifies a dense probe on ANY task; (ii) the two confirmed downstream wins are on 'Georgia is a country' and the spelling of 'large'—neither safety-relevant, and the latter against an erasure that corrupts all L-tokens; (iii) toxicity, the only safety-relevant family, is a predicted LOSS; (iv) set-cover-SPECIFIC selection is established on only 3 slices (Georgia, first-letter I, D); (v) the prospective router is at chance. So the practical reliability gain is delivered as auditability/localization on a narrow homograph phenomenon (effectively Georgia + descriptive Jordan on one model), not as task performance. This is an honest, careful, but narrow empirical contribution for an ICLR-primary target.
  Action: Land one downstream win on a safety-relevant, absorption-structured sub-context (the authors note toxicity sub-attributes are not absorption-structured; search for an attribute whose sub-contexts ARE suppressed-parent, e.g. a specific identity/dialect token, a named-entity safety case). Even a single such win, against the stronger dense baseline from critique 1, would convert 'a capability a probe lacks' into 'a better outcome on a task that matters' and is the largest available score lever.
- [MINOR] (evidence) The cross-dictionary 'Georgia surgical edit reproduces at a far higher selectivity (3.7×10^6)' is a divide-by-epsilon artifact. I confirmed in experiment_2/full_method_out.json that absorber 46143 has kg_collateral = 0.0 exactly, so selectivity_ratio = on_target / max(kg_collateral, EPS) = on_target / 1e-8 ≈ 3.71e6. The number is determined by the EPS floor, not by a more surgical edit; at 16k the same Georgia edit has kg_collateral 2.9e-5 giving 1722×. Presenting 65k as 'far higher selectivity' implies the wider dictionary is meaningfully more surgical when in fact collateral merely rounded below numerical precision. The regime-split 'absorption_mean_selectivity 466997' is likewise dominated by this artifact and by a NO_ON_TARGET_EFFECT case (absorber 60904, 22486×).
  Action: Report floor-limited cases as 'KG collateral < numerical precision; selectivity floor-limited (>= X)' and exclude NO_ON_TARGET_EFFECT and floor-limited cases from any mean/median selectivity. State that 16k and 65k Georgia edits both have collateral at/below numerical precision, so the dictionaries are comparably surgical rather than one being 2000× better.
- [MINOR] (rigor) The a-priori router—listed as a contribution—is not validated out-of-sample. I confirmed experiment_3: prospective absorption-predicted hit-rate is 3/6 = 0.50 (exactly chance, Wilson CI [0.19,0.81]); combined 11/18 with Wilson CI [0.386,0.797], which includes 0.5. The recommended single signal (recall-hole) fired at 1.0 on new letters F/M/W that measured co-firing (false-absorption misses). So on the only genuinely prospective absorption test, the recall-hole router is no better than a coin flip, and the derivation balanced-accuracy of 1.0 is on the fitting set. The paper frames this as 'a screening heuristic with measured error', which is honest, but it should not be presented as an established a-priori predictor.
  Action: State explicitly that the prospective CI includes chance and that recall-hole=1.0 over-predicts absorption on new spelling letters. Either demote the router to 'exploratory diagnostic, not yet validated' or expand the prospective set substantially (the homograph entity testbed of 23 cities / 12 months / 34 names / 24 brands is built but unused) to obtain a CI that excludes 0.5.
- [MINOR] (clarity) United States is internally inconsistent. In §unlearn (Table 2) it is regime='absorption' with a PARTIAL win; I confirmed its artifact values are firing-Jaccard 0.040 but parent recall-hole 0.197. In §selection the paper states 'United States is co-firing/splitting (firing-Jaccard 0.20, hole 0.23), not absorption', and the homograph cross-tab requires hole>0.5 for absorption-type. US (hole 0.197/0.23) fails that threshold, and the recommended router (predict absorption iff hole>0.78) would classify US as CO-FIRING. Yet US is used as one of the 3 'absorption' unlearning cases and gives a KG partial-win—which, if anything, is evidence that the router's regime claim ('co-firing -> dense wins, do not use CCRG') is wrong for US. The reader cannot tell whether US is absorption or co-firing.
  Action: Pick one classification for US and apply it consistently. If US is co-firing (per its hole and the router), move its unlearning result out of the 'absorption regime' set and use it as a case where CCRG helps even though the router predicted co-firing (and discuss why). If it is absorption, reconcile with §selection and the router threshold. Either way, explain the firing-Jaccard discrepancy (0.04 for absorber 846 vs 0.20 aggregate).
- [MINOR] (evidence) The headline joint-outcome statistic rests entirely on a single LLM judge (claude-haiku-4.5, temp 0), with small per-case n (joint CIs over 48-56 judged prompts) and no human validation or second-judge agreement on the unlearning continuations. Given that the win is the paper's centerpiece and the judge defines utility = harmonic_mean(fluency, content_pres), the result's robustness to judge choice is unestablished. (The model-internal KL/PPL corroboration is reported, but it disagrees with the judge on toxicity, where it leans KG 'UNEXPECTED_WIN'.)
  Action: Re-score a stratified sample of continuations with a second, different-family judge (e.g. a GPT- or Gemini-class model) and report inter-judge agreement, and/or a small human spot-check on the Georgia and large cases. Confirm the Δ_joint CIs still exclude 0 under the second judge.
- [MINOR] (novelty) The two-track algorithm is given top billing but is largely inert in the load-bearing results. The C-track ties weak baselines on the only family it is tested on (toxicity, AUC 0.762 vs (a) 0.765) and is described as 'secondary' even in the artifacts. Set-cover-specific selection (beating non-random label-free selectors) holds on only I, D, and Georgia; on L/O/T the strong S-rec matches the unit. The downstream wins and surgical edits trace to individual discovered absorber latents (16009, 8463, 846), not to multi-member grouping. So the prominence of 'a two-track grouping algorithm' as a contribution exceeds what the experiments show the grouping adds over 'identify the anchor's recall hole and pick the precise specialist that covers it'.
  Action: Either provide an ablation isolating the grouping machinery's marginal value (unit vs single-best-absorber on the downstream/auditability tasks) to justify the algorithmic framing, or re-balance the narrative so the algorithm is positioned as the discovery procedure for single absorbers rather than as multi-member units delivering the wins.
</previous_review>

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

### [2] HUMAN-USER prompt · 2026-06-18 07:37:25 UTC

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
