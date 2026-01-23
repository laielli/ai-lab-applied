# Idea Stack

A 3-stage pipeline for developing research ideas from initial sparks to paper-ready proposals.

## Purpose

- **_inbox/**: Raw ideas extracted from paper summaries or captured spontaneously
- **developing/**: Ideas being actively refined with hypotheses and experiment plans
- **ready/**: Fully developed ideas ready to launch as paper projects

## Directory Structure

```
idea_stack/
├── _inbox/          # Raw ideas waiting for initial evaluation
├── developing/      # Ideas being refined and validated
└── ready/           # Ideas ready to become paper projects
```

## Workflow

```
Paper summary "Ideas Sparked" → _inbox/IDEA-XXX.md
         ↓
Evaluate & refine → developing/IDEA-XXX.md
         ↓
Complete criteria → ready/IDEA-XXX.md
         ↓
Launch paper → papers/<paper-name>/
```

---

## Entry Formats

### Stage 1: _inbox/

Raw ideas extracted from papers or captured spontaneously. Minimal structure required.

Filename: `IDEA-XXX-[working-title].md`

```markdown
# Idea: [Working Title]

- **ID**: IDEA-XXX
- **Stage**: inbox
- **Created**: YYYY-MM-DD
- **Source**: PAPER-XXX (or "spontaneous")

## Spark

[What's the core insight, observation, or question?]

## Initial Thoughts

[Rough notes, can be messy. Why might this be interesting?]

## Relevance to Lab Vision

[Brief note on connection to text-to-video retrieval focus areas]
```

### Stage 2: developing/

Ideas being actively refined with clear research direction.

Filename: `IDEA-XXX-[working-title].md`

```markdown
# Idea: [Working Title]

- **ID**: IDEA-XXX
- **Stage**: developing
- **Created**: YYYY-MM-DD
- **Promoted**: YYYY-MM-DD
- **Source**: PAPER-XXX, PAPER-YYY

## Research Question

[Clear articulation of the specific question this research addresses]

## Hypothesis

[Testable prediction with expected outcome]

## Why Novel

[How this differs from existing work; what gap it fills]

## Lab Vision Alignment

[Which focus areas: Temporal Reasoning, Cross-Modal Alignment, Efficient Video Representation, Benchmark/Evaluation]

## Potential Experiments

1. [Experiment 1: description]
2. [Experiment 2: description]
3. ...

## Compute Estimate

- Validation phase: ~X GPU-hours
- Full experiment: ~Y GPU-hours

## Open Questions

- [ ] Question 1
- [ ] Question 2

## Literature Check

- [ ] Searched for recent related work
- [ ] Not scooped by existing papers
- [ ] Identified key baselines

## Promotion Checklist

- [ ] Clear research question
- [ ] Testable hypothesis
- [ ] Novelty argument validated
- [ ] Viable experiment plan (<8 GPU-hours for validation)
- [ ] Aligns with lab vision priorities
```

### Stage 3: ready/

Fully developed ideas ready to launch as paper projects.

Filename: `IDEA-XXX-[working-title].md`

```markdown
# Idea: [Working Title]

- **ID**: IDEA-XXX
- **Stage**: ready
- **Created**: YYYY-MM-DD
- **Promoted**: YYYY-MM-DD
- **Ready**: YYYY-MM-DD
- **Source**: PAPER-XXX, PAPER-YYY

## Research Question

[Finalized, specific research question]

## Hypothesis

[Testable prediction with clear success criteria]

## Why Novel

[Validated novelty argument with literature support]

## Lab Vision Alignment

[Focus areas and strategic priority fit]

## Proposed Experiments

### Validation Experiment (Phase 1)

- **Goal**: [What this proves]
- **Method**: [Brief methodology]
- **Compute**: <8 GPU-hours
- **Success criteria**: [Specific metrics]

### Ablation Studies (Phase 2)

- [Ablation 1]
- [Ablation 2]

### Full Experiment (Phase 3)

- **Datasets**: [MSR-VTT, DiDeMo, etc.]
- **Baselines**: [Methods to compare against]
- **Metrics**: [R@1, R@5, R@10, MedR, etc.]

## Target Venue

- **Conference**: [CVPR/ICCV/NeurIPS/ACL/EMNLP]
- **Deadline**: YYYY-MM-DD
- **Decision date**: YYYY-MM-DD

## Paper Outline

1. Introduction
2. Related Work
3. Method
4. Experiments
5. Conclusion

## Risk Assessment

- **Technical risks**: [What could go wrong]
- **Mitigations**: [How to address]

## Next Step

Launch paper project with `/launch-paper IDEA-XXX`
```

---

## Promotion Criteria

### _inbox → developing

Criteria for promoting an idea from inbox to developing stage:

1. **Clear research question**: Not just "interesting observation" but a specific question to answer
2. **Lab vision alignment**: Connects to at least one focus area (temporal reasoning, cross-modal alignment, efficient representation, benchmarking)
3. **Not scooped**: Quick literature check confirms the idea hasn't been done
4. **Novelty potential**: Differs meaningfully from existing work

### developing → ready

All boxes must be checked:

- [ ] Clear, specific research question that can be answered experimentally
- [ ] Testable hypothesis with predicted outcome and success criteria
- [ ] Novelty argument validated against recent literature
- [ ] Viable experiment plan following single-GPU scaling methodology
- [ ] Validation experiment can be run in <8 GPU-hours
- [ ] Aligns with lab vision strategic priorities
- [ ] Target venue and deadline identified

### ready → paper launch

When an idea is ready, use `/launch-paper IDEA-XXX` to:

1. Create paper directory in `papers/`
2. Initialize paper requirements from idea content
3. Set up experiment infrastructure
4. Mark idea as "launched" with link to paper

---

## ID Conventions

- Ideas: `IDEA-001`, `IDEA-002`, etc.
- IDs are assigned sequentially across all stages
- An idea keeps its ID as it moves through the pipeline
- Check existing ideas before assigning new IDs

---

## Integration with Other Stacks

### From reading_stack

Paper summaries include an "Ideas Sparked" section. Use `/extract-ideas` to:
1. Scan `reading_stack/summaries/` for papers with ideas
2. Create corresponding `IDEA-XXX.md` entries in `idea_stack/_inbox/`
3. Link back to source papers

### To papers/

When an idea is ready, use `/launch-paper` to create a full paper project with the idea content as the foundation.

### With experiment_stack

During the developing stage, validation experiments may be run through `experiment_stack/` to test hypotheses before promotion.

---

## Commands

- `/promote-idea IDEA-XXX`: Evaluate idea and promote to next stage if criteria met
- `/extract-ideas`: Extract ideas from paper summaries into _inbox
- `/launch-paper IDEA-XXX`: Create paper project from ready idea
