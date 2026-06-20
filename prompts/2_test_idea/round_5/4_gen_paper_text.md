# gen_paper_text — test_idea

> Phase: `invention_loop` · round 5 · Substep: `gen_paper_text`
> Run: `run__C1-INh1YNGn` — Catching Silent Feature Absorption in Frozen Sparse Autoencoders: Label-Free Loc
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave the agent(s) in this substep — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_paper_text` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-06-18 04:05:29 UTC

```
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

Sparse autoencoders (SAEs) decompose the activations of large language models (LLMs) into a dictionary of sparsely-activating latents intended to be interpretable, monosemantic units of analysis \citep{Cunningham2023, Bricken2023, Templeton2024}. The appeal is operational: a latent that reliably tracks a human concept can be read off as a classifier, flipped as a steering knob, or compared across model variants. Public SAE suites such as Gemma Scope \citep{Lieberum2024} expose millions of such latents over open models, making this a practical interface for safety-relevant interpretability.

This appeal is undercut by a now well-documented fact: \emph{single SAE latents are not reliable units} \citep{Leask2025}. Two failure modes recur. \emph{Feature splitting} fragments one concept across many latents, so no single latent captures it. \emph{Feature absorption} is more insidious: a more specific child latent suppresses the firing of a more general parent, leaving the parent with unpredictable holes on exactly the sub-contexts the child covers; parent and child become \emph{mutually exclusive in firing} \citep{Chanin2024}. (A related failure, \emph{feature hedging}, merges correlated features into one polysemantic latent in narrow SAEs \citep{Chanin2025}; a hedged latent is not groupable and is out of scope.) On concrete downstream tasks the cost is stark: difference-of-means probes are the strongest concept detectors and raw-latent SAE methods are uncompetitive \citep{Wu2025, Kantamneni2025}, while standardized suites quantify absorption, sparse probing, and targeted erasure \citep{Karvonen2025}. Any method proposing SAE latents as a knowledge representation must clear strong simple baselines and address splitting and absorption head-on.

The task is hard because the obstacles defeat the obvious instruments \emph{by construction}. The intuitive fix for an unreliable single latent is to group several latents into a cluster-level unit. But every existing post-hoc grouping signal is \emph{observational}: which latents fire together (co-activation feature families \citep{ONeill2024, Deng2025}) or which decoder directions point alike. Absorption is precisely the regime where observational signals must fail---the parent and the absorbing child are mutually exclusive in firing, so co-activation can never group them, and their decoders need not be cosine-similar \citep{Chanin2024}. The standard \emph{supervised} remedy, selecting the top-$N$ latents by causal effect on a concept probe (SCR/TPP attribution \citep{Karvonen2024, Marks2024}), is no better: a latent that fires only in a narrow sub-context has low \emph{marginal} attribution and is silently dropped, even though it carries the concept there. The latents one most needs are exactly the ones these instruments discard.

Why has this not been solved post-hoc? Recent architectural remedies---Matryoshka SAEs \citep{Bussmann2025}, hierarchical SAEs \citep{Muchane2025}, and subspace-aware SAEs \citep{Dalili2026}---all \emph{retrain} the SAE to reduce splitting and absorption at training time, and do not help a practitioner holding a frozen public SAE. We take the opposite stance: a \emph{training-free, post-hoc repair of frozen public SAEs}. The methodological gap we fill is the \emph{grouping operator}. Grouping by \emph{interventional co-response}---how latents jointly track a content counterfactual, rather than how they co-fire at baseline---is the matched instrument, with a direct precedent in systems biology, where differential co-expression methods (DiffCoEx \citep{Tesson2010}, WGCNA \citep{Zhang2005}) cluster genes by correlated response to a perturbation precisely because co-regulated genes are often not co-expressed at baseline. Crucially, correlation is the right operator only for the \emph{shared-support} splitting case. Absorbers respond on \emph{disjoint} supports and have low pairwise correlation, so no affinity-merging clustering can even \emph{propose} the right group. The disjoint-support case is a \emph{maximum-coverage} problem, whose classic greedy solution \citep{Nemhauser1978, Feige1998} is the natural---and, we argue, the only correct---proposer for absorption units.

We introduce \textbf{Two-Track Co-Response Grouping (CCRG)} and execute it on a frozen Gemma Scope SAE. We deliberately do not stake the contribution on out-classifying a strong dense probe, because on aggregate detection no raw-latent SAE method does \citep{Wu2025}; our own results confirm this on every task we measure. Instead, the contribution is what a cluster-level unit and its \emph{feature knowledge graph} can do that a single dense hyperplane structurally cannot: \emph{measured, localized, auditable repair}. Four findings result. (1) The emitted knowledge graph carries \emph{measured} editorial utility: across three concept families, 30 KG-named absorber additions recover a suppressed parent's recall hole and survive a Benjamini--Hochberg false-discovery control over all 69 tested repairs, beating a random-addition control; and ablating a single KG-named absorber surgically edits exactly one sub-context with a $1452\times$ median selectivity over collateral, a localization a dense parent direction cannot provide [ARTIFACT:art_sxwT7hK6YFEA] [ARTIFACT:art_0CZwPjG2YMCf]. (2) A one-forward-pass measurement---low firing-Jaccard \emph{and} a parent recall hole---is an a-priori \emph{router} that predicts which regime a concept is in before any grouping, with a measured (not perfect) error rate [ARTIFACT:art_07ju05r0onqB]. (3) Non-spelling absorption is real but \emph{narrow}: it recurs on homograph tokens whose general parent is suppressed (Georgia, Jordan), and once the unit is rebuilt from precision-passing specialists, its set-cover \emph{selection} beats every label-free selector at matched pool size [ARTIFACT:art___vgSpUe6wAF]. (4) On first-letter spelling, the same selection is isolated against three non-random label-free selectors; the set-cover-specific win holds on two of five letters, which we report exactly [ARTIFACT:art_JMA2gBvnakAm].

[FIGURE:fig1]

\paragraph{Summary of contributions.}
\begin{itemize}
\item \textbf{A two-track grouping algorithm} (\S\ref{sec:method}): a training-free procedure that proposes split families by content-response correlation (C-track) and absorption units by a \emph{precision-gated} anchored greedy set-cover (K-track), reconciled and filtered by a single null-anchored, multiplicity-controlled admission rule. To our knowledge maximum-coverage set-cover has not previously been used to group SAE latents.
\item \textbf{Measured auditability as the headline} (\S\ref{sec:audit}): a KG-guided recall-repair loop (30 repairs surviving FDR control across spelling, taxonomic, and numeric families), a KG-localized single-absorber \emph{surgical edit} with side-effect measurement, and LLM member-labeling---each beating a null control on a dimension a dense probe lacks.
\item \textbf{An a-priori firing-structure router} (\S\ref{sec:router}) that predicts when grouping helps, reported as a screening heuristic with its measured error, separating a 12-concept derivation set from a 3-concept prospective test.
\item \textbf{Honestly-scoped within-SAE selection} (\S\ref{sec:selection}): a precision-rebuilt taxonomic homograph unit whose set-cover selection beats all label-free selectors, and a first-letter analysis reporting the per-letter joint of mechanism and selection ($2/5$) against non-random controls.
\item \textbf{Four frozen testbeds, a single-GPU pipeline, and a dedicated account of failure modes} (\S\ref{sec:setup}, \S\ref{sec:negatives}): a co-firing toxicity regime where CCRG does not help, an unconfirmed numeric hierarchy, no dense-probe out-classification on any task, and a confound-bounded null model-diffing result.
\end{itemize}

# Related Work
\label{sec:related}

\paragraph{SAEs and the unreliability of single latents.} Sparse dictionary learning on LLM activations yields interpretable features \citep{Cunningham2023, Bricken2023, Templeton2024, Lieberum2024}, but a growing body of work shows individual latents are not canonical units \citep{Leask2025}. \citet{Chanin2024} introduce and quantify \emph{feature absorption}---a specific child latent suppresses a general parent's firing---demonstrated on first-letter spelling, and \citet{Chanin2025} characterize \emph{hedging}. Benchmarks make the practical cost concrete: AxBench finds difference-of-means strongest and raw-latent SAE methods uncompetitive \citep{Wu2025}; a sparse-probing case study reaches the same conclusion \citep{Kantamneni2025}; and SAEBench standardizes absorption, sparse-probing, and erasure evaluations \citep{Karvonen2025}. We adopt this as our honest bar: our load-bearing claim is not out-classifying a dense probe but delivering an auditable, editable repair a probe cannot.

\paragraph{Post-hoc grouping of SAE features.} Prior grouping is observational: co-activation ``feature families'' \citep{ONeill2024} and sparse feature coactivation modules \citep{Deng2025} group latents by what fires together or which decoders align. Closest to our output, \citet{Winnicki2026} build a feature-level knowledge graph from SAE features, but its edges come from three purely observational sources---corpus co-occurrence weighted by Jaccard overlap of binary presence matrices, a transcoder cross-layer mechanism graph, and contrastive domain filtering---with no interventional signal. Such edges cannot, by construction, express CCRG's central relation: CCRG joins a country anchor latent to a Georgia specialist that is \emph{mutually exclusive in firing} with it (firing-Jaccard $<0.05$). A Jaccard co-occurrence edge between them is $\approx 0$ by definition, decoder geometry need not relate them, and a cross-layer transcoder graph encodes inter-layer pathways rather than within-layer firing-complementarity. CCRG's edge is interventional---the two latents track the same content counterfactual on disjoint supports. We count-match observational clusters to our unit's size so any classification comparison reflects \emph{selection}, not capacity.

\paragraph{Supervised latent selection and word-sense evaluation.} SHIFT and the SCR/TPP family rank individual latents by causal effect on a concept probe and ablate the top-$N$ \citep{Marks2024, Karvonen2024}; a latent firing only in a narrow sub-context has low marginal attribution and is silently dropped---the exact gap our co-response set-cover fills. We use SCR/TPP-style ranking as our oracle-pool baselines (g)/(h). Separately, PS-Eval \citep{Minegishi2025} asks whether SAE features \emph{separate the senses} of polysemous words; it never studies the absorption failure mode, a suppressed parent, or a recall hole, and is a clean cite-and-distinguish rather than a precedent for our homograph-absorption finding.

\paragraph{Architectural remedies and concept editing.} Matryoshka \citep{Bussmann2025}, hierarchical \citep{Muchane2025}, and subspace-aware \citep{Dalili2026} SAEs modify \emph{training} to reduce splitting/absorption; we repair a \emph{frozen} public SAE post-hoc. For our edit demonstration, SAE-TS \citep{Chalnev2024} and SRS \citep{He2025} select a whole \emph{concept} feature with a tuned coefficient; LEACE \citep{Belrose2023} is dense whole-concept erasure that cannot localize to a sub-context; and SAE concept-unlearning work targets text-to-image diffusion \citep{Cywinski2025}. None edits a single \emph{absorber} latent named by an interventional feature-graph edge to recover or change one sub-context while preserving the parent. AxBench \citep{Wu2025} is both our side-effect/fluency evaluation template and our honest concession that diff-of-means beats SAEs on aggregate steering.

\paragraph{Cross-field instruments and robustness.} The C-track imports differential co-expression module discovery \citep{Tesson2010, Zhang2005} and Leiden community detection \citep{Traag2018}; the K-track imports the maximum-coverage greedy with its $(1-1/e)$ guarantee \citep{Nemhauser1978, Feige1998}. The robustness framing engages label-free worst-group-robustness work---group-DRO \citep{Sagawa2019}, JTT \citep{Liu2021}, GEORGE \citep{Sohoni2020}, EIIL \citep{Creager2020}, LfF \citep{Nam2020}, group-aware priors \citep{Rudner2024}, and diverse prototypical ensembles \citep{To2025}---which infer groups over \emph{examples} and \emph{retrain}; CCRG groups \emph{features}, never retrains, and the recovered absorbers \emph{are} the inferred sub-context specialists. Surface invariance draws on LEACE \citep{Belrose2023} and counterfactual invariance \citep{Veitch2021}; minimal-pair supervision draws on counterfactually-augmented data \citep{Kaushik2019}, CEBaB \citep{Abraham2022}, and ParaDetox \citep{Logacheva2022}. The closest ``cluster counterfactual differences'' template is CDLC in vision \citep{Varshney2025}, which clusters diffusion-counterfactual difference vectors into one continuous direction per class; we cluster \emph{discrete} LLM SAE latents into multi-member units and add a set-cover track for which CDLC has no analogue.

# The Two-Track Co-Response Grouping Method
\label{sec:method}

\paragraph{Preliminaries.} Let the frozen SAE have latents $l \in \{1,\dots,L\}$ with encoder activation $a_l(x)$; a latent \emph{fires} on $x$ iff $a_l(x) > 0$ (Gemma Scope uses a JumpReLU, so the threshold is inside the encoder \citep{Lieberum2024}). For a concept $c$ we are given \emph{content-flip minimal pairs} $(x_{\text{off}}, x_{\text{on}})$ in which the concept is absent/present at matched surface form, plus \emph{surface-flip pairs} in which the concept is held constant and surface varies. Content labels are the supervision every matched baseline consumes; the method uses no absorption-specific oracle. We encode at one residual-stream site (\texttt{gemma-2-2b}, layer 12, width 16k canonical; $d_{\text{model}}=2304$, $16{,}384$ latents).

\paragraph{Step 1: interventional content-response and cover sets.} For each latent $l$ and pair $p$, the \emph{content-response} is $r_l(p) = a_l(x_{\text{on}}) - a_l(x_{\text{off}})$. A latent's \emph{cover set} $C_l$ is the set of pairs whose content flip it tracks reliably ($r_l(p)>\tau_{\text{resp}}$ and $a_l(x_{\text{on}})>0$) and precisely (firing-precision $\geq 0.7$ on its own support). Because absorbers fire on only a handful of words, a mean-over-pairs prefilter would discard them; eligibility is therefore \emph{cover-based} (selective \emph{and} covering $\geq 1$ sub-context), retaining the genuinely sparse absorbers. We denote the cover-eligible set $E$.

[FIGURE:fig2]

\paragraph{Step 2: C-track --- correlation communities for splitting.} Where a concept \emph{splits}, sub-latents share firing support and co-respond positively, so pairwise affinity is appropriate. We build a sign-aware soft-thresholded affinity from the positive part of the Spearman correlation between response profiles, $A^{C}_{l,l'} = \max(\rho(r_l, r_{l'}), 0)^{\beta}$ with $\beta=6$ (WGCNA's scale-free criterion \citep{Zhang2005}), and run Leiden community detection (RBConfiguration partition \citep{Traag2018}), with resolution fixed by bootstrap-ARI stability against a shuffle null.

\paragraph{Step 3: K-track --- precision-gated anchored set-cover for absorption.} Absorbers respond on \emph{disjoint} supports and are mutually exclusive in firing with their parent, so their pairwise correlation is low and no affinity-merging clustering can propose them (Figure~\ref{fig:tracks}). We use an anchored greedy maximum-coverage procedure. \textbf{(1) Anchor:} $l^\* = \arg\max_l |C_l|$, the highest-recall ``parent'' candidate, chosen using \emph{only} the pairs and \emph{not} the absorption diagnostic. An \emph{unsupervised parent-validation} step then requires the anchor to fire on the held-out corpus above a floor (we use $5\%$); this rejects a spurious high-cover-set latent that fires $0\%$ on the corpus rather than crowning it anchor. \textbf{(2) Holes:} $H = P \setminus C_{\text{anchor}}$, the pairs the parent goes silent on. \textbf{(3) Greedy cover:} while $H$ is non-empty and improving, add $\arg\max_l |C_l \cap H|$ subject to mutual exclusivity (firing-Jaccard $<0.1$ with members), per-member precision $\geq 0.7$, and a marginal-coverage-gain floor $\geq 0.05$ whose bootstrap CI excludes $0$. A pure maximum-coverage objective will, however, prefer a high-coverage low-precision latent over a high-precision specialist that covers the same hole; we therefore add a \emph{per-sub-context precision gate} (equivalently, a precision-weighted coverage objective $\text{precision}\times\text{coverage}$), evaluated on a held-out fold, so the selected absorber is the precise specialist rather than the broad latent. The greedy max-coverage choice is the classic instrument for ``cover a universe with complementary specialists'' \citep{Nemhauser1978, Feige1998}; coverage-complementarity is a set-level property a pairwise operator cannot express.

\paragraph{Step 4: reconciliation.} For each C-community we designate its highest-recall member as a candidate anchor and run Step 3 to pull in mutually-exclusive absorbers covering its holes; we also seed Step 3 from standalone high-recall latents in no dense community. A final unit is a pure C-community (splitting), a pure K-cover (absorption), or a hybrid; we de-duplicate by highest coverage gain.

\paragraph{Step 5: admission filter with multiplicity control.} A proposed unit is admitted iff it clears \textbf{signature C} (within-unit content-response correlation above the 95th-percentile shuffle null) \textbf{or signature K} (pooled-max minus best-single content-response AUC above the 95th percentile of a best-of-random-$k$ null \emph{matched on marginal AUC}, plus the $k\in\{2,3\}$ absolute gain floor of $0.05$ with bootstrap CI excluding $0$, plus mutual exclusivity and the precision floor), \textbf{and} unit-level surface invariance (pooled surface-response not above the shuffled-surface null). Because many candidate units are tested per concept, we control multiplicity at the \emph{unit-proposal} level: a Bonferroni-within-unit $p$ over the disjunctive signature, then Benjamini--Hochberg across the $M$ candidate units, reporting $M$ and the empirical family-wise false-admit rate under the matched random-$k$ null.

\paragraph{Non-circular diagnostic and auditable graph.} Specialization edges are \emph{scored}, never formed, by the absorption diagnostic of \citet{Chanin2024}. Because the strict form needs an output logit, we use the domain-agnostic \emph{form-free} variant (the probe-projection implemented in SAEBench as \texttt{absorption\_fraction}): $l$ absorbs iff $\tau_c < (\hat{a}_l \cdot d_p)/(a \cdot d_p)$, with $d_p$ a parent-concept probe trained on data \emph{disjoint} from clustering. The anchor is chosen by recall available to every baseline, so a label-free unit beating a supervised oracle is not undercut. Each admitted unit is emitted with logit-lens tokens and top conditioning contexts, plus directed anchor$\to$child specialization edges---a feature-level knowledge graph.

\paragraph{The a-priori router.} Before any grouping, one forward pass yields two label-free signals per concept: (i) the positive-only firing-Jaccard between each per-sub-context detector and the parent, and (ii) the parent's per-sub-context recall holes. The screening rule predicts the \emph{absorption regime} (where grouping helps) iff firing-Jaccard is low \emph{and} the parent has a recall hole, and the \emph{co-firing regime} (where supervised attribution wins and CCRG should not be used) otherwise.

# Testbeds, Baselines, and Protocol
\label{sec:setup}

\paragraph{Constructed testbeds.} We built four frozen, schema-standardized families (Table~\ref{tab:testbeds}) totalling $109{,}754$ examples. All are pure text/data artifacts---no SAE or model weights baked in---so absorption presence is an empirical question for the SAE run, not a construction artifact. Words for the spelling and non-spelling hierarchies are anchored in the real \texttt{gemma-2-2b} vocabulary and a pinned Pile revision, so they never derive from the latents being grouped. The first-letter testbed contributes $17{,}180$ examples over five letters (L/O/T/I/D) [ARTIFACT:art_dpYpjSn2Xvg3]; the non-spelling testbed contributes $24{,}128$ examples over a numeric-quantity hierarchy and a taxonomic is-a-country hierarchy [ARTIFACT:art_t2uUbjSwpd3t]; the toxicity family contributes $37{,}707$ examples from ParaDetox \citep{Logacheva2022} and civil\_comments \citep{Borkan2019} [ARTIFACT:art_8QO7pl6Pd8UQ]; and a supporting family contributes $30{,}739$ examples of CAD-IMDB sentiment \citep{Kaushik2019}, CEBaB aspect-sentiment \citep{Abraham2022}, and a bias\_in\_bios boundary-null \citep{DeArteaga2019} [ARTIFACT:art_21JWypIydPMX].

\begin{table}[t]
\centering
\small
\caption{Constructed testbeds. Counts are released examples. LB = load-bearing, NS = non-spelling spine, SP = supporting, BN = boundary-null.}
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

\paragraph{Baselines.} We compare CCRG units against fifteen baselines (Table~\ref{tab:baselines}), spanning raw latents, observational clusters (count-matched), dense probes (including a LEACE surface-invariant hyperplane), supervised oracle pools, label-free/oracle group-robustness probes, a random-eligible-$k$ pool (the easy floor), and---decisively---three \emph{non-random, label-free, count-matched} selectors (S-rec, S-prec, S-mag). The design isolates \emph{selection at matched pool size}: a unit win over (h) holds capacity fixed and varies how members are chosen; a unit win over (RE-$k$) holds eligibility and pooling fixed; and a unit win over the three S-selectors is what isolates the \emph{set-cover-specific} rule from any sensible label-free ranking.

\begin{table}[t]
\centering
\small
\caption{Baseline glossary. (b)/(c) are count-matched to the unit's member count $k$; (h) is count-and-pool-matched; (RE-$k$) is the random-eligible floor; (S-rec)/(S-prec)/(S-mag) are non-random label-free selectors count-matched to $k$.}
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
(h) & Count-and-pool-matched: max-pool over exactly $k$ SCR/TPP-selected directions \\
(i) & Unmatched difference-of-means / probe on raw labels \\
(j) & Oracle group-DRO probe with true sub-context labels (robustness upper bound) \\
(k) & Label-free group-inference probe (JTT/GEORGE-style) \\
(RE-$k$) & Random-eligible-$k$ pool: $k$ latents drawn at random from $E$, max-pooled \\
(S-rec) & \textbf{Top-$k$ by content-flip recall} \\
(S-prec) & \textbf{Top-$k$ by firing precision} \\
(S-mag) & \textbf{Top-$k$ by mean response magnitude} \\
\bottomrule
\end{tabular}
\end{table}

\paragraph{Statistics.} The primary statistical object is the per-concept paired bootstrap of the AUC difference ($B=10{,}000$, resampling whole content-flip pairs as clusters on the held-out test fold), with exact McNemar confirmatory tests and Holm--Bonferroni across headline claims; any accuracy comparison uses a comparison-matched Youden threshold so no baseline collapses to predict-all-positive. Encoding, gating, hardware, and software pins are deferred to Appendix~\ref{sec:repro}.

# Measured Auditability: method or empirical finding, not a theorem.
```

### [2] SYSTEM-USER prompt · 2026-06-18 04:23:23 UTC

```
<validation-feedback>
Attempt 1 failed validation.

You have not created the output file `.terminal_claude_agent_struct_out.json` yet. Use the Write tool to create it.

Please use the Write tool to overwrite `.terminal_claude_agent_struct_out.json` with corrected JSON. Do not invent new fields; match the schema you were given.
</validation-feedback>
```
