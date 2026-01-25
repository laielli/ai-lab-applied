# Experiment: YouCook2 Density Analysis

- **ID**: EXP-022
- **Created**: 2026-01-25
- **Paper**: idea-010-v-limit
- **Idea**: IDEA-010
- **Priority**: P1
- **Status**: queued

## Objective

Measure d_tripartite on YouCook2 to test whether narrow-domain datasets naturally exhibit higher density than general-purpose video datasets, which could trigger the LIMIT effect.

## Hypothesis

YouCook2, being a narrow-domain dataset (all cooking videos with recipe step descriptions), will have higher density than VATEX, MSR-VTT, and ActivityNet due to:
1. Visual similarity within domain (kitchens, cooking actions)
2. Lexical overlap in recipe terminology
3. Natural "similar distractors" from related recipes

Expected: d > 0.3 (vs current VATEX d = 0.173)

## Method

### Setup

- **Dataset**: YouCook2 (2000 videos, 89 recipes, segment-level captions)
- **Reference**: Existing loader at `/workspace/rtd_ml_engineer/src/data/youcook2.py` (adapt for V-LIMIT)
- **Hardware**: CPU only (no training)

### Configuration

```yaml
# Density computation settings
similarity_thresholds: [0.5, 0.6, 0.7]
density_metric: "tripartite"
embedding_model: "openai/clip-vit-base-patch32"
text_tokenizer: "nltk"  # for Jaccard overlap
```

### Procedure

1. Load YouCook2 annotations (segment-level captions)
2. Compute ground-truth d_tripartite from segment relevance structure:
   - Positive pairs: query-video from same segment
   - Negative pairs: query-video from different segments
3. Compute lexical density (Jaccard token overlap)
4. Compute CLIP-perceived density at thresholds (tau = 0.5, 0.6, 0.7)
5. Compare with MSR-VTT, ActivityNet, VATEX densities from EXP-001 and EXP-021

## Metrics

- **Primary**: d_tripartite (tripartite density)
- **Secondary**:
  - Jaccard token overlap distribution
  - CLIP pairwise similarity distribution
  - Inter-recipe vs intra-recipe density comparison

## Baselines

- MSR-VTT: d = 0.001 (from EXP-001)
- ActivityNet: d = 0.0002 (from EXP-001)
- VATEX (constructed): d = 0.173 (from EXP-002)

## Compute Budget

- **Estimated time**: 2 GPU-hours (embedding extraction only)
- **Phase**: validation (<8h)

## Success Criteria

- **GO (high density)**: YC2 d > 0.3
  - Action: Use YouCook2 as V-LIMIT benchmark
- **PARTIAL (moderate density)**: YC2 d in [0.2, 0.3]
  - Action: Consider hybrid approach (YC2 + synthetic augmentation)
- **NO-GO (low density)**: YC2 d < 0.2
  - Action: Proceed with EXP-020 synthetic scale-up approach

## Dependencies

- [ ] YouCook2 annotations accessible
- [ ] Density computation code from exp001/metrics.py
- [ ] CLIP embedding extraction pipeline
- [ ] Baseline density results from EXP-001

## Analysis Plan

1. **Density comparison table**: YC2 vs MSR-VTT vs ActivityNet vs VATEX
2. **Distribution plots**: Pairwise similarity histograms
3. **Domain analysis**: Inter-recipe vs intra-recipe density breakdown
4. **Decision document**: GO/NO-GO for using YC2 in V-LIMIT

## Notes

- YouCook2 uses segment-level (temporal) captions, not video-level
- May need to aggregate segments to video-level for fair comparison
- Segment-based relevance structure naturally creates dense subgroups (same recipe)
- Compare both segment-level and video-level density computations
