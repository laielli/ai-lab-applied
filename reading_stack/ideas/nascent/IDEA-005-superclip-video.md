# Idea: SuperCLIP for Video-Text Retrieval

- **ID**: IDEA-005
- **Stage**: nascent
- **Created**: 2026-01-17
- **Source Papers**: PAPER-003

## Spark

SuperCLIP's classification supervision improves fine-grained semantic alignment in CLIP with minimal overhead. Can we extend this to video encoders, with special emphasis on temporal tokens (verbs, temporal adverbs)?

## Focus Areas
- Cross-Modal Alignment
- Temporal Reasoning
- Efficient Video Representation

## Initial Thoughts

**Core hypothesis**: Video-text models suffer from the same fine-grained semantic limitations as CLIP. SuperCLIP's approach should transfer, and could be particularly effective for temporal understanding if we weight temporal tokens appropriately.

**Key adaptations needed**:
1. Apply classification head to video encoder output (aggregated features)
2. Consider per-frame vs. video-level classification
3. Temporal token emphasis: verbs (run, jump, before, after) could get higher weights than static attributes
4. Could use verb-specific IDF from action caption datasets

**Why this matters for video**:
- Video captions contain rich temporal language (actions, sequences, transitions)
- Standard contrastive learning on video is even more sparse than images
- Batch sizes are smaller for video (memory constraints), so batch-independence is valuable

**Evaluation targets**:
- ActivityNet Captions (temporal grounding)
- DiDeMo (temporal localization)
- Standard retrieval: MSR-VTT, VATEX

**Open questions**:
- How to balance frame-level vs. video-level classification?
- Should temporal tokens get uniform high weight, or learned weights?
- Does this help with temporal ordering understanding specifically?
