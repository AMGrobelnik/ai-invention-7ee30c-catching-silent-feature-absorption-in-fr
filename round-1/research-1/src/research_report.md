# Two-Track CCRG Implementation Dossier: SAE Pipeline, 11 Baselines, Protocols

## Summary

A decision-complete, code-ready implementation blueprint for the two-track Counterfactual Co-Response Grouping (CCRG) method on frozen Gemma Scope SAEs. Pins the SAE encoding pipeline (defensive from_pretrained loader, JumpReLU firing=encode>0, hook blocks.12.hook_resid_post), the C-track (signed soft-threshold + leidenalg RBConfigurationVertexPartition) and K-track (anchored greedy max-coverage) algorithm with all thresholds, all eleven baselines (a)-(k) as runnable specs (LEACE for f, SAEBench SCR/TPP for g/h, JTT/GEORGE/group-DRO for j/k), the AxBench steering protocol (harmonic-mean LLM-judge 0/1/2), a corrected model-diffing recipe (shared frozen pt-SAE on gemma-2-2b vs gemma-2-2b-it because no gemma-scope-2b-it SAE exists), the statistics plan (paired bootstrap, exact McNemar, MDE n_min=150, Holm-Bonferroni), and a fully-verified 30+ citation table including all four high-risk future-dated arXiv IDs (all resolve).

## Research Findings

This dossier pins every implementation decision for the two-track CCRG method so iteration-2 code can be written with zero methodology ambiguity. All four high-fabrication-risk future-dated arXiv IDs RESOLVE to real papers, and no fabricated citation was found.

WORKSTREAM A — SAE PIPELINE. The load-bearing SAE is sae_lens release 'gemma-scope-2b-pt-res-canonical', sae_id 'layer_12/width_16k/canonical' on google/gemma-2-2b, hook 'blocks.12.hook_resid_post'; 'canonical' means average L0 nearest 100 [1][3]. CRITICAL GOTCHA: SAE.from_pretrained changed from a 3-tuple (sae,cfg,sparsity) (<=v5) to returning the SAE object alone (v6+), with the tuple form deprecated and load_from_pretrained_with_cfg_and_sparsity as the explicit backward path — so a defensive `sae = ret[0] if isinstance(ret,tuple) else ret` loader is required [2]. Gemma Scope SAEs are JumpReLU, so 'firing' = sae.encode(acts)>0 (threshold applied inside encode) [1][4]. MODEL-DIFFING TRAP CAUGHT: there is NO gemma-scope-2b-it residual SAE (0 matches in the SAELens table); the only IT residual release is gemma-scope-9b-it-res, and the jbloom Gemma-2b-IT SAEs are Gemma-1 (incompatible architecture) [5][6]. The pinned recipe is therefore to apply the single frozen pt-SAE as a shared dictionary to activations from BOTH google/gemma-2-2b and google/gemma-2-2b-it; the 9B pt/it pair is a stretch fallback [5]. Layer 12 is the densest Gemma Scope residual layer (widths 16k/32k/65k/131k/262k/524k/1M), so the width-robustness axis 16k->65k/canonical is clean [4]; absorption worsens at wider SAEs [15][37]. Encode via HookedSAETransformer (add_sae + run_with_cache reading '...hook_sae_acts_post', or run_with_cache_with_saes) or manual run_with_cache + sae.encode; mean-pool over tokens (last-token fallback for positional concepts); residual cache dominates memory so chunk+pool+discard in fp16 [1]. Neuronpedia feature JSON: GET https://www.neuronpedia.org/api/feature/gemma-2-2b/12-gemmascope-res-16k/{index} (auto-interp label, top activations, logit-lens tokens), python wrapper neuronpedia-python [7][8][42].

WORKSTREAM B — CCRG ALGORITHM. STEP1 builds content-response matrix R[L x |P|], r_l(p)=a_l(x_on)-a_l(x_off); content-responsive prefilter = mean response above the 95th pct of a within-concept on/off shuffle null; cover set C_l requires firing AND per-latent content-response precision>=0.7 [10][11]. STEP2 C-TRACK (splitting): affinity from positive-part/signed-soft-threshold of Spearman correlation of response profiles (DiffCoEx ((1+rho)/2)^beta or max(rho,0)^beta, beta=6 per WGCNA A=|cor|^beta) [10][11], then leidenalg.find_partition with RBConfigurationVertexPartition, weights=g.es['weight'], resolution_parameter=gamma (RBConfiguration has the resolution knob and needs positive weights; ModularityVertexPartition lacks resolution) [9]; gamma + community count fixed by bootstrap-ARI stability (resample pairs, max mean adjusted_rand_score exceeding shuffle null) [12]. STEP3 K-TRACK (absorption): anchor=argmax|C_l| chosen from PAIRS ONLY (non-circular vs the Chanin diagnostic), then greedy max-coverage adding l*=argmax|C_l intersect Holes| subject to firing-Jaccard<0.1, per-member precision>=0.7, marginal gain>=0.05 with bootstrap CI excluding 0 — justified by the (1-1/e) submodular/set-cover guarantee (Nemhauser-Wolsey-Fisher 1978; Feige 1998) [13][14]; correlation cannot group disjoint-support absorbers, which is why the K-track exists [15][37]. STEP4 reconciliation makes each unit a pure C-community, pure K-cover, or hybrid; de-dup assigns each latent to its highest-coverage-gain unit. STEP5 admission = (signature C: within-unit mean response correlation > shuffle null) OR (signature K: pooled-max AUC minus best-single-member AUC > AUC-matched random-k null, plus k in {2,3} absolute gain>=0.05 with CI, plus mutual-exclusivity+precision), AND unit-level surface invariance vs a surface-shuffle null; report false-admit under both all-latent and AUC-matched random-k nulls (target<=0.05); max-pool for detection (sum-pool ablation only). TIER-0 PILOT runs STEP3 on first-letter content-flip pairs and checks precision/recall of proposed members vs the Chanin diagnostic's parent+absorbers against a random-membership null, with an explicit honest-negative branch [15]. The absorption diagnostic (B7) uses sae_spelling.probing.train_binary_probe (parent=max encoder-cosine with LR probe) and sae_spelling.feature_ablation.calculate_individual_feature_ablations (absorber=latent whose ablation most shifts the concept logit); FeatureAbsorptionCalculator + first_letter_formatter; the form-free generalization and minimal-pair sourcing live in research_iter1_dir2 [15][16].

WORKSTREAM C — ELEVEN BASELINES. (a) best raw latent by held-out AUC/F1; (b) co-firing clusters via sklearn.cluster.HDBSCAN count-matched to k; (c) decoder-cosine clusters count-matched to k; (d) diff-of-means on residual deltas; (e) LogisticRegression on residual deltas; (f) LEACE surface-invariant probe via concept_erasure.LeaceEraser.fit(X,Z_surface) then eraser(X) (LeaceEraser is a frozen dataclass proj_left/proj_right/bias; __call__ erases; z reshaped (n,k) so one-hot or continuous) then fit content probe [17][18]; (g) SAEBench SCR/TPP top-N oracle pool — latents ranked by LR-probe attribution / maximum-mean-difference, k in {5,10,20,50,100,500} default 20 [19][21]; (h) same top-N latents' raw residual decoder directions W_dec[i], max-pooled, isolating selection from marginal attribution at fixed pool size; (i) unmatched diff-of-means/probe on raw labels; (j) oracle group-DRO probe = max-over-groups average loss with strong L2/early-stopping (Sagawa) [22], group-aware-prior alt Mind-the-GAP [28]; (k) label-free JTT (ERM->upweight misclassified->retrain) primary, GEORGE fallback (cluster features->group-DRO), competitor family EIIL/LfF/Diverse-Prototypical-Ensembles [23][24][25][26][27]. SAEBench stable_paper_version is the pinned branch; a 2026 audit (2605.18229) flags SCR/TPP reliability, so (g)/(h) are reference oracles not ground truth [20][43].

WORKSTREAM D — PROTOCOLS. Steering (AxBench): direction = unit-normalized sum of member decoder vectors, alpha=c*R with c in {0,.5,1,2,4,8} added at blocks.12.hook_resid_post via run_with_hooks; collateral = full-vocab next-token KL on unrelated prompts; scoring = harmonic mean of three LLM-judge subscores {concept, instruct, fluency} each 0/1/2 (fluency is LLM-judge, NOT perplexity), ~10 Alpaca instructions/concept; minimal version always-run, decisive Tier-2 [29]. Model-diffing: shared frozen pt-SAE on base vs IT, measure AUC of detecting which model produced the unit-pooled activation vs best-single-latent above a shuffle null [1][5]. Statistics: PRIMARY = within-family paired bootstrap CIs B=10000 on per-example correctness diffs (cross-family descriptive only); central unit-minus-(g)/(h) gap uses paired bootstrap + exact McNemar (statsmodels.stats.contingency_tables.mcnemar(table,exact=True)), reporting the gap SIGN and its SLOPE vs measured reweighting; a-priori MDE n~7.84[p1(1-p1)+p2(1-p2)]/Delta^2 gives ~91/167/384 positives for Delta=.20/.15/.10, pre-register n_min=150 per under-served sub-context; multiplicity via Holm-Bonferroni (statsmodels.stats.multitest.multipletests method='holm'); cluster stability via sklearn.metrics.adjusted_rand_score vs shuffle null. Auditability: MEASURED repair loop (recall hole on (f) -> read KG -> add covering absorber -> recall before/after with paired-bootstrap CI vs random-latent-addition control) [38], plus LLM-judge member-labeling (Neuronpedia logit-lens tokens+contexts -> OpenRouter judge -> compare to KG edge vs shuffle null); cheap OpenRouter model, total LLM spend << $10 with caching.

WORKSTREAM E — CITATIONS. All resolve. Future-dated/high-risk all real: 2606.06333 SASA (Dalili & Mahdavi, Penn State, Jun 2026) [37]; 2604.23829 Domain-Filtered KGs from SAE Features (Winnicki/Gnanasekaran/Darve, Stanford, Apr 2026) [38]; 2506.18141 Sparse Feature Coactivation (Deng et al., Jun 2025) [39]; 2408.00657 Disentangling Dense Embeddings ('feature families', O'Neill et al.) [40]. Foundations verified: DiffCoEx BMC Bioinformatics 2010 [10], WGCNA Zhang&Horvath 2005 [11], Leiden Traag 2019 [12], NWF 1978 [13], Feige 1998 JACM [14], Sagawa 1911.08731 [22], JTT/GEORGE/EIIL/LfF/DPE [23-27], CEBaB/Veitch/Kaushik-CAD-1909.12434/ParaDetox [32-35], AxBench ICML 2025 (not ICLR) [29], LEACE [18], SCR/TPP origin 2411.18895 [21], SAEBench 2503.09532 [19], canonical-units 2502.04878 [30], feature-hedging 2505.11756 [31], CDLC 2505.07073 (vision/diffusion analog) [36].

## Sources

[1] [SAELens Usage docs](https://decoderesearch.github.io/SAELens/dev/usage/) — from_pretrained load pattern, HookedSAETransformer add_sae/run_with_cache/run_with_cache_with_saes, hook_sae_acts_post, sae.encode, hook blocks.12.hook_resid_post

[2] [SAELens Migrating to v6](https://decoderesearch.github.io/SAELens/latest/migrating/) — from_pretrained return-signature change: 3-tuple (deprecated) -> SAE object; load_from_pretrained_with_cfg_and_sparsity backward-compat

[3] [google/gemma-scope-2b-pt-res model card](https://huggingface.co/google/gemma-scope-2b-pt-res) — Load strings for layer_12/width_16k/canonical; canonical = avg L0 nearest 100; config snapshot 2024-10-22

[4] [google/gemma-scope main model card](https://huggingface.co/google/gemma-scope) — Widths per layer (layer 12 has 16k/32k/65k/131k/262k/524k/1M); JumpReLU SAE training and threshold parameter

[5] [SAELens Supported SAEs table](https://decoderesearch.github.io/SAELens/sae_table/) — 0 gemma-scope-2b-it entries; gemma-scope-9b-it-res(-canonical) exists; gemma-scope-2b-pt-res(-canonical) and width_65k present

[6] [jbloom/Gemma-2b-IT-Residual-Stream-SAEs](https://huggingface.co/jbloom/Gemma-2b-IT-Residual-Stream-SAEs) — IT SAEs trained on Gemma-1 2b (gemma_2b_blocks.10... hooks), loadable as gemma-2b-it-res-jb; incompatible with gemma-2-2b architecture

[7] [Neuronpedia API & Exports docs](https://docs.neuronpedia.org/api) — GET /api/feature/{model}/{source}/{index} returns feature JSON (explanations, activations); interactive docs at neuronpedia.org/api-doc

[8] [Neuronpedia feature page (gemma-2-2b 12-gemmascope-res-16k)](https://www.neuronpedia.org/gemma-2-2b/12-gemmascope-res-16k/6810) — Confirms source id format '12-gemmascope-res-16k' for layer-12 16k residual; 16384 features at blocks.12.hook_resid_post

[9] [leidenalg reference](https://leidenalg.readthedocs.io/en/stable/reference.html) — find_partition + RBConfigurationVertexPartition(graph, weights, resolution_parameter); resolution knob; well-defined for positive weights

[10] [DiffCoEx (Tesson, Breitling, Jansen) BMC Bioinformatics 2010](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/1471-2105-11-497) — Differential co-expression via WGCNA soft-threshold; sign-aware module discovery on correlation; source for C-track transfer

[11] [Zhang & Horvath 2005, A general framework for WGCNA](https://pubmed.ncbi.nlm.nih.gov/16646834/) — Soft-threshold adjacency A_ij=|cor|^beta; scale-free topology criterion for beta; emphasizes strong correlations

[12] [Traag, Waltman, van Eck 2019, From Louvain to Leiden](https://www.nature.com/articles/s41598-019-41695-z) — Leiden algorithm guaranteeing well-connected communities (Scientific Reports; arXiv 1810.08473)

[13] [Nemhauser, Wolsey, Fisher 1978, Maximizing submodular set functions-I](https://link.springer.com/article/10.1007/BF01588971) — Greedy (1-1/e) approximation under cardinality; Math. Programming 14:265-294; K-track justification

[14] [Feige 1998, A threshold of ln n for approximating set cover](https://dblp.uni-trier.de/rec/journals/jacm/Feige98.html) — Set-cover ln n threshold; max-k-cover (1-1/e) optimal; JACM 45(4):634-652; K-track justification

[15] [A is for Absorption (Chanin et al.)](https://arxiv.org/abs/2409.14507) — Feature splitting/absorption; absorber fires complementarily to parent; first-letter case study; NeurIPS 2024; Tier-0 oracle

[16] [lasr-spelling/sae-spelling repo](https://github.com/lasr-spelling/sae-spelling) — probing.train_binary_probe (parent=max encoder-cosine vs LR probe); feature_ablation.calculate_individual_feature_ablations; FeatureAbsorptionCalculator; first_letter_formatter

[17] [EleutherAI concept-erasure leace.py](https://github.com/EleutherAI/concept-erasure/blob/main/concept_erasure/leace.py) — LeaceEraser dataclass(proj_left,proj_right,bias); classmethod fit(x,z); __call__ erases; LeaceFitter.update(x,z)+.eraser; z reshaped (n,-1) so one-hot or continuous

[18] [LEACE: Perfect Linear Concept Erasure in Closed Form](https://arxiv.org/abs/2306.03819) — Closed-form erasure preventing all linear classifiers from detecting a concept with minimal damage; baseline (f); NeurIPS 2023

[19] [SAEBench (Karvonen et al.)](https://arxiv.org/abs/2503.09532) — SCR/TPP select latents by probe attribution / maximum-mean-difference; k in {5,10,20,50,100,500}, default 20; absorption + sparse-probing metrics

[20] [adamkarvonen/SAEBench repo](https://github.com/adamkarvonen/SAEBench) — Reference implementation; use stable_paper_version branch for pinned deps for SCR/TPP latent selection (g)/(h)

[21] [Evaluating SAEs on Targeted Concept Erasure Tasks](https://arxiv.org/abs/2411.18895) — Origin of SCR (from SHIFT) and TPP; per-class probes, delete latents most causally relevant to one probe, measure targeted degradation

[22] [Sagawa et al., Distributionally Robust Neural Networks (group-DRO)](https://arxiv.org/abs/1911.08731) — Worst-group loss = max over groups of average loss; needs strong L2/early-stopping; baseline (j); ICLR 2020; repo kohpangwei/group_DRO

[23] [Just Train Twice (JTT)](https://arxiv.org/abs/2107.09044) — Two-stage: ERM then upweight misclassified and retrain; label-free group robustness; baseline (k) primary; repo anniesch/jtt

[24] [No Subclass Left Behind (GEORGE)](https://arxiv.org/abs/2011.12945) — Cluster deep features as noisy subclasses, then group-DRO; baseline (k) fallback; NeurIPS 2020

[25] [Environment Inference for Invariant Learning (EIIL)](https://arxiv.org/abs/2010.07249) — Infer environment partitions for invariant learning without given groups; (k) competitor family; ICML 2021

[26] [Learning from Failure (LfF)](https://arxiv.org/abs/2007.02561) — Train biased net + debiased net upweighting samples against the bias; (k) competitor family; NeurIPS 2020

[27] [Diverse Prototypical Ensembles Improve Robustness to Subpopulation Shift](https://arxiv.org/abs/2505.23027) — Ensemble of diverse prototype classifiers, no group labels; (k) competitor family; ICML 2025; repo minhto2802/dpe4subpop

[28] [Mind the GAP: Group-Aware Priors](https://arxiv.org/abs/2403.09869) — ERM then group-aware prior favoring high-worst-group params; (j) group-aware alternative; AISTATS 2024

[29] [AxBench (Wu et al.)](https://arxiv.org/abs/2501.17148) — Steering scored as harmonic mean of LLM-judge {concept,instruct,fluency} each 0/1/2; DiffMean baseline; ICML 2025; repo stanfordnlp/axbench

[30] [Sparse Autoencoders Do Not Find Canonical Units of Analysis](https://arxiv.org/abs/2502.04878) — SAE stitching (incomplete) + meta-SAEs (non-atomic); larger SAEs do not yield canonical units; ICLR 2025; motivation

[31] [Feature Hedging: Correlated Features Break Narrow SAEs](https://arxiv.org/abs/2505.11756) — Narrow SAEs merge correlated features (hedging) via reconstruction loss; worse the narrower; motivation

[32] [CEBaB (Abraham et al.)](https://arxiv.org/abs/2205.14140) — Restaurant reviews with human counterfactuals over 4 aspects (food/service/ambiance/noise), 3 labels; 2299->15089 texts; NeurIPS 2022

[33] [Counterfactual Invariance to Spurious Correlations (Veitch et al.)](https://arxiv.org/abs/2106.00545) — Formalizes counterfactual invariance; surface-invariance theoretical grounding; NeurIPS 2021

[34] [Kaushik et al., Counterfactually-Augmented Data (CAD)](https://arxiv.org/abs/1909.12434) — Human counterfactual revisions for sentiment/NLI; ICLR 2020; repo acmi-lab/counterfactually-augmented-data; supporting testbed

[35] [ParaDetox (Logacheva et al.)](https://aclanthology.org/2022.acl-long.469/) — Parallel toxic/neutral paraphrase pairs (>10k English); ACL 2022; repo s-nlp/paradetox; toxicity minimal pairs

[36] [CDLC: Concept Directions via Latent Clustering](https://arxiv.org/abs/2505.07073) — Clusters latent difference vectors from factual/counterfactual (diffusion) image pairs; vision analog of clustering counterfactual diffs

[37] [Subspace-Aware Sparse Autoencoders (SASA)](https://arxiv.org/abs/2606.06333) — VERIFIED REAL (Dalili & Mahdavi, Penn State, Jun 2026): single-direction decoders force feature splitting; learned decoder subspaces + Top-s group gating; motivation

[38] [Domain-Filtered Knowledge Graphs from SAE Features](https://arxiv.org/abs/2604.23829) — VERIFIED REAL (Winnicki/Gnanasekaran/Darve, Stanford, Apr 2026): contrastive domain filtering, co-occurrence + transcoder mechanism graphs, automated edge labeling; feature-level KG

[39] [Sparse Feature Coactivation Reveals (Causal/Composable) Semantic Modules](https://arxiv.org/abs/2506.18141) — VERIFIED REAL (Deng et al., Jun 2025): SAE-feature coactivation from few prompts yields composable, causally-ablatable concept/relation modules; precedent

[40] [Disentangling Dense Embeddings with SAEs (O'Neill et al.)](https://arxiv.org/abs/2408.00657) — VERIFIED REAL: SAEs on dense text embeddings; introduces 'feature families' at varying abstraction; steerable semantic search; precedent for cluster-level units

[41] [Gemma Scope (Lieberum et al.)](https://arxiv.org/abs/2408.05147) — JumpReLU SAEs across all layers of Gemma 2 2b/9b; defines the pretrained SAE suite used here

[42] [neuronpedia-python library](https://github.com/hijohnnylin/neuronpedia-python) — Python wrapper (SAEFeature.get(model,source,index)) for the Neuronpedia API; batch feature pulls

[43] [Are Sparse Autoencoder Benchmarks Reliable?](https://arxiv.org/abs/2605.18229) — 2026 audit: SCR/TPP fail multiple evaluation lenses at canonical settings; honest caveat that (g)/(h) are reference oracles not ground truth

## Follow-up Questions

- What is the exact SAE.from_pretrained return signature and W_dec orientation on the sae_lens version actually installed in the iteration-2 environment, and does sae.encode return post-JumpReLU activations (so firing == encode>0)?
- Does the frozen gemma-scope-2b-pt-res-canonical SAE encode google/gemma-2-2b-it activations cleanly under HookedSAETransformer for the shared-dictionary model-diffing recipe, or must the 9B pt/it pair be used (breaking the single-GPU budget)?
- In SAEBench stable_paper_version, which exact module/function emits the per-latent SCR/TPP attribution score and is the selection by |probe weight|, probe-weight x mean-activation, or attribution patching — and what default N (canonical k=20 vs unit-k count-matched) should baselines (g)/(h) use?
- What are Neuronpedia's batch rate limits / API-key requirements and the exact JSON field names for logit-lens top-promoted tokens, needed for the auditability LLM-judge member-labeling demo?

---
*Generated by AI Inventor Pipeline*
