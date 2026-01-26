# Experiment: TFS VATEX Dataset Validation

- **ID**: EXP-011
- **Created**: 2026-01-24
- **Paper**: IDEA-009-temporal-fourier-signatures
- **Source**: SIM-003 (Advisor Q1, Lay Q2)
- **Priority**: P2
- **Status**: running

## Objective

Validate TFS performance on VATEX dataset, which has higher temporal query density (~30%) than MSR-VTT (~6.8%). This addresses the concern that the +8.8% improvement was measured on a small temporal subset.

## Hypothesis

TFS will show consistent improvement over mean pooling on temporal queries in VATEX, matching the pattern observed in MSR-VTT (TFS > attention > mean on temporal queries).

## Method

### Setup

- **Model**: TFS with trained projection
- **Dataset**: VATEX test_public split (1000 videos)
- **Hardware**: CPU (synthetic features)
- **Features**: Synthetic CLIP-like features with controlled temporal structure

### Configuration

```yaml
n_videos: 1000
n_frames: 12
dim: 512
frequencies: [1, 2, 4, 8, 16, 32]
projection_epochs: 30
seed: 42
```

### Procedure

1. Load VATEX annotations (or generate synthetic)
2. Generate synthetic features matching CLIP distribution
3. Identify temporal queries using keyword classification
4. Train projection layers for each pooling method
5. Evaluate on full dataset, temporal subset, non-temporal subset
6. Compare pattern to MSR-VTT results

## Metrics

- **Primary**: R@10 on temporal queries
- **Secondary**: TFS improvement over mean/attention on temporal, pattern consistency

## Baselines

- MSR-VTT TFS temporal R@10: 94.1%
- MSR-VTT Mean temporal R@10: 85.3%
- Expected VATEX improvement: >5% TFS over mean

## Compute Budget

- **Estimated time**: 1-2 GPU-hours (synthetic features, larger dataset)
- **Phase**: validation

## Success Criteria

- TFS outperforms mean pooling on temporal queries (>5% improvement)
- Pattern consistent with MSR-VTT: TFS > attention > mean on temporal
- Temporal query sample size > 200 (larger than MSR-VTT's 136)

## Dependencies

- [x] TFS implementation
- [x] Projection training code
- [x] VATEX dataset loader
- [x] Temporal query classification
