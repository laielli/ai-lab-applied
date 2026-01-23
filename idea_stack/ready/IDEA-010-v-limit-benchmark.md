# Idea: V-LIMIT - Stress-Testing Video Retrieval Embedding Capacity

- **ID**: IDEA-010
- **Stage**: ready
- **Created**: 2026-01-22
- **Promoted to developing**: 2026-01-23
- **Promoted to ready**: 2026-01-23
- **Source**: PAPER-009

## Research Question

Do current video retrieval benchmarks have artificially sparse query-relevance patterns that mask fundamental embedding capacity limitations? Can we create a LIMIT-style benchmark that exposes when single-vector video embeddings fail?

## Hypothesis

Current video retrieval benchmarks (MSR-VTT, DiDeMo, ActivityNet) have low d_tripartite (sparse qrel patterns), allowing simple single-vector embeddings to succeed. A benchmark with dense combinatorial patterns (V-LIMIT) will cause:
1. Dense single-vector models to fail dramatically (like text LIMIT: <20% recall@100)
2. Multi-vector and cross-encoder approaches to succeed
3. BM25-style sparse retrieval to remain competitive

**Predicted outcome**: We will demonstrate a >50 point recall gap between dense single-vector and multi-vector/cross-encoder approaches on V-LIMIT, while this gap is <10 points on current benchmarks.

## Why Novel

PAPER-009 (Weller et al. 2025) established the theoretical framework for embedding capacity limits in text retrieval. No one has:
1. Applied this framework to video retrieval benchmarks
2. Created a video benchmark specifically designed to stress-test embedding capacity
3. Analyzed why simple methods often match complex ones on video retrieval

**Gap**: We don't know if video retrieval SOTA reflects genuine capability or benchmark sparsity.

## Proposed Experiments

### Phase 1: Benchmark Analysis (<8 GPU-hours)

| Exp | Description | Deliverable |
|-----|-------------|-------------|
| 1.1 | Compute d_tripartite for MSR-VTT, DiDeMo, ActivityNet | Difficulty ranking of existing benchmarks |
| 1.2 | Graph density analysis of qrel patterns | Visualization of benchmark structure |

### Phase 2: V-LIMIT Prototype (<24 GPU-hours)

| Exp | Description | Deliverable |
|-----|-------------|-------------|
| 2.1 | Mini V-LIMIT construction (~100 videos, ~1000 queries) | Benchmark dataset with controlled density |
| 2.2 | Model stress test (CLIP, X-CLIP, InternVideo2, ColBERT, cross-encoder) | Performance comparison showing capacity limits |

### Phase 3: Full Benchmark

| Exp | Description | Deliverable |
|-----|-------------|-------------|
| 3.1 | Temporal V-LIMIT variant (sequence queries) | Temporal reasoning stress test |
| 3.2 | Scale-up to 1K videos, 10K queries | Release-ready benchmark |

## Compute Budget

| Phase | GPU-Hours | Deliverable |
|-------|-----------|-------------|
| Validation | <8 | d_tripartite analysis |
| Prototype | <24 | Mini V-LIMIT + model eval |
| Full | ~40 | Complete benchmark |

**Total**: <72 GPU-hours

## Target Venue

**Primary**: NeurIPS 2026 Datasets & Benchmarks Track
**Deadline**: ~May 2026
**Backup**: EMNLP 2026 or ACL 2026

## Success Criteria

1. Demonstrate >50 point recall gap on V-LIMIT vs <10 on existing benchmarks
2. Show correlation between d_tripartite and model performance gap
3. Provide architectural guidance: when single-vector sufficient vs multi-vector needed
4. Release benchmark with multiple difficulty tiers

## Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| Artificially hard benchmark | Include real-world validation; difficulty tiers |
| All methods fail equally | Design gradient of difficulty; ensure some methods succeed |
| Annotation cost too high | Use synthetic generation with controlled structure |

## Status

**LAUNCHED** → `papers/idea-010-v-limit/`

Paper project created 2026-01-23.
