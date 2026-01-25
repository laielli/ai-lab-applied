# Writing Task: IDEA-009 Go/No-Go Decision Document

- **ID**: WRITE-004
- **Created**: 2026-01-25
- **Paper**: IDEA-009-temporal-fourier-signatures
- **Section**: decision document
- **Priority**: P2
- **Status**: pending
- **Source**: SIM-006 (Advisor Q1)

## Task Description

Write a structured decision document that synthesizes all evidence for and against continuing IDEA-009 (TFS/TOPA). This document should provide a clear recommendation and criteria for the go/no-go decision.

## Context

### Paper Overview

IDEA-009 started as "Temporal Fourier Signatures" - encoding temporal position via frequency-domain rotation. After discovering rotation breaks CLIP alignment (-73.3pp), we pivoted to TOPA (additive positional encoding). TOPA preserves alignment but only matches mean pooling performance on our limited test set.

### Current Status

- TFS: Failed (-73.3pp on real CLIP features)
- TOPA: Matches mean pooling (0.0pp delta at scale 0.01)
- Test set: Only 30 videos (insufficient for statistical power)
- Temporal benchmark: Not yet tested

### Decision Context

We need to decide whether to:
1. **Continue**: Invest more time in IDEA-009 (full-scale evaluation, temporal benchmarks)
2. **Shelve**: Document findings and reallocate effort to other ideas
3. **Pivot**: Reframe as analysis/benchmark paper rather than method paper

## Source Materials

- Simulation: SIM-006-topa-pivot-results.md
- Experiment: EXP-014-topa-validation (results)
- Idea document: IDEA-009-temporal-fourier-signatures.md

## Requirements

### Must Include

- Summary of all experiments run (TFS, TOPA)
- Quantitative results table
- List of remaining experiments needed for publication
- Estimated time/compute for remaining work
- Risk assessment (probability of publishable outcome)
- Clear recommendation (continue/shelve/pivot)
- Criteria that would change the recommendation

### Must Avoid

- Overstating promise of current results
- Sunk cost reasoning ("we've invested so much...")
- Vague recommendations

### Tone/Style

Direct, honest, data-driven. The goal is to help make a good decision, not to advocate for any particular outcome.

## Key Points to Make

1. What we learned (rotation breaks alignment; additive preserves it)
2. What we don't know (does TOPA help on temporal queries?)
3. What it would take to publish (improvements on temporal benchmarks)
4. What we'd learn from remaining experiments
5. Opportunity cost of continuing

## Decision Framework

| Evidence Type | Finding | Implication |
|---------------|---------|-------------|
| TFS real features | -73.3pp | Rotation approach dead |
| TOPA alignment | 99.22% preserved | Additive approach viable |
| TOPA retrieval | +0.0pp vs mean | No improvement yet |
| Test set size | 30 videos | Can't detect small effects |
| Temporal benchmark | Not tested | Unknown potential |
