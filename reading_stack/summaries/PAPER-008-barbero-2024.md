# Summary: Round and Round We Go! What makes Rotary Positional Encodings useful?

- **Paper ID**: PAPER-008
- **arXiv**: 2410.06205
- **Authors**: Federico Barbero, Alex Vitvitskyi, Christos Perivolaropoulos, Razvan Pascanu, Petar Velickovic
- **Year**: 2024
- **Summarized**: 2026-01-21

## Focus Area Tags
- Mechanistic DL Theory
- Feature Learning

## One-Line Summary

Through mechanistic analysis of Gemma 7B, this paper reveals that RoPE's effectiveness stems not from token dependency decay (as commonly believed), but from a frequency-based division of labor: high frequencies enable robust positional attention patterns while low frequencies carry semantic information, with mathematical proofs demonstrating that the conventional decay narrative is fundamentally flawed.

## Key Contributions

1. **Mechanistic Analysis of RoPE Usage**: Empirical investigation of how Gemma 7B actually uses RoPE frequencies, revealing that the model exploits highest frequencies for positional attention patterns (diagonal and previous-token heads) while preferentially using lowest frequencies for semantic information.

2. **Refutation of Decay Narrative**: Mathematical proofs demonstrating that the conventional explanation for RoPE (encouraging attention decay with distance) is incorrect:
   - Proposition 3.1: For any query and distance r, there exists a key making RoPE attention maximal at exactly that distance
   - Proposition 3.2: For Gaussian-distributed queries/keys, expected attention is zero regardless of distance (no decay)

3. **Theoretical Framework for Positional vs Semantic Channels**: Formal proofs showing:
   - NoPE cannot learn robust positional attention patterns (Proposition 5.2)
   - RoPE can learn positional patterns via high-frequency components (Theorem 5.3)
   - Low-frequency semantic channels are non-robust over long contexts (Theorem 6.1)

4. **p-RoPE Modification**: Proposes truncating the lowest p fraction of RoPE frequencies, removing non-robust semantic channels while preserving positional information. Achieves improved or matched performance at 8k context length.

## Methodology

### Empirical Analysis Setup

- **Model**: Gemma 7B (28 layers, 16 attention heads, 256 hidden dimension)
- **Validation**: Replicated findings on Llama 3.1 8B
- **Analysis**: Examined query/key norms across frequency bands, identified specific attention heads with distinct usage patterns

### RoPE Formulation

RoPE decomposes query and key vectors into d/2 2D chunks, applying position-dependent rotations:

```
kRoPE(q_i, k_j) = sum_k (q_i^(k))^T * rho(g_k)^(j-i) * k_j^(k)
```

Where:
- `g_k = theta^(-2(k-1)/d)` defines rotation frequencies (theta=10,000 by default)
- Highest frequencies (g_1 ~ 1 rad/token) are most position-sensitive
- Lowest frequencies (g_{d/2} ~ 1/10,000 rad/token) are most position-invariant

### Key Observations

**High-Frequency Behavior (Positional)**:
- Heads 5 and 8 in layer 1 exclusively use highest frequencies
- These exhibit pure positional attention patterns:
  - Diagonal heads: attend to position i when querying position i
  - Previous-token heads: attend to position i-1 when querying position i
- High-frequency usage concentrated in first and last layers

**Low-Frequency Behavior (Semantic)**:
- Low frequencies show consistently high norms across most layers
- Enable semantic matching that is approximately position-invariant
- Example: "apostrophe detection head" combining semantic selectivity with positional constraints

**Banding Patterns**:
- Distinct high-norm "bands" in query/key representations at specific frequencies
- Suggests specialized channels for different types of information

## Mathematical Proofs

### Proposition 3.1: RoPE Maximal at Arbitrary Distance

**Statement**: Given any query q and relative distance r, there exists a key k such that RoPE attention is maximal at distance r.

**Proof Strategy**: Construct k^(k) = rho(g_k)^r * psi^(k), then the maximum occurs at j-i = -r using the irrational rotation property (Lemma A.1 - almost all g_k are rationally independent).

**Implication**: Contradicts the claim that RoPE inherently causes attention to decay with distance.

### Proposition 3.2: No Decay for Gaussian Queries/Keys

**Statement**: For Gaussian-distributed queries and keys, E[q^T R^r k] = 0 regardless of relative distance r.

**Proof**: Exploits orthogonality of rotation matrices and Gaussian isotropic properties. Since rho(g_k) is orthogonal, rotated Gaussians remain Gaussian with zero mean.

**Implication**: Under realistic random initialization assumptions, there is no expected decay pattern.

### Proposition 5.2: NoPE Cannot Learn Positional Patterns

**Statement**: No attention head without position encoding can robustly learn diagonal attention (attending to current position).

**Proof**: By counterexample with repeated token sequence [BOS, x_1, x_1]. For position 3, attention alpha_{3,3} = 1/(exp(a_{3,1}-a_{3,3})+2) < 1/2, violating the requirement alpha_{3,3} > 1-epsilon.

### Theorem 5.3: RoPE Can Learn Positional Patterns

**Statement**: RoPE-equipped attention can learn to attend exclusively to relative position 0 (diagonal pattern).

**Construction**: Set q_i = k_j = psi (equal queries/keys). The activation becomes:

```
q^T R^(j-i) k = sum_k ||psi^(k)||^2 * cos((j-i) * g_k)
```

This maximizes only when j-i = 0 by Lemma A.1's irrational rotation property.

### Theorem 6.1: Semantic Channels Non-Robust Over Long Context

**Statement**: For d=2 (single frequency), no attention head using RoPE can robustly attend to a fixed semantic token across arbitrary sequence lengths.

**Proof Intuition**: Irrational rotations become "dense" over sufficiently long sequences, meaning any phase configuration can be approximated. This makes semantic-based attention unreliable.

**Implication**: Low-frequency channels that models rely upon for semantic matching become misaligned over long contexts, explaining why increasing theta (base frequency) helps with long context.

## Key Results

### Validation Perplexity on Gemma 2B (8k context)

| Encoding | Wikipedia | FlanV2 |
|----------|-----------|--------|
| NoPE | 4.859 | 6.643 |
| RoPE (theta=10k) | 4.463 | 6.443 |
| RoPE (theta=500k) | 4.449 | 6.459 |
| **0.75-RoPE** | **4.441** | **6.442** |

Optimal truncation (removing 25% of lowest frequencies) matches or exceeds standard RoPE.

### Ablation Studies

| Variant | Wikipedia | FlanV2 | Notes |
|---------|-----------|--------|-------|
| 0.75-RoPE | 4.441 | 6.442 | Optimal |
| 0.75-RoPE_reversed | 4.459 | 6.468 | Removing highest instead of lowest |
| RoPE_partial | Degraded | Degraded | Incomplete frequency removal |
| 0.25-RoPE | 4.530 | 6.511 | Too aggressive truncation |

Removing low frequencies (semantic channels) is better than removing high frequencies (positional channels).

### Theoretical Properties Summary

| Property | NoPE | RoPE | p-RoPE |
|----------|------|------|--------|
| Positional patterns | No | Yes | Yes |
| Robust semantic channels | Yes | No | Yes |

p-RoPE combines the best of both: positional capability from RoPE, semantic robustness from NoPE.

## Answers to First-pass Questions

### 1. How does the frequency-based usage pattern in RoPE relate to temporal encoding in video transformers?

The finding that high frequencies enable positional attention while low frequencies carry semantic information has direct implications for video temporal encoding:

- **High-frequency allocation for temporal localization**: Just as Gemma uses highest frequencies for "previous token" and "diagonal" attention, video models could use high-frequency RoPE dimensions for precise frame-level temporal attention
- **Low-frequency allocation for semantic similarity**: Low frequencies being more position-invariant suggests they should handle semantic content matching across frames
- **VideoRoPE alignment**: This paper provides mechanistic justification for VideoRoPE's low-frequency temporal allocation (PAPER-007), explaining WHY putting temporal on low frequencies works - it allows long-range temporal dependencies without the "hash collision" problem that high frequencies cause

### 2. Could the proposed RoPE modifications improve temporal reasoning capabilities in video-text retrieval models?

Yes, through several mechanisms:

- **p-RoPE for long video**: Truncating lowest frequencies (which become non-robust at long context) could improve long video understanding by preventing semantic channel misalignment
- **Frequency schedule design**: Understanding that frequencies serve different purposes (positional vs semantic) enables principled design of video-specific frequency schedules
- **Content-adaptive potential**: The finding that different heads use frequencies differently suggests content-adaptive frequency allocation (as proposed in IDEA-008) could further improve temporal reasoning

### 3. What are the mathematical proofs regarding RoPE behavior and how do they generalize beyond Gemma?

The proofs are architecture-agnostic and apply to any RoPE-equipped transformer:

- Propositions 3.1 and 3.2 depend only on rotation matrix properties
- The irrational rotation Lemma A.1 applies to standard RoPE frequency schedules
- Theorems 5.3 and 6.1 require only that frequencies are rationally independent (true for theta=10,000 schedule)

The authors validated empirical findings on Llama 3.1 8B, suggesting generalization.

### 4. How does the finding that "token dependency decay" is not the core reason for RoPE's effectiveness change our understanding of positional encodings?

This is a paradigm shift:

- **Old narrative**: RoPE works by making attention decay with distance, encouraging local attention
- **New understanding**: RoPE works by providing a mechanism for learning BOTH positional patterns (via high frequencies) AND semantic patterns (via low frequencies), with the decay being an artifact of specific learned behaviors, not an inherent property

This suggests:
- Position encodings should be evaluated on their capacity to support diverse attention patterns, not on assumed decay properties
- Long-context scaling issues stem from low-frequency semantic channel misalignment, not insufficient decay
- Hybrid approaches (like p-RoPE) can preserve positional capability while fixing semantic robustness

### 5. Are there implications for long-context modeling in video understanding?

Significant implications:

- **Root cause identified**: Long-context degradation comes from low-frequency semantic channels becoming unreliable (Theorem 6.1), not from decay properties
- **Fix mechanism**: Either increase theta (current practice) or truncate low frequencies (p-RoPE) to prevent semantic misalignment
- **Video-specific insight**: Videos have inherently longer context (thousands of frame tokens). The semantic channel non-robustness is particularly relevant for video-language models
- **Design principle**: For very long videos, consider allocating temporal dimensions to mid-range frequencies that are both position-discriminative and robust over context length

## Relevance to Lab Vision

### Direct Alignment with Lab Priorities

**Mechanistic Understanding for Temporal Reasoning**:
This paper exemplifies the lab's value of understanding WHY methods work. The mechanistic analysis of RoPE provides actionable insights for designing temporal position encodings in video-text retrieval:

1. **Temporal Reasoning**: The frequency-function separation (positional vs semantic) directly informs how to encode temporal relationships in video. High frequencies for precise frame localization, low frequencies for semantic similarity across time.

2. **Efficient Video Representation**: The finding that p-RoPE can match or exceed standard RoPE while being more robust suggests efficiency gains are possible in video transformers.

3. **Foundation Model Insight**: Since modern video-language models build on LLMs that use RoPE (LLaMA, Mistral), this mechanistic understanding is essential for proper video adaptation.

### Strategic Value

- **Temporal reasoning as differentiator**: This paper provides the theoretical grounding to design better temporal position encodings that capture structure, not just proximity
- **Build on foundation models**: Understanding RoPE's actual mechanics enables principled modification for video without breaking what works for text

## Potential Connections

### Connection to PAPER-005 (RoFormer/RoPE)

PAPER-005 introduced RoPE with the claim that it encourages "decaying inter-token dependency with increasing relative distance." PAPER-008 directly refutes this:

- The decay claim relied on assumptions about constant query/key vectors
- Under realistic conditions (learned, data-dependent Q/K), there is no inherent decay
- The actual mechanism is frequency-based function separation, not decay

This reframes RoPE's contribution: it provides a mechanism for learning diverse attention patterns, not a locality bias.

### Connection to PAPER-007 (VideoRoPE)

PAPER-008 provides mechanistic justification for VideoRoPE's design choices:

| VideoRoPE Design | PAPER-008 Explanation |
|------------------|----------------------|
| Low-frequency temporal allocation | High frequencies cause positional patterns; low frequencies avoid "hash collisions" at long temporal spans |
| Diagonal layout | Maintains access to high-frequency positional channels for spatial relationships |
| Adjustable temporal spacing | Controls how quickly temporal positions "rotate through" frequency channels |

Gap: VideoRoPE uses fixed frequency allocation. PAPER-008's finding that different heads use frequencies differently suggests content-adaptive allocation could improve further.

### Connection to IDEA-008 (TDPE)

PAPER-008 strengthens the case for IDEA-008:

**Validation of content-adaptive hypothesis**:
- Finding: Different heads learn to use different frequencies for different purposes
- TDPE implication: Content-adaptive frequencies (action frames use higher frequencies) extends this learned behavior to explicit design

**Semantic change encoding support**:
- Finding: Low frequencies carry semantic information
- TDPE implication: Modulating effective position based on semantic change rate could better align with how models use low-frequency channels

**Cross-modal alignment insight**:
- Finding: Position encoding supports both positional and semantic functions
- TDPE implication: Text temporal words could map to phase offsets that align with how video positions are encoded

**New gap identified**:
- p-RoPE truncates low frequencies to improve robustness
- TDPE could instead make low frequencies content-adaptive, preserving their semantic function while improving robustness

### Gap This Reveals

The paper focuses on language models. The video extension remains unexplored:

1. **Video-specific frequency analysis**: How do video transformers use RoPE frequencies? Do they show the same positional/semantic split?
2. **Temporal vs spatial frequencies**: Should temporal and spatial dimensions use different frequency bands?
3. **Cross-modal frequency alignment**: How do text tokens and video tokens interact across frequency channels?

## Ideas Sparked

- **Mechanistic analysis of video RoPE**: Replicate this analysis on video transformers (Qwen2-VL, InternVideo) to understand how they use frequencies across spatial and temporal dimensions

- **Frequency-aware temporal encoding**: Design temporal position encoding that explicitly separates high-frequency (frame localization) and low-frequency (temporal semantics) functions, with content-adaptive modulation in between

- **p-RoPE for long video**: Apply low-frequency truncation specifically to video temporal dimensions to improve long video understanding

- **Benchmark for temporal position encoding**: Create an evaluation protocol that separately measures positional pattern capability (like V-NIAH) and semantic matching capability (like V-NIAH-D) to validate frequency-based design choices

## Technical Notes

### Key Mathematical Insight

The irrational rotation property (Lemma A.1) is crucial: because RoPE frequencies (g_k = theta^(-2(k-1)/d)) are almost always rationally independent, the vector of rotations (g_1 * r, g_2 * r, ...) becomes dense in the torus as r increases. This means:

- For any desired phase configuration, there exists a distance r that achieves it
- Low-frequency rotations are particularly prone to arbitrary phase values at long context
- This explains both RoPE's flexibility and its long-context failure modes

### Implementation Note: p-RoPE

```python
def p_rope(q, k, positions, p=0.75, dim=128, base=10000):
    """Apply p-RoPE, keeping only top p fraction of frequencies."""
    # Number of frequency pairs to keep
    n_keep = int(p * dim // 2)

    # Compute frequencies (only for kept dimensions)
    inv_freq = 1.0 / (base ** (torch.arange(0, dim, 2)[:n_keep] / dim))

    # Apply rotations only to first 2*n_keep dimensions
    angles = positions[:, None] * inv_freq[None, :]
    cos_angles, sin_angles = torch.cos(angles), torch.sin(angles)

    # Rotate Q/K in kept dimensions, leave rest unrotated
    # (unrotated dimensions act like NoPE - semantic only)
    ...
```

Key insight: Unrotated dimensions behave like NoPE (content-only matching), while rotated dimensions provide positional capability.

## Citation

```bibtex
@article{barbero2024round,
  title={Round and Round We Go! What makes Rotary Positional Encodings useful?},
  author={Barbero, Federico and Vitvitskyi, Alex and Perivolaropoulos, Christos and Pascanu, Razvan and Veli{\v{c}}kovi{\'c}, Petar},
  journal={arXiv preprint arXiv:2410.06205},
  year={2024}
}
```
