# Idea Dashboard

*Last updated: 2026-01-23*

## Summary

| Stage | Count | Avg Novelty | Avg Impact | High Scoop Risk |
|-------|-------|-------------|------------|-----------------|
| ready | 0 | - | - | 0 |
| developing | 6 | 3.5 | 3.3 | 2 |
| _inbox | 8 | 2.9 | 3.0 | 1 |

## Evaluation Criteria

| Score | Novelty | Impact | Scoop Risk |
|-------|---------|--------|------------|
| 5 | Fundamentally new approach | Could shift research direction | Hot topic, high risk |
| 4 | Novel technique | Strong contribution | Active competition |
| 3 | New combination of ideas | Notable contribution | Moderate risk |
| 2 | Meaningful extension | Useful improvement | Some activity |
| 1 | Incremental improvement | Minor benchmark gain | Low competition |

## Ideas by Stage

### Ready

*Ideas ready to launch as paper projects*

| ID | Title | Novelty | Impact | Scoop | Notes |
|----|-------|---------|--------|-------|-------|
| - | - | - | - | - | No ready ideas |

### Developing

*Ideas with testable hypotheses being refined*

| ID | Title | Novelty | Impact | Scoop | Next Step |
|----|-------|---------|--------|-------|-----------|
| IDEA-003 | Average Pooling Mystery | 3 | 4 | 2 | Run PE on TinyVid for transfer validation |
| IDEA-004 | TinyVid Benchmark | 4 | 4 | 2 | Scale to 10K clips, test PE transfer |
| IDEA-006 | SuperCLIP Distillation | 3 | 3 | 3 | Run validation experiments on Flickr30K |
| IDEA-007 | LLM2CLIP for Video | 4 | 4 | 4 | Cache LLM features, run baseline on PVD |
| IDEA-009 | Temporal Fourier Signatures | 4 | 3 | 3 | Real-world experiments on MSR-VTT/VATEX |
| IDEA-008 | Temporal Dynamics Position Encoding | 4 | 4 | 4 | Prototype ablation vs VideoRoPE |

### Inbox

*New ideas pending initial evaluation*

| ID | Title | Novelty | Impact | Scoop | Promote? |
|----|-------|---------|--------|-------|----------|
| IDEA-005 | SuperCLIP for Video | 2 | 3 | 2 | Yes - has clear direction, merge with IDEA-006 |
| IDEA-010 | V-LIMIT Benchmark | 4 | 4 | 2 | Yes - novel benchmark idea, compute d_tripartite |
| IDEA-011 | Intermediate Layer Probing | 3 | 3 | 2 | Yes - clear hypothesis, pairs with IDEA-003 |
| IDEA-012 | Temporal Module on PE-Core | 2 | 3 | 3 | Yes - straightforward extension, low novelty |
| IDEA-013 | Reverse Reward Contrastive | 3 | 3 | 3 | Yes - novel training signal, testable |
| IDEA-014 | Temporal Caption CC Fine-tuning | 3 | 3 | 3 | Maybe - overlaps with IDEA-007 |
| IDEA-015 | Adaptive Retrieval Routing | 3 | 2 | 2 | Maybe - systems contribution, lower novelty |
| IDEA-016 | Learned Sparse Video Representations | 3 | 3 | 2 | Yes - novel angle (SPLADE for video) |

## Recommendations

### Priority Actions

1. **Promote IDEA-010 (V-LIMIT)** - Strong novelty, theoretical grounding, unique benchmark contribution
2. **Promote IDEA-011** - Pairs well with IDEA-003, quick validation possible with probing methodology
3. **Merge IDEA-005 into IDEA-006** - SuperCLIP video application is subset of distillation idea
4. **Merge IDEA-014 into IDEA-007** - Temporal CC fine-tuning is variation of LLM2CLIP approach
5. **Promote IDEA-008 to ready** - Most developed, has full lit review, complements launched TFS paper

### Stage Readiness Assessment

**Inbox to Developing:**
- IDEA-010: Ready to promote - clear research question, validated against lit, testable
- IDEA-011: Ready to promote - clear hypothesis, experiment methodology from PE paper
- IDEA-013: Ready to promote - novel training signal, clear experiment plan
- IDEA-016: Ready to promote - applies established idea (sparse retrieval) to new domain

**Developing to Ready:**
- IDEA-008: Near ready - extensive lit review completed, needs experiment plan finalization
- IDEA-009: Blocked - partial validation only (5/7 claims), needs real-world experiments
- IDEA-003/004: In progress - TinyVid experiments running, need transfer validation

## Scoop Watch

*Ideas with scoop risk >=4 requiring acceleration*

| ID | Title | Risk Level | Threat | Mitigation |
|----|-------|------------|--------|------------|
| IDEA-007 | LLM2CLIP for Video | 4 | LLM2CLIP authors or others may extend to video | Fast validation (<7 GPU-hours), leverage cached features |
| IDEA-008 | Temporal Dynamics PE | 4 | VideoRoPE (Feb 2025), VRoPE active development | Focus on unique angle: content-adaptive + cross-modal phase |

---

*Updated via `/dashboard` skill on 2026-01-23*
