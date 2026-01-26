# Experiment: TFS with Real CLIP Features

- **ID**: EXP-008
- **Created**: 2026-01-24
- **Paper**: IDEA-009-temporal-fourier-signatures
- **Source**: SIM-003 (Advisor Q3, Lay Q3)
- **Priority**: P1
- **Status**: queued

## Objective

Validate TFS performance using real CLIP features extracted from actual video frames, establishing ecological validity of the synthetic feature results.

## Hypothesis

TFS will show similar relative improvement over mean pooling (+5-10% on temporal queries) with real CLIP features as observed with synthetic features, confirming the method generalizes beyond controlled settings.

## Method

### Setup

- **Model**: CLIP ViT-B/32 for feature extraction, TFS with trained projection
- **Dataset**: MSR-VTT (train/val/test splits)
- **Hardware**: GPU for CLIP extraction + evaluation
- **Frame sampling**: 8 frames uniformly sampled per video

### Configuration

```yaml
clip_model: ViT-B/32
frame_count: 8
frame_resolution: 224x224
extraction_batch_size: 64
projection_training:
  epochs: 10
  learning_rate: 1e-4
  batch_size: 32
```

### Procedure

1. Extract CLIP features for all MSR-VTT videos
   - 8 frames per video, uniformly sampled
   - Save frame features (not aggregated)
2. Apply TFS, mean pooling, attention pooling to frame features
3. Train projection layer on train split
4. Evaluate on test split with temporal/non-temporal breakdown
5. Compare to synthetic feature results

## Metrics

- **Primary**: R@10 on temporal queries, comparison to synthetic baseline
- **Secondary**: All R@K metrics, MedR, agreement with synthetic results

## Baselines

- Synthetic TFS results (Exp 6): 94.1% R@10 temporal, 89.7% non-temporal
- Synthetic mean results (Exp 6): 85.3% R@10 temporal, 90.3% non-temporal

## Compute Budget

- **Estimated time**: 8-12 GPU-hours (extraction: ~6h, training/eval: ~2h)
- **Phase**: validation (critical for paper)

## Success Criteria

- Relative improvement pattern matches synthetic: TFS > attention > mean on temporal
- Absolute performance within 5% of synthetic results
- No unexpected degradation on non-temporal queries

## Dependencies

- [x] MSR-VTT video files accessible
- [x] CLIP model available
- [x] TFS implementation from Exp 6
- [ ] Feature extraction script (needs implementation)
