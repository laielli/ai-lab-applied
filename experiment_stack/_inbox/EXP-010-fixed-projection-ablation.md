# Experiment: Fixed Projection Alternatives for TFS

- **ID**: EXP-010
- **Created**: 2026-01-24
- **Paper**: IDEA-009-temporal-fourier-signatures
- **Source**: SIM-003 (SME Q3)
- **Priority**: P3
- **Status**: queued

## Objective

Explore fixed (non-trained) projection alternatives to reduce the trained projection requirement and restore the "drop-in replacement" appeal of TFS.

## Hypothesis

Fixed projections will underperform trained projection but may narrow the gap sufficiently to be useful. Random orthogonal projections should preserve more structure than identity.

## Method

### Setup

- **Model**: TFS with various projection types
- **Dataset**: MSR-VTT test split (synthetic features)
- **Hardware**: Single GPU

### Configuration

```yaml
projection_types:
  - none: "No projection (direct TFS output)"
  - identity: "Identity matrix"
  - random_orthogonal: "Random orthogonal matrix (fixed at init)"
  - pca: "PCA projection from training set"
  - trained: "Learned projection (baseline)"
seeds: 3
```

### Procedure

1. For each projection type:
   - Initialize projection (if applicable)
   - Apply TFS with projection
   - Evaluate on MSR-VTT test
   - Record temporal/non-temporal breakdown
2. Compare all projection types
3. Analyze which fixed approaches work best

## Metrics

- **Primary**: R@10 gap between fixed projections and trained projection
- **Secondary**: Computational cost of each approach

## Baselines

- Trained projection: 94.1% R@10 temporal (Exp 6)
- No projection: ~80% R@10 (Exp 6C ablation)

## Compute Budget

- **Estimated time**: 3-5 GPU-hours
- **Phase**: ablation

## Success Criteria

- Identify if any fixed projection achieves > 85% of trained projection performance
- Document tradeoff between simplicity and performance

## Dependencies

- [x] TFS implementation
- [x] Exp 6 evaluation code
- [ ] PCA computation from training set
