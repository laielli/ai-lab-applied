# Idea: Adaptive Retrieval Routing Based on Query Complexity

- **ID**: IDEA-015
- **Source**: PAPER-009
- **Created**: 2026-01-23
- **Stage**: nascent
- **Status**: new

## Core Insight

PAPER-009 proves that embedding-based retrieval has fundamental representational limitations tied to embedding dimension and query-relevance matrix sign-rank. Dense qrel patterns require high-dimensional embeddings. This suggests we should route queries adaptively based on complexity.

## Research Question

Can we use query complexity analysis to route between efficient embedding retrieval and expensive cross-encoder reranking, optimizing the efficiency-accuracy tradeoff based on theoretical capacity constraints?

## Potential Approach

1. Analyze query structure (number of constraints, compositional operators like AND/OR)
2. Predict qrel density based on query complexity
3. Route simple queries to single-vector retrieval (fast)
4. Route complex queries to multi-vector or cross-encoder (accurate)
5. Learn routing policy from observed retrieval failures

## Connection to Lab Vision

Provides principled basis for architectural decisions in retrieval systems. Balances efficiency (lab priority) with accuracy on complex queries.

## Source Context

Extracted from: reading_stack/summaries/PAPER-009-weller-2025.md

Ideas Sparked section:
> "IDEA-011: Adaptive Retrieval Routing - Use query complexity analysis to route between efficient embedding retrieval and expensive cross-encoder reranking."
