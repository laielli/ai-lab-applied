# Paper: Positional Encoding Methods in Video-Text Retrieval

- **ID**: PAPER-013
- **Added**: 2026-01-25
- **Source**: SIM-006 (Advisor Q3 - Literature survey)
- **Status**: unread

## Why Read

We need to understand the competitive landscape for positional/temporal encoding in video-text retrieval. Specifically:

1. Have others tried additive positional signals on frozen CLIP features?
2. What positional encoding schemes are used in video-text transformers?
3. Are there published negative results about temporal encoding not helping?
4. What is state-of-the-art for temporal reasoning in video retrieval?

This survey will inform whether IDEA-009/TOPA is exploring novel territory or retreading failed approaches.

## Search Strategy

### Keywords to search

- "positional encoding" + "video retrieval"
- "temporal encoding" + "text-video"
- "frame position" + "CLIP"
- "temporal pooling" + "retrieval"

### Venues to prioritize

- CVPR, ICCV, ECCV (2022-2025)
- NeurIPS, ICML (2022-2025)
- ACL, EMNLP (2022-2025) for multimodal work

### Papers to definitely include

- TimeSformer and variants (temporal attention)
- CLIP4Clip, TS2Net (video-text retrieval methods)
- Any papers citing CLIP for video that discuss pooling strategies

## Focus Areas

- [x] Temporal Reasoning
- [x] Cross-Modal Alignment
- [ ] Efficient Video Representation
- [ ] Benchmark and Evaluation

## Questions to Answer

1. Does anyone use additive positional encoding on frozen features (vs learned)?
2. What temporal modeling approaches have been tried and failed to beat mean pooling?
3. Are there benchmarks specifically designed to require temporal reasoning for retrieval?
4. What gap would a TOPA-style approach fill in the literature?
