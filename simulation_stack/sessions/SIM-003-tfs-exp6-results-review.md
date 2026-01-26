# SIM-003 Simulation Review Summary

**Date**: 2026-01-24
**Session**: `simulation_stack/sessions/SIM-003-tfs-exp6-results.md`

---

## Key Findings

| Persona | Questions | Hardest Challenge |
|---------|-----------|-------------------|
| Advisor | 4 | Is +8.8% on 6.8% of queries enough for a paper? |
| SME | 5 | Single seed, no variance estimates |
| Lay | 5 | Why synthetic features instead of real CLIP? |

---

## Critical P1 Blockers

1. **Variance estimates (EXP-007)** - Single seed makes the +8.8% claim untrustworthy
2. **Real CLIP validation (EXP-008)** - Synthetic features undermine ecological validity

---

## Action Items Routed

| Stack | Items |
|-------|-------|
| experiment_stack/_inbox/ | EXP-007 (variance), EXP-008 (real CLIP), EXP-009 (query validation), EXP-010 (fixed projection) |
| reading_stack/_inbox/ | PAPER-012 (temporal retrieval methods) |
| figure_stack/_inbox/ | FIG-003 (order preservation intuition) |
| writer_stack/_inbox/ | WRITE-002 (contribution framing) |

---

## Strongest Point

The information-theoretic analysis (variance ratios, effective dimensions, order reconstruction) provides unambiguous scientific evidence—this differentiates the work from pure "beat the baseline" papers.

---

## Recommended Preparation

For the real lab meeting, prepare answers for:

| Anticipated Question | Prepared Response |
|---------------------|-------------------|
| "What is the variance across runs?" | Running 5 seeds now |
| "Why synthetic features?" | Controlled setting, real CLIP in progress |
| "Is 6.8% enough?" | Validating on VATEX which has higher temporal density |

---

## Next Steps

1. **Immediate**: Run EXP-007 (multi-seed variance) - this is the single most critical gap
2. **Parallel**: Start EXP-008 (real CLIP features) - can run while variance experiments complete
3. **Quick win**: EXP-009 (temporal query validation) - 2-4 hours manual validation strengthens methodology
4. **Before baselines**: PAPER-012 literature search - ensure no obvious recent method is missing
