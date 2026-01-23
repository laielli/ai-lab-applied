# Experiment: Compute Cost Comparison

- **ID**: EXP-003
- **Created**: 2026-01-23
- **Source**: SIM-001 (SME Q5)
- **Priority**: P2
- **Status**: queued

## Objective

Measure and report computational overhead of temporal attention compared to mean pooling baseline.

## Method

1. Measure inference time per query-video pair for each method
2. Count FLOPs for temporal attention layer
3. Report GPU memory usage during inference
4. Compute efficiency ratio: improvement per compute cost increase

## Success Criteria

- Inference time overhead < 50% over mean pooling
- Clear documentation of compute cost vs. accuracy trade-off
- If overhead > 100%, justify with significant accuracy gains
