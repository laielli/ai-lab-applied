# Idea: Reverse Video Rewards for Contrastive Retrieval Training

- **ID**: IDEA-013
- **Source**: PAPER-002
- **Created**: 2026-01-23
- **Stage**: nascent
- **Status**: new

## Core Insight

ArrowRL introduces a reverse reward mechanism that penalizes models when their outputs are similar for forward and reversed video playback. This successfully teaches temporal direction awareness to VQA models. The same principle could be adapted for contrastive video-text retrieval.

## Research Question

Can ArrowRL's reverse reward concept be adapted to contrastive video-text training, training embeddings where sim(video, text) >> sim(reversed_video, text) for temporally-sensitive pairs?

## Potential Approach

1. Identify temporally-sensitive video-text pairs using TDS (Temporal Divergence Score)
2. Create training triplets: (video, text, reversed_video)
3. Add reverse penalty to contrastive loss: push reversed_video embedding away from text
4. Train standard CLIP-style models with this augmented objective

## Connection to Lab Vision

Directly addresses temporal reasoning in retrieval without architectural changes. Could improve retrieval on temporal benchmarks while maintaining compatibility with existing video-text frameworks.

## Source Context

Extracted from: reading_stack/summaries/PAPER-002-xue-2025.md

Ideas Sparked section:
> "IDEA-005 (potential): Adapt ArrowRL's reverse reward to contrastive video-text training. Train embeddings where sim(video, text) >> sim(reversed_video, text) for temporally-sensitive pairs. Could improve retrieval on temporal benchmarks without architectural changes."
