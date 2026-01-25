# EXP-018: Full MSR-VTT TOPA Validation

**Created**: 2026-01-25
**Paper**: IDEA-009 Temporal Fourier Signatures
**Status**: BLOCKED
**Blocked by**: EXP-017
**Priority**: P1 - Critical for go/no-go decision

---

## Objective

Validate the R@1 improvement (+3.3pp) observed in EXP-014 at full scale with 1000 videos, and determine statistical significance.

## Motivation

EXP-014 showed TOPA improves R@1 from 36.7% to 40.0% on 30 test videos. However:
- This represents only 1 additional correct video
- 30 videos lacks statistical power to detect <15pp effects
- Full MSR-VTT test set (1000 videos) needed for reliable conclusions

**Human feedback**: "R@1, where actually TOPA improves on mean polling, going from 36.7 to 40.0. That is really interesting."

## Method

1. Load full MSR-VTT features from EXP-017
2. Train TOPA, Mean, TFS projections with same protocol as EXP-014:
   - Contrastive loss (InfoNCE)
   - 80/20 train/test split
   - 100 epochs, Adam optimizer
3. Evaluate R@1, R@5, R@10 on test set
4. Compute bootstrap confidence intervals (1000 resamples)
5. Perform statistical test for R@1 improvement

## Evaluation Protocol

| Metric | Description |
|--------|-------------|
| R@1 | Primary metric (most sensitive to ranking quality) |
| R@5 | Secondary metric |
| R@10 | Tertiary metric |
| 95% CI | Bootstrap confidence interval (1000 samples) |
| p-value | One-sided test: TOPA > Mean |

## Success Criteria

| Outcome | R@1 Improvement | 95% CI | Decision |
|---------|-----------------|--------|----------|
| **Confirmed** | ≥ +2pp | Does not include 0 | Strong continue signal |
| **Marginal** | +1 to +2pp | Includes 0 | Continue with caution |
| **Noise** | < +1pp | Wide CI | Likely random, shelve |

## Comparisons

| Method | Expected Performance |
|--------|---------------------|
| TOPA (α=0.01) | Hopefully ≥ Mean + 2pp |
| Mean Pooling | Baseline |
| TFS | Expected to fail (confirm theory) |

## Technical Details

| Parameter | Value |
|-----------|-------|
| Test videos | 800 (80% of 1000) train, 200 test |
| Features | From EXP-017 |
| Training | Same as EXP-014 |
| Bootstrap | 1000 resamples |

## Output

- `log/exp18/results.json`: All metrics with confidence intervals
- `log/exp18/comparison_table.md`: Formatted results table
- `log/exp18/bootstrap_distributions.png`: CI visualization

## Compute Estimate

- GPU: Lambda.ai A10 or local
- Time: ~1 GPU-hour (training + evaluation)

## Blockers

- **EXP-017**: Full MSR-VTT features must be extracted first

## Go/No-Go Impact

This experiment determines whether to continue IDEA-009:
- **If R@1 confirmed**: Proceed to temporal query analysis (EXP-019)
- **If noise**: Shelve IDEA-009, document learnings
