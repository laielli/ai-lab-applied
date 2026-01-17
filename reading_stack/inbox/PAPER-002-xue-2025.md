# Paper: Seeing the Arrow of Time in Large Multimodal Models

- **ID**: PAPER-002
- **arXiv**: 2506.03340
- **Authors**: Zihui Xue, Mi Luo, Kristen Grauman
- **Year**: 2025
- **Venue**: NeurIPS 2025
- **Added**: 2026-01-17
- **Status**: summarized
- **Summary**: reading_stack/summaries/PAPER-002-xue-2025.md
- **Project**: https://vision.cs.utexas.edu/projects/SeeAoT

## Why Read

This paper directly addresses temporal reasoning in video understanding—our lab's primary research theme. Large multimodal models struggle with temporal directionality (distinguishing forward from reverse video), which aligns perfectly with our investigation into why temporal-naive methods (like average pooling) perform well on benchmarks like K400.

The paper introduces:
1. **ArrowRL**: An RL-based training strategy using "reverse rewards" to teach temporal awareness
2. **AoTBench**: A benchmark specifically designed to evaluate temporal understanding

Results show 20%+ accuracy gains on temporal tasks. This is highly relevant to both IDEA-003 (understanding why average pooling works) and IDEA-004 (TinyVid benchmark design), as it provides methods and evaluation frameworks for temporal reasoning.

## Focus Areas
- [x] Temporal Reasoning
- [x] Cross-Modal Alignment
- [x] Benchmark and Evaluation
- [ ] Efficient Video Representation

## Notes

Key aspects to examine:
- How ArrowRL's reverse reward mechanism works in practice
- What temporal aspects AoTBench evaluates (order, direction, causality?)
- Comparison with other temporal modeling approaches
- Computational cost of the RL training strategy
- Whether these techniques can adapt to video retrieval tasks (our focus)

Connections to current lab work:
- IDEA-003: Could ArrowRL explain why PE succeeds without explicit temporal modeling?
- IDEA-004: AoTBench design may inform TinyVid's temporal evaluation methodology
- Kristen Grauman is a leading researcher in video understanding (UT Austin)

## Questions

1. How does ArrowRL's reverse reward mechanism specifically work? Is it contrastive (forward vs. backward) or something else?

2. What temporal phenomena does AoTBench evaluate? Does it test order sensitivity, causality, or direction-dependent actions?

3. How does this compare to explicit temporal modeling (temporal attention, 3D convolutions) in terms of effectiveness and efficiency?

4. Can ArrowRL be applied to contrastive video-text training (our retrieval focus), or is it specific to QA tasks?

5. What is the computational overhead of the RL training strategy?

6. How does model performance scale with video length and temporal complexity?

7. Does the paper analyze which video types/actions require temporal directionality understanding vs. which are direction-invariant?

8. Could this approach be combined with average pooling methods like Perception Encoder?
