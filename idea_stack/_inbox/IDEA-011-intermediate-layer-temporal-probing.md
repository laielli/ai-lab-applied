# Idea: Intermediate Layer Temporal Probing

- **ID**: IDEA-011
- **Source**: PAPER-001
- **Created**: 2026-01-23
- **Stage**: nascent
- **Status**: new

## Core Insight

Perception Encoder demonstrates that optimal embeddings for various tasks exist in intermediate transformer layers rather than the final output. This raises the question: do intermediate layers contain better temporal reasoning features that are compressed away at the output?

## Research Question

Can we identify intermediate layers of video encoders that contain richer temporal features than the output layer, similar to how PE found spatial and language features hidden in intermediate layers?

## Potential Approach

1. Apply PE's layer-probing methodology to temporal tasks (action ordering, temporal grounding)
2. Evaluate each layer's temporal reasoning capability using probes
3. If temporal features exist, develop extraction methods similar to PE's language/spatial alignment

## Connection to Lab Vision

Directly addresses the lab's temporal reasoning priority. If temporal features are being compressed at the output layer, this could explain why simple frame averaging achieves SOTA on current benchmarks - the temporal signal may never reach the output.

## Source Context

Extracted from: reading_stack/summaries/PAPER-001-bolya-2025.md

Ideas Sparked section:
> "IDEA-001: Investigate intermediate layers of video encoders for temporal reasoning features using PE's probing methodology. Hypothesis: temporal features exist but are compressed at output layer similar to spatial/language features."
