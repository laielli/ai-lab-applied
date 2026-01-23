# Experiment: Comparison Against Stronger Temporal Baselines

- **ID**: EXP-004
- **Created**: 2026-01-23
- **Source**: SIM-001 (SME Q4)
- **Priority**: P2
- **Status**: queued

## Objective

Compare temporal attention against established temporal modeling methods (X-Pool, TS2-Net temporal components) to contextualize our contribution.

## Method

1. Implement or adapt X-Pool's temporal pooling mechanism
2. Implement TS2-Net's hierarchical temporal modeling (if feasible)
3. Run comparison on MSRVTT 1K split with same backbone
4. Document any implementation differences from original papers

## Success Criteria

- Temporal attention competitive with or exceeds X-Pool on R@1
- Clear attribution of improvements (temporal modeling vs. other factors)
- If underperforms, explain architectural differences and trade-offs
