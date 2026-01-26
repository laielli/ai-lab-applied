# Simulation Session: IDEA-003 Intermediate Layer Probing Results

- **ID**: SIM-005
- **Paper**: idea-003-avg-pooling
- **Date**: 2026-01-24
- **Type**: experiment-update

---

## Q&A Transcript

### Advisor Questions

#### Q1: Is a 7% accuracy improvement on a synthetic binary classification task enough for a main conference paper?

**Suggested Answer**: Alone, no. 64.3% vs 57.4% on a binary classification probe is a modest signal. However, this finding serves as evidence for our core hypothesis about where temporal information lives in PE. The paper contribution is the *understanding* - why average pooling works - not the probe accuracy itself. We would frame this as an analysis paper with implications for method design, not as a method paper. The gain becomes meaningful if we can show it translates to actual retrieval performance.

**Action if Weak**: Need to run retrieval experiments using intermediate layer features (layer 10 vs layer 23) and show actual R@1/R@5 improvements on benchmarks like K400 or MSR-VTT.

#### Q2: What is the minimal viable paper here - analysis-only or do we need a method contribution?

**Suggested Answer**: There are two viable paths:

1. **Analysis paper** (workshop-quality or short paper): Document the paradox, show the layer probing results, explain why average pooling works. Contribution is scientific understanding.

2. **Method + Analysis paper** (main conference): Add "temporal alignment" - a simple method that uses intermediate layer features (layer 10) for temporal matching while keeping output layer for language alignment. Show retrieval gains.

Given our finding that layer 10 has ~7% more temporal signal, option 2 is more compelling but requires additional experiments.

**Action if Weak**: Clarify paper positioning in writing task. If analysis-only, target workshop venues (e.g., CVPR Video Understanding Workshop). If method+analysis, need temporal alignment experiments.

#### Q3: How does this compete with concurrent work on temporal modeling in video-language models?

**Suggested Answer**: Most temporal modeling work focuses on *adding* temporal mechanisms (temporal attention, token mixing, etc.). Our angle is different: we show that temporal information already exists in intermediate layers and gets compressed out. This is complementary - understanding the baseline helps design better methods. We should survey recent work on layer-wise representations in vision-language models to position ourselves.

**Action if Weak**: Literature review on layer-wise analysis of CLIP-family models. Check arxiv for concurrent work on temporal features in PE specifically.

#### Q4: Given our deadline constraints, is pursuing temporal alignment worth the compute investment?

**Suggested Answer**: The core probing experiments are complete and cost-efficient (single GPU). Temporal alignment would require:
- Implementing layer-selection mechanism
- Re-running retrieval on K400, MSR-VTT, VATEX
- Ablating which layer is optimal

Estimated cost: 24-48 GPU-hours. If successful, this transforms from analysis paper to method paper. Recommend a quick pilot: extract layer 10 features, run simple retrieval with average pooling, compare to layer 23. If we see gains, proceed; if not, write analysis paper.

**Action if Weak**: Define quick pilot experiment (EXP-XXX) with go/no-go criteria before committing to full temporal alignment.

#### Q5: Should we consider this paper alongside IDEA-009 (Temporal Fourier Signatures) or are they separate stories?

**Suggested Answer**: They are complementary but separable:
- IDEA-003: Explains *why* average pooling works (temporal info in intermediate layers)
- IDEA-009: Proposes *what* to do about it (Fourier signatures for temporal modeling)

IDEA-003 could be a short paper or workshop paper that establishes the understanding. IDEA-009 builds on that to propose a method. Alternatively, combine them: understanding + method in one paper. Recommend keeping separate for now - IDEA-003 is more mature.

**Action if Weak**: Write decision document comparing paper strategies: (1) IDEA-003 alone, (2) IDEA-009 alone, (3) combined.

---

### SME Questions

#### Q1: Your probe is logistic regression on concatenated frame pairs. Did you try other architectures? A linear probe might be too weak to detect complex temporal relationships.

**Suggested Answer**: We chose logistic regression deliberately - it's a standard linear probe that tests whether the information is *linearly accessible* in the representation. If temporal order is not linearly decodable, it's less likely to be useful for downstream tasks that use linear projections (like CLIP's joint embedding). That said, we should run an MLP probe as an upper bound to see if there's additional non-linear temporal signal.

**Follow-up Risk**: "What if MLP shows much higher accuracy? Wouldn't that change your conclusions?" Response: Yes, if MLP at output layer matches MLP at layer 10, it would suggest the information is there but non-linearly encoded. We should test this.

#### Q2: 150 videos with 8 frames each seems limited. How do you know this generalizes? What's the variance across videos?

**Suggested Answer**: 150 videos is a reasonable sample for probing experiments (similar to CLIP's internal probing studies). We have 67,200 training pairs which provides statistical power. However, we should report per-video variance and bootstrap confidence intervals. We should also verify on a held-out set from a different domain (e.g., VATEX videos) to check generalization.

**Follow-up Risk**: "What if the pattern doesn't hold on VATEX?" Response: This is a legitimate concern. We should add a cross-dataset validation experiment.

#### Q3: The layer-by-layer pattern shows some non-monotonicity (layer 15 drops, layer 19 rises). How do you explain this?

**Suggested Answer**: This is actually consistent with how transformers work. Different layers specialize for different representations - layer 15-17 might be optimizing for semantic abstraction while layer 19 might have some residual temporal signal. The key finding is that the *peak* is at layer 10, well before the output. We should visualize this as a proper curve plot with error bars to show the overall trend.

**Follow-up Risk**: "Is layer 10 robustly the peak across different video types?" Response: We should stratify by video characteristics (duration, motion intensity) to check robustness.

#### Q4: You train the probe on frame pairs from the same video. What about pairs across videos? Is the probe just learning video identity?

**Suggested Answer**: All pairs are within-video, so the probe must distinguish temporal order, not video identity. The random baseline of 50% confirms we're measuring temporal discrimination, not video-level features. As a control, we could verify by training on shuffled labels - accuracy should drop to 50%.

**Follow-up Risk**: "But videos have different visual characteristics over time. Maybe the probe is learning 'later frames are darker' or similar artifacts?" Response: Valid concern. We should test on videos with controlled lighting or add a domain shift control.

#### Q5: Why layer 10 specifically? Does this relate to PE's architecture choices or layer-specific training objectives?

**Suggested Answer**: PE doesn't have layer-specific objectives - it uses standard contrastive training on image-text pairs with the final layer output. Layer 10 being the temporal peak might reflect when spatial features are consolidated before semantic abstraction begins. This aligns with other work showing different information peaks at different layers. We should cite the PE paper's own findings about spatial feature layers peaking around 18-20.

**Follow-up Risk**: "Is layer 10 the peak because of temporal information or because it's pre-semantic-compression?" Response: These are not mutually exclusive. Both temporal and fine-grained spatial information might be lost in later layers as the model optimizes for language alignment.

---

### Lay Researcher Questions

#### Q1: Can you explain what "relative temporal order" means vs "absolute position"? I'm confused about the distinction.

**Suggested Answer**:
- **Absolute position**: "This is frame 5 out of 10" - knowing the exact location in the sequence
- **Relative order**: "Frame A comes before Frame B" - knowing which of two frames is earlier

Our Exp 1.2 showed PE gets 12.5% accuracy on absolute position (random is 12.5% for 8-way classification), meaning it encodes no absolute position. But Exp 3.1 shows 64.3% on relative order (random is 50%), meaning it does encode relative relationships. This is actually common in transformers without positional encoding - they can learn "before/after" from content without knowing "exactly when."

#### Q2: Why would we expect a model trained on images to have any temporal understanding at all?

**Suggested Answer**: Great question! PE is trained on image-text pairs but processes videos by treating each frame as an independent image, then averaging. The surprising finding is that the per-frame embeddings still contain temporal information from the *visual content* - objects change position, lighting shifts, actions evolve. The model sees these content changes and they're reflected in the embedding space, even without explicit temporal training.

#### Q3: What's a "probe" in this context? I've heard the term but I'm not sure what it means practically.

**Suggested Answer**: A probe is a simple classifier (like logistic regression) that we train on frozen embeddings to test what information they contain. We don't modify the original model - we just take its outputs and ask "can we decode property X from these numbers?" If yes, the model encodes that property; if no, it doesn't. Here, we're probing whether temporal order can be decoded from PE's frame embeddings at each layer.

#### Q4: If layer 10 has more temporal information, why doesn't PE just use layer 10 for video tasks?

**Suggested Answer**: PE is designed for vision-language alignment across images AND video. The output layer (layer 23) is optimized for matching images to text descriptions. This works well because most video descriptions are about "what's happening" (semantic content) not "when things happen" (temporal order). Using layer 10 might hurt text matching. The insight is that if we care specifically about temporal matching, we should consider intermediate layers.

#### Q5: Is 64.3% accuracy actually good? It's not that much better than random (50%).

**Suggested Answer**: For a linear probe on a challenging task, 64.3% is meaningful but not overwhelming. The key insight is the *comparison*: 64.3% at layer 10 vs 57.4% at the output layer. This 7% gap shows that temporal information is lost in later layers. Whether this matters for retrieval depends on whether that 7% translates to actual benchmark improvements. That's our next experiment to run.

---

## Feedback Synthesis

### Strengths

1. **Novel explanatory angle**: While others focus on adding temporal mechanisms, we explain why the simple baseline works. This is a fresh perspective.

2. **Clean experimental design**: Linear probe methodology is standard and interpretable. Layer-by-layer analysis provides clear evidence for the hypothesis.

3. **Efficient experiments**: Completed on single GPU with 150 videos. Reproducible and scalable.

4. **Clear narrative**: "Temporal info peaks at layer 10, gets compressed by layer 23" is a memorable finding that explains the average pooling paradox.

5. **Actionable implications**: Finding suggests concrete improvements (use intermediate layers for temporal tasks).

### Weaknesses/Gaps

1. **Limited to synthetic task**: Probe accuracy doesn't directly translate to retrieval metrics. Need to connect to actual benchmarks.

2. **Sample size concerns**: 150 videos may not generalize. Need cross-dataset validation.

3. **Missing error bars**: Per-layer results don't show variance across videos or training runs.

4. **Architecture-specific**: Results are for PE-Core-L14. Unclear if pattern holds for other CLIP variants.

5. **No method contribution yet**: Analysis paper alone may be workshop-tier without retrieval experiments.

### Contested Points

1. **Paper tier**: Is this main conference material or workshop/short paper? Depends on whether we add retrieval experiments.

2. **Probe architecture choice**: Linear probe is standard but some reviewers prefer MLP for stronger upper bound.

3. **Layer 10 robustness**: Some non-monotonicity in results (layer 15 drop, layer 19 rise) may raise questions about robustness.

4. **Practical impact**: "So what?" criticism - does understanding help if we don't propose a better method?

---

## Action Items

| Priority | Description | Source | Route To |
|----------|-------------|--------|----------|
| P1 | Cross-dataset validation: run layer probing on VATEX videos | SME Q2 | experiment_stack/_inbox/ |
| P1 | Quick pilot: intermediate layer retrieval on K400 | Advisor Q4 | experiment_stack/_inbox/ |
| P2 | MLP probe as upper bound for temporal signal | SME Q1 | experiment_stack/_inbox/ |
| P2 | Layer probing visualization with error bars | SME Q3 | figure_stack/_inbox/ |
| P2 | Paper positioning decision document | Advisor Q2, Q5 | writer_stack/_inbox/ |
| P3 | Stratify by video characteristics (duration, motion) | SME Q3 | experiment_stack/_inbox/ |
| P3 | Literature review on layer-wise CLIP analysis | Advisor Q3 | reading_stack/_inbox/ |

---

## Routing Log

| Action | Routed To | Entry Created |
|--------|-----------|---------------|
| Cross-dataset validation experiment | experiment_stack/_inbox/ | EXP-014-layer-probe-vatex.md |
| Intermediate layer retrieval pilot | experiment_stack/_inbox/ | EXP-015-layer10-retrieval-pilot.md |
| MLP probe experiment | experiment_stack/_inbox/ | EXP-016-mlp-temporal-probe.md |
| Layer probing visualization | figure_stack/_inbox/ | FIG-004-layer-probe-curve.md |
| Paper strategy decision document | writer_stack/_inbox/ | WRITE-003-idea003-positioning.md |
