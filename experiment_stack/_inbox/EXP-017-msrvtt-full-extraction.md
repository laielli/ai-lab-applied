# EXP-017: PE-Video Feature Extraction for R@1 Validation

**Created**: 2026-01-25
**Revised**: 2026-01-25 (pivoted to PE-Video, clarified purpose)
**Paper**: IDEA-009 Temporal Fourier Signatures
**Status**: READY
**Priority**: P1 - Critical for validating R@1 improvement at scale

---

## Objective

Extract PE-Core features for 500+ PE-Video videos to validate TOPA's R@1 improvement (+3.3pp) with sufficient statistical power.

## Research Question

**Does TOPA's R@1 improvement over mean pooling hold at larger scale?**

EXP-014 showed TOPA improved R@1 from 36.7% to 40.0% (+3.3pp) on 30 test videos. However:
- This represents only **1 additional correct video** (12 vs 11)
- 30 videos cannot detect effects smaller than ~15pp with 95% confidence
- 500 videos can detect ~4pp effects, sufficient to confirm or reject the R@1 finding

| Test Size | Detectable Effect (95% CI) | Status |
|-----------|---------------------------|--------|
| 30 videos | >15pp | Current (underpowered) |
| 100 videos | >8pp | Marginal |
| 500 videos | >4pp | **Target (sufficient)** |

## Why PE-Video Instead of MSR-VTT

| Issue | MSR-VTT | PE-Video |
|-------|---------|----------|
| Video availability | ~50% unavailable on YouTube | Fully available on HuggingFace |
| Test set ambiguity | Multiple splits (1k-A, 1k-B, full) | Single dataset |
| Frame sampling | Varies by paper | Standard: 8 frames |
| Model provenance | Multiple CLIP versions | Single PE-Core checkpoint |
| Caption quality | Crowd-sourced, variable | Human-refined + model captions |

**Trade-off**: We cannot directly compare to EXP-014's CLIP results, but we can test whether TOPA's temporal encoding provides benefit on a cleaner dataset with a stronger baseline model.

## Method

1. Download PE-Video shards from HuggingFace (`facebook/PE-Video`)
2. Filter for videos with 8+ frames and captions
3. Extract PE-Core-L14-336 features (8 frames per video)
4. Validate extraction quality (shapes, statistics, reconstruction)
5. Run baseline retrieval to confirm features work

## Technical Details

| Parameter | Value |
|-----------|-------|
| Model | PE-Core-L14-336 |
| Model source | `facebook/PE-Core-L14-336` on HuggingFace |
| Embedding dim | 1024 |
| Frames per video | 8 |
| Frame sampling | Uniform: `indices = linspace(0, total_frames-1, 8).round().int()` |
| Dataset | PE-Video (`facebook/PE-Video`) |
| Target video count | 500+ |

### Caption Source Priority

1. `human_caption` (preferred - 120K videos have these)
2. `model_caption` (fallback - all videos have these)

Track and report the distribution in metadata.

### Shard Strategy

PE-Video has ~1000 shards with ~1000 videos each. Conservative estimate:
- ~30-50% pass 8-frame + caption filter
- Need ~2-3 shards to get 500 videos
- Download shards 0-4 with early stopping at 500 videos

```bash
python src/download_pe_video.py \
    --output_dir datasets/pe-video-500 \
    --shards 0,1,2,3,4 \
    --target_videos 500 \
    --min_frames 8
```

## Implementation

### Step 1: Download Videos (existing script)

Reuse from idea-003-avg-pooling: `src/download_pe_video.py`

### Step 2: Extract Features (new script needed)

Create `papers/idea-009-tfs/scripts/extract_pe_features.py`:

```python
"""Extract PE-Core features from PE-Video for TOPA validation."""
import torch
from pathlib import Path
from pe_utils import load_pe_model, extract_video_features

def main():
    # Load model
    model = load_pe_model("PE-Core-L14-336")

    # Load video metadata
    metadata = json.load(open("datasets/pe-video-500/metadata.json"))

    video_features = []
    text_features = []
    valid_metadata = []

    for video in tqdm(metadata['videos']):
        # Extract 8 frames uniformly
        frames = load_video_frames(video['path'], n_frames=8)

        # Extract features [8, 1024]
        with torch.no_grad():
            v_feat = model.encode_image(frames)
            t_feat = model.encode_text(video['caption'])

        video_features.append(v_feat)
        text_features.append(t_feat)
        valid_metadata.append(video)

    # Stack and save
    torch.save({
        'video_features': torch.stack(video_features),  # [N, 8, 1024]
        'text_features': torch.stack(text_features),    # [N, 1024]
        'metadata': valid_metadata
    }, 'log/exp17/pe_video_features.pt')
```

### Step 3: Validate Extraction

Run these checks before marking complete:

```python
# 1. Shape validation
data = torch.load('log/exp17/pe_video_features.pt')
assert data['video_features'].shape == (N, 8, 1024)
assert data['text_features'].shape == (N, 1024)

# 2. Statistics validation (features should be normalized)
v_norms = data['video_features'].norm(dim=-1)
assert v_norms.mean().item() > 0.95 and v_norms.mean().item() < 1.05

# 3. No NaN/Inf
assert not torch.isnan(data['video_features']).any()
assert not torch.isinf(data['video_features']).any()

# 4. Save/load reconstruction
torch.save(data, 'tmp.pt')
data2 = torch.load('tmp.pt')
assert torch.allclose(data['video_features'], data2['video_features'])
```

### Step 4: Baseline Retrieval Validation

Confirm features work with simple retrieval:

```python
# Text-to-video retrieval with diagonal matching
# (caption[i] should retrieve video[i])
video_embeds = data['video_features'].mean(dim=1)  # [N, 1024]
video_embeds = F.normalize(video_embeds, dim=-1)
text_embeds = F.normalize(data['text_features'], dim=-1)

sim = text_embeds @ video_embeds.T  # [N, N]
ranks = (sim.argsort(dim=1, descending=True) == torch.arange(N).unsqueeze(1)).nonzero()[:, 1]

r1 = (ranks < 1).float().mean().item()
r5 = (ranks < 5).float().mean().item()
r10 = (ranks < 10).float().mean().item()

print(f"Baseline retrieval: R@1={r1:.1%}, R@5={r5:.1%}, R@10={r10:.1%}")
# Expected: R@10 > 70% (PE on its own data should be strong)
```

## Output

| File | Description |
|------|-------------|
| `log/exp17/pe_video_features.pt` | Video + text features + metadata |
| `log/exp17/extraction_stats.json` | Feature statistics, caption source distribution |
| `log/exp17/baseline_retrieval.json` | Mean pooling R@1/R@5/R@10 |

### Feature File Schema

```python
{
    'video_features': Tensor[N, 8, 1024],   # Frame features
    'text_features': Tensor[N, 1024],       # Caption features
    'metadata': [
        {
            'id': str,
            'path': str,
            'caption': str,
            'caption_source': 'human' | 'model',
            'frame_count': int,
            'duration': float
        },
        ...
    ]
}
```

## Success Criteria

| Criterion | Target | Validation |
|-----------|--------|------------|
| Videos extracted | ≥500 | `len(metadata) >= 500` |
| Feature shape | [N, 8, 1024] | Shape check |
| Features normalized | norms ∈ [0.95, 1.05] | Statistics check |
| No invalid values | No NaN/Inf | `torch.isnan().any() == False` |
| Baseline R@10 | ≥70% | Retrieval check |
| Human captions | Report % | Metadata analysis |

## Compute Estimate

| Stage | Time | Notes |
|-------|------|-------|
| Download 5 shards | ~30 min | Network dependent, ~5GB |
| Video filtering | ~15 min | CPU-bound |
| Feature extraction | ~45 min | 500 videos × 8 frames × ~0.1s/frame |
| Validation | ~5 min | CPU |
| **Total** | ~1.5 hours | + 1 GPU-hour for extraction |

## Dependencies

- [x] PE-Video on HuggingFace (`facebook/PE-Video`)
- [x] PE-Core model weights (`facebook/PE-Core-L14-336`)
- [x] Download script (`papers/idea-003-avg-pooling/src/download_pe_video.py`)
- [x] PE utilities (`papers/idea-003-avg-pooling/src/pe_utils.py`)
- [ ] Feature extraction script (create as described above)

## Blockers

None - ready to implement extraction script and execute.

## Connection to EXP-018

This experiment provides the features for EXP-018 (TOPA Scale Validation):
- EXP-017 extracts features → EXP-018 trains and evaluates TOPA
- Same features used for all methods (TOPA, Mean, TFS) in EXP-018
- Baseline retrieval here establishes the "Mean pooling" performance

## Notes

- PE-Core output layer (layer 23 + projection) is aligned with text
- TOPA theory (additive encoding preserves alignment) should apply to PE like CLIP
- If baseline R@10 < 70%, investigate before proceeding to EXP-018
