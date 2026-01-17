# Summary: Seeing the Arrow of Time in Large Multimodal Models

- **Paper ID**: PAPER-002
- **arXiv**: 2506.03340
- **Authors**: Zihui Xue, Mi Luo, Kristen Grauman (UT Austin)
- **Venue**: NeurIPS 2025
- **Project**: https://vision.cs.utexas.edu/projects/SeeAoT
- **Summarized**: 2026-01-17

## Focus Area Tags
- Temporal Reasoning
- Cross-Modal Alignment
- Benchmark and Evaluation

## One-Line Summary

ArrowRL, an RL-based training strategy using reverse video rewards built on GRPO, significantly improves temporal direction sensitivity in video LMMs, validated on the new AoTBench benchmark with 20%+ gains on temporal tasks.

## Key Contributions

1. **ArrowRL Training Algorithm**: A novel RL approach based on Group Relative Policy Optimization (GRPO) that uses a reverse reward mechanism to encourage divergent interpretations between forward and reversed video playback, teaching models temporal directionality awareness.

2. **AoTBench Benchmark**: The first dedicated benchmark for evaluating Arrow of Time (AoT) perception in LMMs, comprising three tasks: sequence direction classification, directional caption matching, and AoT-sensitive VQA.

3. **Empirical Validation**: Demonstrates substantial improvements (up to +21% on temporal tasks, +65.9% relative gain on Vinoground) while maintaining performance on temporally-insensitive benchmarks.

4. **Diagnostic Analysis**: Reveals that baseline LMMs exhibit a "universal failure mode" where responses are identical regardless of video playback direction, achieving only chance-level performance on temporal direction tasks.

## Methodology

### ArrowRL Algorithm

Built on GRPO, ArrowRL introduces a dual-reward structure:

**Reward Formulation**:
- Fidelity Reward: `r_fid = Similarity(output, ground_truth)`
- Reverse Reward: `r_rev = 1 - Similarity(output, reversed_video_output)`
- Combined: `r = r_fid + alpha * r_rev`

**Key Innovation**: Dynamic weighting via threshold gamma (default 0.75). When the reversed video prediction is too similar to ground truth (non-temporally-sensitive sample), alpha is set to 0 to avoid penalizing valid predictions.

**Training Details**:
- 2,000 RL steps on 6 NVIDIA GH200 GPUs
- 16-frame maximum during training
- ~24.6K training examples selected for high temporality
- Training data: UCF101 MCQ (1.1K), LLaVA-Video-178K filtered (11.8K), RTime captions (11.7K)

### AoTBench Benchmark

| Task | Dataset Source | Size | Evaluation |
|------|---------------|------|------------|
| Sequence Direction Classification | ReverseFilm + UCF101 | 613 videos | Binary accuracy |
| Directional Caption Matching | RTime | 2,000 videos | V2T & T2V MCQ |
| AoT-sensitive VQA | Curated from 8 benchmarks | 1,800 samples | MCQ accuracy |

High Temporal Divergence Score (TDS) samples were prioritized -- samples where model predictions are highly sensitive to temporal direction.

## Key Results

### AoTBench Performance

| Model | ReverseFilm | UCF | T2V | V2T | AoT-VQA | Avg |
|-------|-------------|-----|-----|-----|---------|-----|
| Qwen2.5-VL-7B base | 50.0% | 51.6% | 53.4% | 66.6% | 49.6% | 54.2% |
| + ArrowRL | 51.4% | 54.8% | 55.6% | 69.6% | 58.8% | 58.0% |
| Qwen2-VL-7B base | 52.8% | 51.5% | 50.7% | 63.7% | 48.6% | 53.5% |
| + ArrowRL | **71.9%** | **72.5%** | 53.3% | 69.2% | 57.4% | **64.9%** |

**Notable**: Qwen2-VL-7B shows +19.1% on ReverseFilm, +21.0% on UCF after ArrowRL training.

### Transfer to General Benchmarks

ArrowRL preserves (and often improves) performance on temporally-insensitive benchmarks:
- VideoMME: 67.78% -> 68.11%
- NExT-QA: 77.11% -> 78.11%
- Vinoground: +65.9% relative improvement

### Ablation Studies

| Configuration | AoTBench Avg |
|---------------|--------------|
| SFT only (no RL) | 57.4% |
| ArrowRL (alpha=0, no reverse reward) | Below baseline |
| ArrowRL (fixed gamma=1.0) | 59.8% |
| **ArrowRL (dynamic gamma=0.75)** | **61.4%** |

Optimal hyperparameters: alpha=0.25, gamma=0.75.

### Model Comparisons

| Model | Vinoground |
|-------|-----------|
| Proprietary (GPT-4o) | 74.8% |
| Video-R1-7B | 73.1% |
| LLaVA-Video-7B | 71.4% |
| **Qwen2.5-VL + ArrowRL** | **75.5%** |

## Answers to First-pass Questions

**Q1: How does ArrowRL's reverse reward mechanism work?**

The reverse reward penalizes outputs that remain similar when the input video is reversed. For each training sample, both forward and reversed videos are processed, and the model is rewarded for producing divergent responses (indicating temporal awareness). A dynamic threshold (gamma=0.75) disables the reverse penalty for samples where temporal direction genuinely doesn't matter.

**Q2: What temporal phenomena does AoTBench evaluate?**

Three distinct phenomena: (1) basic sequence direction classification (forward vs reversed), (2) directional caption matching (matching videos to captions that differ only in temporal direction, e.g., "unwrapping" vs "wrapping"), (3) AoT-sensitive VQA where correct answers depend on understanding temporal flow.

**Q3: Comparison to explicit temporal modeling?**

ArrowRL is a training strategy, not an architectural change. It can be applied to any video LMM without modifying the architecture. The paper shows it's more effective than supervised fine-tuning (SFT) alone and doesn't require explicit temporal attention mechanisms.

**Q4: Application to contrastive video-text training (retrieval)?**

The paper focuses on VQA and captioning tasks, not retrieval. However, the reverse reward concept could potentially be adapted to contrastive learning by encouraging embeddings to differ between forward and reversed videos. This is an open direction.

**Q5: Computational overhead?**

Moderate: 2,000 RL steps on 6 NVIDIA GH200 GPUs with ~24.6K training samples. More expensive than SFT but feasible for lab-scale research.

**Q6: Scaling with video length/complexity?**

Not explicitly studied. Training uses 16 frames maximum. The paper doesn't analyze performance vs. video duration.

**Q7: Analysis of direction-invariant vs direction-dependent actions?**

Yes, implicitly via the dynamic gamma threshold. The TDS (Temporal Divergence Score) identifies which samples truly require temporal reasoning. Actions like "standing" are flagged as direction-invariant; "pouring water" as direction-dependent.

**Q8: Combination with average pooling methods?**

Not explored. ArrowRL targets autoregressive LMMs, not embedding-based retrieval models like Perception Encoder. Could be an interesting future direction.

## Relevance to Lab Vision

**Direct Relevance to Temporal Reasoning Priority**:

This paper directly addresses the lab's primary theme of temporal reasoning in video understanding. Key connections:

1. **Validates H1 from IDEA-003**: The paper confirms that current video LMMs have a "universal failure mode" on temporal direction tasks, achieving chance-level performance. This supports our hypothesis that benchmarks may not adequately test temporal reasoning.

2. **Benchmark Design for IDEA-004 (TinyVid)**: AoTBench's three-task structure provides a template for evaluating temporal understanding:
   - Direction classification (binary)
   - Directional matching (contrastive)
   - Temporal-sensitive QA (compositional)

   TinyVid could incorporate similar tasks at CIFAR scale.

3. **The Reverse Reward Concept**: Could inspire training strategies for contrastive video-text models. Instead of only positive pairs, explicitly train on (video, text) vs (reversed_video, text) to force temporal awareness.

4. **TDS Metric**: The Temporal Divergence Score for identifying temporally-sensitive samples could be adapted to curate TinyVid-Real from K400.

**Gap Identified**: ArrowRL is designed for autoregressive VQA, not embedding-based retrieval. Adapting the reverse reward concept to contrastive learning (CLIP-style) is unexplored.

## Potential Connections

- **PAPER-001 (Perception Encoder)**: PE achieves SOTA on K400 video retrieval with zero temporal modeling. ArrowRL's findings suggest this may be because K400 doesn't require temporal direction understanding, not because PE implicitly captures it.

- **IDEA-003 (Average Pooling)**: ArrowRL supports hypothesis H1 (benchmark artifact). If models with average pooling succeed on K400 but ArrowRL-trained models show massive gains on AoTBench, K400 may not test temporal reasoning. However, PE's lack of temporal PE is a separate issue from model training.

- **IDEA-004 (TinyVid)**: AoTBench's design principles should inform TinyVid:
  - Include direction-sensitive tasks (already explored with cyclic motions)
  - Use TDS-like metrics to verify temporal signal
  - Test both classification and retrieval modalities

- **Gap for New Research**: No work applies ArrowRL-style reverse rewards to contrastive retrieval training. This could be a novel contribution: "Temporal-Aware Contrastive Learning via Reverse Video Rewards."

## Ideas Sparked

- **IDEA-005 (potential)**: Adapt ArrowRL's reverse reward to contrastive video-text training. Train embeddings where sim(video, text) >> sim(reversed_video, text) for temporally-sensitive pairs. Could improve retrieval on temporal benchmarks without architectural changes.

- **TinyVid Enhancement**: Add AoTBench-style tasks to TinyVid:
  1. Direction classification (forward vs reversed)
  2. Directional caption retrieval
  3. Order-sensitive QA

  Use TDS to verify synthetic videos have genuine temporal signal.

- **Temporal Benchmark Analysis**: Apply AoTBench evaluation to K400 to quantify what fraction of K400 actually requires temporal direction understanding. Could explain PE's success.

## Critical Assessment

**Strengths**:
- Novel training approach that works across multiple base models
- Rigorous benchmark with three complementary tasks
- Strong empirical results with good ablations
- Identifies fundamental failure mode in current LMMs

**Limitations**:
- Focused on VQA, not retrieval (our primary focus)
- Computational cost of RL training may limit adoption
- 16-frame training limit may not capture long-range temporal dependencies
- No analysis of video length or temporal complexity scaling
- Transfer to retrieval tasks unexplored

**Quality Signals**:
- From top lab (Kristen Grauman, UT Austin)
- NeurIPS 2025 acceptance
- Clear problem formulation and solution
- Comprehensive evaluation across multiple models and benchmarks
- Released benchmark and code

## Summary for Lab Discussion

ArrowRL demonstrates that current video LMMs have essentially no temporal direction awareness (chance-level on forward vs reversed classification), but this can be trained via RL with reverse video rewards. The AoTBench benchmark provides a template for rigorous temporal evaluation.

**Key takeaway for our work**: If state-of-the-art LMMs fail at basic temporal direction tasks, it suggests that benchmarks like K400 (where PE excels with average pooling) may not meaningfully test temporal reasoning. This supports IDEA-003's investigation into why average pooling works.

**Actionable next steps**:
1. Evaluate PE on AoTBench-style tasks to verify temporal blindness
2. Adapt AoTBench task structure to TinyVid design
3. Explore reverse reward concept for contrastive retrieval training
