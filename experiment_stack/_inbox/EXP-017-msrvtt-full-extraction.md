# EXP-017: PE-Video Feature Extraction (500+ videos)

**Created**: 2026-01-25
**Revised**: 2026-01-25 (pivoted from MSR-VTT to PE-Video)
**Paper**: IDEA-009 Temporal Fourier Signatures
**Status**: READY
**Priority**: P1 - Critical for validating TOPA at scale

---

## Objective

Extract PE-Core features for 500+ PE-Video videos to enable large-scale validation of TOPA's temporal encoding benefits.

## Motivation

The current TOPA validation (EXP-014) uses only 30 test videos. The observed R@1 improvement needs validation at larger scale.

**Why PE-Video instead of MSR-VTT:**

| Issue | MSR-VTT | PE-Video |
|-------|---------|----------|
| Video availability | ~50% unavailable on YouTube | Fully available on HuggingFace |
| Test set ambiguity | Multiple splits (1k-A, 1k-B, full) | Single dataset |
| Frame sampling | Varies by paper | Standard: 8 frames |
| Model provenance | Multiple CLIP versions | Single PE-Core checkpoint |
| Caption quality | Crowd-sourced, variable | Human-refined + model captions |

## Method

1. Download PE-Video shards from HuggingFace (`facebook/PE-Video`)
2. Filter for videos with 8+ frames and human captions
3. Extract PE-Core-L14-336 features (8 frames per video)
4. Save features matching EXP-015 format for code reuse

## Technical Details

| Parameter | Value |
|-----------|-------|
| Model | PE-Core-L14-336 |
| Embedding dim | 1024 |
| Frames per video | 8 (uniform temporal sampling) |
| Sampling | Uniform across video duration |
| Dataset | PE-Video (facebook/PE-Video) |
| Target video count | 500+ |
| Caption source | `human_caption` field (fallback: `model_caption`) |

## Implementation

Reuse infrastructure from idea-003-avg-pooling:
- `src/download_pe_video.py` - Download and filter videos
- `src/pe_utils.py` - PE model utilities

```bash
# Download 500+ videos (may need multiple shards)
cd papers/idea-003-avg-pooling
python src/download_pe_video.py \
    --output_dir datasets/pe-video-500 \
    --shards 0,1,2,3,4 \
    --target_videos 500 \
    --min_frames 8

# Extract features (new script needed)
python src/extract_pe_features.py \
    --input_dir datasets/pe-video-500 \
    --output_path log/exp17/pe_video_features.pt \
    --model PE-Core-L14-336 \
    --frames_per_video 8
```

## Output

| File | Description |
|------|-------------|
| `log/exp17/pe_video_features.pt` | Video features [N, 8, 1024] |
| `log/exp17/pe_video_text_features.pt` | Caption text features [N, 1024] |
| `log/exp17/pe_video_metadata.json` | Video IDs, captions, frame counts |
| `log/exp17/extraction_log.txt` | Processing details |

## Success Criteria

| Criterion | Target |
|-----------|--------|
| Videos processed | ≥500 |
| Feature shape | [N, 8, 1024] where N ≥ 500 |
| Captions available | ≥95% of videos have captions |
| Baseline R@10 | ≥80% (PE on its own data should be strong) |

## Baseline Validation

Run mean pooling retrieval to verify features are correct:

```python
# Expected: High R@10 since PE trained on PE-Video
video_embeds = features.mean(dim=1)  # [N, 1024]
video_embeds = F.normalize(video_embeds, dim=-1)
text_embeds = F.normalize(text_features, dim=-1)
sim = video_embeds @ text_embeds.T
# Expect R@10 > 80% for diagonal matching
```

## Compute Estimate

| Stage | Time |
|-------|------|
| Download 5 shards | ~30 min (network dependent) |
| Video filtering | ~15 min |
| Feature extraction | ~1 GPU-hour (A10) |
| **Total** | ~2 hours |

## Dependencies

- [x] PE-Video on HuggingFace (`facebook/PE-Video`)
- [x] PE-Core model weights on HuggingFace
- [x] Download script from idea-003-avg-pooling
- [ ] Feature extraction script (create from pe_utils.py)

## Blockers

None - ready to execute.

## Notes

- PE-Core uses layer 23 output with projection for text-video alignment
- Features should be extracted at the standard output layer (not intermediate)
- This provides cleaner evaluation than MSR-VTT without YouTube availability issues
