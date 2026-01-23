# Idea: Classification-Based CLIP Distillation

- **ID**: IDEA-006
- **Stage**: developing
- **Created**: 2026-01-17
- **Promoted**: 2026-01-17
- **Source Papers**: PAPER-003

## Research Question

Can SuperCLIP's classification-based supervision provide better distillation targets for video-text models than standard contrastive embedding similarity?

## Hypothesis

Classification logits from a SuperCLIP teacher will yield better student models than embedding-based distillation because:
1. Classification targets are batch-independent and cacheable
2. Dense vocabulary supervision provides richer gradients than single similarity scores
3. Deterministic targets reduce variance in student training

**Predicted outcome**: Students trained with classification distillation will show higher retrieval recall on video-text benchmarks (MSR-VTT, DiDeMo) than embedding-distilled baselines at equivalent model size.

## Why Novel

Existing CLIP distillation methods (TinyCLIP, CLIPA) focus on:
- Token-level feature matching
- Embedding space alignment
- Data-efficient training strategies

None leverage classification-based auxiliary objectives as distillation targets. SuperCLIP's IDF-weighted soft labels provide a new, semantically grounded supervision signal that has not been explored for distillation.

**Gap**: The distillation literature treats CLIP as a contrastive model only. SuperCLIP reveals that classification supervision improves fine-grained features—this benefit should transfer to students.

## Potential Experiments

### Validation Phase (<8 GPU-hours)

1. **Setup**: Train SuperCLIP teacher on CC3M subset (or use pretrained if available)
2. **Distill**: Compare three student training strategies:
   - Baseline: Embedding MSE only
   - Classification: Vocabulary KL-divergence only
   - Hybrid: Embedding MSE + Vocabulary KL
3. **Evaluate**: Zero-shot image-text retrieval on Flickr30K
4. **Metric**: Recall@1, Recall@5 for all three conditions

### Ablation Phase (<24 GPU-hours)

1. **Student sizes**: Test 3 student scales (ViT-S, ViT-B, ViT-L)
2. **Loss weighting**: Sweep hybrid loss coefficients
3. **IDF sensitivity**: Compare uniform vs. IDF-weighted targets
4. **Video extension**: Apply to video encoder (ViT-B + temporal pooling) on MSR-VTT

### Full Experiments (if validation succeeds)

1. Scale to larger datasets (WebVid-10M, CC12M)
2. Comprehensive video-text benchmarks (MSR-VTT, DiDeMo, ActivityNet)
3. Efficiency analysis (FLOPs vs. recall trade-off)

## Open Questions

- Does classification distillation preserve cross-modal alignment as well as embedding distillation?
- Can we combine with LoRA-style adaptation for efficient fine-tuning?
- Does this work better for vision-only students or joint vision-language students?
- How does vocabulary size affect distillation quality?
- Should temporal tokens (verbs, adverbs) receive higher weight for video?

## Promotion Criteria

- [x] Clear research question
- [x] Testable hypothesis
- [x] Novelty argument
- [x] Viable experiment plan
- [ ] Validation experiment completed with positive signal
