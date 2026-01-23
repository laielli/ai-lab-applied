# Experiment: Add Additional Retrieval Metrics

- **ID**: EXP-005
- **Created**: 2026-01-23
- **Source**: SIM-001 (SME Q3)
- **Priority**: P2
- **Status**: queued

## Objective

Expand evaluation metrics beyond R@K and MdR to better discriminate between methods.

## Method

1. Add MnR (Mean Rank) to all experiments
2. Consider adding nDCG@K for graded relevance assessment
3. Analyze per-difficulty breakdowns (if query difficulty annotations exist)
4. Report metric correlations to understand what each captures

## Success Criteria

- At least one additional metric shows discrimination between methods (unlike MdR=2.0 for all)
- Clear interpretation of what improvement means for each metric
