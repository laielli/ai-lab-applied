# Experiment: TFS Real CLIP Features Pilot

- **ID**: EXP-012
- **Created**: 2026-01-24
- **Paper**: IDEA-009-temporal-fourier-signatures
- **Idea**: IDEA-009
- **Priority**: P1
- **Status**: queued
- **Source**: SIM-004 (Advisor Q2)

## Objective

Test whether TFS shows improvement on temporal queries when using real CLIP features (not synthetic). This is the critical experiment to determine if the TFS hypothesis holds with actual video data.

## Hypothesis

TFS will show a consistent improvement (>2pp) on temporal queries compared to mean pooling when using real CLIP features extracted from actual videos, because real features contain meaningful temporal structure that synthetic features lack.

**Null hypothesis**: TFS shows no significant improvement with real features, indicating the approach doesn't work regardless of feature quality.

## Method

### Setup

- **Model**: CLIP ViT-B/32 for feature extraction
- **Dataset**: MSR-VTT (pilot: 100 videos, full: 1000 videos)
- **Hardware**: 1x A100 or V100 GPU
- **Seeds**: [42, 123, 456] (minimum 3 for variance estimate)

### Configuration

```yaml
# Pilot configuration (de-risking)
num_videos: 100
num_frames: 8
seeds: [42, 123, 456]
temporal_query_keywords:
  - "first"
  - "then"
  - "finally"
  - "before"
  - "after"
  - "while"
  - "begins"
  - "ends"
  - "starts"
  - "stops"

# Feature extraction
model: "openai/clip-vit-base-patch32"
frame_sampling: "uniform"

# Evaluation
metrics: ["R@1", "R@5", "R@10"]
stratify_by: ["temporal", "non_temporal"]
```

### Procedure

1. **Download videos**: Select 100 random videos from MSR-VTT
2. **Extract frames**: 8 uniformly sampled frames per video
3. **Extract CLIP features**: ViT-B/32 visual encoder
4. **Run TFS evaluation**: Same protocol as EXP-007 but with real features
5. **Multi-seed analysis**: Run with 3 seeds, compute mean and variance
6. **Compare to synthetic**: Side-by-side comparison with synthetic feature results

### Pilot Design Rationale

- **100 videos** instead of 1000: ~10x faster, sufficient to detect large effects
- **3 seeds** instead of 5: Faster while still providing variance estimate
- **Clear escalation path**: If pilot shows promise, expand to full dataset

## Metrics

- **Primary**: R@10 on temporal queries, averaged across seeds
- **Secondary**: R@1, R@5, overall retrieval metrics
- **Statistical**: Paired t-test (TFS vs Mean), effect size (Cohen's d)

## Baselines

- **Mean pooling**: R@10 on temporal queries (expected ~90% based on synthetic)
- **Attention pooling**: R@10 on temporal queries (expected ~91% based on synthetic)
- **Synthetic TFS**: Results from EXP-007 for direct comparison

## Compute Budget

- **Video download**: ~4GB for 100 videos
- **Feature extraction**: ~0.5 GPU-hours
- **Evaluation (3 seeds)**: ~0.5 GPU-hours
- **Total estimated time**: 2 GPU-hours (including overhead)
- **Phase**: validation (<8h)

## Success Criteria

### Proceed to full experiment if:
- TFS improvement on temporal queries > 2pp (averaged across seeds)
- p-value < 0.10 (suggestive, if not significant)
- Effect consistent in direction across all seeds

### Shelve project if:
- TFS improvement < 1pp (averaged across seeds)
- Inconsistent direction across seeds (some positive, some negative)
- p-value > 0.5

### Ambiguous (expand to full dataset):
- TFS improvement 1-2pp with consistent direction
- p-value 0.10-0.50

## Dependencies

- [x] TFS implementation (`src/tfs/core.py`)
- [x] Evaluation code (`src/experiments/exp6_msrvtt_retrieval.py`)
- [ ] CLIP feature extraction script
- [ ] Video download script (partial videos)
- [ ] MSR-VTT test split file access

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Video download issues | Use pre-extracted features if available (e.g., from other papers) |
| CLIP extraction OOM | Reduce batch size, use smaller model |
| Still no improvement | Accept negative result, document clearly |

## Connection to Go/No-Go Decision

This experiment is critical for the TFS project decision (WRITE-001). Results should be available before the 1-week decision deadline.

**Decision mapping**:
- Strong positive (>5pp, p<0.05): Proceed to full paper
- Moderate positive (2-5pp, consistent): Proceed with caution
- Weak positive (1-2pp): Consider pivoting scope
- No improvement: Shelve project

## Next Steps After This Experiment

If successful:
1. Expand to full MSR-VTT (1000 videos)
2. Run on VATEX with real features
3. Begin paper draft focusing on validated claims

If unsuccessful:
1. Document negative result
2. Update IDEA-009 status to "abandoned" or "pivoted"
3. Consider mechanism-only workshop paper
