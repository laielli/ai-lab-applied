# Writing Task: IDEA-003 Paper Positioning Decision Document

- **ID**: WRITE-003
- **Created**: 2026-01-24
- **Paper**: idea-003-avg-pooling
- **Section**: strategy document (not paper section)
- **Source**: SIM-005 (Advisor Q2, Q5)
- **Priority**: P2
- **Status**: pending

## Task Description

Write a decision document that evaluates different paper strategies for IDEA-003 findings. Help clarify whether to pursue:

1. **Analysis-only paper**: Document the paradox, show layer probing results, explain why average pooling works
2. **Method + Analysis paper**: Add "temporal alignment" approach using intermediate layers
3. **Combined with IDEA-009**: Merge with Temporal Fourier Signatures work

## Context

### Paper Overview

IDEA-003 investigates why simple average pooling over frame embeddings achieves SOTA on video retrieval despite discarding temporal order. Key finding: temporal information peaks at layer 10 (~64% probe accuracy) and decays to ~57% at output layer.

### Current Status

- Exp 1.2, 1.4, 3.1 complete (probing experiments)
- EXP-014, EXP-015, EXP-016 queued (validation and pilot experiments)
- No method contribution yet

### Target Venue Options

| Option | Venue Type | Requirements |
|--------|------------|--------------|
| Analysis-only | Workshop (CVPR VU) or Short Paper | Understanding + clear story |
| Method + Analysis | Main conference (CVPR/ICCV) | Retrieval improvements |
| Combined | Main conference | Both understanding + method |

## Source Materials

- Exp 3.1 results (layer probing)
- IDEA-003 document in idea_stack
- IDEA-009 document (Temporal Fourier Signatures)
- SIM-005 session transcript

## Requirements

### Must Include

- Clear pros/cons for each strategy
- Venue recommendations for each path
- Timeline implications (deadlines, compute)
- Go/no-go criteria for method path
- Relationship to IDEA-009

### Must Avoid

- Overclaiming analysis-only contribution
- Underestimating effort for method contribution
- Vague recommendations

### Tone/Style

Direct, strategic, decision-oriented

## Key Points to Make

1. Analysis-only is publishable but lower tier
2. Method contribution requires EXP-015 success
3. IDEA-009 is orthogonal and can proceed independently
4. Decision depends on EXP-015 pilot results

## Decision Framework

Structure the document as:

1. **Current Evidence Summary**
2. **Option A: Analysis Paper**
   - What it includes
   - Target venues
   - Timeline
   - Pros/cons
3. **Option B: Method + Analysis Paper**
   - What additional work is needed
   - Go/no-go criteria
   - Target venues
   - Timeline
   - Pros/cons
4. **Option C: Combined with IDEA-009**
   - Synergies and conflicts
   - Timeline implications
   - Recommendation
5. **Recommended Path**
   - Primary recommendation
   - Contingency plan
   - Decision points
