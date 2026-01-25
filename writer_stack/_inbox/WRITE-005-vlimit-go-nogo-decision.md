# Writing Task: V-LIMIT Go/No-Go Decision Document

- **ID**: WRITE-005
- **Paper**: idea-010-v-limit
- **Type**: decision-document
- **Source**: SIM-007 (Advisor Q2, Q4)
- **Priority**: P1
- **Deadline**: 2026-02-08 (two weeks from now)

## Purpose

Create a formal decision document establishing clear criteria for continuing or abandoning the V-LIMIT paper project. This provides accountability and prevents sunk-cost fallacy from driving continued investment in a potentially unviable direction.

## Content Requirements

### 1. Current Status Summary
- Phase 1 and 2 results recap
- Resources invested to date
- Key finding: LIMIT effect did not replicate at d=0.173, 100 videos

### 2. Decision Criteria

**Continue if (EXP-020 shows):**
- BM25 outperforms CLIP by >= 10pt at high density
- OR ColBERT shows >= 15pt improvement over CLIP
- OR clear density threshold is identified where methods diverge

**Pivot if:**
- BM25-CLIP gap remains < 5pt at d>=0.4, 500 videos
- AND no clear boundary conditions emerge

**Abandon if:**
- No publishable findings emerge from boundary analysis
- AND opportunity cost of continued investment exceeds potential value

### 3. Pivot Options

If V-LIMIT doesn't pan out:
1. **Negative result paper**: "The LIMIT Effect Does Not Transfer to Video Retrieval" (workshop-level)
2. **Redirect to IDEA-009**: Temporal Fourier Signatures has stronger experimental signal
3. **New direction**: Investigate why video retrieval differs from text retrieval

### 4. Timeline

- 2026-01-27: Start EXP-020
- 2026-02-03: EXP-020 results available
- 2026-02-05: Analysis complete
- 2026-02-08: Go/no-go decision finalized

### 5. Resource Allocation Post-Decision

- If GO: Full commitment to V-LIMIT, EXP-021+ planned
- If NO-GO: Redirect 80% effort to IDEA-009, 20% to negative result writeup

## Deliverable Format

Markdown document suitable for inclusion in `papers/idea-010-v-limit/decisions/` or main project STATUS.md.

## Notes

This document serves as pre-commitment mechanism. Write it now, before EXP-020 results are known, to avoid post-hoc rationalization.
