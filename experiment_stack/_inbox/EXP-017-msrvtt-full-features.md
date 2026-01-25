# Experiment: MSR-VTT Full Test Set Feature Extraction

- **ID**: EXP-017
- **Created**: 2026-01-25
- **Paper**: IDEA-009-temporal-fourier-signatures
- **Source**: SIM-006 (Advisor Q4)
- **Priority**: P1
- **Status**: queued

## Objective

Extract CLIP ViT-B/32 frame-level features for the complete MSR-VTT test set (1000 videos) to enable statistically meaningful evaluation of TOPA and other pooling methods.

## Hypothesis

With 1000 test videos instead of 30, we will have sufficient statistical power to detect improvements of 2-3pp with confidence (rather than requiring 10pp+ effects).

## Method

### Setup

- **Model**: CLIP ViT-B/32 (frozen)
- **Dataset**: MSR-VTT test split (1000 videos)
- **Hardware**: Single GPU (feature extraction, not training)

### Configuration

```yaml
clip_model: ViT-B/32
frame_sampling: uniform, 12 frames per video
output_format: numpy arrays (N_videos x 12 x 512)
batch_size: 64 (frame batches)
```

### Procedure

1. Download/verify MSR-VTT test videos (1000 videos)
2. Extract 12 uniformly-sampled frames per video
3. Run CLIP visual encoder on all frames
4. Store frame-level features (before pooling)
5. Verify extraction by computing mean-pooled retrieval metrics

## Metrics

- **Primary**: Successful extraction of all 1000 videos
- **Secondary**: Mean pooling R@1/R@5/R@10 on full test set (sanity check)

## Compute Budget

- **Estimated time**: 2-4 GPU-hours (feature extraction only)
- **Phase**: prerequisite for future experiments

## Success Criteria

- All 1000 videos processed successfully
- Mean pooling retrieval metrics match published CLIP baselines on MSR-VTT

## Dependencies

- [ ] MSR-VTT test videos accessible
- [ ] CLIP model checkpoint available
- [ ] Storage for ~12000 frame embeddings (1000 * 12 * 512 * 4 bytes = ~24MB)
