# EXP-017: Full MSR-VTT CLIP Feature Extraction

**Created**: 2026-01-25
**Paper**: IDEA-009 Temporal Fourier Signatures
**Status**: READY
**Priority**: P1 - Critical for validating R@1 improvement

---

## Objective

Extract CLIP features for the full MSR-VTT test set (1000 videos) to enable large-scale validation of the R@1 improvement observed in EXP-014.

## Motivation

The current validation (EXP-014) uses only 30 test videos from a 148-video subset. The observed +3.3pp R@1 improvement (40.0% vs 36.7%) is based on just 1 additional correct video. This is insufficient to determine if the improvement is real or noise.

**Human feedback**: "If that's an improvement, then that could be a big deal, if that plays out at a larger scale."

## Method

1. Download MSR-VTT test split (1000 videos)
2. Extract ViT-B/32 CLIP features for all videos
3. Use 6 frames per video (uniform temporal sampling)
4. Save features in same format as existing 148-video dataset

## Technical Details

| Parameter | Value |
|-----------|-------|
| Model | CLIP ViT-B/32 |
| Embedding dim | 512 |
| Frames per video | 6 |
| Sampling | Uniform temporal |
| Dataset | MSR-VTT test split |
| Video count | 1000 |

## Output

- `log/exp17/msrvtt_full_features.pt`: Video features (1000 x 6 x 512)
- `log/exp17/msrvtt_full_captions.json`: Corresponding captions
- `log/exp17/extraction_log.txt`: Processing details

## Success Criteria

| Criterion | Target |
|-----------|--------|
| Videos processed | 1000 |
| Feature shape | [1000, 6, 512] |
| Format compatibility | Matches EXP-014 input format |

## Compute Estimate

- GPU: Lambda.ai A10 (24GB)
- Time: ~2 GPU-hours
- Storage: ~50MB for features

## Blockers

None - ready to execute.

## Dependencies

- EXP-018 is blocked by this experiment
