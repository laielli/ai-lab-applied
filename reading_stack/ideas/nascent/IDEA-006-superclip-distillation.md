# Idea: Classification-Based CLIP Distillation

- **ID**: IDEA-006
- **Stage**: nascent
- **Created**: 2026-01-17
- **Source Papers**: PAPER-003

## Spark

SuperCLIP's classification head produces explicit, batch-independent semantic predictions. These could serve as better distillation targets than standard CLIP embeddings, especially for video-text models where small students are needed for deployment.

## Focus Areas
- Cross-Modal Alignment
- Efficient Video Representation

## Initial Thoughts

**Core hypothesis**: Classification-based supervision provides more stable, explicit learning targets for student models than contrastive embedding similarity.

**Why classification might distill better**:

1. **Batch independence**: Teacher's classification logits can be computed and cached, no need for negative samples during student training

2. **Dense supervision**: Every vocabulary token provides a supervision signal (vs. single embedding similarity)

3. **Fine-grained features**: Soft labels encourage semantic feature learning that might transfer better than global similarity

4. **Stability**: Classification targets are deterministic given input, while contrastive targets depend on batch composition

**Potential approaches**:

1. **Vocabulary distillation**: Student matches teacher's vocabulary-level predictions
2. **Hybrid distillation**: Combine classification KD with embedding MSE
3. **Progressive distillation**: Use classification targets for early training, switch to embedding matching for fine-tuning

**Key comparisons**:
- TinyCLIP (token-level distillation)
- CLIPA (data-efficient CLIP training)
- Standard feature distillation baselines

**Target application**: Efficient video-text retrieval models for deployment. Video models are expensive; distillation is critical for practical use.

**Open questions**:
- Does classification distillation preserve cross-modal alignment as well as embedding distillation?
- Can we combine with LoRA-style adaptation for efficient fine-tuning?
- Does this work better for vision-only students or joint vision-language students?
