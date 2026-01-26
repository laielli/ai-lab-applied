# Experiment: TFS Multi-Seed Variance Analysis

- **ID**: EXP-007
- **Created**: 2026-01-24
- **Paper**: IDEA-009-temporal-fourier-signatures
- **Source**: SIM-003 (SME Q1)
- **Priority**: P1
- **Status**: COMPLETED - RESULTS NEGATIVE

## Objective

Establish statistical validity of TFS results by running multiple random seeds and reporting variance estimates. Critical for publication credibility.

## Hypothesis

The +8.8% improvement on temporal queries will remain statistically significant (p < 0.05) across multiple seeds, with variance < 3%.

## Method

### Setup

- **Model**: TFS with trained projection (same architecture as Exp 6)
- **Dataset**: MSR-VTT test split (2000 queries, 136 temporal)
- **Hardware**: Single GPU
- **Seeds**: 5 random seeds (controlling feature generation, projection init, any sampling)

### Configuration

```yaml
seeds: [42, 123, 456, 789, 1024]
metrics: [R@1, R@5, R@10, MedR]
splits: [all, temporal, non-temporal]
methods: [mean_pooling, tfs, attention_pooling]
```

### Procedure

1. For each seed:
   - Generate synthetic features with seed
   - Train projection layer with seed
   - Evaluate on full MSR-VTT test
   - Compute metrics for all/temporal/non-temporal splits
2. Aggregate across seeds
3. Compute mean, std, 95% CI for each metric/split combination
4. Perform paired t-test: TFS vs mean pooling on temporal queries

## Metrics

- **Primary**: R@10 on temporal queries (mean +/- std across seeds)
- **Secondary**: p-value for TFS vs mean pooling difference

## Baselines

- Mean pooling: Expected ~85.3% R@10 on temporal (from Exp 6)
- TFS: Expected ~94.1% R@10 on temporal (from Exp 6)

## Compute Budget

- **Estimated time**: 5-10 GPU-hours (5 full evaluations)
- **Phase**: validation

## Success Criteria

- TFS temporal improvement remains > 5% across all seeds
- Standard deviation < 3%
- p-value < 0.05 for paired comparison

## Dependencies

- [x] Exp 6 code available
- [x] Synthetic feature generation code
- [x] Temporal query classification
- [x] None blocking

---

## RESULTS (2026-01-24)

### HYPOTHESIS REJECTED

The +8.8% improvement on temporal queries does NOT replicate across multiple seeds.

### Per-Seed Results (R@10 on temporal queries)

| Seed | TFS | Mean | Attention | TFS vs Mean |
|------|-----|------|-----------|-------------|
| 42 | 94.1% | 92.6% | 92.6% | +1.5pp |
| 123 | 88.2% | 91.2% | 94.1% | **-2.9pp** |
| 456 | 92.6% | 89.7% | 92.6% | +2.9pp |
| 789 | 89.7% | 91.2% | 89.7% | **-1.5pp** |
| 1024 | 94.1% | 94.1% | 88.2% | 0.0pp |

### Aggregate Statistics

| Metric | TFS | Mean | Attention |
|--------|-----|------|-----------|
| Mean | 91.76% | 91.76% | 91.32% |
| Std | 2.67% | 1.68% | 3.05% |

### Statistical Test

**TFS vs Mean (paired t-test)**: p = 1.0 (NOT SIGNIFICANT)

### Success Criteria Evaluation

| Criterion | Target | Actual | Status |
|-----------|--------|--------|--------|
| Improvement > 5% | >5% | 0.0% | **FAIL** |
| Std < 3% | <3% | 2.67% | PASS |
| p-value < 0.05 | <0.05 | 1.0 | **FAIL** |

### Key Insight

The original Exp 6 result (+8.8pp with seed=42) was a **lucky seed artifact**. With multiple seeds, TFS and mean pooling show statistically identical performance on temporal queries.

### Implications

1. Cannot claim reproducible TFS advantage with synthetic features
2. Need real CLIP features to test actual hypothesis
3. Synthetic features don't have meaningful temporal structure to exploit
