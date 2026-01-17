# Lab Vision

## Mission

Build state-of-the-art text-to-video retrieval systems through engineering-focused applied research. Bridge theoretical insights with practical implementations. Publish papers that advance the field while delivering reproducible, high-performance systems.

## Research Identity

### AI-Agent First

- **Lean into Agents**: Leverage the new age AI agentic systems by seeking research contribution concepts that can be validated quickly with small scale experiments executed by parallel agents
- **Idea Validation Scaling**: Validation that is quick and cheap allows for the investigation of many more ideas; Enables a "fail-fast" approach
- **Quality is Still King**: Idea and experiment quality must remain to a high standard. The brilliance of our lab is in our ability to retain quality while Idea-scaling

### Single-GPU Scaling Methodology

The core principle enabling Idea Validation Scaling: **mathematical equivalence through gradient accumulation**.

```
8 GPUs × 4 accumulation steps = 1 GPU × 32 accumulation steps
→ IDENTICAL gradients, IDENTICAL scaling curves
```

This means any scaling law experiment can be validated on a single GPU before committing expensive multi-GPU compute. The loss curve is identical—just slower.

**Concrete Protocol**:

1. **Validation Phase** (<8 GPU-hours): Run overnight on 1 GPU to trace scaling curve
2. **Go/No-Go Decision**: If curve shows promise → approve compute; if not → iterate cheap
3. **Scale-up Phase**: Only after validation, commit to full multi-GPU run

**Compute Thresholds**:

| Phase | Budget | Decision Point |
|-------|--------|----------------|
| Idea validation | <8 GPU-hours | Does the idea work at all? |
| Ablation studies | <24 GPU-hours | Which components matter? |
| Full experiment | Varies | Final paper-quality results |

See `standards/ml.md` for detailed methodology and confidence metrics for extrapolation.

### Core Approach

- **Engineering-focused**: Start with practical problems, draw on theory for solutions
- **Performance-driven**: Achieve SOTA results with principled methods
- **Reproducible**: All results backed by clean code and clear evaluation
- **Theoretically grounded**: Understand WHY methods work to improve them

### Values

- **Impact over elegance**: Working systems > beautiful theory
- **Rigor in evaluation**: Correct benchmarks > inflated metrics
- **Practical insight**: Understanding that improves performance > abstract knowledge

## Focus Areas (In Scope)

### Primary Themes

1. **Temporal Reasoning**
   - Modeling temporal relationships in video for retrieval
   - Understanding how actions, events, and causality affect relevance
   - Capturing long-range dependencies and temporal structure
   - Temporal grounding and moment retrieval

2. **Cross-Modal Alignment**
   - Mapping text queries to video content in shared embedding spaces
   - Fine-grained alignment between language and visual concepts
   - Handling semantic gaps between modalities
   - Compositional understanding across text and video

3. **Efficient Video Representation**
   - Scalable encoding for large-scale video retrieval
   - Balancing representation quality with computational cost
   - Sparse and selective attention mechanisms
   - Hierarchical video understanding

4. **Benchmark and Evaluation**
   - Rigorous evaluation on standard benchmarks (MSR-VTT, DiDeMo, ActivityNet, etc.)
   - Understanding dataset biases and limitations
   - Developing better evaluation protocols for temporal understanding

### Subdomain Keywords (for search/exploration)

text-to-video retrieval, video-text matching, temporal grounding, moment retrieval, cross-modal learning, vision-language models, video understanding, CLIP, contrastive learning, transformer attention, video encoding, dense retrieval, compositional reasoning, action recognition, event understanding

## Research Taste

### Good Problems (pursue)

- Improves SOTA on established benchmarks with principled methods
- Addresses real limitations in current systems (e.g., temporal reasoning gaps)
- Provides insights that generalize beyond specific datasets
- Offers practical techniques that can be adopted by practitioners
- Balances novelty with reproducibility

### Bad Problems (avoid)

- Incremental benchmark improvements without insight
- Methods requiring prohibitive compute (100+ GPU days)
- Narrow tricks that only work on specific datasets
- Complex architectures with marginal gains
- Work without proper baselines or ablations

### Paper Quality Signals

- Clear performance gains on multiple benchmarks
- Ablations that reveal which components matter
- Analysis that explains when and why the method works
- Reproducible results with released code
- Connects to broader challenges in the field

### Strategic Priorities

- **Temporal reasoning as differentiator**: Most video-language work treats video as bags of frames. Methods that truly capture temporal structure have high novelty.
- **Efficiency matters**: Industry deployment requires practical efficiency. Methods that achieve strong results at lower cost are valuable.
- **Cross-benchmark generalization**: Methods that transfer across datasets signal genuine capability vs. dataset-specific overfitting.
- **Build on foundation models**: Leverage CLIP, BLIP, VideoMAE, etc. Focus on architectural innovations and fine-tuning strategies rather than pretraining from scratch.

## Non-Goals (Out of Scope)

Explicit boundaries:

- Pure theoretical papers without experimental validation
- Video generation or synthesis (we focus on understanding/retrieval)
- General-purpose video classification (unless directly relevant to retrieval)
- Methods requiring pretraining from scratch on massive datasets
- Survey/review papers (we create new methods)

## Agent Instructions

### Explorer Agent

When searching literature or identifying research directions:

- Prioritize recent papers from CVPR, ICCV, ECCV, NeurIPS, ACL, EMNLP
- Look for gaps in temporal reasoning and cross-modal alignment
- Track advances in foundation models (CLIP, BLIP, VideoMAE, etc.)
- Search using Subdomain Keywords above
- Flag papers with strong baselines and ablations

### Paper Agent

When evaluating paper proposals:

- Check alignment with Focus Areas (temporal + cross-modal)
- Verify benchmark evaluation is comprehensive
- Ensure method has clear ablations planned
- Reject if it falls under Non-Goals

### Orchestrator

When prioritizing work:

- Advance papers addressing temporal reasoning gaps
- Prioritize work with multiple benchmark evaluations
- Deprioritize pure engineering without insight
- Balance exploration (new ideas) with exploitation (finishing papers)
