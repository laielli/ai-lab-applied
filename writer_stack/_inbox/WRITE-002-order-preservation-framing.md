# Writing Task: Order Preservation Contribution Framing

- **ID**: WRITE-002
- **Created**: 2026-01-24
- **Paper**: IDEA-009-temporal-fourier-signatures
- **Section**: introduction / method preamble
- **Source**: SIM-003 (Advisor Q4, Contested Points)
- **Priority**: P3
- **Status**: pending

## Task Description

Draft framing language for the TFS contribution that positions "temporal order preservation" as the right goal, avoiding overpromising while making a compelling case. Address the concern that the revised scope (from "temporal dynamics" to "order preservation") might seem like a reduced claim.

## Context

### Paper Overview

TFS provides a rotation-based encoding that preserves frame order information through the aggregation operation. After internal methodology audit, we revised claims to focus on order preservation rather than broader temporal dynamics understanding.

### Target Venue

Workshop paper initially, with potential expansion to main track (CVPR/ICCV/NeurIPS)

### Challenge

Reviewers might see "order preservation" as a weaker claim than "temporal understanding." Need to argue that:
1. Order preservation is the fundamental building block of temporal reasoning
2. Current methods (mean pooling) provably lose this information
3. The information-theoretic analysis provides novel scientific insight
4. Strong results on temporal queries validate practical relevance

## Source Materials

- PRD: IDEA-009 documentation
- Experiments: EXP-001 through EXP-006 results
- Related papers: RoPE, positional encoding literature

## Requirements

### Must Include

- Clear problem statement: mean pooling loses temporal order
- Mathematical precision: what exactly TFS preserves
- Empirical relevance: why temporal queries matter for video retrieval
- Scope acknowledgment: what TFS does NOT claim to do

### Must Avoid

- Overpromising ("understands temporal dynamics")
- Dismissing limitations
- Jargon without explanation

### Tone/Style

Technical but accessible. Confident but honest about scope.

## Key Points to Make

1. Video retrieval fundamentally requires distinguishing events that differ in order
2. Mean pooling is provably order-agnostic (same output for any permutation)
3. TFS provides order-sensitive aggregation with theoretical guarantees
4. This is the RIGHT abstraction: order preservation enables temporal reasoning

## Framing Strategies to Explore

1. **Foundation framing**: "We address the foundational problem of order preservation, which underlies all temporal reasoning"

2. **Information-theoretic framing**: "We show that standard pooling destroys order information and propose a method that preserves it"

3. **Benchmark-driven framing**: "Current benchmarks under-test temporal understanding; we identify a gap and propose a solution"

4. **Building block framing**: "TFS provides an order-preserving primitive that can be composed with other temporal reasoning modules"

## Expected Output

2-3 paragraphs suitable for:
- Introduction (problem motivation section)
- Method section preamble (before technical details)
- A clear "contribution statement" that is honest and compelling
