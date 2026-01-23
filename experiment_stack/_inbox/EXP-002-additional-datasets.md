# Experiment: Additional Dataset Evaluation (ActivityNet, DiDeMo)

- **ID**: EXP-002
- **Created**: 2026-01-23
- **Source**: SIM-001 (Advisor Q1)
- **Priority**: P1
- **Status**: queued

## Objective

Evaluate temporal attention method on ActivityNet Captions and DiDeMo datasets to verify generalization of +2.4 R@1 improvement beyond MSRVTT.

## Method

1. Prepare ActivityNet Captions paragraph-to-video retrieval setup
2. Prepare DiDeMo localization-as-retrieval setup
3. Run all 4 pooling conditions on both datasets
4. Compare improvement magnitude to MSRVTT results

## Success Criteria

- R@1 improvement >= +1.5 on both additional datasets
- Go/no-go decision: If improvement < +1.5 on either dataset, reconsider CVPR submission
- Consistent ranking of methods (temporal attention > fixed attention > mean pooling)
