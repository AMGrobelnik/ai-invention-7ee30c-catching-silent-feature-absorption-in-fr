# review_paper — test_idea

> Phase: `invention_loop` · round 2 · `review_paper`
> Run: `run__C1-INh1YNGn` — Catching Silent Feature Absorption in Frozen Sparse Autoencoders: Label-Free Loc
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `review_paper` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-06-17 17:48:29 UTC

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

Sparse autoencoders (SAEs) decompose the activations of large language models (LLMs) into a dictionary of sparsely-activating latents intended to be interpretable, monosemantic units of analysis \citep{Cunningham2023, Bricken2023, Templeton2024}. The promise is operational: a latent that reliably tracks a human concept can be read off as a classifier, flipped as a steering knob, or compared across model variants for model-diffing. Public SAE suites such as Gemma Scope \citep{Lieberum2024} expose millions of such latents over open models, making this a practical interface for safety-relevant interpretability.

This promise is undercut by a now well-documented fact: \emph{single SAE latents are not reliable units} \citep{Leask2025}. Two failure modes recur. \emph{Feature splitting} fragments one concept across many latents, so no single latent captures it. \emph{Feature absorption} is more insidious: a more specific child latent suppresses the firing of a more general parent latent, leaving the parent with unpredictable holes on exactly the sub-contexts the child covers; parent and child are \emph{mutually exclusive in firing} \citep{Chanin2024}. (A related failure, \emph{feature hedging}, merges correlated features into one polysemantic latent in narrow SAEs \citep{Chanin2025}; a hedged latent is not groupable and is out of scope.) On concrete downstream tasks the practical cost is stark: difference-of-means probes are the strongest concept detectors and raw-latent SAE methods are uncompetitive \citep{Wu2025}, while standardized suites quantify absorption, sparse-probing, and targeted erasure \citep{Karvonen2025}. Any method that proposes SAE latents as a knowledge representation must therefore clear strong, simple baselines and address splitting and absorption head-on.

The task is hard because the obstacles defeat the obvious instruments \emph{by construction}. The intuitive fix for an unreliable single latent is to group several latents into a cluster-level unit. But every existing post-hoc grouping signal is \emph{observational}: which latents fire together (co-activation feature families \citep{ONeill2024, Deng2025}) or which decoder directions point alike (geometry). Absorption is precisely the regime where observational signals must fail---the parent and the absorbing child are mutually exclusive in firing, so co-activation can never group them, and their decoders need not be cosine-similar \citep{Chanin2024}. The standard \emph{supervised} remedy, selecting the top-$N$ latents by causal effect on a concept probe (SCR/TPP attribution \citep{Karvonen2024, Marks2024}), is no better: a latent that fires only in a narrow sub-context has low \emph{marginal} attribution and is silently dropped, even though it carries the concept there. The latents one most needs are exactly the ones these instruments discard.

Why has this not been solved post-hoc? Recent architectural remedies---Matryoshka SAEs \citep{Bussmann2025}, hierarchical SAEs \citep{Muchane2025}, and subspace-aware SAEs \citep{Dalili2026}---all \emph{retrain} the SAE to reduce splitting and absorption at training time. They do not help a practitioner holding a frozen public SAE, and none produces a human-auditable multi-member unit over an existing dictionary. We take the opposite stance: a \emph{training-free, post-hoc repair of frozen public SAEs}. The methodological gap we fill is the \emph{grouping operator}. We observe that grouping by \emph{interventional co-response}---how latents jointly track a content counterfactual, rather than how they co-fire at baseline---is the matched instrument, with a direct precedent in systems biology, where differential co-expression methods (DiffCoEx \citep{Tesson2010}, WGCNA \citep{Zhang2005}) cluster genes by correlated response to a perturbation precisely because co-regulated genes are often not co-expressed at baseline. Crucially, correlation is the right operator only for the \emph{shared-support} splitting case. Absorbers respond on \emph{disjoint} supports and have low pairwise correlation, so no affinity-merging clustering can even \emph{propose} the right group. The disjoint-support case is a \emph{maximum-coverage} problem, whose classic greedy solution \citep{Nemhauser1978, Feige1998} is the natural---and, we argue, the only correct---proposer for absorption units.

We introduce \textbf{Two-Track Co-Response Grouping (CCRG)} and, unlike the previous iteration of this work, we \emph{execute} it on a frozen Gemma Scope SAE rather than pre-registering it. Three findings result. (1) On the first-letter spelling testbed---the regime where absorption is guaranteed to exist---the label-free unit is the best classifier on all five letters and recovers the parent plus per-token absorbers; this is the load-bearing positive. (2) Absorption \emph{generalizes} beyond spelling: the K-track recovers numeric and country absorbers that marginal-attribution pools drop. (3) Most informatively, we replace a prior label-based regime claim with a \emph{direct measurement of SAE-latent firing}, which reveals that toxicity is a co-firing (splitting) regime, not an absorption regime, so the set-cover track is unnecessary there and attribution selection wins. This firing-structure measurement is a cheap diagnostic that predicts, before any grouping, whether CCRG can help on a given concept---turning what could have been an over-claim into a falsifiable scope statement.

[FIGURE:fig1]

\paragraph{Summary of contributions.}
\begin{itemize}
\item \textbf{A two-track grouping algorithm} (\S\ref{sec:method}). A concrete, training-free procedure that proposes split families by content-response correlation (C-track) and absorption units by an anchored greedy set-cover (K-track), reconciles them, and filters them with a single null-anchored, multiplicity-controlled admission rule. To our knowledge, maximum-coverage set-cover has not previously been used to group SAE latents, and it is exactly the operator the disjoint-support absorption regime requires.
\item \textbf{An executed primary result on first-letter spelling} (\S\ref{sec:firstletter}). The label-free unit is the best starts-with-letter classifier on all five letters (AUC 0.86--0.96), beating the best raw latent, count-matched observational clusters, and a count-matched oracle-attribution pool; it recovers the diagnostic parent plus $\geq 2$ absorbers on 4/5 letters and beats the count-matched pool on absorbed-slice recall (paired-bootstrap CI excluding 0) on the two best-powered letters.
\item \textbf{Absorption generalizes beyond spelling} (\S\ref{sec:nonspelling}). On a novel non-spelling testbed the unit recovers a numeric (\texttt{integer}) and a country (\texttt{Georgia}) absorber that marginal-attribution pools drop at matched pool size, with near-zero false positives.
\item \textbf{A firing-structure test for when grouping helps} (\S\ref{sec:toxicity}). Measuring real SAE-latent firing on toxicity shows the regime is co-firing, not absorption, so CCRG does not help and attribution wins---an honest negative that doubles as an a-priori applicability test, replacing the previous label-based proxy.
\item \textbf{Four frozen testbeds and a single-GPU pipeline} (\S\ref{sec:setup}). 109{,}754 examples across spelling, a numeric/taxonomic absorption hierarchy, toxicity, and sentiment/aspect, with eleven baselines and honestly reported failure modes.
\end{itemize}

# Related Work
\label{sec:related}

\paragraph{SAEs and the unreliability of single latents.} Sparse dictionary learning on LLM activations yields interpretable features \citep{Cunningham2023, Bricken2023, Templeton2024, Lieberum2024}, but a growing body of work shows individual latents are not canonical units \citep{Leask2025}. \citet{Chanin2024} introduce and quantify \emph{feature absorption}---a specific child latent suppresses a general parent's firing---demonstrated on first-letter spelling, and \citet{Chanin2025} characterize \emph{hedging}. Dense-latent analyses confirm that single-latent semantics are unstable \citep{Sun2025}, and benchmarks make the practical cost concrete: AxBench finds difference-of-means strongest and raw-latent SAE methods uncompetitive \citep{Wu2025}; SAEBench standardizes absorption, sparse-probing, and erasure evaluations \citep{Karvonen2025}; and recent audits caution these benchmarks are imperfect ground truth \citep{Chanin2026}. We do not stake our load-bearing claim on out-classifying a strong dense probe; our central comparison is against SAE-\emph{selection} baselines.

\paragraph{Post-hoc grouping of SAE features.} Prior grouping is observational: co-activation ``feature families'' \citep{ONeill2024}, sparse feature coactivation modules \citep{Deng2025}, and decoder-geometry clusters group latents by what fires together or which decoders align. Closest to our output, \citet{Winnicki2026} build a knowledge graph from SAE features via co-occurrence and decoder geometry. Our edges differ in kind: they are \emph{interventional specialization edges} (an absorbed/split child of an anchor) over \emph{multi-member} co-response units, encoding conditioning environments invisible to co-occurrence, and we measure their utility rather than only displaying them. By construction, observational signals cannot group an absorbed parent and child, which are mutually exclusive in firing; we therefore count-match observational clusters to our unit's size so any win reflects \emph{selection}, not capacity.

\paragraph{Supervised latent selection.} SHIFT and the SCR/TPP family rank individual latents by causal effect on a concept probe and ablate the top-$N$ \citep{Marks2024, Karvonen2024}. A latent firing only in a narrow sub-context has low marginal attribution and is silently dropped---the exact gap our co-response set-cover fills. We use SCR/TPP-style ranking as our oracle-pool baselines.

\paragraph{Architectural remedies vs. our setting.} Matryoshka \citep{Bussmann2025}, hierarchical \citep{Muchane2025}, and subspace-aware \citep{Dalili2026} SAEs modify \emph{training} to reduce splitting/absorption. They are orthogonal to our setting: we repair a \emph{frozen} public SAE post-hoc and emit an auditable graph rather than retraining a dictionary.

\paragraph{Cross-field instruments and robustness.} The C-track imports differential co-expression module discovery \citep{Tesson2010, Zhang2005} and Leiden community detection \citep{Traag2018}; the K-track imports the maximum-coverage / set-cover greedy with its $(1-1/e)$ guarantee \citep{Nemhauser1978, Feige1998}. The supporting robustness framing engages label-free worst-group-robustness work---group-DRO \citep{Sagawa2019}, JTT \citep{Liu2021}, GEORGE \citep{Sohoni2020}, EIIL \citep{Creager2020}, LfF \citep{Nam2020}, group-aware priors \citep{Rudner2024}, and diverse prototypical ensembles \citep{To2025}---which infer groups over \emph{examples} and \emph{retrain}; CCRG instead groups \emph{features}, never retrains, and the recovered absorbers \emph{are} the inferred sub-context specialists. Surface-invariance draws on LEACE concept erasure \citep{Belrose2023} and counterfactual invariance \citep{Veitch2021}; minimal-pair supervision draws on counterfactually-augmented data \citep{Kaushik2019}, CEBaB \citep{Abraham2022}, and ParaDetox \citep{Logacheva2022}. The closest ``cluster counterfactual differences'' template is CDLC in vision \citep{Varshney2025}, which clusters diffusion-counterfactual difference vectors into one continuous direction per class; we cluster \emph{discrete} LLM SAE latents into multi-member units and add a set-cover track for which CDLC has no analogue.

# The Two-Track Co-Response Grouping Method
\label{sec:method}

\paragraph{Preliminaries.} Let the frozen SAE have latents $l \in \{1,\dots,L\}$ with encoder activation $a_l(x)$; a latent \emph{fires} on $x$ iff $a_l(x) > 0$ (Gemma Scope uses a JumpReLU, so the threshold is inside the encoder \citep{Lieberum2024}). For a concept $c$ we are given \emph{content-flip minimal pairs} $(x_{\text{off}}, x_{\text{on}})$ in which the concept is absent/present at matched surface form, plus \emph{surface-flip pairs} in which the concept is held constant and surface varies. The content labels are the supervision every matched baseline consumes; the method uses no absorption-specific oracle. We encode at one residual-stream site (\texttt{gemma-2-2b}, layer 12, width 16k canonical; hook \texttt{blocks.12.hook\_resid\_post}; $d_{\text{model}}=2304$, 16{,}384 latents) \citep{Lieberum2024}.

\paragraph{Step 1: interventional content-response.} For each latent $l$ and pair $p$, the \emph{content-response} is $r_l(p) = a_l(x_{\text{on}}) - a_l(x_{\text{off}})$. We retain \emph{content-responsive} latents whose response exceeds a within-concept shuffle null. A latent's \emph{cover set} $C_l$ is the set of pairs whose content flip it tracks reliably ($r_l(p)>\tau_{\text{resp}}$ and $a_l(x_{\text{on}})>0$) and precisely (firing-precision $\geq 0.7$ on its own support). Because absorbers fire on only a handful of words, a mean-over-pairs prefilter would discard them; eligibility is therefore \emph{cover-based} (selective \emph{and} covering $\geq 1$ sub-context), which retains the genuinely sparse absorbers.

\paragraph{Step 2: C-track --- correlation communities for splitting.} Where a concept \emph{splits}, sub-latents share firing support and co-respond positively, so pairwise affinity is appropriate. We build a sign-aware soft-thresholded affinity from the positive part of the Spearman correlation between response profiles, $A^{C}_{l,l'} = \max(\rho(r_l, r_{l'}), 0)^{\beta}$ with $\beta=6$ (WGCNA's scale-free criterion \citep{Zhang2005}), and run Leiden community detection (RBConfiguration partition \citep{Traag2018}). Resolution is fixed by bootstrap-ARI stability against a shuffle null. (In practice Leiden's C extension intermittently hangs on tied-rank graphs; we run it in a subprocess with a 45\,s timeout and fall back to agglomerative clustering, recorded per run.)

\paragraph{Step 3: K-track --- anchored greedy set-cover for absorption.} Absorbers respond on \emph{disjoint} supports and are mutually exclusive in firing with their parent, so their pairwise correlation is low and no affinity-merging clustering can propose them (Figure~\ref{fig:tracks}). We use a different operator: an anchored greedy maximum-coverage procedure. \textbf{(1) Anchor:} $l^\* = \arg\max_l |C_l|$, the highest-recall ``general/parent'' candidate, chosen using \emph{only} the pairs and \emph{not} the absorption diagnostic, with ties broken toward the broadest support. \textbf{(2) Holes:} $H = P \setminus C_{\text{anchor}}$, the pairs the parent goes silent on. \textbf{(3) Greedy cover:} while $H$ is non-empty and improving, add $\arg\max_l |C_l \cap H|$ subject to mutual exclusivity (firing-Jaccard $<0.1$ with members), per-member precision $\geq 0.7$, and a marginal-coverage-gain floor $\geq 0.05$ whose bootstrap CI excludes 0. The greedy max-coverage choice is the classic instrument for ``cover a universe with complementary specialists,'' with the $(1-1/e)$ guarantee \citep{Nemhauser1978, Feige1998}; coverage-complementarity is a set-level property, which is exactly why a pairwise operator cannot express it.

[FIGURE:fig2]

\paragraph{Step 4: reconciliation.} For each C-community we designate its highest-recall member as a candidate anchor and run Step 3 to pull in mutually-exclusive absorbers covering its holes; we also seed Step 3 from standalone high-recall latents in no dense community. A final unit is a pure C-community (splitting), a pure K-cover (absorption), or a hybrid; we de-duplicate by highest coverage gain.

\paragraph{Step 5: admission filter with multiplicity control.} A proposed unit is admitted iff it clears \textbf{signature C} (within-unit content-response correlation above the 95th-percentile shuffle null) \textbf{or signature K} (pooled-max minus best-single content-response AUC above the 95th percentile of a best-of-random-$k$ null \emph{matched on marginal AUC}, plus the $k\in\{2,3\}$ absolute gain floor of $0.05$ with bootstrap CI excluding 0, plus mutual exclusivity and the precision floor), \textbf{and} unit-level surface invariance (pooled surface-response not above the shuffled-surface null). Because many candidate units are tested per concept, we control multiplicity at the \emph{unit-proposal} level: a Bonferroni-within-unit $p$ over the disjunctive (C-or-K) signature, then Benjamini--Hochberg across the $M$ candidate units in a concept, and we report $M$ and the \emph{empirical} family-wise false-admit rate under the matched random-$k$ null---separate from the Holm--Bonferroni used across headline claims.

\paragraph{Proposal-step pilot.} Before any absorber-recovery claim relies on the K-track, a never-dropped pilot runs Step 3 on content-flip pairs \emph{alone} and checks that the proposed anchor and absorbers match the parent and absorbers the supervised diagnostic of \citet{Chanin2024} identifies (membership F1 above a random-membership null), and that the recall-argmax anchor actually coincides with the diagnostic parent (\emph{anchor fidelity}). A failure here is reported as a proposal-step failure, not silently omitted.

\paragraph{Non-circular diagnostic and auditable graph.} Specialization edges are \emph{scored}, never formed, by the absorption diagnostic of \citet{Chanin2024}. Because the strict form needs an output logit, we use the domain-agnostic \emph{form-free} variant (the appendix probe-projection, implemented in SAEBench as \texttt{absorption\_fraction}): $l$ absorbs iff $\tau_c < (\hat{a}_l \cdot d_p)/(a \cdot d_p)$, with $d_p$ a parent-concept probe trained on data \emph{disjoint} from clustering. The anchor is chosen by recall available to every baseline, so ``the unsupervised unit beats the supervised oracle'' is not undercut. Each admitted unit is emitted with logit-lens tokens and top conditioning contexts, plus directed anchor$\to$child specialization edges---a feature-level knowledge graph.

# Testbeds, Baselines, and Protocol
\label{sec:setup}

\paragraph{Constructed testbeds.} We built four frozen, schema-standardized families (Table~\ref{tab:testbeds}) totalling 109{,}754 examples. All are pure text/data artifacts---no SAE or model weights baked in---so absorption presence is an empirical question for the SAE run, not a construction artifact. Words for the spelling and non-spelling hierarchies are anchored in the real \texttt{gemma-2-2b} vocabulary and a pinned Pile revision, so they never derive from the latents being grouped (non-circular). The first-letter testbed contributes 17{,}180 examples over five letters (L/O/T/I/D) with 0 deterministic flip/span violations [ARTIFACT:art_dpYpjSn2Xvg3]; the non-spelling testbed contributes 24{,}128 examples over a numeric-quantity hierarchy and a taxonomic ``is-a-country'' hierarchy [ARTIFACT:art_t2uUbjSwpd3t]; the toxicity family contributes 37{,}707 examples from ParaDetox \citep{Logacheva2022} and civil\_comments \citep{Borkan2019} [ARTIFACT:art_8QO7pl6Pd8UQ]; and a supporting family contributes 30{,}739 examples of CAD-IMDB sentiment \citep{Kaushik2019}, CEBaB aspect-sentiment \citep{Abraham2022}, and a bias\_in\_bios boundary-null \citep{DeArteaga2019} [ARTIFACT:art_21JWypIydPMX].

\begin{table}[t]
\centering
\small
\caption{Constructed testbeds. Counts are released examples; pairs are reconstructable minimal pairs. LB = load-bearing, NS = non-spelling spine, SP = supporting, BN = boundary-null.}
\label{tab:testbeds}
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

\paragraph{Baselines.} We compare CCRG units against eleven baselines (Table~\ref{tab:baselines}), spanning raw latents, observational clusters (count-matched for classification), dense probes (including a LEACE surface-invariant hyperplane), supervised oracle pools, and label-free/oracle group-robustness probes. The design isolates \emph{selection at matched pool size}: against the count-and-pool-matched attribution pool (h), the unit and (h) pool the same number of directions and vary only \emph{how} members are chosen.

\begin{table}[t]
\centering
\small
\caption{Baseline glossary. (b)/(c) are count-matched to the unit's member count $k$; (h) is count-and-pool-matched to isolate the selection criterion.}
\label{tab:baselines}
\begin{tabular}{cl}
\toprule
ID & Baseline \\
\midrule
(a) & Best raw single latent (held-out AUC/F1) \\
(b) & Observational co-activation / feature-family clusters, count-matched to $k$ \\
(c) & Decoder-geometry (cosine) clusters, count-matched to $k$ \\
(d) & Counterfactually-matched difference-of-means \\
(e) & Linear probe on raw residual activations \\
(f) & Surface-invariant matched probe (LEACE-erased surface direction) \\
(g) & Supervised oracle pool: top-$N$ latents by SCR/TPP attribution \\
(h) & Count-and-pool-matched: max-pool over exactly $k$ SCR/TPP-selected raw directions \\
(i) & Unmatched difference-of-means / probe on raw labels \\
(j) & Oracle group-DRO probe with true sub-context labels (robustness upper bound) \\
(k) & Label-free group-inference probe (JTT/GEORGE-style) \\
\bottomrule
\end{tabular}
\end{table}

\paragraph{Encoding and gating.} The SAE is loaded directly from Gemma Scope \texttt{params.npz} (canonical \texttt{layer\_12/width\_16k}); the residual is captured by a forward hook on \texttt{model.layers[12]}. Each run gates on reconstruction fidelity before analysis: on first-letter, reconstruction cosine $0.924$, explained variance $0.857$, mean L0 $95.9$, and exact word-token localization (0/64 mismatches) [ARTIFACT:art_0ueMMR8Tt02P]; on toxicity, reconstruction cosine $0.916$ [ARTIFACT:art_-o2RPMOZp37A]; on the non-spelling testbed, encode-time FVU $0.18$/$0.20$ and token-alignment $0.975$/$1.000$ [ARTIFACT:art_QGSdsKY6U1vK].

\paragraph{Statistics and the primary endpoint.} The primary statistical object is the per-concept paired bootstrap CI ($B=10{,}000$ on per-example correctness differences), with an exact McNemar confirmatory and Holm--Bonferroni across claims. We declare a single \emph{primary falsification endpoint} on first-letter (the guaranteed-signal regime): the method works iff (E1) the K-track proposal step, given only content-flip pairs, recovers the diagnostic parent plus $\geq 2$ absorbers above a random-membership null, \emph{and} (E2) the resulting label-free unit beats the count-matched pools on classification and absorbed-slice recall with a CI excluding 0. The honest-null branches reported below are \emph{secondary characterizations} of how the method behaves, not co-equal successes; a clean E1$\wedge$E2 failure on first-letter would mean the method does not work.

# Results: First-Letter Spelling (Primary Endpoint)
\label{sec:firstletter}

We ran the full pipeline on all five letters in $\sim$8 minutes on one RTX 4090, with \$0 in LLM spend (the diagnostic is the form-free probe-projection) [ARTIFACT:art_0ueMMR8Tt02P].

\paragraph{C1 classification: the label-free unit is the best classifier on all five letters.} Treating each method's pooled activation as a starts-with-letter classifier, the co-response unit attains the highest held-out AUC on every letter---L $0.905$, O $0.917$, T $0.859$, I $0.961$, D $0.956$---beating the best raw latent (a), the count-matched co-activation (b) and decoder-geometry (c) clusters, \emph{and} the count-and-pool-matched oracle-attribution pool (h) in every case (Figure~\ref{fig:c1}). The margin over (h) is large and significant on the harder letters (unit$-$(h) AUC: T $+0.205$, CI $[0.064,0.333]$; I $+0.405$, CI $[0.286,0.524]$; D $+0.456$, CI $[0.333,0.578]$) and positive but not significant on L ($+0.091$) and O ($+0.150$). On I, where every individual baseline is weak ($\leq 0.833$), the unit reaches $0.961$: pooling the right complementary members recovers signal no single selection criterion captures. This is the load-bearing positive---cluster-level units are a more reliable unit of analysis than single latents, observational clusters, or supervised attribution pools.

[FIGURE:fig3]

\paragraph{E1 absorber recovery: 4/5, with one honest anchor failure.} Given only content-flip pairs, the K-track recovers the diagnostic-identified parent plus $\geq 2$ absorbers above the 95th-percentile random-membership null on L, O, T, and D (membership F1 vs.\ null: L $0.308$ vs.\ $0.103$; O $0.300$ vs.\ $0.150$; T $0.263$ vs.\ $0.211$; D $0.381$ vs.\ $0.190$, with 7 absorbers). On these four letters the recall-argmax anchor \emph{is} the diagnostic parent (anchor corpus-firing rate $0.27$--$0.39$). The units are human-auditable: for L, anchor latent 205 (logit-lens \texttt{Lohan/Ls/LS/LF}) plus absorbers 3069=\texttt{list}, 2416=\texttt{line}, 8463=\texttt{large}, 4736=\texttt{l\ldots ing}; for D, anchor 6210 (\texttt{PhysRevD/DPR/DSS}) plus 1970=\texttt{different}, 7293=\texttt{director}, 10769=\texttt{day}. A 70-edge anchor$\to$absorbed-child knowledge graph is emitted. E1 \emph{fails} on I by anchor fidelity only: the highest-cover-set latent (1227) fires 0\% on the corpus and has code-token logit-lens---a spurious anchor, not the semantic parent. We report this as a mechanism finding: the recall-argmax heuristic is not always the concept parent, yet the pooled unit remains the best I classifier (AUC $0.961$).

\paragraph{E2 absorbed-slice recall: the unit beats count-matched pools.} On the absorbed slice---words on which the parent goes silent---the unit beats the count-matched pool (h) directionally on all five letters and significantly on the two best-powered slices: T $0.925$ vs.\ $0.763$ (CI of difference $[0.054,0.269]$) and I $0.775$ vs.\ $0.496$ (CI $[0.178,0.380]$). It also beats the count-matched observational clusters (b)/(c) significantly on every letter, and beats the larger 10-latent oracle pool g10 significantly throughout. We deliberately base the E2 verdict on these \emph{non-circular} downstream metrics rather than on a recovered-absorber \emph{count}: the count is circular for the oracle baselines, because the diagnostic and the attribution pools (g)/(h) both rank by the same probe direction $d_p$, so they trivially overlap the diagnostic. The 20-latent oracle pool (g) is competitive on the slice (e.g.\ L $0.883$), but it is not count-matched; at matched pool size the co-response unit wins.

\paragraph{Steering: lowest collateral on the primary letter.} As a generality demonstration, we steer with the unit's mean-member-decoder direction and compare, at \emph{matched} on-target effect, the full-vocabulary KL divergence on unrelated prompts against a best-single-member (hub) direction and a non-SAE difference-of-means direction (Figure~\ref{fig:steer}). On the primary letter L the unit is the most surgical---KL $16.4$ versus hub $27.9$ and diff-of-means $30.4$ at the same on-target shift---and likewise on D ($28.6$ vs.\ $33.3$/$30.5$). On O and T a non-SAE diff-of-means is more surgical, and on I the hub is; we report steering honestly as a demonstration, not a load-bearing claim, and note that the unit's advantage tracks the letters where E1 anchor fidelity holds.

[FIGURE:fig5]

\paragraph{Admission.} The K-unit is admitted via signature K on all five letters (surface-invariant, $p_{\text{surf}}=1.0$); the empirical false-admit rate under the matched random-$k$ null is $0.03$--$0.09$, at or near the $0.05$ target. We note a real limitation: within the eligible set, random $k$-latent pools also classify well (random-gain-$>$-0.05 fraction $\approx 0.92$--$1.0$), so the admission filter's discriminative power comes from the surface-invariance gate and the matched-null signature-K test, not from pooling per se.

# Results: Absorption Generalizes Beyond Spelling
\label{sec:nonspelling}

Absorption is documented empirically almost only on first-letter spelling: the original study is spelling-only \citep{Chanin2024}, SAEBench's sole absorption eval is \texttt{absorption\_first\_letter} \citep{Karvonen2025}, and the Matryoshka/hierarchical mitigations measure it via the spelling metric \citep{Bussmann2025, Muchane2025}. We therefore treat the non-spelling testbed as both a generality test and a novel empirical question, gated by an explicit non-triviality pre-check [ARTIFACT:art_QGSdsKY6U1vK].

\paragraph{The non-triviality gate passes on both hierarchies.} On the \emph{numeric} hierarchy the parent latent 14823 (content-response precision $1.000$, negative-firing $0.0006$) covers $0.829$ of content flips but only $0.427$ of the corpus, missing 1{,}060 positives---genuine holes. The K-track fills them with a year and two decimal absorbers. On the \emph{taxonomic} hierarchy the parent latent 3792 (recall $0.953$) admits Georgia, Jordan, and United-States specialists. Both gates pass: absorption is \emph{not} spelling-specific.

\paragraph{The K-track recovers absorbers the oracle pool drops, with near-zero false positives.} At matched overall recall, the compact 4-latent unit beats the marginal-attribution pools on the absorbed sub-context that defines each hierarchy (Table~\ref{tab:nonspelling}). On numeric \texttt{integer}, unit recall $0.283$ versus (g) $0.107$ and (h) $0.110$ (unit$-$(g) $+0.177$, CI $[0.120,0.237]$, Holm $p=8\!\times\!10^{-8}$; unit$-$(h) $+0.173$, CI $[0.117,0.233]$), with the unit at \emph{zero} false positives versus $0.12$/$0.13$ for the oracle pools. On taxonomic \texttt{Georgia}, unit recall $0.713$ versus (h) $0.520$ (unit$-$(h) $+0.193$, CI $[0.073,0.307]$, Holm $p=0.035$), again at near-zero false positives ($0.014$ vs.\ $0.85$/$0.65$). The honest nuance: gains are sub-context-specific, not blanket wins over the 20-latent oracle (on numeric year/date/decimal the larger pool wins); the form-free diagnostic corroborates the K-track edges for taxonomic (top-1 agreement $0.318$ vs.\ null $0.002$; the Jordan edge agrees $0.99$) but diverges for numeric, where coverage-based and projection-based absorber notions disagree; and a non-SAE dense probe reaches recall $1.0$ at zero false positives---the ``simple baselines can match raw-SAE'' point, reported plainly.

\begin{table}[t]
\centering
\small
\caption{Non-spelling absorber recovery at matched overall recall. The compact K-track unit beats the count-matched attribution pool (h) and the larger oracle pool (g) on the defining absorbed sub-context, with near-zero false positives. Recall on the absorbed slice; FP = false-positive rate.}
\label{tab:nonspelling}
\begin{tabular}{llccccc}
\toprule
Hierarchy & Absorbed sub-context & unit & (g) pool & (h) pool & dense probe & unit FP \\
\midrule
Numeric & \texttt{integer} & \textbf{0.283} & 0.107 & 0.110 & 0.643 & 0.000 \\
Taxonomic & \texttt{Georgia} & \textbf{0.713} & 0.800 & 0.520 & 0.807 & 0.014 \\
\bottomrule
\end{tabular}
\end{table}

# Results: A Firing-Structure Test for When Grouping Helps
\label{sec:toxicity}

The previous iteration argued that both splitting and absorption regimes occur in safety data using civil\_comments sub-attribute \emph{label} co-occurrence. A reviewer correctly noted that label co-occurrence is not latent co-firing: a single general toxicity latent can fire across all sub-attributes regardless of label disjointness, so the label statistic does not establish that any pairwise operator fails on real SAE latents. We replace the proxy with a \emph{direct measurement} of SAE-latent firing [ARTIFACT:art_-o2RPMOZp37A].

\paragraph{Toxicity is a co-firing regime, not an absorption regime.} The general toxicity latent (12714, Neuronpedia: ``profanity and vulgar expressions'') fires on $94.3\%$ of toxic content-flips (precision $0.996$). Distinct, on-target detector latents exist for the label-disjoint sub-attributes---threat (11630, ``conflict and violence'', AUC $0.828$), identity\_attack (11573, ``race, identity, social justice'', AUC $0.930$), insult (13367, ``hypocrite/moron/coward'', AUC $0.871$)---and they cover the general latent's recall holes (cover-fraction $0.74$/$0.93$). \emph{But they co-fire with the general latent}: the toxic-only firing-Jaccard is $0.403$ (threat, CI $[0.392,0.414]$), $0.292$ (identity\_attack, CI $[0.282,0.303]$), and $0.655$ (insult)---all far above the $0.10$ mutual-exclusivity threshold absorption requires (Figure~\ref{fig:firing}). The SAE firing structure thus \emph{departs sharply from the label co-occurrence structure} (label-Jaccard: threat $0.044$, identity\_attack near-zero): there is no mutual exclusivity, so the K-track's necessity is \textbf{refuted} on toxicity. The set-cover track correctly adds zero absorbers here.

[FIGURE:fig4]

\paragraph{Consequently, grouping does not help and attribution wins.} The $k{=}3$ co-response unit ties the count-matched observational and single-latent baselines on toxicity classification (AUC $0.762$ vs.\ (a) $0.765$, (b) $0.797$, (c) $0.792$) but is beaten by attribution selection ((g) $0.892$, (h) $0.837$) and a full-residual probe ((e) $0.859$); unit$-$(h) AUC CI $[-0.093,-0.055]$, Holm $p\approx 5\!\times\!10^{-71}$. It \emph{collapses} on the disjoint sub-attributes (threat $0.626$ vs.\ (h) $0.929$; identity\_attack $0.633$ vs.\ (h) $0.936$). The pre-registered selection ordering $(f)<(g)/(h)<\text{unit}$ on worst-sub-context recall does \emph{not} hold (f $0.086 <$ unit $0.237 <$ g $0.393 <$ h $0.451$), and the unit$-$(g)/(h) gap \emph{shrinks} under sub-population reweighting toward the under-served sub-attributes (slope $-0.474$, CI $[-0.536,-0.412]$). This is a clean, decisive honest negative.

\paragraph{Why this strengthens, not weakens, the contribution.} The firing-Jaccard is a single cheap forward pass over data one already has, and it predicts the outcome \emph{before} any grouping: where detectors are mutually exclusive with the parent (spelling, numeric, taxonomic), CCRG recovers absorbers and out-classifies attribution pools at matched size; where they co-fire (toxicity), the regime is splitting/co-activation and supervised attribution is the right tool. Rather than over-claiming a universal win, we deliver an a-priori applicability test. The C-track unit on toxicity is also less interpretable than the absorption units (its anchor is the profanity latent, but its co-members include off-target name and acronym latents), consistent with the C-track being the secondary track.

\paragraph{Admission and the strengthened surface control.} On toxicity, $M=31$ candidate units were tested; 11 were admitted, with an empirical family-wise false-admit rate of $0.08$ under the random-$k$ null and bootstrap cluster-stability ARI $0.79$ (CI $[0.70,0.92]$) against a shuffle-null ARI of $0$. The surface-invariance gate is load-bearing, so we enlarged the surface-flip pair sets (first-letter $590\to1{,}700$; toxicity $546\to1{,}631$) and re-judged with an independent model family: an Anthropic judge confirms $85.2\%$ ($465/546$) of the original gpt-4o-mini-accepted toxicity pairs, removing the iter-1 same-model generate-and-judge circularity, for \$1.72 total [ARTIFACT:art_YwjLYapklnVk]. We report the per-concept surface-response null sizes used per admission.

# Discussion
\label{sec:discussion}

\paragraph{What is established.} CCRG, executed on a frozen Gemma Scope SAE, produces auditable multi-member units that (i) out-classify raw latents, count-matched observational clusters, and a count-matched supervised attribution pool on all five first-letter spelling tasks; (ii) recover the parent plus per-token absorbers on 4/5 letters and beat the count-matched pool on absorbed-slice recall; and (iii) recover numeric and country absorbers that marginal-attribution drops at matched pool size, establishing that absorption is not a spelling artifact. These are SAE-\emph{selection} comparisons, so the load-bearing claim does not depend on out-classifying a strong dense probe---which, honestly, we do not always do (a dense probe matches the unit on the non-spelling slices).

\paragraph{The contribution is regime-scoped, and we can say which regime a priori.} The most important methodological lesson is that grouping helps exactly in the absorption regime (mutually-exclusive parent/child firing) and not in the co-firing/splitting regime, and that a single firing-Jaccard measurement separates the two before grouping. This reframes the method from ``a universal repair'' to ``a repair for absorption, with a test for applicability,'' which is both more defensible and more useful: a practitioner can run the cheap test and know whether to reach for set-cover grouping or for supervised attribution.

\paragraph{Honest failure modes.} (1) The recall-argmax anchor is not always the semantic parent (letter I: a code-token latent fires 0\% on the corpus yet maximizes cover-set size); a parent-validation step is needed for unsupervised deployment. (2) E2 is significant on the two best-powered absorbed slices and directional elsewhere; the recovered-absorber \emph{count} is circular for oracle baselines and is reported descriptively only. (3) Within the eligible set, random $k$-pools also classify well, so admission power comes from the surface-invariance gate, not pooling. (4) On toxicity the unit ties weak baselines and loses to attribution, and its advantage shrinks under sub-population shift. (5) The form-free diagnostic corroborates K-track edges for taxonomic but not numeric absorption. Each is reported with its statistic rather than spun as future work.

\paragraph{Limitations: model-diffing.} The goal mandates a model-diffing demonstration, but no instruction-tuned Gemma Scope SAE exists for the 2B model (Google's IT residual SAEs cover only 9B). Diffing would therefore require applying the shared frozen pretrained SAE to base and instruction-tuned activations---a confounded setup, not a paired-SAE diff. We do not present a model-diffing result and state this as an explicit infrastructure limitation rather than deferring it to open-ended future work. We also scope the method to splitting and absorption: a hedged single polysemantic latent is not groupable \citep{Chanin2025}.

# Conclusion
\label{sec:conclusion}

We presented Two-Track Co-Response Grouping, a training-free method that organizes the latents of a frozen public SAE into reliable, auditable concept units by their interventional response to content counterfactuals---correlation communities for shared-support splitting and an anchored greedy set-cover for disjoint-support absorption that no pairwise-affinity clustering can propose. Executed on Gemma Scope, the label-free unit is the best classifier on all five first-letter spelling tasks (AUC 0.86--0.96), beating raw latents, count-matched observational clusters, and a count-matched oracle-attribution pool; it recovers per-token absorbers and beats the count-matched pool on absorbed-slice recall; and absorption generalizes to numeric (\texttt{integer}) and country (\texttt{Georgia}) hierarchies with near-zero false positives. A direct measurement of SAE-latent firing shows that toxicity is a co-firing regime in which grouping does not help and supervised attribution wins---turning a potential over-claim into a cheap, a-priori applicability test. We release four frozen testbeds, the single-GPU pipeline, and a complete account of where the method works and where it does not.

\paragraph{Future work.} Add an unsupervised parent-validation step to fix the anchor-fidelity failure; extend the firing-Jaccard applicability test into a routing rule that picks set-cover grouping versus attribution per concept; and revisit model-diffing if a paired instruction-tuned SAE becomes available.

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
</supplementary_materials>

<previous_review>
Your review from the previous iteration. Check which critiques have been addressed
in the revised paper. Do NOT re-raise critiques that have been adequately fixed.
Only re-raise if the fix is insufficient.

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

### [2] HUMAN-USER prompt · 2026-06-17 17:48:29 UTC

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

### [3] SKILL-INPUT — aii-web-tools · 2026-06-17 17:53:51 UTC

The agent loaded the **aii-web-tools** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-web-tools
description: "Web research toolkit: web search (Serper/Google), web page fetch as markdown (HTML and PDF), and regex grep over full page/PDF text. Use whenever a task needs to search the web, read a page, mine a paper/PDF, verify citations, or extract exact quotes, numbers, or methodology from a URL."
---

## Web tools

You have three web capabilities: **search**, **fetch**, and **grep** (exact
regex extraction over a full page or PDF).

**Pick where they come from, in this order:**

1. **If you have built-in `WebSearch` / `WebFetch` tools, PREFER those over the
   scripts below.** They may be **deferred tools** (listed by name but with
   schemas not yet loaded) — if so, call `ToolSearch("select:WebSearch,WebFetch")`
   ONCE to load them, then use them normally. Do not skip them just because they
   need that one extra load step; they are the preferred path. Pair them with the
   `aii_web_tools__fetch_grep` script below when you need exact text / numbers /
   methodology that a summary would miss, or when reading a PDF.
2. **Only if you have NO built-in `WebSearch` / `WebFetch`** (e.g. the OpenHands
   backend), use the scripts in this skill (below). They are our own
   implementations — Serper.dev for search, html2text + PyMuPDF for fetch, and
   regex grep over the full document text. They work without any built-in web
   tools.

Workflow either way: **search** (discover) → **fetch** (read for the gist) →
**grep** (pull exact details / read PDFs).

---

## Running the scripts

Run every script with the skill's pre-provisioned interpreter (it already has
`requests`, `html2text`, `pymupdf`, `python-dotenv`). Set `PY` once:

```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-web-tools"
export PY="$SKILL_DIR/../.ability_client_venv/bin/python"
```

### 1. Search the web (Serper.dev / Google)

```bash
$PY "$SKILL_DIR/scripts/aii_fast_web_search.py" --query "neuro-symbolic FOL translation LLM" --max-results 10
```

Returns ranked title / URL / snippet lines. Use it first to scan the
landscape; snippets are for discovery only — fetch a page before judging it.

### 2. Fetch a page as markdown (HTML or PDF)

```bash
$PY "$SKILL_DIR/scripts/aii_fast_web_fetch.py" fetch --url "https://arxiv.org/abs/2303.11366" --max-chars 10000
```

`--max-chars` caps output (default 10000); `--char-offset N` pages further in.
Handles PDFs transparently via PyMuPDF.

### 3. Grep a page or PDF (exact regex extraction)

```bash
$PY "$SKILL_DIR/scripts/aii_fast_web_fetch.py" grep --url "https://arxiv.org/pdf/2303.11366" --pattern "verbal reinforcement" --max-matches 20 --context-chars 200
```

Returns only the matching sections with surrounding context — the right tool
for exact numbers, table values, methodology, or long PDFs where a summary
would lose the detail. `-i` for case-insensitive.

**Parallelize** independent searches/fetches in one turn; only sequence a
fetch after the search that produced its URL.

---

## Notes

- The scripts call our ability server. If a script prints
  `Ability service not available`, the server is down — say so rather than
  silently improvising a different search method.
- Do **not** hand-roll your own `requests`/scraping for search when these
  tools are available: Serper returns clean Google results and the fetch/grep
  scripts already handle HTML, PDFs, and encoding.
````
