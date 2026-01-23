# Idea: SuperCLIP for Video-Text Retrieval

- **ID**: IDEA-006
- **Stage**: developing
- **Created**: 2026-01-17
- **Promoted**: 2026-01-17
- **Updated**: 2026-01-23
- **Source Papers**: PAPER-003
- **Merged**: IDEA-005 (SuperCLIP for Video-Text Retrieval)

## Research Question

Can SuperCLIP's classification-based supervision improve video-text retrieval, either through direct application to video encoders or as distillation targets for efficient video-text models?

## Hypothesis

Classification-based supervision will improve video-text retrieval because:
1. **Dense vocabulary supervision** provides richer gradients than single similarity scores
2. **Temporal token emphasis** (verbs, adverbs) can be weighted via IDF to improve temporal understanding
3. **Batch-independence** is especially valuable for video where batch sizes are memory-constrained
4. **Deterministic targets** reduce variance in training

**Predicted outcome**: Models trained with SuperCLIP-style classification supervision will show higher retrieval recall on temporal-focused benchmarks (ActivityNet, DiDeMo) compared to standard contrastive baselines.

## Why Novel

Existing approaches:
- **CLIP distillation** (TinyCLIP, CLIPA): Focus on embedding matching, not classification
- **Video-text models**: Use standard contrastive loss without auxiliary classification
- **SuperCLIP**: Only demonstrated on images, not extended to video

**Our contributions**:
1. First application of classification supervision to video-text retrieval
2. Temporal token weighting via verb/adverb IDF from action caption datasets
3. Classification-based distillation for efficient video encoders

## Two Complementary Approaches

### Approach A: Direct SuperCLIP for Video

Apply classification head directly to video encoder:
- Video-level classification on aggregated features
- Optional: Per-frame classification with temporal pooling
- Temporal token emphasis: Higher IDF weights for verbs (run, jump), temporal adverbs (before, after, while)

**Key adaptations**:
1. Apply classification head to video encoder output (aggregated features)
2. Use verb-specific IDF computed from action caption datasets (ActivityNet, HowTo100M)
3. Consider frame-level vs. video-level classification balance

### Approach B: Classification-Based Distillation

Use SuperCLIP teacher's classification logits as distillation targets:
- Classification logits are cacheable (compute once, reuse)
- Dense supervision for student training
- Can distill to smaller/faster video encoders

**Why distillation helps for video**:
- Video encoders are expensive; efficient students are valuable
- Classification targets provide richer signal than embedding similarity alone
- Batch-independent targets critical when video batch sizes are small

## Potential Experiments

### Validation Phase (<8 GPU-hours)

**Experiment V1: Direct Classification**
1. Add classification head to frozen video encoder (PE-Core or CLIP4Clip)
2. Fine-tune on MSR-VTT with SuperCLIP-style loss
3. Compare: Standard contrastive vs. Contrastive + Classification
4. Metric: R@1, R@5, R@10

**Experiment V2: Temporal Token Weighting**
1. Compute verb/adverb IDF from ActivityNet captions
2. Apply weighted classification loss
3. Evaluate on temporal benchmarks (ActivityNet, DiDeMo)
4. Compare: Uniform IDF vs. Temporal-emphasized IDF

**Experiment V3: Distillation Comparison**
1. Train SuperCLIP teacher on image data (CC3M subset)
2. Distill to video student with three strategies:
   - Baseline: Embedding MSE only
   - Classification: Vocabulary KL-divergence only
   - Hybrid: Embedding MSE + Vocabulary KL
3. Evaluate: Zero-shot retrieval on MSR-VTT

### Ablation Phase (<24 GPU-hours)

1. **Student sizes**: ViT-S, ViT-B, ViT-L video encoders
2. **Loss weighting**: Sweep hybrid loss coefficients
3. **IDF variants**: Uniform vs. IDF vs. Temporal-IDF
4. **Frame vs. Video classification**: Per-frame, video-level, or both
5. **Temporal pooling**: Mean, attention, learned aggregation

### Full Experiments (if validation succeeds)

1. Scale to WebVid-10M, PE-Video Dataset
2. Comprehensive benchmarks: MSR-VTT, DiDeMo, ActivityNet, VATEX
3. Temporal-specific evaluation: Does it improve temporal ordering understanding?
4. Efficiency analysis: FLOPs vs. recall trade-off

## Open Questions

- Does classification distillation preserve cross-modal alignment?
- How to balance frame-level vs. video-level classification?
- Should temporal tokens get uniform high weight, or learned weights?
- Does this help specifically with temporal ordering understanding?
- Can we combine with LoRA-style adaptation for efficient fine-tuning?
- How does vocabulary size affect performance?

## Evaluation Targets

**Primary** (temporal-focused):
- ActivityNet Captions (temporal grounding)
- DiDeMo (temporal localization)

**Secondary** (standard retrieval):
- MSR-VTT
- VATEX
- LSMDC

## Promotion Criteria

- [x] Clear research question
- [x] Testable hypothesis
- [x] Novelty argument
- [x] Viable experiment plan
- [ ] Validation experiment completed with positive signal
