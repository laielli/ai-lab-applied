# Idea: LLM2CLIP for Video-Text Retrieval

- **ID**: IDEA-007
- **Stage**: developing
- **Created**: 2026-01-20
- **Promoted**: 2026-01-20
- **Source Papers**: PAPER-004, PAPER-001

## Research Question

Can LLM2CLIP's caption contrastive (CC) fine-tuning framework be applied to video-text retrieval, leveraging LLM world knowledge about temporal dynamics (action sequences, causality, event ordering) to improve video understanding without explicit temporal modeling?

## Hypothesis

Post-training video encoders with CC-finetuned LLM text features will outperform standard CLIP text encoder baselines because:

1. **Temporal world knowledge**: LLMs encode implicit understanding of action sequences ("opening" vs. "closing"), causality, and event ordering that transfers through text supervision
2. **Long caption handling**: CC-finetuned LLMs excel at dense descriptions (+14.8% on long-text retrieval), which aligns with detailed temporal video captions
3. **Cross-domain transfer**: LLM2CLIP's 20x improvement on cross-lingual tasks (English-only training) suggests strong domain transfer potential to video

**Predicted outcome**: Video encoders post-trained with CC-finetuned LLM features will achieve >2% R@1 improvement on PE-Video Dataset (PVD) compared to original CLIP/PE text encoder baselines, with larger gains on motion-heavy and temporally-sensitive queries.

## Why Novel

**Gap in existing work**: No prior work applies CC-finetuned LLMs to video-text retrieval.

Current video-text approaches either:
- Use frozen CLIP text encoders (limited language understanding)
- Train video-specific text encoders from scratch (expensive, limited data)
- Focus on temporal modeling in the vision encoder (ignores language-side temporal knowledge)

LLM2CLIP demonstrates that LLMs can dramatically improve image-text retrieval (+16.5% on EVA02), but this has not been explored for video. The key insight is that LLMs already understand temporal language—we can leverage this without additional temporal supervision.

**Unique contribution**: Transfer LLM temporal world knowledge to video retrieval through text supervision alone, complementing rather than replacing explicit temporal modeling.

## Potential Experiments

### Primary Dataset: PE-Video Dataset (PVD)

**Why PVD**:
- **1M diverse videos** with high visual fidelity and large resolution
- **120K expert-annotated clips** with human-verified captions (automated + refined)
- **Motion-centered** content ideal for temporal reasoning experiments
- First-person and third-person views across 10 high-level categories
- All videos include descriptions and keywords
- Direct integration with PE codebase (PAPER-001, already in code_stack)
- Available on HuggingFace: [facebook/PE-Video](https://huggingface.co/datasets/facebook/PE-Video)

### Validation Phase (<8 GPU-hours)

**Goal**: Prove concept using pretrained components (no Stage 1 training).

1. **Setup**:
   - Use Microsoft's pretrained `LLM2CLIP-Llama-3-8B-Instruct-CC-Finetuned`
   - Precompute LLM features for PVD 120K annotated subset captions
   - Cache features offline (eliminates LLM inference during training)
   - Use PE codebase video loading infrastructure (already analyzed in code_stack)

2. **Baseline**:
   - PE video encoder (ViT + mean pooling, matching PAPER-001 setup)
   - Train with original PE/CLIP text features
   - Standard contrastive loss

3. **Experiment**:
   - Same PE video encoder architecture
   - Train with CC-finetuned LLM text features (frozen, cached)
   - Same contrastive loss and training schedule

4. **Evaluation**:
   - PVD text-to-video retrieval (R@1, R@5, R@10)
   - Split results by category (10 high-level categories available)
   - Split by motion intensity (PVD metadata: 120K = highest motion samples)

5. **Success criterion**: >2% R@1 improvement over PE baseline

### Ablation Phase (<24 GPU-hours)

1. **Video encoder architectures** (within PE framework):
   - Mean pooling (PE default, matches IDEA-003 investigation)
   - Attention pooling (`pool_type="attn"`)
   - Add 2-layer temporal transformer on top

2. **Caption analysis** (PVD has rich annotations):
   - Short descriptions (keywords/tags)
   - Full video descriptions (detailed captions)
   - Combined (expect larger gains on detailed descriptions)

3. **Temporal sensitivity probe**:
   - Create temporally-reversed captions from PVD descriptions
   - Measure retrieval accuracy drop for PE baseline vs. LLM2CLIP
   - Hypothesis: LLM2CLIP will be more sensitive to temporal reversal
   - Leverage PVD's motion-centered content for strong signal

4. **Category analysis**: Compare gains across PVD's 10 categories
   - Identify which video types benefit most from LLM temporal knowledge

### Full Experiments (if validation succeeds)

1. **Temporal Caption CC Fine-tuning** (requires new training):
   - Create temporal caption pairs from PVD annotations
   - Hard negatives: temporally reversed events
   - Fine-tune LLM specifically for temporal discriminability
   - Leverage PVD's motion-centered selection for strong temporal signal

2. **Scale to full PVD**:
   - Expand from 120K annotated to full 1M videos
   - Use PVD video descriptions (available for all 1M) with synthetic augmentation

3. **Cross-benchmark transfer**:
   - Train on PVD, evaluate on MSR-VTT, DiDeMo, ActivityNet
   - Test if PVD's high-quality annotations transfer to other benchmarks

4. **Combination experiments**:
   - LLM2CLIP + explicit temporal modeling (does it stack?)
   - LLM2CLIP + SuperCLIP classification head (IDEA-006 synergy)
   - LLM2CLIP + PE intermediate features (PAPER-001 insight)

## Efficiency Analysis

| Component | Cost | Notes |
|-----------|------|-------|
| LLM feature precomputation | ~2 GPU-hours | One-time for 120K PVD captions, cached |
| Video encoder training | ~4 GPU-hours | PE ViT-B, 120K PVD scale |
| Evaluation | <1 GPU-hour | Inference only |
| **Total validation** | **<7 GPU-hours** | Within budget |

Key efficiency advantages:
- **Offline LLM caching**: 13x speedup (from LLM2CLIP paper)
- **PE codebase integration**: Video loading already implemented (`video_transform.py`)
- **PVD HuggingFace hosting**: Easy download, no preprocessing needed
- **Motion-centered subset**: 120K highest-motion samples = strong signal with less data

## Open Questions

1. **Temporal knowledge source**: How much improvement comes from LLM temporal knowledge vs. simply better language understanding?
   - *Probe*: Compare gains across PVD's 10 categories (motion-heavy vs. static scenes)

2. **Caption quality interaction**: Does PVD's expert annotation quality amplify or reduce LLM2CLIP gains?
   - *Probe*: Compare expert captions vs. auto-generated descriptions

3. **Stacking with temporal modeling**: Does LLM2CLIP complement explicit temporal encoders, or is the gain redundant?
   - *Probe*: Compare PE mean pooling vs. temporal transformer with both text encoders

4. **Domain specificity**: Does CC fine-tuning on image captions transfer to video, or do we need video-specific CC training?
   - *Probe*: Compare pretrained CC-LLM vs. PVD-caption-finetuned CC-LLM

5. **Motion intensity correlation**: Do higher-motion videos (PVD's 120K subset) show larger gains from LLM temporal knowledge?
   - *Probe*: Stratify results by motion intensity metadata

6. **Cross-benchmark transfer**: Do gains on PVD transfer to standard benchmarks (MSR-VTT, DiDeMo)?
   - *Defer to full experiments*

## Connections to Other Ideas

- **PAPER-001 (Perception Encoder)**: Direct synergy—PVD is PE's training data, PE codebase is already analyzed in code_stack. This experiment extends PE with better text understanding via LLM2CLIP.
- **IDEA-003 (Average Pooling Mystery)**: If LLM world knowledge provides implicit temporal understanding, this could explain why PE's simple mean pooling achieves SOTA—the text encoder carries the temporal signal. PVD experiments can test this directly.
- **IDEA-004 (TinyVid)**: Could use TinyVid as fast validation testbed before scaling to full PVD
- **IDEA-006 (Classification Distillation)**: CC-finetuned LLM could serve as teacher for classification distillation; potentially synergistic with PE video encoders

## Promotion Criteria

- [x] Clear research question
- [x] Testable hypothesis
- [x] Novelty argument
- [x] Viable experiment plan
- [ ] Validation experiment completed with positive signal
