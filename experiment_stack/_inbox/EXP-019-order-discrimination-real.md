# Experiment: Order Discrimination with Real CLIP Features

- **ID**: EXP-019
- **Created**: 2026-01-25
- **Paper**: IDEA-009-temporal-fourier-signatures
- **Source**: SIM-006 (SME Q2)
- **Priority**: P2
- **Status**: queued

## Objective

Test whether TOPA's positional encoding enables order discrimination when applied to real CLIP features (not synthetic). This validates whether the positional signal survives the presence of rich semantic content.

## Hypothesis

TOPA should still distinguish forward from reversed sequences on real CLIP features, though accuracy may be lower than the 100% achieved with synthetic features due to semantic content that correlates with temporal position.

## Method

### Setup

- **Model**: TOPA (scale=0.01, 0.02)
- **Dataset**: Real CLIP features from EXP-017 (MSR-VTT) or existing 148-video set
- **Hardware**: Single GPU (CPU sufficient)

### Configuration

```yaml
features: real_clip_vit_b32
test_type: binary_classification (forward vs reversed)
classifier: logistic_regression or simple_mlp
train_test_split: 80/20
scales: [0.01, 0.02, 0.05]
```

### Procedure

1. Load real CLIP frame features
2. For each video, create forward and reversed versions
3. Apply TOPA encoding (mean pool after)
4. Train simple classifier to distinguish forward/reversed
5. Evaluate on held-out test set
6. Compare with mean pooling baseline (expected: 50% random chance)

## Metrics

- **Primary**: Classification accuracy (forward vs reversed)
- **Secondary**: Accuracy by position scale setting

## Baselines

- Mean Pooling: Expected 50% (cannot distinguish ordering)
- Random: 50%
- Synthetic features TOPA: 100% (from EXP-014)

## Compute Budget

- **Estimated time**: <1 GPU-hour
- **Phase**: validation

## Success Criteria

- TOPA accuracy > 70% (well above chance)
- TOPA significantly outperforms mean pooling (p < 0.05)

If TOPA accuracy is near 50%:
- Positional encoding is too weak at scale 0.01
- Semantic content dominates positional signal
- Method may not provide useful temporal information for retrieval

## Dependencies

- [ ] Real CLIP features available (from EXP-017 or existing set)
- [ ] Classification framework implemented
