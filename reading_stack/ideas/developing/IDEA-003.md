# IDEA-003: The Surprising Effectiveness of Average Pooling

**Status**: Developing → Investigating
**Source**: PAPER-001 (Bolya et al., Perception Encoders)
**Created**: 2026-01-16
**Investigation**: `papers/idea-003-avg-pooling/`

## Core Question

Why does simple average pooling over frame embeddings achieve SOTA on video retrieval benchmarks (76.9% on K400), despite losing all temporal ordering information?

## Observation

From PAPER-001:
- PE uses N=8 frame averaging with no temporal attention
- Achieves SOTA on K400 video retrieval
- Contradicts intuition that temporal reasoning requires temporal structure

## Hypotheses

| ID | Hypothesis | Status | Evidence |
|----|------------|--------|----------|
| H1 | **Benchmark Artifact** — K400 doesn't require temporal reasoning | Needs testing | — |
| H2 | **Implicit Temporal Encoding** — Frames encode temporal context via motion blur, object states | Primary focus | — |
| H3 | **Position Encoding Signal** — RoPE preserves temporal signal | ❌ Refuted | Codebase shows RoPE is purely spatial |
| H4 | **High-Dimensional Preservation** — 1536-d averaging preserves info | Secondary | — |

## Key Finding (Exp 1.1)

**PE has ZERO temporal modeling**:
- `encode_video` simply averages frame embeddings
- RoPE is purely 2D spatial (patch x, y)
- No temporal position encoding exists
- All frames receive identical position encodings

This means H2 (implicit temporal encoding) is the most likely explanation.

## Investigation Status

**Phase 1: Understanding** (In Progress)
- [x] Exp 1.1: PE Codebase Analysis — COMPLETE
- [ ] Exp 1.2: Frame Order Prediction Probe — Framework ready
- [ ] Exp 1.3: Frame Shuffle Baseline — Framework ready
- [ ] Exp 1.4: Temporal Visualization — Framework ready

**Phase 2: Deep Investigation** (Pending)
- [ ] Exp 2.1: Position Encoding Ablation
- [ ] Exp 2.2: Implicit Temporal Feature Analysis
- [ ] Exp 2.3: SSv2 Evaluation

**Phase 3: Improvement** (Pending)
- [ ] Design amplification methods based on findings

## Paper Potential

**If H2 confirmed**:
- Design temporal-aware pooling that amplifies implicit temporal features
- Compare against attention-based methods
- Demonstrate efficiency (minimal compute overhead)

**If H1 confirmed**:
- Argue for new temporal benchmarks
- Demonstrate PE fails on truly temporal tasks (SSv2)
- Propose benchmark for temporal reasoning

**Either direction is publishable** — novel understanding of a surprising empirical result.

## Next Steps

1. Acquire K400 validation set subset (or use public videos)
2. Run Exp 1.2-1.4 to validate/refute H2
3. Based on findings, proceed to Phase 2

## Related Work

- Bolya et al. 2025 (PE paper) — source observation
- Something-Something v2 — temporal benchmark
- K400 — current benchmark (may be artifact-prone)
