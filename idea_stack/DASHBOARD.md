# Idea Dashboard

*Last updated: 2026-01-23*

## Summary

| Stage | Count | Avg Novelty | Avg Impact | High Scoop Risk |
|-------|-------|-------------|------------|-----------------|
| ready | 0 | - | - | 0 |
| developing | 5 | 3.6 | 3.6 | 2 |
| _inbox | 7 | 2.9 | 2.9 | 1 |

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

| ID | Title | Novelty | Impact | Scoop | Status | Next Step |
|----|-------|---------|--------|-------|--------|-----------|
| IDEA-003 | Average Pooling Mystery | 3 | 4 | 2 | Active investigation | Run Exp 1.2-1.4, test H5 intermediate layer probing |
| IDEA-004 | TinyVid Benchmark | 4 | 4 | 2 | Phase 3 complete | Scale to 10K clips, test PE transfer validation |
| IDEA-006 | SuperCLIP Distillation | 3 | 3 | 3 | **Launched** | See papers/idea-006-superclip-distillation/ |
| IDEA-007 | LLM2CLIP for Video | 4 | 4 | **4** | **Launched** | See papers/idea-007-llm2clip-video/ |
| IDEA-009 | Temporal Fourier Signatures | 4 | 3 | 3 | **Launched**, 5/7 claims validated | Real-world experiments on MSR-VTT/VATEX |

### Inbox

*New ideas pending initial evaluation*

| ID | Title | Novelty | Impact | Scoop | Promote? | Notes |
|----|-------|---------|--------|-------|----------|-------|
| IDEA-008 | Temporal Dynamics Position Encoding | 4 | 4 | **4** | **Yes - near ready** | Extensive lit review, 5 components designed |
| IDEA-010 | V-LIMIT Benchmark | 4 | 4 | 2 | **Yes** | Novel theory-driven benchmark |
| IDEA-012 | Temporal Module on PE-Core | 2 | 3 | 3 | Maybe | Straightforward extension |
| IDEA-013 | Reverse Reward Contrastive | 3 | 3 | 3 | **Yes** | Novel training signal from ArrowRL |
| IDEA-014 | Temporal Caption CC Fine-tuning | 3 | 3 | 3 | Merge | Overlaps with IDEA-007 |
| IDEA-015 | Adaptive Retrieval Routing | 3 | 2 | 2 | Maybe | Systems contribution |
| IDEA-016 | Learned Sparse Video Representations | 3 | 3 | 2 | **Yes** | SPLADE for video, novel angle |

## Stage Readiness Assessment

### Inbox to Developing

| ID | Research Question | Approach | Experiment Plan | Ready? |
|----|------------------|----------|-----------------|--------|
| IDEA-008 | Can we design position encoding for video temporal features? | Extend RoPE with content-adaptive frequencies | Ablation vs VideoRoPE | **Yes** |
| IDEA-010 | Do embedding capacity limits affect video retrieval? | Create LIMIT-style benchmark | Compute d_tripartite, test SOTA | **Yes** |
| IDEA-012 | Can lightweight temporal module improve PE? | Add temporal layers on frozen PE | Compare vs full video encoders | Yes |
| IDEA-013 | Can reverse video rewards improve retrieval? | Adapt ArrowRL for contrastive training | Train on TDS-filtered pairs | **Yes** |
| IDEA-014 | Can temporal caption pairs improve CC fine-tuning? | Create temporal hard negatives | Apply supervised SimCSE | Merge with IDEA-007 |
| IDEA-015 | Can query complexity predict retrieval failure? | Route queries by complexity | Learn routing policy | Needs refinement |
| IDEA-016 | Can sparse representations overcome capacity limits? | Learn video concept vocabulary | Train sparse encoder | **Yes** |

### Developing to Ready

| ID | Testable Hypothesis | Novelty Argument | Validation Status | Ready? |
|----|---------------------|------------------|-------------------|--------|
| IDEA-003 | Implicit temporal encoding explains avg pooling SOTA | Understanding surprising empirical result | H3 refuted, H2/H5 primary | Blocked - need Exp 1.2-1.4 |
| IDEA-004 | TinyVid findings transfer to K400 | CIFAR for video retrieval | Phase 3 complete (53% R@1) | Blocked - need PE transfer test |
| IDEA-006 | Classification distillation beats embedding | First for video-text | Infrastructure ready | Blocked - awaiting experiments |
| IDEA-007 | LLM temporal knowledge improves video retrieval | First CC-LLM for video | Infrastructure ready | Blocked - awaiting experiments |
| IDEA-009 | Rotation preserves order in summation | Summable order-preserving encoding | 5/7 claims validated | **Near ready** - need real-world |

## Recommendations

### Priority Actions

1. **Promote IDEA-008 to developing** - Most complete inbox idea, extensive lit review, clear novelty (content-adaptive frequencies + cross-modal phase). High scoop risk demands acceleration.

2. **Promote IDEA-010 to developing** - Strong theoretical grounding from PAPER-009, unique benchmark contribution, low scoop risk allows deliberate development.

3. **Promote IDEA-013 to developing** - Novel training signal, clear experiment plan, testable hypothesis.

4. **Promote IDEA-016 to developing** - Applies established sparse retrieval to video, clear novelty angle.

5. **Merge IDEA-014 into IDEA-007** - Temporal CC fine-tuning is a natural extension of LLM2CLIP work.

### Ideas to Watch

| ID | Reason | Action |
|----|--------|--------|
| IDEA-003/004 | Paired investigation, TinyVid enables fast IDEA-003 iteration | Continue parallel development |
| IDEA-009 | Dynamics claim failed but core contribution validated | Pivot paper focus |

## Scoop Watch

*Ideas with scoop risk >= 4 requiring acceleration*

| ID | Title | Risk Level | Threat | Mitigation |
|----|-------|------------|--------|------------|
| IDEA-007 | LLM2CLIP for Video | **4** | Microsoft/LLM2CLIP authors may extend | Fast validation (<7 GPU-hrs), pre-register |
| IDEA-008 | Temporal Dynamics PE | **4** | VideoRoPE, VRoPE active development | Focus unique angle: content-adaptive + cross-modal |

---

*Updated via `/dashboard` skill on 2026-01-23*
