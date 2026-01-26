# SIM-004 Simulation Review Summary

**Date**: 2026-01-24
**Session**: `simulation_stack/sessions/SIM-004-tfs-validation-results.md`

---

## Critical Finding

**The +8.8pp improvement claimed in SIM-003 does NOT replicate.**

Multi-seed analysis shows TFS vs Mean: 0.0pp difference (p=1.0)

---

## Experiments Run

| Experiment | Result | Implication |
|------------|--------|-------------|
| EXP-007 (5 seeds) | TFS = Mean (91.76% vs 91.76%) | Original result was seed artifact |
| EXP-008 (8 frames) | Mean beats TFS (-4.4pp) | Seed/config sensitive |
| EXP-011 (VATEX) | TFS > Mean (+1.7pp) | Small but consistent pattern |

---

## P1 Blockers

1. **Go/no-go decision document** (WRITE-001) - Define explicit criteria for project continuation
2. **Pilot with real CLIP features** (EXP-012) - Test hypothesis with actual video data

---

## Action Items Routed

| Stack | Items |
|-------|-------|
| writer_stack/_inbox/ | WRITE-001 (decision doc), WRITE-002 (timeline) |
| experiment_stack/_inbox/ | EXP-012 (real features pilot), EXP-013 (classifier validation) |
| reading_stack/_inbox/ | PAPER-001 (temporal dataset survey) |

---

## Key Question

**Is the project salvageable?**

- **Salvageable elements**: Mechanism validation (600K-1Mx order variance), VATEX pattern holds
- **Dead elements**: +8.8pp retrieval improvement claim
- **Unknown**: Whether real CLIP features will show different results

---

## Recommended Next Steps

1. **This week**: Run EXP-012 pilot (100 videos with real CLIP features)
2. **If pilot shows >2pp**: Proceed to full evaluation
3. **If pilot shows <2pp**: Shelve project with documented learnings

---

## Hard Truth

The simulated Advisor's assessment:
- 30% chance: Good venue (CVPR/ICCV/NeurIPS)
- 50% chance: Workshop or secondary venue
- 20% chance: Project should be shelved

The mechanism is real, but downstream benefit is unproven.
