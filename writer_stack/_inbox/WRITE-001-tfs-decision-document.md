# Writing Task: TFS Project Go/No-Go Decision Document

- **ID**: WRITE-001
- **Created**: 2026-01-24
- **Paper**: IDEA-009-temporal-fourier-signatures
- **Section**: decision-document
- **Priority**: P1
- **Status**: pending

## Task Description

Create a formal go/no-go decision document for the TFS project that:
1. Summarizes the current state of evidence
2. Defines explicit success criteria for continuation
3. Sets a timeline for the decision
4. Documents the decision rationale

## Context

### Paper Overview

TFS (Temporal Fourier Signatures) proposes order-preserving video aggregation via rotation-based encoding. The core mechanism is validated (600K-1Mx order variance ratio), but the downstream benefit (retrieval performance) is not demonstrated.

**Critical finding**: The +8.8pp improvement on temporal queries does NOT replicate across seeds (p=1.0, multi-seed average = 0.0pp).

### Why This Document is Needed

The project has reached a decision point. Without clear criteria, there's risk of:
- Sunk cost fallacy (continuing because of past investment)
- Opportunity cost (blocking resources from other projects)
- Indefinite debugging without clear endpoint

## Source Materials

- SIM-004 simulation session (Advisor Q1, Q3)
- `papers/idea-009-tfs/STATUS.md`
- `papers/idea-009-tfs/log/validation_experiments_summary.md`

## Requirements

### Must Include

1. **Current Evidence Summary**
   - What's validated (mechanism)
   - What's failed (dynamics, retrieval)
   - What's untested (real features)

2. **Decision Criteria**
   - Specific thresholds for "proceed" vs "shelve"
   - Timeline for decision (1 week recommended)
   - Who makes the final call

3. **Pilot Experiment Success Criteria**
   - What result from EXP-012 would justify continuation?
   - What result would mandate shelving?

4. **Fallback Options**
   - Workshop paper on mechanism alone
   - Pivot to different downstream task
   - Shelve with documented negative result

### Must Avoid

- Vague criteria ("if results look promising")
- Open-ended timelines
- Avoiding the hard decision

### Tone/Style

Direct, honest, decision-focused. This is an internal document, not a paper.

## Key Points to Make

1. The main retrieval result is invalidated - we cannot claim +8.8pp improvement
2. The mechanism is validated but "so what?" is unanswered
3. Synthetic features are inadequate for hypothesis testing
4. Real features pilot (EXP-012) is the critical experiment
5. If pilot fails, project should be shelved with documented learnings

## Suggested Structure

```markdown
# TFS Project Decision Document

## Executive Summary
[2-3 sentences on current state and recommendation]

## Evidence Summary
### Validated Claims
### Failed Claims
### Untested Hypotheses

## Decision Criteria
### Proceed Criteria
### Shelve Criteria
### Timeline

## Pilot Experiment (EXP-012)
### Design
### Success Criteria
### Expected Timeline

## Fallback Options
### Option A: Workshop Paper
### Option B: Task Pivot
### Option C: Shelve

## Recommendation
[Clear recommendation with rationale]

## Decision Record
[To be filled after decision is made]
```
