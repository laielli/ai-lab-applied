# IDEA-003: The Surprising Effectiveness of Average Pooling

**Status**: Developing → Investigating
**Source**: PAPER-001 (Bolya et al., Perception Encoders)
**Created**: 2026-01-16
**Updated**: 2026-01-23
**Investigation**: `papers/idea-003-avg-pooling/`
**Merged**: IDEA-011 (Intermediate Layer Temporal Probing)

## Core Question

Why does simple average pooling over frame embeddings achieve SOTA on video retrieval benchmarks (76.9% on K400), despite losing all temporal ordering information?

## Observation

From PAPER-001:
- PE uses N=8 frame averaging with no temporal attention
- Achieves SOTA on K400 video retrieval
- Contradicts intuition that temporal reasoning requires temporal structure

Additionally, PE demonstrates that optimal embeddings for various tasks exist in intermediate transformer layers rather than the final output. This raises the question: **do intermediate layers contain temporal features that are compressed away at the output?**

## Hypotheses

| ID | Hypothesis | Status | Evidence |
|----|------------|--------|----------|
| H1 | **Benchmark Artifact** — K400 doesn't require temporal reasoning | Needs testing | — |
| H2 | **Implicit Temporal Encoding** — Frames encode temporal context via motion blur, object states | Primary focus | — |
| H3 | **Position Encoding Signal** — RoPE preserves temporal signal | ❌ Refuted | Codebase shows RoPE is purely spatial |
| H4 | **High-Dimensional Preservation** — 1536-d averaging preserves info | Secondary | — |
| H5 | **Intermediate Layer Temporal Features** — Temporal features exist in intermediate layers but are compressed at output | New (from IDEA-011) | — |

## Key Finding (Exp 1.1)

**PE has ZERO temporal modeling**:
- `encode_video` simply averages frame embeddings
- RoPE is purely 2D spatial (patch x, y)
- No temporal position encoding exists
- All frames receive identical position encodings

This means H2 (implicit temporal encoding) or H5 (intermediate layer compression) are the most likely explanations.

## Investigation Status

### Phase 1: Understanding (In Progress)
- [x] Exp 1.1: PE Codebase Analysis — COMPLETE
- [ ] Exp 1.2: Frame Order Prediction Probe — Framework ready
- [ ] Exp 1.3: Frame Shuffle Baseline — Framework ready
- [ ] Exp 1.4: Temporal Visualization — Framework ready

### Phase 2: Deep Investigation (Pending)
- [ ] Exp 2.1: Position Encoding Ablation
- [ ] Exp 2.2: Implicit Temporal Feature Analysis
- [ ] Exp 2.3: SSv2 Evaluation (truly temporal benchmark)

### Phase 3: Intermediate Layer Probing (NEW - from IDEA-011)

Apply PE's layer-probing methodology to temporal tasks:

- [ ] Exp 3.1: **Layer-wise Temporal Probing**
  - Extract embeddings from each transformer layer (1-50)
  - Train linear probes for temporal ordering (frame A before/after B)
  - Plot accuracy vs. layer to find temporal feature peak

- [ ] Exp 3.2: **Task-Specific Layer Analysis**
  - Action ordering: Which layer best predicts action sequence?
  - Temporal grounding: Which layer localizes moments best?
  - Compare to PE's findings for spatial/language tasks

- [ ] Exp 3.3: **Temporal Feature Extraction**
  - If temporal features peak at intermediate layer (e.g., layer 35):
  - Design temporal alignment similar to PE's language/spatial alignment
  - Train projector to surface temporal features at output

### Phase 4: Improvement (Pending)
- [ ] Design amplification methods based on findings
- [ ] Temporal-aware pooling that leverages discovered features
- [ ] Compare against attention-based methods

## Paper Potential

**If H2 confirmed** (implicit encoding):
- Design temporal-aware pooling that amplifies implicit temporal features
- Compare against attention-based methods
- Demonstrate efficiency (minimal compute overhead)

**If H5 confirmed** (intermediate layer compression):
- First demonstration that temporal features are "hidden" like spatial/language
- Novel temporal alignment technique to surface these features
- Direct extension of PE's central insight to temporal domain

**If H1 confirmed** (benchmark artifact):
- Argue for new temporal benchmarks
- Demonstrate PE fails on truly temporal tasks (SSv2)
- Propose benchmark for temporal reasoning

**All directions are publishable** — novel understanding of a surprising empirical result.

## Connection to Lab Vision

Directly addresses the lab's temporal reasoning priority. If temporal features are being compressed at the output layer, this could explain why simple frame averaging achieves SOTA on current benchmarks — the temporal signal may never reach the output but still influences intermediate representations.

## Next Steps

1. Run Exp 1.2-1.4 to validate/refute H2 (implicit encoding)
2. Run Exp 3.1 to test H5 (intermediate layer compression)
3. Based on findings, proceed to Phase 4 (improvement)

## Related Work

- Bolya et al. 2025 (PE paper) — source observation, layer probing methodology
- Something-Something v2 — temporal benchmark
- K400 — current benchmark (may be artifact-prone)
- VideoRoPE, VRoPE — temporal position encoding attempts

## Promotion Criteria

- [x] Clear research question
- [x] Testable hypotheses
- [x] Novelty argument
- [x] Viable experiment plan
- [ ] Validation experiments completed (Exp 1.2-1.4 or 3.1)
