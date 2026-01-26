# Simulation Session: TFS Experiment 6 Results

- **ID**: SIM-003
- **Paper**: IDEA-009-temporal-fourier-signatures
- **Date**: 2026-01-24
- **Type**: experiment-update

---

## Q&A Transcript

### Advisor Questions

#### Q1: Is +8.8% on 6.8% of queries enough for a publication? What venue is realistic here?

**Suggested Answer**: The +8.8% improvement on temporal queries is statistically meaningful (136 queries is not negligible), but the overall MSR-VTT tie at 90% R@10 means we cannot claim a general improvement. For a top venue (CVPR/ICCV main), we likely need either: (a) validation on additional datasets where temporal queries are more prevalent, or (b) a stronger theoretical contribution that justifies the method beyond empirical gains. A workshop paper or findings track is achievable with current results.

**Action if Weak**: Queue experiments on VATEX and DiDeMo to establish broader evidence. Consider reframing as a method paper with strong analysis rather than a "beats SOTA" paper.

#### Q2: How does this position us against attention pooling methods? Are we solving a problem that attention already handles?

**Suggested Answer**: Attention pooling achieves +2.9% vs mean on temporal queries (vs our +8.8%), so TFS provides a 2-3x larger improvement on these queries. However, attention is more flexible and does not require a trained projection. Our positioning should emphasize that TFS provides an explicit, interpretable mechanism for order encoding versus attention's implicit learned weighting. The information-theoretic analysis (effective dimensions, order reconstruction) provides novel understanding that attention-based work lacks.

**Action if Weak**: Run head-to-head comparison with more sophisticated attention variants (e.g., temporal self-attention). Strengthen the analysis story as the differentiator.

#### Q3: The synthetic features concern me. What is the path to real CLIP features, and how long will it take?

**Suggested Answer**: Synthetic features were a deliberate methodology choice to isolate the pooling mechanism from confounds in CLIP extraction (frame sampling, resolution, etc.). However, this is a legitimate concern for reviewers. Real CLIP extraction on MSR-VTT is straightforward (1-2 days implementation, ~8 GPU-hours extraction). We should run at least one validation experiment with real features before paper submission.

**Action if Weak**: Prioritize EXP with real CLIP features as P1 blocker.

#### Q4: What is the minimal viable paper here, and what is the timeline to get there?

**Suggested Answer**: Minimal viable paper requires: (1) current MSR-VTT results with confidence intervals (3 seeds minimum), (2) one additional dataset validation (VATEX preferred for temporal captions), (3) real CLIP feature validation experiment. Timeline: 2-3 weeks for experiments, 1 week for writeup. Target: workshop paper at nearest deadline, with option to expand for main track later.

**Action if Weak**: Create explicit experiment schedule with deadlines. Evaluate whether the timeline fits any upcoming deadlines.

### SME Questions

#### Q1: You only ran one random seed. What is the variance across runs? Could the +8.8% be within noise?

**Suggested Answer**: This is a valid concern. With synthetic features and a trained projection layer, there is variance from both feature generation and projection training. We should run 3-5 seeds and report mean +/- std. Given the effect size (+8.8% vs +2.9% for attention), I expect the difference to remain significant, but we need to verify this.

**Follow-up Risk**: "What if variance is 3-4%? Does your result hold?" -- Need to prepare for this scenario.

#### Q2: How did you classify temporal vs non-temporal queries? What is the inter-annotator agreement?

**Suggested Answer**: We used keyword-based classification (words like "before", "after", "then", "while", "first", "last", "sequence"). This is a heuristic approach, not human-annotated. We should acknowledge this limitation and ideally validate a sample with human annotation. The 6.8% rate may undercount temporal queries that use implicit temporal language.

**Follow-up Risk**: "Could selection bias in your keyword list inflate the improvement?" -- Should create and test an expanded keyword list, or sample for human validation.

#### Q3: The trained projection is essential (Table shows -10% without it). Does this undermine the claim of a general-purpose pooling method?

**Suggested Answer**: Yes, this is a limitation we need to acknowledge. The projection requirement means TFS is not a drop-in replacement for mean pooling. However, the projection training is lightweight (same cost as training a classifier head) and could be framed as "TFS-Trained" vs "TFS-Fixed" variants. We should explore fixed projections (e.g., identity, random orthogonal) to see if any approach narrows the gap.

**Follow-up Risk**: "What is the projection actually learning? Is it compensating for a flaw in TFS?" -- Run analysis on projection weights to understand what it learns.

#### Q4: Why does non-temporal performance degrade by 0.6%? Is there a precision/recall tradeoff?

**Suggested Answer**: The -0.6% degradation on non-temporal queries suggests TFS may over-emphasize order information that is irrelevant for those queries. This could be a specialization tradeoff: better temporal performance at slight cost to non-temporal. We should analyze error cases to understand if specific query types suffer.

**Follow-up Risk**: "Could you get the best of both worlds with a gating mechanism?" -- This could be future work but risks scope creep.

#### Q5: What recent temporal-aware retrieval methods should you compare against? Is attention pooling really the right baseline?

**Suggested Answer**: We should compare against: (1) temporal attention/positional encoding in video transformers, (2) methods like TAN (Temporal Alignment Network) if applicable, (3) recent work on video-text pretraining with temporal objectives. Attention pooling is necessary but not sufficient as a baseline.

**Follow-up Risk**: "You need to show TFS vs [specific recent method]" -- Queue literature search for recent temporal-aware retrieval methods.

### Lay Researcher Questions

#### Q1: Why would rotating embeddings preserve temporal order? Can you explain the intuition without math?

**Suggested Answer**: Imagine each frame's embedding as an arrow in high-dimensional space. Mean pooling just averages all the arrows together, losing any sense of which came first. TFS rotates each arrow by a different angle based on its position in the video. When you average the rotated arrows, the final direction depends on which arrows were rotated which way -- which depends on the order. If you shuffle the frames, each frame gets a different rotation, producing a different final direction. The rotation pattern is like a fingerprint of the sequence order.

#### Q2: 6.8% of queries are temporal. Is temporal understanding actually important for video retrieval, or is this a niche problem?

**Suggested Answer**: This is a fair challenge. Many current benchmarks have low temporal query density because they were designed for image-like retrieval. However, video's unique value IS temporal structure -- "man falls off bike then gets up" is different from "man on ground near bike." As video retrieval matures, we expect more temporally complex queries. TFS is preparing for that future. We should also test on datasets designed for temporal understanding (ActivityNet Captions, VATEX).

#### Q3: Why use synthetic features instead of just running CLIP? Does this make the results less believable?

**Suggested Answer**: Synthetic features let us isolate the pooling mechanism. Real CLIP extraction introduces confounds: How many frames? What resolution? Which CLIP variant? By generating features with the same distribution as CLIP but with known properties, we can be certain any differences come from the pooling method. That said, we acknowledge this limits ecological validity and plan to validate with real CLIP features.

#### Q4: What is the simplest baseline that might achieve similar results? Did you try just concatenating frame positions as features?

**Suggested Answer**: Good question. Simpler approaches include: (1) positional embeddings added to frames (like transformers), (2) learned frame weights based on position, (3) temporal pyramid pooling. We compared against attention pooling (which implicitly learns position) but should include more explicit positional baselines. The rotation approach is novel because it preserves order through the aggregation itself, not by adding information.

#### Q5: The projection layer seems to do a lot of work. Is the rotation actually necessary, or is the projection layer doing all the heavy lifting?

**Suggested Answer**: The ablation shows projection alone (without TFS) does not help mean pooling. The projection enables cross-modal alignment after rotation, but the rotation is what creates the order-sensitive representation. We can verify this by showing that permutation sensitivity (Exp 1A) exists before any projection. The projection is necessary but not sufficient; the rotation is the key mechanism.

---

## Feedback Synthesis

### Strengths

1. **Clear mechanism validation**: The variance ratio experiments (Exp 1A) provide unambiguous evidence that TFS preserves order information, a clean scientific demonstration.
2. **Information-theoretic depth**: The effective dimension and order reconstruction analyses go beyond standard retrieval metrics, providing novel insight into what the pooling methods actually capture.
3. **Honest scope adjustment**: Revising claims from "temporal dynamics" to "order preservation" demonstrates intellectual rigor and sets appropriate expectations.
4. **Attention comparison validates approach**: The fact that attention pooling falls between mean and TFS suggests temporal awareness matters, and TFS provides more explicit encoding.
5. **Actionable results table**: The breakdown by temporal vs non-temporal queries is compelling and tells a clear story.

### Weaknesses/Gaps

1. **Single seed, no variance estimates**: Critical gap that undermines statistical claims. Must be addressed before any submission.
2. **Synthetic features only**: While methodologically justified, reviewers will question ecological validity. At minimum need one real-CLIP validation.
3. **Small temporal query sample**: 136 queries is defensible but borderline. Would benefit from larger temporal test set or additional datasets.
4. **Trained projection requirement**: Reduces the "simple drop-in" appeal. Need to either fix this limitation or reframe the contribution.
5. **Limited baseline comparisons**: Attention pooling alone may not satisfy reviewers expecting comparison to recent temporal-aware methods.
6. **No theoretical analysis**: Why do rotations work better than other positional encoding schemes? Missing formal justification.

### Contested Points

1. **Contribution sufficiency**: Some reviewers will see +8.8% on temporal queries as strong; others will dismiss it as too narrow. Framing is crucial.
2. **Synthetic vs real features**: Methodology reviewers may appreciate the controlled setting; empirical reviewers may reject it. Need both.
3. **Order preservation vs temporal reasoning**: The revised framing is honest but may seem like a reduced claim. Need to argue why order preservation is the right goal.

---

## Action Items

| Priority | Description | Source | Route To |
|----------|-------------|--------|----------|
| P1 | Run 3-5 random seeds for variance estimates | SME Q1 | experiment_stack/_inbox/ |
| P1 | Extract and test with real CLIP features | Advisor Q3, Lay Q3 | experiment_stack/_inbox/ |
| P2 | Validate temporal query classification with human sample | SME Q2 | experiment_stack/_inbox/ |
| P2 | Test on VATEX dataset (temporal captions) | Advisor Q1, Lay Q2 | experiment_stack/_inbox/ |
| P2 | Search for recent temporal-aware retrieval methods | SME Q5 | reading_stack/_inbox/ |
| P2 | Create figure showing order preservation intuition | Lay Q1 | figure_stack/_inbox/ |
| P3 | Explore fixed projection alternatives | SME Q3 | experiment_stack/_inbox/ |
| P3 | Analyze non-temporal query error cases | SME Q4 | experiment_stack/_inbox/ |
| P3 | Write framing section on order preservation contribution | Advisor Q4, Contested | writer_stack/_inbox/ |

---

## Routing Log

| Action | Routed To | Entry Created |
|--------|-----------|---------------|
| Multi-seed variance experiment | experiment_stack/_inbox/ | EXP-007-tfs-variance-seeds.md |
| Real CLIP features experiment | experiment_stack/_inbox/ | EXP-008-tfs-real-clip-features.md |
| Temporal classification validation | experiment_stack/_inbox/ | EXP-009-temporal-query-validation.md |
| VATEX dataset validation | (existing) | EXP-006 already covers this |
| Literature search: temporal retrieval | reading_stack/_inbox/ | PAPER-012-temporal-retrieval-methods.md |
| Order preservation intuition figure | figure_stack/_inbox/ | FIG-003-order-preservation-intuition.md |
| Fixed projection ablation | experiment_stack/_inbox/ | EXP-010-fixed-projection-ablation.md |
| Contribution framing writeup | writer_stack/_inbox/ | WRITE-002-order-preservation-framing.md |
