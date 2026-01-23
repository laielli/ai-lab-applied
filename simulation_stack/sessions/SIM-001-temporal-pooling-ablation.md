# Simulation Session: Temporal Pooling Ablation Results

- **ID**: SIM-001
- **Paper**: temporal-retrieval
- **Date**: 2026-01-23
- **Type**: experiment-update

---

## Q&A Transcript

### Advisor Questions

#### Q1: Is +2.4 R@1 a meaningful enough improvement for CVPR given the competitive landscape in text-to-video retrieval?

**Suggested Answer**: The +2.4 R@1 improvement (5.7% relative) is on the lower end for a CVPR main contribution. However, this is only the ablation study - the full method may include additional components. The consistent gains across R@1/5/10 suggest the improvement is robust rather than noise. We should contextualize against recent CVPR papers: typical improvements are 2-5 R@1 for methodological contributions. Our +2.4 is within range but not dominant.

**Action if Weak**: Run experiments on ActivityNet and DiDeMo to show consistent improvements across datasets. If gains are smaller there, the contribution may not be sufficient.

#### Q2: What's the minimal viable story here? Can we frame this as a new insight about temporal modeling rather than just an engineering improvement?

**Suggested Answer**: The key insight is that query-conditioned temporal weighting outperforms query-agnostic approaches (fixed attention only gives +0.8). This suggests videos have query-relevant temporal structure that can be exploited. The story is: "Videos contain query-specific temporal salience patterns, and learning to attend to them improves retrieval."

**Action if Weak**: Need qualitative analysis showing which frames get attended for different queries. Without this, the contribution feels incremental rather than insightful.

#### Q3: Should we target this deadline or wait for stronger results?

**Suggested Answer**: Given the current results, we're at the margin of acceptance. If additional datasets show consistent 2+ R@1 gains and we have compelling qualitative analysis, the deadline is feasible. If experiments show smaller gains elsewhere, we should wait and strengthen the method.

**Action if Weak**: Define clear go/no-go criteria before the deadline. If ActivityNet shows <1.5 R@1 gain, pivot to strengthening the method.

#### Q4: How does this position us against competing labs working on similar temporal modeling for retrieval?

**Suggested Answer**: Several groups (e.g., Microsoft Research Asia, FAIR) have explored temporal modeling for video understanding. Our contribution is specifically about query-conditioned temporal attention for retrieval. We need to survey recent work to ensure no direct overlap. The ablation study design (mean vs. max vs. fixed vs. query-conditioned) is a clean contribution that isolates the value of query-conditioning.

**Action if Weak**: Conduct thorough literature search for query-conditioned temporal attention in retrieval. If direct overlap exists, need to differentiate clearly.

### SME Questions

#### Q1: What's the variance across runs? Is +2.4 R@1 statistically significant?

**Suggested Answer**: We need to report this - currently only single-run results are shown. Standard practice is 3-5 runs with standard deviation. Given the improvement magnitude (+2.4), it should be significant, but we must verify.

**Follow-up Risk**: "Did you do significance testing?" If we only have single runs, this is a major weakness that could sink the paper.

#### Q2: The mean pooling baseline seems surprisingly strong at 42.3 R@1. Did you tune it properly or is there something special about your implementation?

**Suggested Answer**: The baseline follows standard practice: extract CLIP features for sampled frames (8-16 per video), mean pool, compute cosine similarity with text embedding. The 42.3 is consistent with reported numbers in recent papers using CLIP ViT-B/32 on MSRVTT 1K split. We should cite prior work showing similar baseline numbers to establish fairness.

**Follow-up Risk**: "Did you use the same hyperparameters for baseline and your method?" Need to confirm fair comparison - same learning rate, batch size, training schedule.

#### Q3: Why did you only report MdR when it's the same across all methods? What about MnR or other metrics?

**Suggested Answer**: MdR (median rank) being 2.0 for all methods suggests the methods mainly differ in their top-ranked predictions. We should add MnR (mean rank) and potentially nDCG if it discriminates. The identical MdR is actually interesting - it suggests our method improves precision at the top without hurting the overall ranking distribution.

**Follow-up Risk**: "Is the improvement concentrated in easy or hard examples?" Should add per-difficulty analysis if available.

#### Q4: The ablation only has 4 conditions. What about temporal transformers, hierarchical pooling, or other stronger baselines?

**Suggested Answer**: The current ablation isolates the value of query-conditioning specifically. Adding temporal transformers would introduce many additional variables. However, we should add at least one stronger baseline (e.g., X-Pool, TS2-Net temporal components) to show our method compares favorably to more complex approaches.

**Follow-up Risk**: "If you compared against X-Pool's temporal modeling, how would you fare?" Need concrete comparison point.

#### Q5: Did you control for computational cost? How much overhead does temporal attention add?

**Suggested Answer**: We haven't reported compute cost yet. Temporal attention adds minimal inference overhead (one attention layer over ~8-16 frames). Training cost depends on attention architecture. We should report FLOPs or inference time comparison.

**Follow-up Risk**: "Is the improvement worth the added complexity?" If temporal attention adds 2x compute for +2.4 R@1, reviewers may question the trade-off.

### Lay Researcher Questions

#### Q1: Why would we expect query-conditioned attention to help? What's the intuition?

**Suggested Answer**: Consider a query "person picks up a cup" - the action might happen in frames 10-15 of a 30-frame video. Mean pooling dilutes this signal with irrelevant frames. Query-conditioned attention can learn to focus on the action-relevant frames. The max pooling failure (40.8 vs. 42.3) suggests that multiple frames matter - we need soft attention, not hard selection.

#### Q2: How is "temporal attention" different from just using a text-video cross-attention mechanism?

**Suggested Answer**: Temporal attention here specifically refers to weighting frames based on query relevance, then aggregating. This is distinct from full cross-attention which would attend over frame patches. Our approach is more lightweight - we first get frame-level representations, then weight frames. Full cross-attention is more expensive but potentially more powerful.

#### Q3: The improvement seems small - would a user actually notice the difference between 42.3 and 44.7 R@1?

**Suggested Answer**: At scale, yes. In a system retrieving from millions of videos, +2.4 R@1 means the correct video appears at rank 1 for 2.4% more queries - that's potentially thousands of improved user experiences daily. However, we should acknowledge that +2.4 is incremental rather than transformative. The contribution is more about understanding temporal modeling than achieving SOTA.

#### Q4: What does "query-independent temporal weights" mean in the Fixed Attention ablation?

**Suggested Answer**: Fixed attention learns a set of temporal weights during training that are applied to all videos regardless of the query. For example, it might learn "frame 5 is usually important." In contrast, query-conditioned attention computes different weights for each query-video pair. The gap (43.1 vs. 44.7) shows that query-specific weighting matters.

#### Q5: Why is max pooling worse than mean pooling? Wouldn't the "best" frame be most representative?

**Suggested Answer**: Videos are not just their most salient frame - they capture processes, actions, and relationships over time. Max pooling loses this temporal coverage. For a query about an activity, we need information from multiple frames showing the activity progression. Mean pooling preserves more information, while max pooling discards context.

---

## Feedback Synthesis

### Strengths

- Clean ablation study design that isolates the value of query-conditioning
- Consistent improvements across R@1/5/10 metrics suggest robustness
- The insight that query-conditioned > query-independent attention is novel and actionable
- Baseline implementation appears fair (42.3 R@1 is reasonable for CLIP ViT-B/32)
- The failure of max pooling provides useful negative result about temporal modeling

### Weaknesses/Gaps

- No statistical significance testing (single run only)
- Only one dataset (MSRVTT) - unclear if findings generalize
- Missing compute cost comparison
- No qualitative analysis showing attention patterns
- No comparison against stronger temporal modeling baselines (X-Pool, TS2-Net)
- MdR identical across methods - need more discriminative metrics
- +2.4 R@1 is marginal for top-tier venue as sole contribution

### Contested Points

- Whether +2.4 R@1 constitutes sufficient contribution for CVPR (borderline)
- Whether query-conditioned temporal attention is novel enough vs. existing cross-attention methods
- Whether the MSRVTT 1K split is sufficient or if multiple datasets are required
- Trade-off between method complexity and improvement magnitude

---

## Action Items

| Priority | Description | Source | Route To |
|----------|-------------|--------|----------|
| P1 | Run 3-5 runs and report variance/significance | SME Q1 | experiment_stack/_inbox/ |
| P1 | Run experiments on ActivityNet and DiDeMo | Advisor Q1 | experiment_stack/_inbox/ |
| P1 | Add qualitative attention visualization | Advisor Q2 | figure_stack/_inbox/ |
| P2 | Add compute cost comparison (FLOPs/inference time) | SME Q5 | experiment_stack/_inbox/ |
| P2 | Compare against X-Pool/TS2-Net temporal modeling | SME Q4 | experiment_stack/_inbox/ |
| P2 | Add MnR metric to results table | SME Q3 | experiment_stack/_inbox/ |
| P3 | Literature search for query-conditioned temporal attention | Advisor Q4 | reading_stack/_inbox/ |

---

## Routing Log

| Action | Routed To | Entry Created |
|--------|-----------|---------------|
| Statistical significance testing | experiment_stack/_inbox/ | EXP-001 |
| Additional dataset experiments | experiment_stack/_inbox/ | EXP-002 |
| Attention visualization | figure_stack/_inbox/ | FIG-001 |
| Compute cost comparison | experiment_stack/_inbox/ | EXP-003 |
| Stronger baseline comparison | experiment_stack/_inbox/ | EXP-004 |
| Additional metrics (MnR) | experiment_stack/_inbox/ | EXP-005 |
| Literature search on query-conditioned attention | reading_stack/_inbox/ | PAPER-010 |
