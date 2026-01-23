# Writer Stack

A system for managing writing tasks and producing paper content.

## Purpose

- **_inbox/**: Writing tasks waiting to be completed
- **summaries/**: Completed writing outputs ready for integration

## Directory Structure

```
writer_stack/
├── _inbox/      # Writing tasks to complete
└── summaries/   # Completed writing outputs
```

## Workflow

```
Writing task → _inbox/WRITE-XXX.md
         ↓
Gather context → Read relevant materials
         ↓
Draft content → summaries/WRITE-XXX.md
         ↓
Review & integrate → papers/<name>/paper/
```

---

## Entry Formats

### _inbox/ Format

Writing task specification. Filename: `WRITE-XXX-[section]-[paper].md`

```markdown
# Writing Task: [Section Name] for [Paper Name]

- **ID**: WRITE-XXX
- **Created**: YYYY-MM-DD
- **Paper**: [paper-name]
- **Section**: [introduction / related work / method / experiments / conclusion / abstract]
- **Priority**: P0/P1/P2/P3
- **Status**: pending

## Task Description

[What specifically needs to be written?]

## Context

### Paper Overview

[Brief description of the paper's contribution]

### Target Venue

[Conference/journal and style requirements]

### Word/Page Limit

[If applicable]

## Source Materials

- PRD: [path to paper requirements]
- Experiments: [EXP-XXX, EXP-YYY]
- Related papers: [PAPER-XXX, PAPER-YYY]
- Existing draft: [path if revising]

## Requirements

### Must Include

- [Required element 1]
- [Required element 2]

### Must Avoid

- [Thing to avoid]

### Tone/Style

[Formal, technical, accessible, etc.]

## Related Work Categories

(For related work sections)

- [ ] Category 1: [papers to cite]
- [ ] Category 2: [papers to cite]

## Key Points to Make

1. [Point 1]
2. [Point 2]
3. ...

## Reviewer Concerns to Address

(If revision)

- [Concern 1]: [how to address]
- [Concern 2]: [how to address]
```

### summaries/ Format

Completed writing output. Filename: `WRITE-XXX-[section]-[paper].md`

```markdown
# Writing Output: [Section Name] for [Paper Name]

- **ID**: WRITE-XXX
- **Created**: YYYY-MM-DD
- **Completed**: YYYY-MM-DD
- **Paper**: [paper-name]
- **Section**: [section type]
- **Status**: completed

## Draft Content

[The actual written content goes here]

---

## Metadata

### Word Count

[X words]

### Citations Used

- [citation 1]
- [citation 2]
- ...

### Figures/Tables Referenced

- Figure X: [description]
- Table Y: [description]

## Notes for Integration

### Placement

[Where this fits in the paper]

### Dependencies

- Requires [figure/table] to be finalized
- Connects to [other section]

### Open Questions

- [Question for author to resolve]

## Review Checklist

- [ ] Accurate technical claims
- [ ] All citations verified
- [ ] Consistent notation with rest of paper
- [ ] Within word/page limit
- [ ] Addresses reviewer concerns (if revision)
```

---

## Writing Task Types

### Introduction

- Motivation and problem statement
- Key contributions
- Paper outline

### Related Work

- Literature survey organized by theme
- Positioning against prior work
- Gap identification

### Method

- Technical approach description
- Mathematical formulation
- Algorithm pseudocode

### Experiments

- Experimental setup
- Results presentation
- Analysis and discussion

### Conclusion

- Summary of contributions
- Limitations
- Future work

### Abstract

- Complete paper summary
- 150-250 words typically

### Rebuttal

- Response to reviewer comments
- Point-by-point addressing

---

## Priority Levels

- **P0 (Critical)**: Blocking submission, needs immediate attention
- **P1 (High)**: Important for upcoming deadline
- **P2 (Medium)**: Should be done soon
- **P3 (Low)**: Nice to have, no urgency

---

## ID Conventions

- Writing tasks: `WRITE-001`, `WRITE-002`, etc.
- IDs are assigned sequentially
- Keep the same ID when moving from _inbox to summaries

---

## Integration with Other Stacks

### Inputs From

- **papers/**: Paper requirements, existing drafts
- **experiment_stack/results/**: Results to write up
- **reading_stack/summaries/**: Related work references
- **advisor_stack/feedback/**: Writing feedback to address

### Outputs To

- **papers/<name>/paper/**: Integrated into paper draft

---

## Writing Guidelines

### General Principles

1. **Clarity over cleverness**: Be clear and direct
2. **One idea per paragraph**: Logical flow
3. **Active voice**: Prefer active constructions
4. **Precise language**: Avoid vague terms
5. **Show, don't tell**: Evidence over claims

### Technical Writing

1. **Define terms**: Introduce notation clearly
2. **Consistent symbols**: Same symbol, same meaning
3. **Cite appropriately**: Support claims with references
4. **Figures help**: Use visuals to explain complex ideas

### Common Issues to Avoid

- Overclaiming results
- Missing baselines/comparisons
- Undefined notation
- Inconsistent terminology
- Passive voice overuse

---

## Commands

- Writer agent handles all writing tasks
- Process tasks from _inbox/ to summaries/
- Integrate outputs into paper drafts
