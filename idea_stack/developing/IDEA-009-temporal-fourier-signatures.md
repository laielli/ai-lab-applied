# Idea: Temporal Fourier Signatures (TFS) → TOPA Pivot

- **ID**: IDEA-009
- **Stage**: PIVOTING (was shelved)
- **Created**: 2026-01-21
- **Promoted**: 2026-01-21
- **Launched**: 2026-01-21
- **Shelved**: 2026-01-24
- **Pivot**: 2026-01-24 → TOPA (Temporal Order-Preserving Aggregation)
- **Source Papers**: PAPER-005 (RoFormer/RoPE), PAPER-006 (Complex Embeddings), PAPER-008 (Mechanistic RoPE)
- **Related Ideas**: IDEA-008 (TDPE)

---

## PIVOT NOTICE (2026-01-24)

**Status**: PIVOTING from rotation-based TFS to additive TOPA after identifying fundamental theoretical issue.

**Root Cause Identified**: TFS rotation breaks CLIP alignment
```
TFS applies: video_embed = rotate(frames, phases) → rotated space
Text remains: text_embed = unchanged            → original space
Result: Fundamental misalignment that projection cannot recover
```

**New Approach (TOPA)**: Additive positional encoding preserves alignment
```python
# Instead of rotation, use small additive perturbation
video_embed = frames + sinusoidal_pos * 0.1  # slight perturbation
text_embed = unchanged                        # same space
```

**Implementation Complete**: `papers/idea-009-tfs/src/tfs/topa.py`
**Validation Experiment**: EXP-014 ready to run

---

## ORIGINAL SHELVING NOTICE

**Critical Finding**: With real CLIP features, TFS degrades performance by -11.4 percentage points compared to mean pooling.

**Key Learnings**:
1. Synthetic feature evaluation is insufficient - must validate with real features
2. Single-seed results are unreliable - always run multi-seed
3. Mechanism validation ≠ application success
4. The +8.8pp claim was a seed artifact (p=1.0 across 5 seeds)
5. **NEW**: Rotation-based encoding fundamentally breaks CLIP alignment

**Full Report**: `papers/idea-009-tfs/STATUS.md` and `papers/idea-009-tfs/log/FINAL_VALIDATION_SUMMARY.md`

---

## Original Research Question

Can we design video frame embeddings that **preserve temporal dynamics and ordering when summed/averaged**, enabling efficient single-vector retrieval while retaining the temporal reasoning capabilities of sequence-based methods?

## Original Hypothesis

By encoding frame position via rotation (inspired by RoPE/complex embeddings) before aggregation, the resulting sum will:
1. **Preserve ordering**: Different orderings of the same content → different sums
2. **Encode temporal dynamics**: Rapid changes → high-frequency energy; slow changes → low-frequency
3. **Enable cross-modal alignment**: Text temporal words can be mapped to matching phase structure

## What Worked (Mechanism Validated)

| Claim | Status | Evidence |
|-------|--------|----------|
| Order preservation | ✓ Validated | 600K-1Mx variance ratio (Exp 1A) |
| Order reconstruction | ✓ Validated | 79% vs 24% accuracy (Exp 4B) |
| Information capacity | ✓ Validated | 12.8 effective dims (Exp 4A) |
| Cross-modal alignment | ✓ Validated | 100% accuracy (Exp 3A) |

## What Failed (Application Not Validated)

| Claim | Status | Evidence |
|-------|--------|----------|
| Retrieval improvement | ✗ FAILED | -11.4pp with real features |
| Dynamics encoding | ✗ FAILED | Theory flaw (Exp 2A-C) |
| Efficiency advantage | ✗ FAILED | Similar to attention |

## Validation Experiments Summary

| Experiment | Question | Result |
|------------|----------|--------|
| EXP-007 | Is +8.8pp significant? | NO - p=1.0, seed artifact |
| EXP-011 | VATEX pattern? | WEAK - +1.7pp only |
| EXP-008 | Synthetic controlled | NO - Mean beats TFS |
| EXP-012C | Real CLIP features | NEGATIVE - TFS -11.4pp |

## Why Shelved

The TFS mechanism successfully preserves temporal order in embeddings, but this does **not translate to retrieval improvement**. With real CLIP features:

1. Temporal information may already be encoded in semantic content
2. Rotation encoding interferes with existing CLIP structure
3. The added positional information is redundant or harmful

## Files

- Paper directory: `papers/idea-009-tfs/`
- Final status: `papers/idea-009-tfs/STATUS.md`
- Validation summary: `papers/idea-009-tfs/log/FINAL_VALIDATION_SUMMARY.md`

---

## TOPA Pivot (2026-01-24)

### Theoretical Insight

The core issue with TFS is that **rotation is a unitary transformation** that maps CLIP embeddings to an orthogonal subspace, fundamentally breaking the pre-trained alignment with text embeddings.

| Approach | CLIP Alignment | Temporal Expressiveness |
|----------|---------------|------------------------|
| Rotation (TFS) | Destroys | Excellent |
| Additive position | Preserves | Moderate |
| Weighted averaging | Best | Limited |

### TOPA Design

TOPA uses **additive** positional encoding instead of rotation:

```python
class TemporalOrderPreservingAggregation(nn.Module):
    def forward(self, frames):  # [B, T, D]
        # 1. Add sinusoidal position (small scale preserves alignment)
        pos_frames = frames + self.pos_encoding[:T] * 0.1

        # 2. Position-weighted aggregation
        weights = softmax(self.frame_weights[:T])
        weighted_mean = (pos_frames * weights).sum(dim=1)

        # 3. Temporal difference features (captures dynamics)
        diffs = frames[:, 1:] - frames[:, :-1]
        diff_features = self.diff_proj(diffs.mean(dim=1))

        return self.output_proj(cat([weighted_mean, diff_features]))
```

### Initial Results

Order discrimination test (100 samples):
- **TOPA**: 100% accuracy (can distinguish forward vs reversed)
- **Mean pooling**: 0% accuracy (permutation invariant)

### Next Steps

1. **EXP-014**: Run TOPA validation on real CLIP features
2. Success criteria:
   - TOPA R@10 ≥ Mean R@10 - 2pp (don't hurt baseline)
   - Alignment preservation ≥ 95%
   - TOPA > Mean on temporal queries

### Key Files

- `papers/idea-009-tfs/src/tfs/topa.py` - TOPA implementation
- `papers/idea-009-tfs/src/experiments/exp14_topa_validation.py` - Validation experiment
- `papers/idea-009-tfs/experiment_stack/_inbox/EXP-014-topa-validation.md` - Experiment spec

---

*Pivoting to TOPA on 2026-01-24 after identifying rotation as the root cause of CLIP alignment failure.*
