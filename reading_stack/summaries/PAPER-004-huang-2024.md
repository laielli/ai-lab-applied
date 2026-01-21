# Summary: LLM2CLIP: Powerful Language Model Unlocks Richer Visual Representation

- **Paper ID**: PAPER-004
- **arXiv**: 2411.04997
- **Authors**: Weiquan Huang, Aoqi Wu, Yifan Yang, Xufang Luo, Yuqing Yang, Liang Hu, Qi Dai, Chunyu Wang, Xiyang Dai, Dongdong Chen, Chong Luo, Lili Qiu (Tongji University, Microsoft)
- **Venue**: NeurIPS 2024 SSL Workshop, AAAI 2026
- **Code**: https://github.com/microsoft/LLM2CLIP
- **Summarized**: 2026-01-20

## Focus Area Tags
- Cross-Modal Alignment
- Foundation Models
- Benchmark and Evaluation

## One-Line Summary

LLM2CLIP introduces a caption-to-caption contrastive fine-tuning framework that transforms LLMs into discriminative text encoders, enabling them to replace CLIP's text encoder and achieve substantial gains on retrieval tasks (+16.5% on EVA02) with efficient offline feature precomputation.

## Key Contributions

1. **Caption Contrastive (CC) Fine-tuning Framework**: Solves the fundamental problem that LLMs have poor feature separability for discriminative tasks. Raw LLMs achieve only 5.2% caption retrieval accuracy (CRA) on COCO—essentially random for distinguishing captions of the same image. CC fine-tuning improves this to 29.5%, making LLMs viable as CLIP text encoders.

2. **Two-Stage Training Pipeline**: Stage 1 applies supervised SimCSE contrastive learning on caption pairs to improve LLM discriminative capability. Stage 2 uses the CC-finetuned LLM to post-train CLIP's vision encoder with frozen LLM weights.

3. **Offline Feature Precomputation**: Text features are computed once and cached, reducing training time from 17 hours to 1.3 hours (13x speedup) for Llama-3.1-8B. This achieves nearly 4x faster training than LoRA-based alternatives.

4. **Broad Foundation Model Improvements**: The method successfully enhances CLIP, EVA02, and SigLip2 across short-text, long-text, and cross-lingual retrieval benchmarks without modifying the base architectures.

## Methodology

### The Core Problem: LLM Feature Separability

LLMs are trained for next-token prediction, producing output features optimized for generation rather than discrimination. The paper demonstrates this quantitatively:

| Model | Caption Retrieval Accuracy (COCO 5K) |
|-------|--------------------------------------|
| Llama3-8B (unfinetuned) | 5.2% |
| Llama3.2-1B (unfinetuned) | 5.6% |
| CLIP ViT-L text encoder | 66.0% |
| Llama3-8B (CC-finetuned) | 29.5% |

The 5.2% accuracy indicates the LLM "barely distinguishes between different captions of the same image"—inadequate for contrastive learning.

### Stage 1: Caption Contrastive Fine-tuning

**Objective**: Enhance output feature separability through lightweight fine-tuning.

**Key Design Choices**:
- **Sentence Representation**: Average pooling over all output tokens (outperforms [EOS] token)
- **Attention**: Bidirectional attention (causal mask removed) improves results
- **Fine-tuning**: LoRA with rank=16, alpha=32 for parameter efficiency
- **Loss**: Supervised SimCSE where original caption and re-annotated caption (from ShareCaptioner) form positive pairs; all other captions are negatives

**Training Configuration**:
- Dataset: 30M DreamLIP captions + 1.5M E5 pure-text pairs
- Batch size: 2048
- Max sequence length: 512 tokens
- Training time: 68 hours on 32 A100 GPUs

### Stage 2: LLM2CLIP Cross-modal Post-training

**Architecture**:
- Replace original CLIP text encoder with CC-finetuned LLM
- LLM weights: Frozen (no gradients)
- Vision encoder: Full training
- Adapter: 4-layer linear MLP (inverted bottleneck design)

**Data Strategy**:
- 50% real captions + 50% MLLM-generated dense captions (optimal ratio from ablations)
- Dense captions leverage LLM's "open-world knowledge" for richer supervision

**Efficiency Innovation**:
Since the LLM is frozen, text features can be precomputed offline and cached. This eliminates repeated LLM inference during training, providing 13x speedup (17h to 1.3h on identical hardware).

## Key Results

### Short-Text Retrieval (Flickr30K, COCO)

| Base Model | Resolution | Data | Flickr I2T | Flickr T2I |
|------------|-----------|------|------------|------------|
| CLIP ViT-L/14 | 224 | +15M | 93.0 | 83.5 |
| EVA02 ViT-L/14 | 224 | +60M | 95.9 | 85.1 |
| SigLIP2 | 224 | +60M | 95.2 | 84.6 |

Average improvements across 5 short-text benchmarks:
- CLIP: +16.4 I2T, +23.3 T2I
- EVA02: +15.3 I2T, +14.3 T2I
- SigLIP2: +10.2 I2T, +10.6 T2I

### Long-Text Retrieval (ShareGPT4V, Urban-1k, DOCCI)

| Base Model | I2T Gain | T2I Gain |
|------------|----------|----------|
| EVA02 +60M | +14.8 | +15.8 |
| SigLIP2 +60M | +14.8 | +15.8 |

Long-text retrieval shows the largest gains, demonstrating the LLM's advantage for processing complex, detailed captions.

### Cross-Lingual Retrieval

**Flickr-CN (Chinese)**:
- EVA-L-224 baseline: 4.4% I2T, 0.9% T2I
- EVA-L-224 +LLM2CLIP: 90.6% I2T, 75.6% T2I (20x improvement)

**XM3600 (36 languages)**:
- SigLIP2 baseline: 59.7% I2T, 48.2% T2I
- SigLIP2 +LLM2CLIP: 69.1% I2T, 56.3% T2I (+9.4 I2T, +8.1 T2I)

Critically, the model is trained only on English data—multilingual gains emerge from the LLM's inherent multilingual capabilities.

### ImageNet Zero-Shot Classification

| Model | Zero-Shot | Linear Probe |
|-------|-----------|--------------|
| CLIP L/14 baseline | 76.6% | 84.8% |
| CLIP L/14 +LLM2CLIP | 74.1% (-2.5) | 85.2% (+0.4) |

Zero-shot drops slightly (attributed to category word frequency mismatches), but linear probe improves, indicating better underlying visual features.

### Multimodal LLM Integration (LLaVA 1.5)

LLM2CLIP vision encoders improve LLaVA 1.5 performance on 87.5% of benchmarks:
- VQAv2: +0.76
- GQA: +0.29
- MMBench: +1.63
- TextVQA: +1.53

## Ablation Studies

### Stage 1: Training Method Comparison

| Configuration | Flickr I2T | Flickr T2I |
|---------------|------------|------------|
| Supervised SimCSE | 88.9 | 78.8 |
| Unsupervised SimCSE | 77.2 | - |
| MNTP only (no contrastive) | 82.0 | 71.7 |

**Finding**: Supervised SimCSE substantially outperforms unsupervised (+11.7 I2T). Contrastive learning is essential.

### Stage 1: Attention and Pooling

| Attention | Pooling | I2T | T2I |
|-----------|---------|-----|-----|
| Bidirectional | Average | 88.9 | 78.8 |
| Causal | Average | 89.4 | 78.7 |
| Bidirectional | [EOS] | Lower | Lower |

Bidirectional vs. causal shows minimal difference; average pooling consistently outperforms [EOS] token.

### Stage 2: Adapter Design

| Adapter | Flickr I2T | Flickr T2I |
|---------|------------|------------|
| No Adapter | 89.2 | 77.7 |
| Linear x1 | 88.5 | 77.5 |
| Linear x2 | 89.6 | 78.1 |
| Linear x4 | 88.9 | 78.8 |

4-layer linear adapter provides small but consistent improvement.

### Data Composition (Dense Caption Ratio)

| MLLM Caption % | I2T | T2I |
|----------------|-----|-----|
| 0% (real only) | 91.1 | 81.5 |
| 50% (default) | 91.9 | 81.7 |
| 100% (dense only) | 89.2 | 77.2 |

**Finding**: 50/50 ratio of real and dense captions is optimal. Dense-only hurts performance.

### LLM Encoder Comparison

| Text Encoder | I2T | T2I |
|--------------|-----|-----|
| Llama-3.1-8B (no CC) | 85.2 | 74.6 |
| Llama-3.1-8B (CC-finetuned) | 92.2 | 81.5 |
| NV-Embed-v2 | 90.4 | 80.0 |
| BGE-EN-ICL | 89.1 | 78.5 |

CC fine-tuning is critical—without it, raw LLMs underperform even specialized embedding models.

## Answers to First-pass Questions

**Q1: What specific properties of LLM feature spaces make them poorly suited for direct CLIP training? Why does caption contrastive fine-tuning solve this issue?**

LLMs are trained for next-token prediction (generative objective), which optimizes for capturing natural language distributions rather than discriminating between semantically similar texts. The output features cluster captions by linguistic patterns rather than semantic content, resulting in only 5.2% caption retrieval accuracy—captions describing the same image are not distinctively represented.

CC fine-tuning introduces a discriminative objective: pull together different captions of the same image (positive pairs), push apart captions of different images (negatives). This restructures the feature space for semantic discrimination, improving CRA to 29.5% (473% relative improvement).

**Q2: Can this approach extend to video-language models? What modifications would be needed?**

The approach should extend to video-language models with the following adaptations:
1. Replace CLIP vision encoder with a video encoder (e.g., TimeSformer, VideoMAE)
2. Generate/collect temporal captions describing actions, events, sequences
3. Apply CC fine-tuning on temporal caption pairs (e.g., original vs. re-annotated action descriptions)
4. For Stage 2, post-train the video encoder with frozen CC-finetuned LLM

The LLM's world knowledge about temporal sequences ("pouring water" implies certain physical dynamics) could enhance temporal understanding beyond what text encoders provide.

**Q3: What does the CC fine-tuning reveal about generative vs. discriminative text understanding?**

Generative LLMs excel at predicting likely next tokens but fail at distinguishing between semantically similar completed sentences. The 5.2% CRA suggests that "a fluffy white cat" and "a playful kitten" may have similar LLM representations because they share distributional properties—but CLIP needs to distinguish them for retrieval.

This reveals a fundamental dichotomy: generation requires modeling what is likely; discrimination requires modeling what is different. CC fine-tuning bridges this gap by adding a discriminative objective to generative representations.

**Q4: What are the limitations of offline feature precomputation?**

Limitations include:
1. **No dynamic text augmentation**: Cannot apply text augmentation during training (augmentations must be pre-computed)
2. **Storage overhead**: Caching features for large datasets requires significant storage
3. **Fixed LLM**: Cannot continue adapting the LLM during Stage 2 training
4. **Limited to frozen encoders**: If joint LLM training is desired, offline caching is not possible

The benefits (13x speedup) generally outweigh these limitations for most use cases.

**Q5: For video retrieval with dense temporal descriptions, what caption length and complexity is optimal?**

The paper shows 50/50 ratio of real (short) and MLLM-generated dense (long) captions is optimal. For video:
- Pure dense captions hurt performance (89.2% vs 91.9% I2T)
- Dense captions provide richer supervision but may overfit to verbosity
- Temporal descriptions should balance event-level density with natural language patterns

Recommendation: Mix standard video captions (1-2 sentences) with dense temporal descriptions (detailed action sequences) at roughly equal ratio.

**Q6: Does this approach work across different foundation models?**

Yes. The method successfully improves:
- CLIP ViT-L/14 (original OpenAI CLIP)
- EVA02 (efficient vision transformer)
- SigLip2 (sigmoid-based CLIP variant)

This suggests the approach is architecture-agnostic for the vision encoder. The key requirement is a contrastive vision-language training setup that can incorporate the LLM text features.

**Q7: How would temporal dynamics interact with LLM world knowledge?**

LLMs encode substantial world knowledge about temporal sequences:
- Physical causality ("pouring water into a glass" implies water level rises)
- Action sequences ("cooking a meal" involves cutting, heating, plating)
- Temporal language ("before", "after", "while", "then")

This world knowledge could compensate for lack of explicit temporal modeling in video encoders. The LLM understands that "unwrapping a gift" is directionally different from "wrapping a gift" even without seeing the video. Combining with temporal video features could yield synergistic improvements.

**Q8: Could improvements apply to video QA and temporal grounding?**

The LLaVA 1.5 improvements suggest yes. LLM2CLIP vision encoders improve VQA benchmarks, which require understanding visual content for answering questions. For temporal grounding (localizing text queries in video), the better text understanding should improve query representation, and the better visual features should improve segment matching.

**Q9: What does the zero-shot vs. linear probe trade-off mean for video classification?**

Zero-shot drops (-2.5%) because category words (like "goldfish" or "umbrella") have different frequency distributions in LLM training data vs. CLIP's original training. However, linear probe improves (+0.4%), indicating the underlying visual features are better.

For video classification: if using prompt-based zero-shot, expect slight degradation on standard categories. If using learned classifiers (linear probe, fine-tuning), expect improvements.

**Q10: What is the minimum data volume for meaningful gains?**

From ablations:
- 3M samples: Improvements on long-text retrieval, minimal on short-text
- 15M samples: Clear improvements on both
- 60M samples: Best overall performance

For our compute constraints, 15M appears to be the practical minimum for broad improvements. Long-text retrieval benefits emerge earlier (3M), so temporal video descriptions may require less data.

**Q11: Could cross-lingual transfer apply to domain transfer in video?**

Yes, the cross-lingual results are striking: English-only training yields 20x improvement on Chinese retrieval. This suggests the LLM's broad knowledge generalizes across domains it wasn't explicitly trained on.

For video domain transfer: training on action videos (e.g., Kinetics) could transfer to instructional videos (e.g., HowTo100M) through shared LLM knowledge about actions and procedures.

**Q12: How does this compare to temporal models, and could LLM world knowledge compensate for lack of temporal modeling?**

LLM2CLIP focuses on image-text alignment, not temporal modeling. However, the LLM's world knowledge about temporal sequences could partially compensate:
- LLM understands action directionality ("opening" vs. "closing")
- LLM knows typical event sequences
- LLM can process long, detailed temporal descriptions

This connects to IDEA-003: if LLM world knowledge provides implicit temporal understanding, combining with explicit temporal modeling could be synergistic.

## Relevance to Lab Vision

### Direct Alignment with Focus Areas

**Cross-Modal Alignment (Primary)**:
This paper directly addresses how to improve text-to-image alignment by upgrading the text encoder. For video, the same principle applies: better language understanding should improve video-text matching. The CC fine-tuning framework could be applied to temporal captions to improve temporal language understanding.

**Efficient Video Representation**:
The offline precomputation strategy (13x speedup) aligns perfectly with our single-GPU scaling methodology. Text features can be cached and reused, making large-scale video experiments more tractable.

**Foundation Models**:
LLM2CLIP demonstrates how to enhance existing foundation models (CLIP, EVA02, SigLip2) without pretraining from scratch—directly matching our strategic priority to "build on foundation models."

### Implications for Lab Priorities

**Temporal Reasoning Gap**:
The paper does not address temporal reasoning—it treats each image independently. However, the improved text understanding (especially for long, complex captions) could benefit dense temporal descriptions in video. The LLM's world knowledge about temporal sequences is an untapped resource.

**Cross-Benchmark Generalization**:
LLM2CLIP shows gains across Flickr30K, COCO, ShareGPT4V, Urban-1k, DOCCI, and 36-language XM3600. This cross-benchmark robustness signals genuine capability improvement, not dataset-specific overfitting.

**Compute Efficiency**:
The offline precomputation enables efficient experimentation:
- Compute LLM features once for entire dataset
- Run multiple vision encoder experiments without LLM overhead
- 4x faster than LoRA-based alternatives

This directly supports our "fail-fast" idea validation approach.

### Relevance to Existing Ideas

**IDEA-005 (SuperCLIP for Video)**: LLM2CLIP and SuperCLIP are complementary approaches:
- SuperCLIP: Classification supervision for fine-grained semantics
- LLM2CLIP: LLM text encoder for richer language understanding

A combined approach could use LLM2CLIP's text encoder with SuperCLIP's classification head.

**IDEA-006 (Classification Distillation)**: LLM2CLIP's CC-finetuned LLM could serve as a distillation teacher. The improved text features provide richer targets than original CLIP text embeddings.

## Potential Connections

- **Connection to PAPER-001 (Perception Encoder)**: PE uses intermediate layer features for better representations. LLM2CLIP uses LLM features. Could we combine—use CC-finetuned LLM features with PE's intermediate layer visual features?

- **Connection to PAPER-002 (ArrowRL)**: ArrowRL improves temporal direction awareness through reverse video rewards. LLM2CLIP improves text understanding. Could LLM world knowledge about temporal direction ("opening" vs. "closing") help ArrowRL training?

- **Connection to PAPER-003 (SuperCLIP)**: Both papers improve CLIP through auxiliary objectives. SuperCLIP adds classification loss; LLM2CLIP upgrades the text encoder. These are orthogonal and potentially complementary.

- **Gap this reveals**: No work applies CC-finetuned LLMs to video-text retrieval. The combination of LLM temporal knowledge with video visual features is unexplored.

## Limitations and Research Directions

### Paper Limitations

1. **No temporal modeling**: Focused on image-text; does not address video or temporal reasoning
2. **Stage 1 training cost**: 68 hours on 32 A100s for CC fine-tuning is substantial
3. **Zero-shot degradation**: Slight drop on ImageNet zero-shot (-2.5%)
4. **Dense caption dependency**: Requires MLLM-generated captions for optimal results

### Research Directions for Our Lab

1. **LLM2CLIP for Video**: Apply CC fine-tuning to temporal captions (action descriptions, event sequences). Use CC-finetuned LLM to post-train video encoders.

2. **Temporal Caption CC Fine-tuning**: Create positive pairs from temporal captions:
   - Original: "Person opens door, walks inside, closes door"
   - Re-annotated: "Someone enters a building through a door"
   - Negative: "Person closes door, walks outside, opens door" (reversed)

3. **Efficient Validation**: Use offline precomputation for video experiments:
   - Cache LLM features for video captions (MSR-VTT, DiDeMo)
   - Run multiple video encoder experiments efficiently
   - Fits single-GPU validation paradigm

4. **Combine with Classification Supervision**: LLM2CLIP + SuperCLIP:
   - Use CC-finetuned LLM for text encoding
   - Add IDF-weighted classification head for fine-grained semantics
   - Potentially synergistic improvements

## Ideas Sparked

- **IDEA-007 (potential)**: LLM2CLIP for Video-Text Retrieval—Apply CC fine-tuning to temporal caption datasets, then post-train video encoders. Hypothesis: LLM world knowledge about temporal sequences will improve video retrieval without explicit temporal modeling. Validate on MSR-VTT and DiDeMo.

- **IDEA-008 (potential)**: Temporal Caption Contrastive Fine-tuning—Create a CC fine-tuning dataset specifically for temporal reasoning. Positive pairs: same event described differently. Hard negatives: temporally reversed events. Could improve LLM discriminability for action understanding.

---

## Code/Resource Reference

**Models on HuggingFace**:
- `microsoft/LLM2CLIP-Llama-3-8B-Instruct-CC-Finetuned` (CC-finetuned LLM)
- `microsoft/LLM2CLIP-EVA02-L-14-336` (Post-trained vision encoder)
- `microsoft/LLM2CLIP-Openai-L-14-336`
- `microsoft/LLM2CLIP-Openai-B-16`

**GitHub**: https://github.com/microsoft/LLM2CLIP

**Key Implementation Details**:
- LoRA rank: 16, alpha: 32
- Bidirectional attention with average pooling
- 4-layer linear adapter for Stage 2
- 50% real + 50% dense caption ratio
- Offline text feature caching for 13x speedup

## Sources

- [arXiv Paper](https://arxiv.org/abs/2411.04997)
- [arXiv HTML](https://arxiv.org/html/2411.04997v4)
- [GitHub Repository](https://github.com/microsoft/LLM2CLIP)
- [HuggingFace Models](https://huggingface.co/microsoft/LLM2CLIP-EVA02-L-14-336)
- [Project Page](https://microsoft.github.io/LLM2CLIP/)
