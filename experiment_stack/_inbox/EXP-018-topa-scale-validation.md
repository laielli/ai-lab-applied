# EXP-018: TOPA Scale Validation on PE-Video

**Created**: 2026-01-25
**Revised**: 2026-01-25 (pivoted from MSR-VTT to PE-Video)
**Paper**: IDEA-009 Temporal Fourier Signatures
**Status**: BLOCKED
**Blocked by**: EXP-017
**Priority**: P1 - Critical for go/no-go decision

---

## Objective

Validate TOPA's temporal encoding benefits at scale on PE-Video (500+ videos), testing whether the alignment-preserving temporal encoding improves retrieval.

## Motivation

EXP-014 showed promising results on 30 test videos but lacked statistical power. This experiment:
1. Increases sample size 15x (30 → 500+ videos)
2. Uses cleaner dataset (PE-Video vs problematic MSR-VTT)
3. Tests on model trained for this data (PE-Core on PE-Video)

## Hypothesis

TOPA's additive positional encoding preserves PE's cross-modal alignment while encoding temporal order. This should:
1. Match or beat mean pooling on standard retrieval
2. Show improvement on temporally-dependent queries
3. Enable order discrimination (forward vs reversed video)

## Method

1. Load PE-Core features from EXP-017 (500+ videos, 8 frames each)
2. Train TOPA, Mean, and TFS projections with contrastive loss
3. Evaluate R@1, R@5, R@10 with bootstrap confidence intervals
4. Test order discrimination (forward vs reversed)
5. Analyze performance on temporal vs non-temporal queries

## Technical Details

### Model Configuration

| Parameter | Value |
|-----------|-------|
| Input dim | 1024 (PE-Core-L14-336) |
| Output dim | 512 |
| Frames | 8 per video |
| TOPA position scale | 0.01 (from EXP-014) |
| TOPA temporal diff | Enabled |

### Training Protocol

| Parameter | Value |
|-----------|-------|
| Train/Test split | 80/20 (400/100 videos) |
| Loss | InfoNCE (contrastive) |
| Optimizer | Adam |
| Learning rate | 1e-4 |
| Epochs | 100 |
| Batch size | 32 |
| Seeds | 3 (for variance estimation) |

### Methods to Compare

| Method | Description |
|--------|-------------|
| **TOPA (α=0.01)** | Additive position + temporal diff |
| **TOPA-minimal** | Additive position only |
| **Mean pooling** | Simple average (baseline) |
| **TFS** | Rotation-based (expected to fail) |

## Evaluation Protocol

### Primary Metrics

| Metric | Description |
|--------|-------------|
| R@1, R@5, R@10 | Text-to-video retrieval accuracy |
| 95% CI | Bootstrap confidence intervals (1000 samples) |
| MRR | Mean Reciprocal Rank |

### Secondary Metrics

| Metric | Description |
|--------|-------------|
| Alignment preservation | cos_sim(TOPA(frames), text) / cos_sim(mean(frames), text) |
| Order discrimination | Accuracy distinguishing forward vs reversed |
| Temporal query R@1 | Performance on temporally-dependent queries |

### Temporal Query Classification

Use keyword heuristics to identify temporal queries:
```python
TEMPORAL_KEYWORDS = [
    'then', 'after', 'before', 'first', 'next', 'finally',
    'while', 'during', 'until', 'starts', 'ends', 'begins',
    'followed by', 'leads to', 'turns into'
]
```

## Success Criteria

| Outcome | Condition | Decision |
|---------|-----------|----------|
| **Strong continue** | R@1 ≥ Mean + 2pp (p < 0.05) | Full IDEA-009 development |
| **Continue with caution** | R@1 ≥ Mean + 1pp | Investigate temporal subset |
| **Neutral** | R@1 within ±1pp of Mean | Check temporal queries specifically |
| **Shelve** | R@1 < Mean - 2pp | Document learnings, shelve IDEA-009 |

### Order Discrimination

| Outcome | Condition |
|---------|-----------|
| **Pass** | TOPA > 90% accuracy, Mean ≈ 50% |
| **Fail** | TOPA ≤ 60% accuracy |

### Alignment Preservation

| Outcome | Condition |
|---------|-----------|
| **Pass** | Preservation ratio ≥ 95% |
| **Fail** | Preservation ratio < 90% |

## Output

| File | Description |
|------|-------------|
| `log/exp18/results.json` | All metrics with CIs |
| `log/exp18/retrieval_comparison.md` | Formatted results table |
| `log/exp18/order_discrimination.json` | Forward/reverse accuracy |
| `log/exp18/temporal_query_analysis.json` | Per-query-type breakdown |
| `log/exp18/bootstrap_distributions.png` | CI visualization |

## Compute Estimate

| Stage | Time |
|-------|------|
| Training (3 seeds × 4 methods) | ~2 GPU-hours |
| Evaluation + bootstrap | ~30 min |
| **Total** | ~2.5 GPU-hours |

## Dependencies

- [x] TOPA implementation (`papers/idea-009-tfs/src/tfs/topa.py`)
- [x] Contrastive training code (from EXP-014)
- [ ] EXP-017: PE-Video features extracted

## Implementation

Adapt EXP-014 code with PE dimensions:

```python
from src.tfs.topa import TOPAWithProjection, TOPAMinimal

# PE-Core dimensions
INPUT_DIM = 1024  # PE-Core-L14-336
OUTPUT_DIM = 512

# Initialize models
topa = TOPAWithProjection(
    dim=INPUT_DIM,
    output_dim=OUTPUT_DIM,
    position_scale=0.01,
    use_temporal_diff=True
)

topa_minimal = TOPAMinimal(
    dim=INPUT_DIM,
    position_scale=0.01
)

# Training loop same as EXP-014
```

## Expected Results

Based on theory and EXP-014 pilot:

| Method | Expected R@10 | Rationale |
|--------|---------------|-----------|
| Mean pooling | ~85-90% | PE trained on PE-Video |
| TOPA | ~85-92% | Should match or slightly beat mean |
| TFS | ~20-40% | Rotation breaks alignment |

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| PE alignment differs from CLIP | Test alignment preservation first |
| 500 videos insufficient | Can extend to 1000+ if needed |
| No temporal queries in PE-Video | Manually identify temporal captions |

## Notes

- PE-Video captions may be less temporally descriptive than action datasets
- If temporal subset is too small, consider ActivityNet-Captions as follow-up
- TFS expected to fail, but include for theoretical validation
