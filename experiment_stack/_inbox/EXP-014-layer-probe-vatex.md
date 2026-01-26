# Experiment: Layer Probing Cross-Dataset Validation (VATEX)

- **ID**: EXP-014
- **Created**: 2026-01-24
- **Paper**: idea-003-avg-pooling
- **Idea**: IDEA-003
- **Source**: SIM-005 (SME Q2)
- **Priority**: P1
- **Status**: queued

## Objective

Validate that the layer 10 temporal probing peak generalizes beyond PE-Video dataset to VATEX videos. Address concern that 150 videos from a single source may not represent broader patterns.

## Hypothesis

The temporal ordering accuracy pattern (peak at layer 10, decay to layer 23) will replicate on VATEX videos, confirming this is a fundamental property of PE architecture rather than dataset-specific artifact.

## Method

### Setup

- **Model**: PE-Core-L14-336 (same as Exp 3.1)
- **Dataset**: VATEX validation split (sample 150 videos for comparison)
- **Hardware**: Single GPU (M3 Max or Lambda)

### Configuration

```yaml
model: PE-Core-L14-336
dataset: vatex_val
num_videos: 150
frames_per_video: 8
pairs_per_video: 56  # n*(n-1)/2 pairs
layers_to_probe: [0, 1, 8, 10, 11, 15, 17, 19, 23]
probe_type: logistic_regression
train_split: 0.8
```

### Procedure

1. Sample 150 videos from VATEX validation set
2. Extract 8 uniformly-spaced frames per video
3. Extract embeddings at each layer (0, 1, 8, 10, 11, 15, 17, 19, 23)
4. Generate frame pairs with temporal order labels
5. Train logistic regression probe at each layer
6. Report validation accuracy with 95% confidence intervals

## Metrics

- **Primary**: Validation accuracy at each layer
- **Secondary**: Peak layer location, accuracy drop from peak to output

## Baselines

- **PE-Video results (Exp 3.1)**: Layer 10 = 64.3%, Layer 23 = 57.4%
- **Random baseline**: 50%

## Compute Budget

- **Estimated time**: 4 GPU-hours
- **Phase**: validation

## Success Criteria

- Pattern replicates: layer 10 > layer 23 by at least 3%
- Peak location is within 2 layers of layer 10
- 95% CI does not overlap between peak and output layer

## Dependencies

- [x] Exp 3.1 completed with PE-Video dataset
- [ ] VATEX videos accessible
- [ ] Probe code from Exp 3.1 reusable
