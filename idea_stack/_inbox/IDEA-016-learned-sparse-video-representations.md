# Idea: Learned Sparse Video Representations

- **ID**: IDEA-016
- **Source**: PAPER-009
- **Created**: 2026-01-23
- **Stage**: nascent
- **Status**: new

## Core Insight

PAPER-009 shows that BM25 achieves 95.5% recall@100 on LIMIT (vs <20% for dense embeddings) because of its high implicit dimensionality. This suggests that sparse, high-dimensional representations can overcome the fundamental capacity limits of dense embeddings.

## Research Question

Can we learn sparse video representations over a learned concept vocabulary, combining the capacity benefits of high-dimensional sparse representations with learned semantic features?

## Potential Approach

1. Learn a video concept vocabulary (action concepts, object concepts, temporal concepts)
2. Train video encoder to produce sparse activations over this vocabulary
3. Each video activates a sparse subset of concept dimensions
4. Use efficient sparse retrieval (like BM25) for matching
5. Bridge between dense CLIP embeddings and explicit concept detection

## Connection to Lab Vision

Addresses fundamental capacity limitations while maintaining efficiency through sparsity. SPLADE exists for text retrieval; this would be the video equivalent.

## Source Context

Extracted from: reading_stack/summaries/PAPER-009-weller-2025.md

Ideas Sparked section:
> "IDEA-012: Learned Sparse Video Representations - BM25's success on LIMIT comes from high implicit dimensionality. Apply this insight to video. Learn sparse video representations over a learned concept vocabulary."
