# Lab Meeting Stack

A system for preparing lab meeting presentations and processing feedback.

## Purpose

- **_inbox/**: Upcoming presentations to prepare
- **feedback/**: Processed meeting feedback and action items

## Directory Structure

```
lab_meeting_stack/
├── _inbox/      # Presentations to prepare
└── feedback/    # Processed meeting feedback
```

## Workflow

```
Schedule meeting → _inbox/MEETING-XXX.md
         ↓
Prepare agenda & figures → Update entry + figure_stack
         ↓
Hold meeting → Capture feedback
         ↓
Process feedback → feedback/MEETING-XXX.md
         ↓
Route actions → idea_stack, experiment_stack, writer_stack
```

---

## Entry Formats

### _inbox/ Format

Upcoming meeting preparation. Filename: `MEETING-XXX-[date]-[topic].md`

```markdown
# Meeting: [Topic/Paper Name]

- **ID**: MEETING-XXX
- **Date**: YYYY-MM-DD
- **Time**: HH:MM
- **Type**: [progress update / paper review / idea pitch / practice talk]
- **Paper**: [paper-name] (if applicable)
- **Status**: preparing

## Objective

[What do you want to get out of this meeting?]

## Agenda

1. [Topic 1] (X min)
2. [Topic 2] (X min)
3. Discussion (X min)

## Content to Present

### Progress Since Last Meeting

- [Accomplishment 1]
- [Accomplishment 2]

### Current Status

- **What's working**: [brief description]
- **What's not working**: [challenges]
- **Blockers**: [if any]

### Questions for Group

1. [Question needing group input]
2. [Question needing group input]

### Next Steps (Proposed)

1. [Planned next step]
2. [Planned next step]

## Preparation Checklist

- [ ] Figures/visuals prepared
- [ ] Demo ready (if applicable)
- [ ] Results tables updated
- [ ] Questions formulated
- [ ] Related work reviewed

## Figures

- [figure_stack/figures/FIG-XXX/ or paths to visuals]
```

### feedback/ Format

Processed meeting feedback. Filename: `MEETING-XXX-[date]-[topic].md`

```markdown
# Meeting: [Topic/Paper Name]

- **ID**: MEETING-XXX
- **Date**: YYYY-MM-DD
- **Type**: [progress update / paper review / idea pitch / practice talk]
- **Paper**: [paper-name]
- **Status**: processed

## Meeting Summary

[2-3 sentence summary of discussion]

## Key Feedback

### Positive

- [What resonated well]
- [Strengths identified]

### Concerns/Questions

- [Concern 1]
- [Concern 2]

### Suggestions

- [Suggestion 1]
- [Suggestion 2]

## Action Items

### Ideas to Explore

- [ ] [Idea from discussion] → idea_stack/_inbox/

### Experiments to Run

- [ ] [Suggested experiment] → experiment_stack/_inbox/

### Writing Tasks

- [ ] [Writing feedback] → writer_stack/_inbox/

### Other Actions

- [ ] [Action item]

## Decisions Made

- [Decision 1]
- [Decision 2]

## Routing Log

| Action | Routed To | Entry Created | Date |
|--------|-----------|---------------|------|
| [Idea] | idea_stack/_inbox/ | IDEA-XXX | YYYY-MM-DD |

## Follow-up Meeting

- **Needed**: Yes / No
- **Proposed date**: YYYY-MM-DD
- **Focus**: [what to cover next time]
```

---

## Meeting Types

### Progress Update

Regular check-in on paper or project progress:
- What's been done since last meeting
- Current blockers and challenges
- Proposed next steps

### Paper Review

Detailed review of paper draft:
- Section-by-section feedback
- Writing and presentation suggestions
- Related work gaps

### Idea Pitch

Presenting new research ideas:
- Problem motivation
- Proposed approach
- Expected contribution
- Feasibility assessment

### Practice Talk

Rehearsal for conference presentation:
- Timing feedback
- Clarity of explanations
- Figure clarity
- Q&A preparation

---

## ID Conventions

- Meetings: `MEETING-001`, `MEETING-002`, etc.
- IDs are assigned sequentially
- Keep the same ID when moving from _inbox to feedback

---

## Integration with Other Stacks

### Inputs From

- **papers/**: Status updates, draft reviews
- **experiment_stack/**: Results to present
- **idea_stack/**: Ideas to pitch

### Outputs To

- **idea_stack/_inbox/**: New ideas from discussion
- **experiment_stack/_inbox/**: Suggested experiments
- **writer_stack/_inbox/**: Writing tasks
- **figure_stack/**: Figures for presentations

---

## Best Practices

1. **Prepare thoroughly**: Don't wing lab meetings
2. **Clear objectives**: Know what feedback you need
3. **Capture everything**: Take detailed notes during meeting
4. **Process quickly**: Route feedback within 24 hours
5. **Close the loop**: Follow up on action items
