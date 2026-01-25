# Experiment: V-LIMIT High-Density Scaling Test

- **ID**: EXP-020
- **Paper**: idea-010-v-limit
- **Status**: inbox
- **Source**: SIM-007 (Advisor Q1, Q3)
- **Priority**: P1

## Objective

Test whether the LIMIT phenomenon emerges at higher density and larger scale than the Phase 2 pilot experiment.

## Background

EXP-003 showed no divergence between BM25 and CLIP at d=0.173 on 100 videos. The original LIMIT paper demonstrated 30+ point gaps under high-density conditions. This experiment scales up to determine whether the effect emerges with more challenging conditions.

## Hypothesis

At density d>=0.4 and 500+ videos, BM25 will outperform CLIP by at least 10 points on R@10, partially replicating the LIMIT effect.

## Method

1. **Scale benchmark to 500 videos** from VaTeX
2. **Generate high-density queries** targeting d>=0.4 (increase lexical overlap via modified templates)
3. **Evaluate same methods**: Random, BM25, CLIP, ColBERT
4. **Statistical analysis**: Same metrics (R@1, R@5, R@10, MRR) with significance tests

## Success Criteria

- If BM25 > CLIP by >= 10pt: LIMIT partially replicates, continue V-LIMIT paper
- If BM25 > CLIP by 5-10pt: Weak signal, needs further investigation
- If BM25 ~= CLIP (< 5pt gap): LIMIT does not transfer to video domain, consider pivot

## Estimated Compute

- 500 videos x 4 methods x 5000 queries = ~2.5M retrieval operations
- CLIP/ColBERT encoding: ~2 hours on single A100
- Total: ~4 hours wall time

## Dependencies

- EXP-002 benchmark construction code (complete)
- VaTeX dataset access (available)
- High-density query generation templates (to be developed)

## Notes

This is a decisive experiment for the V-LIMIT paper. Results directly inform go/no-go decision (see WRITE-005).
