# Idea: V-LIMIT - Stress-Testing Video Retrieval Embedding Capacity

- **ID**: IDEA-010
- **Stage**: developing
- **Created**: 2026-01-22
- **Promoted**: 2026-01-23
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

## Lab Vision Alignment

- **Temporal Reasoning**: Temporal sequence queries naturally create dense qrel patterns
- **Benchmark and Evaluation**: Directly addresses lab priority of understanding benchmark limitations
- **Efficient Video Representation**: Provides principled guidance for when single-vector is sufficient

## Potential Experiments

### Phase 1: Benchmark Analysis (<8 GPU-hours)

1. **Exp 1.1: d_tripartite Computation**
   - Compute d_tripartite for MSR-VTT, DiDeMo, ActivityNet qrel matrices
   - Compare to LIMIT text benchmark
   - Correlate with observed model performance gaps

2. **Exp 1.2: Graph Density Analysis**
   - Analyze bipartite graph structure of existing benchmarks
   - Identify if current benchmarks have near-bipartite qrel (easy) vs dense qrel (hard)

### Phase 2: V-LIMIT Prototype (<24 GPU-hours)

3. **Exp 2.1: Mini V-LIMIT Construction**
   - Create ~100 videos, ~1000 queries with combinatorial structure
   - Design A: Attribute combinations (action × object × scene)
   - Ensure dense qrel by construction

4. **Exp 2.2: Model Stress Test**
   - Evaluate on mini V-LIMIT:
     - CLIP (single-vector baseline)
     - X-CLIP, InternVideo2 (video-specific)
     - ColBERT-style multi-vector
     - Cross-encoder reranker
   - Measure recall@10, recall@100, d_tripartite correlation

### Phase 3: Full Benchmark (if validation succeeds)

5. **Exp 3.1: Temporal V-LIMIT Variant**
   - Design B: Temporal sequence combinations
   - Queries: "first A, then B, finally C"
   - Specifically stress-tests temporal reasoning capacity

6. **Exp 3.2: Scale-up**
   - Expand to 1K videos, 10K queries
   - Multiple difficulty tiers (2-attribute, 3-attribute, etc.)

## Compute Estimate

- Validation phase (Exp 1.1-1.2): ~4 GPU-hours
- Prototype construction and evaluation (Exp 2.1-2.2): ~16 GPU-hours
- Full benchmark: ~40 GPU-hours

## Open Questions

- [ ] What is the right scale for V-LIMIT? (number of videos, queries, attributes)
- [ ] How to ensure linguistic diversity while maintaining combinatorial structure?
- [ ] Can we create V-LIMIT using existing video datasets with additional annotations?
- [ ] Should V-LIMIT focus on temporal, attribute, or multi-modal combinations?
- [ ] How to balance benchmark difficulty with practical usefulness?

## Literature Check

- [x] Searched for related work (LIMIT, embedding capacity theory)
- [x] Not scooped - no video-specific embedding capacity benchmarks exist
- [x] Identified key baselines (CLIP, X-CLIP, InternVideo2, ColBERT)

## Risks

- Creating an artificially hard benchmark that doesn't reflect real use cases
- If all methods fail equally, benchmark provides limited signal
- Annotation cost for dense qrel patterns may be high

## Promotion Criteria

- [x] Clear research question
- [x] Testable hypothesis
- [x] Novelty argument
- [x] Viable experiment plan
- [ ] Validation experiment completed (Exp 1.1: d_tripartite analysis)
