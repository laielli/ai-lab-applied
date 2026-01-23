# Summary: Perception Encoder: The best visual embeddings are not at the output of the network

- **Paper ID**: PAPER-001
- **arXiv**: 2504.13181
- **Summarized**: 2026-01-16

## Focus Area Tags
- Cross-Modal Alignment
- Efficient Video Representation
- Benchmark and Evaluation

## Initial Thoughts

- **The Surprising Effectiveness of Simple Average Pooling**: This is perhaps the most surprising aspect of the paper: Simple average pooling over frame embeddings for video representation outperforms complex temporal attention/modeling. This raises questions: How can it be that the lossiness of average pooling does not significantly hamper this approach? Do the individual embeddings encode temporal aspects somehow? Perhaps the RoPE embeddings are at play here? If so, can this effect be amplified or harnessed for even better results? An investigation into this result could be the basis for an interesting paper.

- **PE-Video Dataset is a valuable resource**: This new training resource seems unprecedented in terms of the combination of quality and scale. Usually the addition of such a dataset to a research subfield opens up contribution opportunities. We should think deeply about what types of experiments are only now possible due to the presence of this resource.

- **Is the Video-Data Engine practically useful?**: The Video-Data Engine itself may not lead directly to a research contribution, but such a pipeline could be useful for internal model training purposes.

## One-Line Summary

Perception Encoder demonstrates that optimal visual embeddings for downstream tasks exist in intermediate transformer layers rather than the final output, and introduces language alignment and spatial alignment techniques to extract these hidden representations, achieving SOTA on both image and video benchmarks.

## Key Contributions

1. **Intermediate Layer Discovery**: The paper's central insight is that contrastive vision-language training produces strong general-purpose embeddings hidden in intermediate network layers. The final CLIP pooling and projection operations compress or obscure these representations, causing performance to drop dramatically at the output layer for certain tasks (e.g., LLM-based grounding shows "abysmal" final-layer performance).

2. **Language Alignment**: A technique to extract intermediate layer features for multimodal language modeling. Uses a pretrained Llama3.2 3B decoder (unfrozen) with a 2-layer MLP vision projector on layer 47 of PEcoreG, with LayerScale and DropPath regularization. Successfully lifts strong intermediate features to the end of the network.

3. **Spatial Alignment**: A self-distillation approach that distills from the model's own frozen features, complemented by SAM 2.1 mask-based correspondence learning for spatial alignment. Addresses the dichotomy where different spatial tasks (detection vs. tracking) peak at vastly different layers (~40 vs. ~30).

4. **Video Data Engine & PE-Video Dataset (PVD)**: A robust video data engine using the image encoder as a frame-based encoder to generate well-aligned synthetic video captions. Released a dataset of 1M diverse high-resolution videos with 120K human-refined detailed captions.

5. **Unified Image-Video Encoder**: A single encoder (PEcoreG at 2B parameters) that outperforms specialized models on both image (vs. SigLIP2) and video (vs. InternVideo2) benchmarks using only 22M synthetic video-caption pairs.

## Methodology

### Architecture
- **PE Core**: Vision-language CLIP models in 5 sizes (T/16 to G/14). The G/14 model has 1.88B parameters with 1536 width, 50 layers depth, processing 448px images.
- **PE Lang**: LLM-aligned encoders (L/14, G/14 at 448px) with tiling-tuned variants for high-resolution inputs.
- **PE Spatial**: Dense prediction models with frozen teacher self-distillation and SAM 2.1 refinement. Available in distilled sizes (T/16 to L/14) plus main G/14.
- **PE-AV**: Audio-visual extension with frame encoder, temporal video encoder, audio encoder, and audio-video fusion encoder.

### Training Pipeline (Two-Stage)
1. **Stage 1 - Image Pretraining**: Robust contrastive learning on 5.4B image-text pairs with architectural and regularization enhancements (LayerScale, DropPath). Ablations conducted on 20M subset.

2. **Stage 2 - Video Finetuning**: Use image model as frame encoder to develop video data engine. Generate synthetic captions (via their captioner + Llama 3.2 vision for frame captions). Finetune on synthetic video-text data.

### Video Handling
- Uniformly samples N=8 frames from video clips
- Extracts frame-level embeddings with image encoder
- **Simple average pooling** over frame embeddings for video representation
- No temporal attention or complex temporal modeling - this simplicity is surprisingly effective

### Language Alignment Details
- Ablated LLM sizes (1B vs 3B), freezing weights, projector types (2-layer MLP outperforms linear)
- Tested output layers 41, 47, 50 - **layer 47 is optimal**
- Final setup: Llama3.2 3B (unfrozen), 2-layer MLP projector on layer 47, LayerScale + DropPath
- Scaled to 70M samples for +2.1 point improvement

### Spatial Alignment Details
- Identified that detection/depth peak at layer ~40 while tracking peaks at layer ~30
- Self-distillation from frozen features + SAM 2.1 for spatial correspondence
- Enables SOTA detection without using detection data for alignment

## Key Results

### Zero-Shot Image & Video Classification
| Model | ImageNet-1k | ImageNet-A | ObjectNet | Avg Robustness | K400 Video |
|-------|-------------|------------|-----------|----------------|------------|
| PE-Core-G14-448 | 85.4% | 92.6% | 88.2% | 86.6% | 76.9% |
| PE-Core-L14-336 | 83.5% | - | - | - | - |
| SigLIP2 | Lower | - | - | - | Lower |
| InternVideo2 | - | - | - | - | Lower |

### Multimodal LLM (PE Lang with Llama 3.1-8B)
| Benchmark | Score |
|-----------|-------|
| DocVQA | 94.6 |
| TextVQA | 86.5 |
| InfographicVQA | 80.9 |
| PerceptionTest | 82.7 |

### Spatial Tasks (PE Spatial G14-448)
| Task | Score |
|------|-------|
| COCO box mAP | 66.0 (SOTA) |
| LVIS box/mask mAP | 54.2/49.3 |
| ADE20k mIoU | 49.3 |
| DAVIS tracking J&F | 61.5 |

### Video Data Engine Ablation
- Video classification: +3.9% over image-only baseline
- Video retrieval: +11.1% over image-only baseline
- Achieved with much less video data than InternVideo2 or VideoPrism

### Layer Analysis
- OCR QA peaks at layer ~47/50
- Zero-shot tracking peaks much earlier in network
- Performance drops rapidly toward final layer for many tasks
- PE Lang's final layer becomes optimal after language alignment

## Answers to First-pass Questions

**Q1: What specific mechanism allows intermediate layers to produce better embeddings than the final output?**

The final CLIP pooling and projection operations compress representations to optimize for the contrastive objective. During this process, rich task-relevant features learned in intermediate layers get "hidden" as the network focuses on image-text matching. Layer ~47 retains OCR/language features while layer ~30-40 retains spatial/tracking features. The final layer shows "abysmal" performance for tasks far from pretraining (e.g., LLM-based grounding). This appears to be a general property of contrastive VLMs - they learn general features but fail to output them.

**Q2: How do the language alignment and spatial alignment techniques work in practice?**

**Language Alignment**: Trainable. Uses Llama 3.2 3B decoder (unfrozen) with 2-layer MLP projector attached to layer 47 of frozen PEcore. Trained with LayerScale and DropPath regularization on 70M samples. This "lifts" intermediate features to the end of the network.

**Spatial Alignment**: Trainable via self-distillation. The model distills from its own frozen intermediate features, complemented by SAM 2.1 mask-based correspondence learning for spatial refinement. This unifies the optimal layers for different spatial tasks into a single aligned representation.

**Q3: For video retrieval, how does the model handle temporal information?**

**Simple frame averaging** - the model treats video as N=8 uniformly sampled frames, encodes each with the image encoder, and applies mean pooling. Despite being extremely simple with no temporal attention or explicit temporal modeling, this achieves SOTA on Kinetics-400. The paper cites prior work noting average pooling outperforms more complex pooling strategies. However, this is a significant limitation for tasks requiring true temporal reasoning.

**Q4: What is the computational overhead of the alignment techniques compared to standard approaches?**

The language alignment trains an LLM decoder (3B parameters) on top of the frozen encoder features from layer 47. The spatial alignment uses self-distillation (no additional parameters at inference) plus SAM 2.1 refinement. At inference, PE Core has no overhead vs. standard CLIP. PE Lang requires running through the LLM decoder. PE Spatial has no additional overhead (features are aligned during training). The ablations were conducted at 20M samples, with full training at 70M samples - substantially smaller than typical foundation model training.

**Q5: How does performance vary across different intermediate layers?**

There's a clear dichotomy:
- **OCR/Language tasks**: Peak at layer ~47 (out of 50)
- **Dense spatial tasks** (detection, depth): Peak at layer ~40
- **Tracking tasks**: Peak much earlier at layer ~30
- **Final layer**: Performance drops rapidly for most tasks except those closest to pretraining objective

The principled selection approach: for language tasks, they ablated layers 41, 47, 50 and found layer 47 optimal. For spatial tasks, they identified the dichotomy and developed alignment to unify different optimal layers.

**Q6: What are the characteristics of the synthetically-annotated video dataset?**

**PE Video Dataset (PVD)**:
- 1M diverse high-resolution videos with high visual fidelity
- Split into 10 high-level categories
- 120K samples (highest motion) annotated via video captioning engine + human refinement
- Captions generated by their captioner (trained with/without human-refined data) + Llama 3.2 vision for frame captions
- Available on HuggingFace: `facebook/PE-Video`

**Q7: How does this approach compare to other recent vision-language models on the same benchmarks?**

| Model | ImageNet | K400 Video | DocVQA | COCO mAP |
|-------|----------|------------|--------|----------|
| PE (Core/Lang/Spatial) | 85.4% | 76.9% | 94.6 | 66.0 |
| SigLIP2 | Lower | Lower | - | - |
| InternVideo2 | - | Lower (with more data) | - | - |
| QwenVL2.5 / InternVL3 | - | - | Lower | - |
| DINOv2 | - | - | - | Lower |
| AIMv2-3B | Lower on lang | - | - | - |

PE matches AIMv2-3B on language tasks and DINOv2-g on spatial tasks despite using only contrastive pretraining.

**Q8: Can the intermediate layer insight be applied to other video-language architectures?**

The insight appears general to contrastive VLMs. The paper explicitly states that "a well-tuned large-scale contrastive model can learn general embeddings in the process of fitting its objective, but it fails to output them." This suggests:
- Other CLIP-style models likely have similar hidden representations
- The language/spatial alignment techniques could potentially transfer
- The layer-probing methodology could be applied to diagnose other models
- However, the specific optimal layers may vary by architecture/training

## Relevance to Lab Vision

This paper is **highly relevant** to our lab priorities:

### Direct Alignment with Focus Areas

1. **Cross-Modal Alignment**: The language alignment technique directly addresses our interest in mapping text queries to video in shared embedding spaces. The insight that intermediate layers contain richer features is immediately applicable.

2. **Efficient Video Representation**: The finding that simple frame averaging with high-quality alignment achieves SOTA challenges assumptions about needing complex temporal modeling. This is efficient and scalable.

3. **Benchmark and Evaluation**: Comprehensive evaluation across classification, retrieval, QA, and spatial tasks provides a strong baseline and comparison point.

### Relevance to Temporal Reasoning Priority

The paper's approach to video (frame averaging) is both a **strength and limitation**:
- **Strength**: Achieves SOTA on Kinetics-400 with minimal complexity
- **Critical Gap**: No explicit temporal modeling. This aligns with our lab's strategic priority that "most video-language work treats video as bags of frames."

Research in the broader VLM community shows these models suffer from "time blindness" - achieving 0% on benchmarks requiring temporal reasoning (vs. 98% human). This gap is an **opportunity** for our lab.

### Resources for Building On

- Full code available: https://github.com/facebookresearch/perception_models
- Models on HuggingFace: PE-Core, PE-Lang, PE-Spatial variants
- PE-Video dataset: 1M videos + 120K refined captions
- Clean PyTorch implementation following open_clip structure

## Potential Connections

- **Connection to temporal reasoning work**: The intermediate layer insight could be investigated for temporal features specifically. Do certain layers capture temporal structure better?

- **Gap this reveals**: PE achieves SOTA on video classification/retrieval without ANY temporal modeling. This suggests either:
  1. Current benchmarks don't require temporal reasoning (bias issue)
  2. There's room to improve by adding temporal modeling on top of PE features

- **Connection to our baseline implementation priority**: PE provides an excellent starting point for our text-to-video retrieval baseline. We should evaluate on temporal-focused benchmarks (DiDeMo, ActivityNet-Captions) where frame averaging may struggle.

- **Layer probing as diagnostic**: Could apply their layer-probing methodology to understand where temporal features exist in other video encoders.

## Limitations and Research Directions for Our Lab

### Paper's Limitations

1. **No temporal modeling**: Simple frame averaging cannot capture action sequences, causality, or temporal relationships. "Time blindness" is a known issue in VLMs.

2. **Fixed frame sampling**: N=8 frames may miss important temporal dynamics in longer videos.

3. **Benchmark saturation**: High performance on K400 may reflect benchmark limitations rather than true video understanding.

4. **Compute requirements**: G-scale model (2B params) requires significant resources despite being "efficient" relative to alternatives.

### Research Directions for Our Lab

1. **Temporal layer probing**: Investigate whether intermediate layers contain temporal features that are also being compressed at the output.

2. **PE + Temporal modules**: Use PE as frozen backbone, add lightweight temporal reasoning layers. Could achieve gains efficiently.

3. **Temporal benchmark evaluation**: Evaluate PE on temporal-focused benchmarks (moment retrieval, temporal grounding) where frame averaging should struggle.

4. **Intermediate layer routing**: Could different downstream tasks benefit from different layer combinations? Dynamic layer selection?

5. **Video data engine improvements**: Their synthetic captioning approach could be extended with temporal annotations (action sequences, before/after relationships).

## Ideas Sparked

- **IDEA-001**: Investigate intermediate layers of video encoders for temporal reasoning features using PE's probing methodology. Hypothesis: temporal features exist but are compressed at output layer similar to spatial/language features.

- **IDEA-002**: Build temporal reasoning module on top of frozen PE-Core. Leverage their strong frame representations while adding explicit temporal modeling that's missing.

- **IDEA-003**: Investigate the surprising effectiveness of simple average pooling. How can it be that the lossiness of average pooling does not significantly hamper this approach? Is it a benchmark issue? Do the individual embeddings encode temporal aspects somehow? Perhaps the RoPE embeddings are at play here? Whatever the cause, can it be amplified or harnessed for even better results?

- **IDEA-004**: A toy dataset and model for video retrieval. Experimentation for video retrieval can be prohibitive due to the sheer scale of models and datasets. What if there were a CIFAR or ARK-style dataset that consisted of small videos; small in terms of video dimensions, but still exhibited temporal features needed to solve action or motion-centric tasks? Can we develop such a dataset and demonstrate some of the findings from PerceptionEncoder could have been discovered on a much smaller dataset/model?

---

## Code/Resource Reference

```python
# Basic PE-Core usage
import torch
from PIL import Image
import core.vision_encoder.pe as pe
import core.vision_encoder.transforms as transforms

model = pe.CLIP.from_config("PE-Core-L14-336", pretrained=True)
model = model.cuda()

preprocess = transforms.get_image_transform(model.image_size)
tokenizer = transforms.get_text_tokenizer(model.context_length)

image = preprocess(Image.open("image.png")).unsqueeze(0).cuda()
text = tokenizer(["a cat", "a dog"]).cuda()

with torch.no_grad(), torch.autocast("cuda"):
    image_features, text_features, logit_scale = model(image, text)
    probs = (logit_scale * image_features @ text_features.T).softmax(dim=-1)
```

**Resources**:
- GitHub: https://github.com/facebookresearch/perception_models
- Models: `facebook/PE-Core-{T,S,B,L,G}*`, `facebook/PE-Lang-*`, `facebook/PE-Spatial-*`
- Dataset: `facebook/PE-Video` on HuggingFace
- Paper: https://arxiv.org/abs/2504.13181
