# Idea: Temporal Dynamics Position Encoding (TDPE)

- **ID**: IDEA-008
- **Stage**: nascent
- **Created**: 2026-01-21
- **Source Papers**: PAPER-005 (RoFormer/RoPE), PAPER-006 (Complex Embeddings), PAPER-007 (VideoRoPE), PAPER-008 (Mechanistic RoPE)
- **Related Ideas**: IDEA-009 (Temporal Fourier Signatures - summable aggregation)

## Spark

Both RoPE and Complex Embeddings provide principled position encoding for NLP, but neither addresses video-specific challenges: non-uniform temporal spacing, semantic change rates, and cross-modal alignment with text temporal language. Can we design a position encoding specifically for text-to-video retrieval that encodes relative temporal relationships, semantic changes, and ordering dynamics?

## Focus Areas
- Cross-Modal Alignment
- Temporal Reasoning
- Efficient Video Representation

## Initial Thoughts

### Core Design

Extend rotary/complex embeddings with video-specific components:

```
f(frame, t) = A(frame) * P(t) * D(frame, t)
```

Where:
- **A(frame)**: Amplitude = visual content (from frozen encoder)
- **P(t)**: Position = phase encoding of temporal position
- **D(frame, t)**: Dynamics = semantic change rate encoding

### Five Key Components

**1. Content-Adaptive Frequencies**
- Insight from PAPER-006: Sentiment words learn higher frequencies (more position-sensitive)
- Insight from PAPER-008: Different attention heads naturally use different frequencies for different purposes (positional vs semantic)
- Video analog: Action-defining frames should be more position-sensitive than static backgrounds
- Implementation: `omega_j(frame) = omega_base_j + MLP(visual_features)[j]`
- **Mechanistic basis**: High frequencies → precise frame localization; Low frequencies → temporal semantics

**2. Semantic Change Encoding**
- Position alone doesn't capture "how much happened" between frames
- Proposal: Modulate phase based on cumulative semantic change
- `effective_pos(t) = sum(alpha + beta * ||f(t) - f(t-1)||)`
- Effect: High-activity segments have larger "effective distance"

**3. Asymmetric Temporal Encoding**
- Video has directional temporal flow ("A then B" != "B then A")
- Separate rotation rates for forward vs backward relative positions
- Enables distinction between anticipation and causality

**4. Multi-Scale Temporal Hierarchy**
- Design frequency schedule for video temporal scales
- Frame-level (motion/pose), shot-level (scene continuity), event-level (narrative)
- **Mechanistic basis** (PAPER-008): Explicitly separate high-freq (positional) and low-freq (semantic) functions

**5. Cross-Modal Phase Alignment**
- Text temporal words ("first", "then", "finally") map to phase offsets
- Creates soft alignment between text temporal language and video positions

### Why This Matters

| Aspect | RoPE | Complex Embed | TDPE |
|--------|------|---------------|------|
| Frequencies | Fixed | Learned per-word | Content-adaptive |
| Change rate | Ignored | Ignored | Explicit encoding |
| Cross-modal | N/A | N/A | Phase alignment |

### Key Research Questions

1. Does content-adaptive frequency improve temporal grounding?
2. Does semantic change encoding help on action-heavy vs static videos?
3. Does cross-modal phase alignment improve queries with temporal language?
4. Does asymmetric encoding help causal/ordering reasoning?

### Evaluation Targets

- **Temporal grounding**: ActivityNet Captions, Charades-STA
- **Temporal localization**: DiDeMo, QVHighlights
- **Retrieval with temporal queries**: Subset of MSR-VTT/VATEX with temporal language

### Open Questions

- How to handle videos with variable frame rates?
- Should semantic change be computed in feature space or pixel space?
- How many learnable parameters does this add (efficiency constraint)?
- Can this be integrated into existing video transformers (ViViT, TimeSformer)?
- Does this complement or conflict with learned temporal attention (VideoMAE)?

---

## Mechanistic Foundations (from PAPER-008)

### Key Insight: Frequency-Function Separation in RoPE

PAPER-008's mechanistic analysis of Gemma 7B reveals that RoPE frequencies serve distinct purposes:

| Frequency Band | Role | Mechanism |
|----------------|------|-----------|
| **High frequencies** (θ ~ 1 rad/token) | Positional patterns | Enable diagonal attention, previous-token attention |
| **Low frequencies** (θ ~ 1/10000 rad/token) | Semantic information | More position-invariant, content-based matching |

### Implications for TDPE Design

1. **Content-Adaptive Frequencies Are Mechanistically Sound**
   - Different heads already use different frequencies for different purposes
   - TDPE makes this explicit: action frames → high freq (precise localization), static scenes → low freq (semantic context)

2. **Multi-Scale Hierarchy Has Mechanistic Basis**
   - Don't just use arbitrary frequency schedules
   - Explicitly assign: high freq → frame-level motion, low freq → event-level semantics

3. **Long Video Robustness via p-RoPE Principle**
   - Low frequencies become unreliable at long context (Theorem 6.1)
   - For long videos: consider truncating or stabilizing lowest frequencies
   - Or: use semantic change encoding to make low-freq channels content-aware

4. **No Inherent Decay - Must Be Learned**
   - RoPE doesn't inherently favor nearby frames
   - TDPE's semantic change encoding provides explicit inductive bias for temporal locality

### Revised Design Principle

```
TDPE = Explicit separation of positional (high-freq) and semantic (low-freq) functions
     + Content-adaptive modulation of both
     + Semantic change encoding for robust temporal locality
```

---

## Literature Review (2026-01-21)

### Highly Relevant Prior Work

#### 1. VideoRoPE (Feb 2025) - [arXiv:2502.05173](https://arxiv.org/abs/2502.05173)
**Most directly relevant**. Extends RoPE to video with 3D structure.

Key contributions:
- Identifies four criteria: structure, frequency allocation, spatial symmetry, temporal scaling
- Uses **low-frequency temporal allocation** to mitigate periodic oscillations
- Diagonal layout for spatial symmetry
- Adjustable temporal spacing to decouple temporal and spatial indexing

**Gap vs TDPE**: VideoRoPE uses **fixed** frequency allocation. Our content-adaptive frequencies are novel.

#### 2. VRoPE (Feb 2025) - [arXiv:2502.11664](https://arxiv.org/abs/2502.11664)
Addresses video-text transitions in Video LLMs.

Key contributions:
- Restructures positional indices for smooth video-text transitions
- Balanced encoding strategy mitigating attention biases
- Symmetric positional transformations for implicit temporal capture

**Gap vs TDPE**: Focuses on video-text interface, not content-adaptive encoding or semantic change.

#### 3. V-CORE / Causality-Aware Temporal Projection (Jan 2026) - [arXiv:2601.01804](https://arxiv.org/abs/2601.01804)
**Relevant to asymmetric encoding component**.

Key contributions:
- Block-causal attention enforcing unidirectional information flow
- Addresses "temporal leakage" from unconstrained bidirectional attention
- Learnable Spatial Aggregation (LSA) + Causality-Aware Temporal Projector (CATP)

**Overlap**: Similar motivation to our asymmetric temporal encoding. Consider citing/comparing.

#### 4. CAPE/DAPE - Context-Adaptive Position Encoding - [arXiv:2405.14722](https://arxiv.org/abs/2405.14722)
**Relevant to content-adaptive component**.

Key contributions:
- Dynamically adjusts based on input context and learned priors
- First semantically-dependent adaptive position encoding for transformers
- Better length extrapolation

**Gap vs TDPE**: Applied to text only. Video adaptation is novel.

#### 5. SaPE² - 2D Semantic-Aware Position Encoding (May 2025) - [arXiv:2505.09466](https://arxiv.org/abs/2505.09466)
**Relevant to semantic awareness component**.

Key contributions:
- Dynamically adapts position representations using local content
- Better aggregation for visually similar but spatially distant patches
- Improves translation equivariance

**Gap vs TDPE**: Image-only, no temporal dimension. Video extension is novel.

#### 6. EventFormer (Feb 2024) - [arXiv:2402.13566](https://arxiv.org/abs/2402.13566)
**Relevant to event-aware encoding**.

Key contributions:
- Hierarchical event encoding (frame + event levels)
- Event extraction strategies (contrastive, kmeans, window)
- Aggregates visually similar consecutive frames as events

**Connection**: Similar intuition to semantic change encoding. Different approach (discrete events vs continuous change rate).

#### 7. MOOSE (June 2025) - [arXiv:2506.01119](https://arxiv.org/abs/2506.01119)
**Relevant to motion/change encoding**.

Key contributions:
- Embeds temporal dynamics via optical flow as distinct modality
- Each visual patch has corresponding motion patch embedding

**Gap vs TDPE**: Adds separate modality. We modulate position encoding itself.

#### 8. "Round and Round We Go!" (Oct 2024) - [arXiv:2410.06205](https://arxiv.org/abs/2410.06205) - PAPER-008
**Critical mechanistic foundation for TDPE**.

Key contributions:
- **Refutes conventional wisdom**: RoPE does NOT inherently cause attention decay with distance
- **Frequency roles discovered**: High frequencies → positional patterns (diagonal, previous-token); Low frequencies → semantic information
- **Mathematical proofs**: For any distance r, there exists a key making attention maximal at exactly that distance (Prop 3.1)
- **Low-freq fragility**: Theorem 6.1 shows low-frequency semantic channels become unreliable at long context
- **p-RoPE fix**: Truncating lowest 25% of frequencies improves robustness (4.441 vs 4.463 perplexity)

**Critical implications for TDPE**:
1. High frequencies for frame localization, low frequencies for temporal semantics → explicit separation in TDPE
2. Content-adaptive frequencies extend what heads already do implicitly
3. Explains WHY VideoRoPE's low-frequency temporal allocation works
4. Suggests p-RoPE-style truncation for long video robustness

### What's Novel in TDPE

| Component | Prior Work | TDPE Innovation |
|-----------|------------|-----------------|
| Video RoPE | VideoRoPE, VRoPE | **Content-adaptive** frequencies (vs fixed) |
| Semantic change | EventFormer (discrete events) | **Continuous** change rate modulating position |
| Asymmetric attention | V-CORE (causal projection) | **Position encoding level** (vs attention mask) |
| Multi-scale | VideoRoPE (fixed schedule) | **Content-conditioned** scale selection |
| Cross-modal alignment | None found | **Text temporal words → phase offset** is novel |
| Mechanistic basis | PAPER-008 (analysis only) | **Explicit design** based on freq-function separation |

### Novelty Assessment

**Strong novelty**:
- Content-adaptive frequencies for video (not done before)
- Semantic change rate modulating effective position (vs discrete events)
- Cross-modal phase alignment for temporal language

**Moderate novelty** (similar ideas exist, different approach):
- Asymmetric temporal encoding (V-CORE does this at attention level)
- Multi-scale hierarchy (VideoRoPE has this, but fixed)

### Papers to Add to Reading Stack

1. **VideoRoPE** - Must read, most similar work
2. **V-CORE** - For asymmetric/causal reasoning comparison
3. **EventFormer** - For event-aware video retrieval comparison

### Recommended Positioning

Position TDPE as:
> "While VideoRoPE extends RoPE to video with fixed frequency schedules, and V-CORE enforces causal constraints at the attention level, TDPE introduces **content-adaptive** position encoding that modulates frequencies based on visual content and semantic change rate, enabling finer-grained temporal reasoning for text-to-video retrieval."

### Next Steps

1. ~~Add VideoRoPE to reading_stack for detailed analysis~~ ✓ PAPER-007
2. ~~Add mechanistic RoPE paper~~ ✓ PAPER-008
3. Add V-CORE, EventFormer to reading_stack for comparison
4. Prototype ablation: TDPE vs VideoRoPE on temporal grounding benchmark
5. Focus experiments on:
   - Cross-modal phase alignment (most novel component)
   - Explicit freq-function separation (high-freq localization, low-freq semantics)
   - p-RoPE-style truncation for long video robustness
6. Mechanistic analysis: Replicate PAPER-008 analysis on video transformer to validate frequency usage patterns
