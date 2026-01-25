# Experiment: Temporal Benchmark Go/No-Go Validation

- **ID**: EXP-018
- **Created**: 2026-01-25
- **Paper**: IDEA-009-temporal-fourier-signatures
- **Source**: SIM-006 (Advisor Q2)
- **Priority**: P1
- **Status**: queued

## Objective

Determine whether TOPA provides meaningful improvement over mean pooling on queries that specifically require temporal reasoning. This is the go/no-go decision point for continuing IDEA-009.

## Hypothesis

If temporal information matters for retrieval, TOPA should outperform mean pooling by >5pp on temporal queries while matching performance on non-temporal queries. If not, the direction should be shelved.

## Method

### Setup

- **Model**: TOPA (scale=0.01) vs Mean Pooling
- **Dataset**: One of:
  - DiDeMo (temporal moment queries)
  - ActivityNet Captions (event sequences)
  - Charades-STA (temporal localization)
- **Hardware**: Single GPU

### Configuration

```yaml
pooling_methods:
  - mean
  - topa_0.01
  - topa_0.02
evaluation:
  temporal_queries: queries with temporal language ("before", "after", "then", "while")
  non_temporal_queries: remaining queries
min_videos: 500
```

### Procedure

1. Select benchmark with temporal query structure (prefer DiDeMo)
2. Extract CLIP features for 500+ videos
3. Partition queries into "temporal" and "non-temporal" based on language patterns
4. Evaluate TOPA and mean pooling on both query subsets
5. Compare performance gaps

## Metrics

- **Primary**: R@1 delta on temporal queries (TOPA - Mean)
- **Secondary**: R@1 delta on non-temporal queries (should be near zero)

## Baselines

- Mean Pooling: Expected baseline on temporal queries (unknown)
- TOPA: Expected to match or beat on temporal queries

## Compute Budget

- **Estimated time**: 4-8 GPU-hours
- **Phase**: validation (<8h)

## Success Criteria

| Result | Decision |
|--------|----------|
| TOPA > Mean by 5pp+ on temporal queries | **GO**: Pursue IDEA-009 with temporal focus |
| TOPA matches Mean on temporal queries | **NO-GO**: Shelve IDEA-009, positional encoding doesn't help |
| TOPA < Mean on temporal queries | **NO-GO**: Approach is counterproductive |

## Dependencies

- [ ] EXP-017 completed (or use different feature set)
- [ ] Temporal/non-temporal query classification defined
- [ ] Benchmark selected and accessible
