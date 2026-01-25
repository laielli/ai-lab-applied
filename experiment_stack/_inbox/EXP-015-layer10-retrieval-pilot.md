# Experiment: Intermediate Layer Retrieval Pilot (Revised)

- **ID**: EXP-015
- **Created**: 2026-01-24
- **Revised**: 2026-01-24
- **Paper**: idea-003-avg-pooling
- **Idea**: IDEA-003
- **Source**: SIM-005 (Advisor Q4), revised based on PE architecture analysis
- **Priority**: P1
- **Status**: queued

## Critical Design Insight

**Layer 10 visual features are NOT aligned with text embeddings.**

PE's contrastive training only aligns layer 23 visual ↔ layer 23 text. The `self.proj` projection head was trained specifically for layer 23 features. Naive cosine similarity between layer 10 visual and layer 23 text will produce poor results due to this alignment gap.

### PE Architecture Reality

```
PE-Core-L14-336:
├── Visual Encoder (24 layers)
│   ├── Layer 0-9: Early features (NOT aligned with text)
│   ├── Layer 10: Peak temporal signal (64.3% probe accuracy)
│   ├── Layer 11-22: Intermediate features
│   └── Layer 23 + proj: Output (ALIGNED with text via contrastive training)
│
└── Text Encoder (24 layers)
    └── Layer 23 + proj: Output (ALIGNED with visual layer 23)
```

## Objective

Test whether layer 10's temporal signal can improve retrieval, **accounting for the text alignment gap**. This requires a multi-phase approach that isolates the temporal signal question from the alignment question.

## Hypothesis

Layer 10 features retain more temporal information (64.3% vs 57.4% on temporal probe). This temporal signal may help retrieval for temporally-specific queries, but only if we properly account for the alignment gap.

## Method

### Phase A: Zero-Shot Layer 10 Retrieval (Baseline)

Apply existing projection to layer 10 features to establish lower bound.

```yaml
experiment: phase_a_zero_shot
visual_features: layer_10 + existing_proj  # Projection not trained for L10
text_features: layer_23 (standard)
retrieval: cosine_similarity
expected_outcome: Worse than layer 23 baseline (alignment gap)
success_criterion: >50% of baseline R@1 (not catastrophically worse)
```

**Purpose**: Establish how much the alignment gap hurts. If performance is reasonable, the projection may transfer across layers.

### Phase B: Hybrid Temporal Reranking

Use layer 23 for text-video matching, layer 10 for temporal reranking.

```yaml
experiment: phase_b_hybrid
stage1:
  features: layer_23
  retrieval: top-100 candidates
stage2:
  features: layer_10
  method: video-video similarity reranking
  scope: temporal queries only
evaluation:
  query_split: temporal vs non-temporal queries
  success_criterion: Temporal queries improve with layer 10 reranking
```

**Purpose**: Test if layer 10's temporal signal can help specific query types without requiring text alignment.

### Phase C: Trained Projection (Contingent)

**Only proceed if Phase A/B show promise.**

Train a small projection head to align layer 10 → text space.

```yaml
experiment: phase_c_trained_proj
training:
  freeze: PE model
  trainable: nn.Linear(1024, 1024)  # width → output_dim
  data: PE-Video subset (~10k video-caption pairs)
  loss: contrastive
  estimated_time: 2-4 GPU-hours
purpose: Upper bound on layer 10's retrieval potential
```

## Setup

- **Model**: PE-Core-L14-336
- **Dataset**: MSR-VTT 1K-A test split (standard text-video retrieval benchmark)
- **Hardware**: Single GPU
- **Frames**: 8 per video

**Why MSR-VTT instead of K400?** K400 is an action recognition dataset with class labels, not descriptive captions. MSR-VTT provides natural language descriptions suitable for text-video retrieval evaluation.

## Configuration

```yaml
model: PE-Core-L14-336
dataset: msrvtt_1ka  # Standard 1000-video test split
num_videos: 1000
frames_per_video: 8
layers:
  text_retrieval: [10, 23]  # Compare both
  video_video: 10  # For reranking
text_encoder: PE text tower (layer 23)
retrieval_stages:
  - phase_a: layer10_zero_shot
  - phase_b: hybrid_reranking
```

## Procedure

### Phase A: Zero-Shot Baseline
1. Load MSR-VTT 1K-A test split (1000 video-caption pairs)
2. Extract layer 10 embeddings for all frames, average pool
3. Apply existing `self.proj` (trained for layer 23) to layer 10 pooled features
4. Compute text embeddings (layer 23, standard)
5. Run text-to-video retrieval
6. Compare R@1, R@5, R@10 to layer 23 baseline

### Phase B: Temporal-Aware Reranking
1. Classify queries as temporal vs non-temporal using heuristics + manual validation
2. Run layer 23 retrieval to get top-100 candidates per query
3. For temporal queries, apply two reranking strategies:
   - **Strategy 1 (Coherence)**: Boost videos similar to other top candidates in L10 space
   - **Strategy 2 (Temporal Distinctiveness)**: Boost videos where L10 ranking differs most from L23
4. Compare performance on temporal vs non-temporal query subsets

**Hypothesis for Phase B**: If layer 10 captures temporal information that layer 23 loses, then:
- Videos ranked higher by L10 than L23 may be better temporal matches
- Videos with high L10 coherence may share temporal patterns with other relevant videos

## Metrics

### Primary
- **R@1, R@5, R@10**: Text-to-video retrieval
- **Median Rank**: Overall ranking quality

### Phase-Specific
- **Phase A**: Absolute R@1, ratio to layer 23 baseline
- **Phase B**: R@1 improvement on temporal queries, MRR change

### Qualitative
- Which queries improve/degrade with layer 10?
- Temporal coherence of retrieved videos

## Baselines

- **Layer 23 (standard)**: Expected ~45-50% R@1 on MSR-VTT 1K-A (typical CLIP-based methods)
- **Random**: 0.1% R@1 (1/1000 videos)

Note: The 76.9% figure previously cited was from K400 action recognition, not text-video retrieval.

## Compute Budget

- **Phase A**: ~1 GPU-hour
- **Phase B**: ~1 GPU-hour
- **Phase C** (if pursued): ~2-4 GPU-hours
- **Total (Phases A+B)**: ~2 GPU-hours

## Success Criteria (Decision Matrix)

| Phase A | Phase B | Interpretation | Next Step |
|---------|---------|----------------|-----------|
| <30% of baseline | No temporal gain | Layer 10 not useful | Analysis paper only |
| <30% of baseline | Temporal queries improve | Hybrid approach viable | Develop temporal reranking method |
| >50% of baseline | Any | Projection may transfer | Proceed to Phase C |
| >70% of baseline | Temporal gains | Strong signal | Layer 10 is viable for retrieval |

### Go Decision (proceed with temporal alignment)
- Phase A: Layer 10 retains >50% of layer 23 R@1
- OR Phase B: Layer 10 reranking improves temporal queries by >2 points

### No-Go Decision (write analysis paper only)
- Phase A: Layer 10 <30% of layer 23 performance
- AND Phase B: No improvement on temporal queries

## Dependencies

- [x] Layer probing shows layer 10 has more temporal info (64.3%)
- [x] PE architecture analysis confirming alignment constraints
- [ ] MSR-VTT dataset downloaded (videos + captions)
- [x] PE feature extraction code ready (PELayerExtractor)
- [x] Text-video retrieval pipeline implemented
- [ ] Temporal query annotation/classification (heuristic + manual validation)

## Implementation

Code: `papers/idea-003-avg-pooling/src/layer10_retrieval.py`

Key classes:
- `Layer10Retriever`: Implements all three phases
- `TemporalQueryClassifier`: Heuristic classification of temporal queries
- `HybridReranker`: Layer 10-based video-video reranking

## Key Insight

The original EXP-015 design would have produced misleading negative results due to the alignment gap, not because layer 10 lacks temporal value. This revised design properly isolates the temporal signal question from the alignment question.
