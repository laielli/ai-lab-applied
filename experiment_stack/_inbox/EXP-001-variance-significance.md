# Experiment: Statistical Significance Testing for Temporal Attention

- **ID**: EXP-001
- **Created**: 2026-01-23
- **Source**: SIM-001 (SME Q1)
- **Priority**: P1
- **Status**: queued

## Objective

Run multiple training runs (3-5) for all pooling methods to establish variance and statistical significance of the +2.4 R@1 improvement.

## Method

1. Repeat training for all 4 conditions (mean pooling, max pooling, fixed attention, temporal attention) with 3-5 different random seeds
2. Report mean and standard deviation for R@1, R@5, R@10
3. Conduct paired t-test or Wilcoxon signed-rank test between temporal attention and mean pooling
4. Use same hyperparameters across all runs

## Success Criteria

- Standard deviation reported for all metrics
- p < 0.05 for improvement over mean pooling baseline
- If p > 0.05, investigate why variance is high
