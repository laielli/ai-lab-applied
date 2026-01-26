# Experiment: YouCook2 Density Analysis

- **ID**: EXP-022
- **Created**: 2026-01-25
- **Paper**: idea-010-v-limit
- **Idea**: IDEA-010
- **Priority**: P1
- **Status**: queued

## Objective

Measure d_tripartite on YouCook2 to test whether narrow-domain datasets naturally exhibit higher density than general-purpose video datasets, which could trigger the LIMIT effect.

## Hypothesis

YouCook2, being a narrow-domain dataset (all cooking videos with recipe step descriptions), will have higher density than MSR-VTT and ActivityNet due to:
1. **Recipe-based relevance structure**: Multiple videos share the same recipe type ID (e.g., 89 recipe categories across 414 videos = ~4.6 videos per recipe on average). A query from one video is relevant to ALL videos sharing its recipe_type ID, not just the source video.
2. Visual similarity within domain (kitchens, cooking actions)
3. Lexical overlap in recipe terminology

**Key difference from MSR-VTT**: MSR-VTT has 1:1 query-video mapping (each caption describes exactly one video). YouCook2's recipe structure creates natural many-to-many relevance where queries for one video are also relevant to other videos of the same recipe.

Expected: d ~ 0.01 to 0.02 (10-20x higher than MSR-VTT d = 0.001, ActivityNet d = 0.0002)

## Method

### Setup

- **Dataset**: YouCook2 via HuggingFace (`lmms-lab/YouCook2`)
  - **Actual statistics** (verified from HuggingFace):
    - 414 unique videos across 89 recipe types
    - 4,650 total segments (val: 3,180, test: 1,470)
    - ~11 segments per video on average
  - **Split**: Use val set (3,180 segments across ~280 videos)
- **Data Access**:
  ```python
  from datasets import load_dataset
  dataset = load_dataset("lmms-lab/YouCook2")
  val_data = dataset["val"]
  # Expected fields: youtube_id, recipe_type, id (segment), sentence, start, end
  ```
- **Data Schema Verification** (run before proceeding):
  ```python
  # Verify expected fields exist
  sample = val_data[0]
  assert "youtube_id" in sample, "Need video identifier field"
  assert "recipe_type" in sample, "Need recipe grouping field"
  assert "sentence" in sample, "Need caption field"
  print(f"Videos: {len(set(val_data['youtube_id']))}")
  print(f"Recipes: {len(set(val_data['recipe_type']))}")
  print(f"Segments: {len(val_data)}")
  ```
- **Hardware**:
  - Part A: CPU only (<1 hour)
  - Part B (optional): GPU for CLIP embeddings (~2 hours)

### Relevance Rules

The key to computing d_tripartite is defining when a query-video pair is "relevant." YouCook2's recipe structure provides a natural definition:

```yaml
relevance_rules:
  # Primary rule: Recipe-based relevance
  recipe_based:
    definition: "A query is relevant to a video if they share the same recipe_type ID"
    formula: "relevant(q, v) = (recipe_type(q) == recipe_type(v))"
    note: "recipe_type is a numeric category ID (e.g., '226'), not a semantic name"
    rationale: |
      Videos within the same recipe category share similar cooking steps.
      A caption from one video is relevant to ALL videos of that recipe category.
      This creates natural cross-video relevance within recipe groups.

  # Density formula
  d_tripartite:
    formula: "d = |relevant_pairs| / (|Q| x |V|)"
    where:
      - "Q = set of all queries (segment captions)"
      - "V = set of all videos"
      - "relevant_pairs = {(q,v) : recipe_type(q) == recipe_type(v)}"

  # Expected density calculation
  expected_density:
    rationale: |
      With 89 recipes across 414 videos (~4.6 videos/recipe):
      - Each query is relevant to ~4.6 videos on average
      - d ≈ 4.6 / 414 ≈ 0.011
      This is 10x higher than MSR-VTT (0.001) but lower than Mini V-LIMIT (0.173).
      Actual density depends on recipe distribution (some recipes may have more videos).
```

### Configuration

```yaml
# Density computation settings (aligned with EXP-001)
similarity_thresholds: [0.70, 0.75, 0.80, 0.85, 0.90, 0.95]
density_metric: "tripartite"
embedding_model: "openai/clip-vit-base-patch32"
text_tokenizer: "nltk"  # for Jaccard overlap
```

### Procedure

#### Part A: Ground-Truth Density (CPU-only)

1. **Load and verify data**:
   - Load YouCook2 from HuggingFace
   - Run schema verification to confirm fields exist
   - Log actual counts: videos, recipes, segments

2. **Build relevance matrix**:
   - Group segments by youtube_id
   - Group videos by recipe_type
   - For each (query, video) pair: mark relevant if same recipe_type

3. **Compute d_tripartite**:
   ```python
   # Q = all segment captions, V = all videos
   relevant_pairs = sum(1 for q in Q for v in V
                        if recipe_type[q] == recipe_type[v])
   d_tripartite = relevant_pairs / (len(Q) * len(V))
   ```

4. **Compute density by granularity**:
   - **Video-level**: Aggregate captions per video, compute d
   - **Segment-level**: Use individual segments as queries, compute d

5. **Recipe distribution analysis**:
   - Count videos per recipe
   - Identify high-density recipes (many videos) vs low-density (few videos)
   - Report variance in per-recipe density

#### Part B: CLIP-Perceived Density (Optional, requires GPU)

1. Extract CLIP text embeddings for all captions
2. Extract CLIP video embeddings (frame sampling)
3. Compute pairwise similarities at thresholds [0.70, 0.75, 0.80, 0.85, 0.90, 0.95]
4. Compare CLIP-perceived density vs ground-truth recipe-based density

## Metrics

- **Primary**: d_tripartite (recipe-based relevance)
  - Overall density
  - Per-recipe density distribution (mean, std, min, max)
- **Secondary**:
  - Videos per recipe distribution
  - Segment-level vs video-level density comparison
  - CLIP pairwise similarity distribution (Part B only)

## Baselines

| Dataset | d_tripartite | Relevance Structure | Source |
|---------|--------------|---------------------|--------|
| MSR-VTT | 0.001 | 1:1 (each caption → one video) | EXP-001 |
| ActivityNet | 0.0002 | 1:1 (each caption → one video) | EXP-001 |

**Reference** (not direct baseline): Mini V-LIMIT achieves d=0.173 through synthetic construction (activity clustering + query templates). YouCook2's natural density is expected to be lower but still significantly higher than MSR-VTT/ActivityNet due to recipe grouping.

## Compute Budget

- **Part A**: <1 hour CPU (annotation processing, relevance matrix)
- **Part B**: ~2 GPU-hours (CLIP embedding extraction)
- **Phase**: validation (<8h total)

## Success Criteria

- **GO (significant density increase)**: YC2 d > 0.05
  - Action: Use YouCook2 as a natural dense benchmark
  - Rationale: 50x improvement over MSR-VTT indicates meaningful density
- **PARTIAL (moderate density)**: YC2 d in [0.01, 0.05]
  - Action: YouCook2 useful for analysis but may need augmentation for V-LIMIT stress test
- **NO-GO (minimal density)**: YC2 d < 0.01
  - Action: Recipe structure doesn't create sufficient density; focus on synthetic approaches

## Dependencies

- [ ] YouCook2 accessible via HuggingFace (`lmms-lab/YouCook2`)
- [ ] Schema verification passes (recipe_type field exists)
- [ ] Density computation code from exp001/metrics.py
- [ ] CLIP embedding extraction pipeline (Part B only)

## Analysis Plan

1. **Schema verification**: Confirm HuggingFace dataset structure
2. **Density computation**: d_tripartite with recipe-based relevance
3. **Recipe analysis**: Distribution of videos per recipe, density variance
4. **Comparison table**: YC2 vs MSR-VTT vs ActivityNet
5. **Decision document**: GO/PARTIAL/NO-GO based on density results

## Notes

- YouCook2's density comes from recipe-based grouping, not annotation density
- Expected density ~0.01 based on 89 recipes / 414 videos structure
- This is a fundamentally different relevance structure than MSR-VTT's 1:1 mapping
- High-density recipes (many videos) will dominate the overall density
- Part B (CLIP) deferred until Part A confirms recipe-based density is meaningful
