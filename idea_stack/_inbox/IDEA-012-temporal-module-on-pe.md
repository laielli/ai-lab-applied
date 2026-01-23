# Idea: Temporal Reasoning Module on Frozen PE-Core

- **ID**: IDEA-012
- **Source**: PAPER-001
- **Created**: 2026-01-23
- **Stage**: nascent
- **Status**: new

## Core Insight

PE-Core achieves SOTA on video retrieval with simple frame averaging and no temporal modeling. This suggests the frame-level representations are strong, but temporal reasoning is missing. A lightweight temporal module on top could add temporal capabilities efficiently.

## Research Question

Can we add explicit temporal reasoning capabilities to PE-Core's strong frame representations by adding a lightweight temporal reasoning module, while keeping the base model frozen?

## Potential Approach

1. Use PE-Core as a frozen frame encoder
2. Add lightweight temporal reasoning layers (temporal transformer, temporal attention)
3. Train only the temporal module on video tasks
4. Compare against full video encoders on temporal benchmarks

## Connection to Lab Vision

Aligns with lab priorities of building on foundation models efficiently. Leverages PE's strong frame representations while adding missing temporal modeling - the best of both worlds.

## Source Context

Extracted from: reading_stack/summaries/PAPER-001-bolya-2025.md

Ideas Sparked section:
> "IDEA-002: Build temporal reasoning module on top of frozen PE-Core. Leverage their strong frame representations while adding explicit temporal modeling that's missing."
