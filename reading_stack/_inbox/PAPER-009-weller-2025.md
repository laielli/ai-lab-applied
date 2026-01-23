# Paper: On the Theoretical Limitations of Embedding-Based Retrieval

- **ID**: PAPER-009
- **arXiv**: 2508.21038
- **Authors**: Orion Weller, Michael Boratko, Iftekhar Naim, Jinhyuk Lee (Google DeepMind, Johns Hopkins University)
- **Year**: 2025
- **Added**: 2026-01-22
- **Status**: summarized

## Why Read

This paper provides fundamental theoretical insights into the limitations of vector embedding models for retrieval tasks. It demonstrates that embedding dimension places hard constraints on the number of top-k document combinations that can be represented, which is directly relevant to text-to-video retrieval where we need to handle diverse queries and relevance definitions. The paper connects communication complexity theory to practical IR problems and introduces the LIMIT dataset that exposes these theoretical limitations in state-of-the-art models. Understanding these fundamental constraints will inform architectural choices for our retrieval systems (e.g., when to use single-vector vs multi-vector vs cross-encoder approaches).

## Focus Areas
- [ ] Mechanistic DL Theory
- [x] Feature Learning
- [ ] Knowledge Distillation
- [x] Theory-Inspired Applications

## Notes

The paper bridges theoretical computer science (communication complexity, sign-rank) with modern neural IR to prove that for any fixed embedding dimension d, there exist query-document relevance patterns that cannot be represented. Key contributions:

1. **Theoretical framework**: Connects the minimum embedding dimension needed to represent a retrieval task to the sign-rank of the query-relevance (qrel) matrix. Proves that rankrop(A) (row-wise order-preserving rank) equals the minimum dimension needed.

2. **Empirical validation**: Uses "free embedding" optimization (directly optimizing vectors on test data) to show the theoretical limits hold in practice. Finds critical-n points where dimension d becomes insufficient, fitting a polynomial: y = -10.5322 + 4.0309d + 0.0520d² + 0.0037d³

3. **LIMIT dataset**: A simple natural language instantiation where queries ask "who likes X?" and documents state "Person Y likes X and Z". Despite simplicity, SOTA models fail (< 20% recall@100) because the dense qrel pattern requires representing all C(46,2) = 1035 combinations.

4. **Practical implications**:
   - Multi-vector models (ColBERT) perform better but still struggle
   - BM25 succeeds due to very high implicit dimensionality
   - Cross-encoders solve the task easily (Gemini 2.5 Pro achieves 100%)
   - Instruction-following and reasoning tasks will increasingly hit these limits

The work suggests that as retrieval tasks become more diverse (through instructions, multi-modality), single-vector embeddings will increasingly encounter representational bottlenecks.

## Questions

1. How do these theoretical limitations manifest in video-text retrieval specifically? Video retrieval often involves complex multi-modal queries with diverse relevance criteria (scene similarity, action matching, semantic alignment, etc.). Does the high-dimensional nature of video embeddings help, or do we still hit similar bottlenecks?

2. Can we characterize the qrel matrix structure of typical text-to-video retrieval benchmarks (e.g., MSR-VTT, MSVD) using the graph density metrics from Section 10? Are they closer to the "disjoint" pattern (easier) or "dense" pattern (harder)?

3. The paper shows multi-vector models like ModernColBERT perform better but still struggle. What is the theoretical relationship between number of vectors and representational capacity? Is there a sign-rank-like bound for multi-vector architectures?

4. For instruction-following video retrieval (e.g., "find videos with running AND swimming"), do we need to design evaluation sets that test all relevant combinations, similar to LIMIT? Current benchmarks may be hiding these limitations by using sparse qrel patterns.

5. Could we use the sign-rank framework to guide architectural choices? For instance, estimate the required embedding dimension based on the expected diversity of relevance patterns in our target application?

6. The paper mentions sparse models have high implicit dimensionality. Could learned sparse representations (e.g., SPLADE) provide a middle ground between dense single-vector and expensive cross-encoders for complex video retrieval?

7. How do these results apply to cross-modal retrieval? The theoretical bounds assume a single embedding space, but video-text retrieval uses separate encoders. Does the cross-modal projection introduce additional constraints or opportunities?

8. Can we design hybrid architectures that use single-vector for first-stage retrieval but switch to multi-vector or cross-encoder when detecting queries that require representing many combinations (high graph density)?
