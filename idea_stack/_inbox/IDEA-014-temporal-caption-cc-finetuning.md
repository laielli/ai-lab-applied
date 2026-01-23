# Idea: Temporal Caption Contrastive Fine-tuning

- **ID**: IDEA-014
- **Source**: PAPER-004
- **Created**: 2026-01-23
- **Stage**: nascent
- **Status**: new

## Core Insight

LLM2CLIP's Caption Contrastive (CC) fine-tuning transforms LLMs into discriminative text encoders by training on caption pairs. This could be extended specifically for temporal reasoning by creating hard negatives from temporally-reversed events.

## Research Question

Can we create a CC fine-tuning dataset specifically for temporal reasoning where positive pairs describe the same event differently, and hard negatives are temporally reversed versions of the same event?

## Potential Approach

1. Create temporal caption pairs from video datasets:
   - Original: "Person opens door, walks inside, closes door"
   - Re-annotated: "Someone enters a building through a door"
   - Hard negative: "Person closes door, walks outside, opens door" (reversed)
2. Apply supervised SimCSE on these temporal pairs
3. Use CC-finetuned LLM for video-text retrieval

## Connection to Lab Vision

Improves text encoder's ability to discriminate temporal relationships, complementing visual temporal modeling. Could help LLMs distinguish "A then B" from "B then A" in retrieval queries.

## Source Context

Extracted from: reading_stack/summaries/PAPER-004-huang-2024.md

Ideas Sparked section:
> "IDEA-008 (potential): Temporal Caption Contrastive Fine-tuning - Create a CC fine-tuning dataset specifically for temporal reasoning. Positive pairs: same event described differently. Hard negatives: temporally reversed events. Could improve LLM discriminability for action understanding."
