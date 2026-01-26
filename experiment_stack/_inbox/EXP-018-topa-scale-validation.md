# EXP-018: TOPA Scale Validation on PE-Video

**Created**: 2026-01-25
**Revised**: 2026-01-25 (addressed verification issues)
**Paper**: IDEA-009 Temporal Fourier Signatures
**Status**: BLOCKED
**Blocked by**: EXP-017
**Priority**: P1 - Critical for go/no-go decision

---

## Objective

Validate TOPA's R@1 improvement (+3.3pp) at scale on PE-Video (500+ videos) with sufficient statistical power.

## Research Question

**Does TOPA's R@1 improvement hold at larger scale?**

This is NOT testing temporal query improvement (that's EXP-019 on DiDeMo). This experiment validates whether the R@1 finding from EXP-014 is real or noise.

## Prior Results: EXP-014 (CLIP on MSR-VTT subset)

Results from `papers/idea-009-tfs/log/exp14/exp14_final_results.json`:

| Method | R@1 | R@5 | R@10 |
|--------|-----|-----|------|
| **TOPA (α=0.01)** | **40.0%** | 66.7% | 83.3% |
| Mean | 36.7% | 66.7% | 83.3% |
| TFS | 3.3% | 3.3% | 10.0% |

**Key findings:**
- R@1 improvement: **+3.3pp** (but only 1 additional correct video out of 30)
- R@5/R@10: Identical to mean pooling
- Alignment preservation: **99.2%**
- TFS: Catastrophic failure (-73.3pp), confirms rotation breaks alignment

**Limitation:** 30 test videos is underpowered. Need 500+ for statistical confidence.

## Hypothesis

TOPA's additive positional encoding preserves cross-modal alignment while encoding temporal order. On PE-Video:
1. Alignment preservation should remain ≥95%
2. R@1 improvement should replicate (+2pp or more with p<0.05)
3. Order discrimination should work (TOPA >90%, Mean ≈50%)

## Method

### Phase 0: Alignment Preservation Check (5 min)

**Before any training**, validate TOPA preserves PE-Core alignment:

```python
from src.tfs.topa import measure_alignment_preservation, TOPAMinimal

# Load 50 sample videos from EXP-017
data = torch.load('log/exp17/pe_video_features.pt')
frames = data['video_features'][:50]  # [50, 8, 1024]
text = data['text_features'][:50]     # [50, 1024]

# Check alignment
topa = TOPAMinimal(dim=1024, position_scale=0.01)
result = measure_alignment_preservation(topa, frames, text)

print(f"Alignment preservation: {result['preservation_ratio']:.1%}")
assert result['preservation_ratio'] >= 0.95, \
    "STOP: TOPA doesn't preserve PE alignment. Investigate before proceeding."
```

**If alignment < 95%:** Do not proceed. Investigate why PE differs from CLIP.

### Phase 1: Order Discrimination (30 min)

Quick validation that TOPA encodes order:

```python
# Create forward and reversed versions
forward = frames  # [N, 8, D]
reversed = frames.flip(dims=[1])  # [N, 8, D]

# Encode with TOPA
topa_fwd = topa(forward)
topa_rev = topa(reversed)

# Train simple classifier
# Expected: TOPA achieves ~100% accuracy, Mean achieves ~50%
```

**If TOPA < 80% accuracy:** Mechanism not working on PE. Investigate.

### Phase 2: Full Retrieval Validation (2 hours)

Only proceed if Phase 0 and Phase 1 pass.

1. Load PE-Core features from EXP-017 (500+ videos, 8 frames each)
2. 80/20 train/test split (400/100 videos)
3. Train projections with contrastive loss (3 seeds)
4. Evaluate R@1, R@5, R@10 with bootstrap CIs

## Technical Details

### Model Configuration

| Parameter | Value | Source |
|-----------|-------|--------|
| Input dim | 1024 | PE-Core-L14-336 |
| Output dim | 512 | Standard |
| Frames | 8 | PE protocol |
| Position scale | 0.01 | EXP-014 (validated) |
| Temporal diff | Enabled | TOPA default |

### Training Protocol

| Parameter | Value |
|-----------|-------|
| Train/Test split | 80/20 (400/100 videos) |
| Loss | InfoNCE (contrastive) |
| Optimizer | Adam |
| Learning rate | 1e-4 |
| Epochs | 100 |
| Batch size | 32 |
| Seeds | 3 |

### Methods to Compare

| Method | Description | Expected |
|--------|-------------|----------|
| **TOPA (α=0.01)** | Full: position + diff + weights | Best or tied |
| **TOPA-minimal** | Position only | Isolate position effect |
| **Mean pooling** | Simple average | Baseline |
| ~~TFS~~ | ~~Rotation-based~~ | Removed (already validated failure) |

**Note:** TFS removed since EXP-014 already confirmed catastrophic failure. No need to re-validate.

## Evaluation Protocol

### Primary Metrics

| Metric | Description |
|--------|-------------|
| R@1 | Primary (most sensitive to ranking quality) |
| R@5, R@10 | Secondary |
| 95% CI | Bootstrap (1000 samples) |

### Statistical Testing

```python
# Bootstrap test for R@1 improvement
n_bootstrap = 1000
topa_r1_samples = []
mean_r1_samples = []

for _ in range(n_bootstrap):
    idx = np.random.choice(len(test_set), size=len(test_set), replace=True)
    topa_r1_samples.append(compute_r1(topa_preds[idx], labels[idx]))
    mean_r1_samples.append(compute_r1(mean_preds[idx], labels[idx]))

delta = np.array(topa_r1_samples) - np.array(mean_r1_samples)
p_value = (delta <= 0).mean()  # One-sided test
ci_95 = np.percentile(delta, [2.5, 97.5])
```

## Success Criteria

| Outcome | Condition | Decision |
|---------|-----------|----------|
| **Strong continue** | R@1 ≥ Mean + 2pp AND p < 0.05 | Proceed to EXP-019 (temporal benchmark) |
| **Continue cautiously** | R@1 ≥ Mean + 1pp AND p < 0.10 | Proceed with lower confidence |
| **Neutral** | R@1 within ±1pp OR p ≥ 0.10 | R@1 improvement likely noise |
| **Shelve** | R@1 < Mean - 1pp | TOPA hurts performance |

### Phase Gates

| Phase | Pass Condition | Fail Action |
|-------|----------------|-------------|
| Phase 0 | Alignment ≥ 95% | Investigate PE vs CLIP difference |
| Phase 1 | Order accuracy ≥ 80% | Mechanism broken, investigate |
| Phase 2 | R@1 ≥ Mean + 1pp | If also fails EXP-019, shelve IDEA-009 |

## Output

| File | Description |
|------|-------------|
| `log/exp18/phase0_alignment.json` | Alignment check results |
| `log/exp18/phase1_order_discrimination.json` | Forward/reverse accuracy |
| `log/exp18/phase2_retrieval_results.json` | Full metrics with CIs |
| `log/exp18/bootstrap_analysis.json` | Statistical test results |

## Compute Estimate

| Phase | Time | GPU |
|-------|------|-----|
| Phase 0: Alignment check | 5 min | Yes |
| Phase 1: Order discrimination | 30 min | Yes |
| Phase 2: Full training (3 seeds × 3 methods) | 2 hours | Yes |
| Evaluation + bootstrap | 15 min | No |
| **Total** | ~3 hours | ~2.5 GPU-hours |

## Dependencies

- [x] TOPA implementation (`papers/idea-009-tfs/src/tfs/topa.py`)
- [x] EXP-014 results documented (paper repo)
- [x] Contrastive training code
- [ ] **EXP-017**: PE-Video features extracted (BLOCKING)

## Relationship to Other Experiments

```
EXP-014 (completed) → EXP-017 (extract features) → EXP-018 (scale validation)
                                                          ↓
                                               EXP-019 (temporal benchmark)
                                               (only if EXP-018 passes)
```

- **EXP-014**: Pilot on CLIP/MSR-VTT (30 videos) - showed +3.3pp R@1
- **EXP-017**: Extract PE-Video features (500 videos)
- **EXP-018**: Scale validation on PE-Video (this experiment)
- **EXP-019**: Temporal benchmark on DiDeMo (if EXP-018 shows improvement)

## Limitations

1. **PE-Video is not temporal**: Captions describe scenes, not temporal sequences. This experiment validates R@1 improvement, not temporal query performance.
2. **Different model**: PE-Core vs CLIP. Results may not directly compare to EXP-014.
3. **Different dataset**: PE-Video vs MSR-VTT. Domain shift possible.

**These are acceptable** because:
- Primary goal is statistical power for R@1, not temporal claims
- Temporal claims tested separately in EXP-019 on DiDeMo
- If TOPA works on PE, it's more general (not CLIP-specific)

## Notes

- Always run Phase 0 alignment check first
- If alignment fails, do not proceed - need to investigate PE architecture
- TFS intentionally excluded (waste of compute, already validated failure)
- Report all seeds, not just best
