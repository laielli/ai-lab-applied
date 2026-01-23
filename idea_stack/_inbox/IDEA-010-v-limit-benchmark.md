# Idea: V-LIMIT - Stress-Testing Video Retrieval Embedding Capacity

- **ID**: IDEA-010
- **Stage**: nascent
- **Created**: 2026-01-22
- **Source Papers**: PAPER-009

## Spark

PAPER-009 (Weller et al. 2025) proves that embedding-based retrieval has fundamental representational limitations tied to embedding dimension and query-relevance matrix sign-rank. Dense qrel patterns require high-dimensional embeddings to represent, and current SOTA dense retrievers fail dramatically on the LIMIT dataset (<20% recall@100) while BM25 (high implicit dimensionality) and cross-encoders succeed.

The core insight: **we do not know where video retrieval benchmarks fall on the easy-hard spectrum**. Current benchmarks may be artificially easy (sparse qrel) and hiding fundamental limitations of single-vector video embeddings. As video retrieval tasks become more complex (instruction-following, compositional queries, fine-grained temporal reasoning), we risk hitting representational bottlenecks without understanding why.

## Focus Areas
- Feature Learning
- Theory-Inspired Applications

## Initial Thoughts

### The Opportunity

Create a LIMIT-style benchmark for text-to-video retrieval that:
1. **Exposes embedding capacity limitations** through dense combinatorial qrel patterns
2. **Provides theoretical grounding** for understanding method failures
3. **Guides architectural decisions** (when to use multi-vector, when to require cross-encoder reranking)

### Possible Designs

**Design A: Attribute Combinations**
- Videos with multiple annotated attributes (action, object, scene, person, time-of-day)
- Queries combine attribute requirements: "person running in park with dog"
- Ground truth requires exact combination matching
- Vary number of attributes to trace capacity curve

**Design B: Temporal Sequence Combinations**
- Videos with sequences of events/actions
- Queries specify temporal patterns: "first A, then B, finally C"
- Ground truth requires matching temporal order
- Natural dense qrel: many videos have subsets of required sequence

**Design C: Multi-Modal Constraint Combinations**
- Videos with audio, visual, and text (OCR) content
- Queries require combinations across modalities
- "video with person speaking AND text showing 'welcome'"

### Analysis Component

Beyond the benchmark, apply PAPER-009's framework to existing benchmarks:
- Compute d_tripartite for MSR-VTT, DiDeMo, ActivityNet
- Correlate benchmark difficulty with graph density
- Understand if current SOTA numbers reflect genuine capability vs. benchmark sparsity

### Expected Findings

If hypothesis is correct:
1. Current benchmarks will show low d_tripartite (sparse qrel)
2. V-LIMIT will show high d_tripartite by design
3. Dense single-vector models will fail on V-LIMIT
4. Multi-vector and cross-encoder approaches will succeed
5. This explains why simple methods often match complex ones on current benchmarks

### Connection to Lab Priorities

**Temporal Reasoning**: Temporal sequence queries naturally create dense qrel patterns (many videos contain subsets of required temporal structure). V-LIMIT could specifically stress-test temporal reasoning capacity.

**Benchmark Innovation**: Directly addresses lab priority of "rigorous evaluation on standard benchmarks" by understanding benchmark limitations.

**Architectural Guidance**: Provides principled basis for deciding when single-vector is sufficient vs. when multi-vector/cross-encoder is needed.

### Open Questions

1. What is the right scale for V-LIMIT? (number of videos, queries, attributes)
2. How to ensure linguistic diversity while maintaining combinatorial structure?
3. Can we create V-LIMIT using existing video datasets with additional annotations?
4. How to balance benchmark difficulty with practical usefulness?
5. Should V-LIMIT focus on one type of combination (temporal, attribute, multi-modal) or be comprehensive?

### Risks

- Creating an artificially hard benchmark that does not reflect real use cases
- If all methods fail equally, benchmark provides limited signal
- Annotation cost for dense qrel patterns may be high

### Next Steps to Develop

1. Compute d_tripartite for 2-3 existing video retrieval benchmarks
2. Design minimal V-LIMIT prototype with ~50 videos, ~500 queries
3. Run existing models (CLIP, X-CLIP, InternVideo) to validate that benchmark exposes limitations
4. If successful, expand to full benchmark with multiple difficulty levels
