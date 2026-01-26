# Experiment: MLP Temporal Probe Upper Bound

- **ID**: EXP-016
- **Created**: 2026-01-24
- **Paper**: idea-003-avg-pooling
- **Idea**: IDEA-003
- **Source**: SIM-005 (SME Q1)
- **Priority**: P2
- **Status**: queued

## Objective

Test whether a non-linear probe (MLP) can extract more temporal ordering information than logistic regression. This provides an upper bound on accessible temporal signal and addresses concerns about linear probe being too weak.

## Hypothesis

MLP may achieve higher accuracy than logistic regression at all layers, but the *pattern* should remain: peak at intermediate layers, decay toward output. If MLP at layer 23 matches MLP at layer 10, it would suggest temporal info is there but non-linearly encoded.

## Method

### Setup

- **Model**: PE-Core-L14-336
- **Dataset**: Same as Exp 3.1 (150 PE-Video videos)
- **Hardware**: Single GPU

### Configuration

```yaml
model: PE-Core-L14-336
dataset: pe_video_subset
num_videos: 150
frames_per_video: 8
layers_to_probe: [10, 23]  # Focus on key comparison
probe_type: mlp
mlp_hidden: [512, 256]
mlp_activation: relu
train_split: 0.8
epochs: 50
learning_rate: 1e-3
```

### Procedure

1. Use same frame embeddings from Exp 3.1
2. Train 2-layer MLP probe (concatenated pairs -> hidden -> binary prediction)
3. Compare to logistic regression baseline
4. Report accuracy with bootstrap confidence intervals
5. Analyze: does MLP close the gap between layer 10 and layer 23?

## Metrics

- **Primary**: MLP validation accuracy at layers 10 and 23
- **Secondary**: Accuracy gain over logistic regression, gap preservation

## Baselines

- **Logistic regression (Exp 3.1)**: Layer 10 = 64.3%, Layer 23 = 57.4%
- **Random**: 50%

## Compute Budget

- **Estimated time**: 2 GPU-hours
- **Phase**: validation

## Success Criteria

- MLP at layer 10 > MLP at layer 23 (pattern preserved)
- If MLP at layer 23 approaches MLP at layer 10: revise conclusions about "lost" temporal info

## Dependencies

- [x] Exp 3.1 completed
- [x] Frame embeddings cached
- [ ] MLP probe implementation
