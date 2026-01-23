# Advisor Stack

A system for processing advisor feedback and routing actionable items to appropriate stacks.

## Purpose

- **_inbox/**: Raw feedback from advisor meetings, reviews, or communications
- **feedback/**: Processed feedback with extracted action items and routing

## Directory Structure

```
advisor_stack/
├── _inbox/      # Raw feedback waiting to be processed
└── feedback/    # Processed feedback with extracted actions
```

## Workflow

```
Advisor meeting/review → _inbox/FEEDBACK-XXX.md
         ↓
Process & extract actions → feedback/FEEDBACK-XXX.md
         ↓
Route to appropriate stacks:
  - Ideas → idea_stack/_inbox/
  - Experiments → experiment_stack/_inbox/
  - Writing tasks → writer_stack/_inbox/
  - Paper feedback → papers/<name>/feedback/
```

---

## Entry Formats

### _inbox/ Format

Raw feedback capture. Filename: `FEEDBACK-XXX-[date]-[topic].md`

```markdown
# Feedback: [Topic/Meeting Name]

- **ID**: FEEDBACK-XXX
- **Date**: YYYY-MM-DD
- **Source**: [Advisor name/meeting type]
- **Context**: [Paper name, idea, or general]
- **Status**: unprocessed

## Raw Notes

[Capture feedback as received - meeting notes, email content, review comments]

## Immediate Impressions

[Initial thoughts on what needs to be done]
```

### feedback/ Format

Processed feedback with extracted actions. Filename: `FEEDBACK-XXX-[date]-[topic].md`

```markdown
# Feedback: [Topic/Meeting Name]

- **ID**: FEEDBACK-XXX
- **Date**: YYYY-MM-DD
- **Processed**: YYYY-MM-DD
- **Source**: [Advisor name/meeting type]
- **Context**: [Paper name, idea, or general]
- **Status**: processed

## Summary

[2-3 sentence summary of the key feedback]

## Key Points

1. [Main point 1]
2. [Main point 2]
3. ...

## Action Items

### Ideas to Explore

- [ ] [Idea description] → route to idea_stack/_inbox/
- [ ] [Idea description] → route to idea_stack/_inbox/

### Experiments to Run

- [ ] [Experiment description] → route to experiment_stack/_inbox/

### Writing Tasks

- [ ] [Section/revision needed] → route to writer_stack/_inbox/

### Paper-Specific Actions

- [ ] [Action for specific paper] → route to papers/<name>/

### Follow-ups

- [ ] [Follow-up item with deadline]

## Routing Log

| Action | Routed To | Entry Created | Date |
|--------|-----------|---------------|------|
| [Idea] | idea_stack/_inbox/ | IDEA-XXX | YYYY-MM-DD |
| [Experiment] | experiment_stack/_inbox/ | EXP-XXX | YYYY-MM-DD |

## Response Required

- [ ] Yes / No
- **Deadline**: YYYY-MM-DD
- **Response content**: [Brief description of what to communicate back]
```

---

## Processing Guidelines

### What to Extract

1. **New research ideas**: Any suggestions for new directions or approaches
2. **Experiment suggestions**: Specific experiments or ablations to run
3. **Writing feedback**: Comments on paper drafts, sections to revise
4. **Literature pointers**: Papers to read, related work to cite
5. **Strategic guidance**: Prioritization advice, venue recommendations

### Routing Rules

| Type | Destination | Entry Type |
|------|-------------|------------|
| New idea | idea_stack/_inbox/ | IDEA-XXX |
| Experiment | experiment_stack/_inbox/ | EXP-XXX |
| Writing task | writer_stack/_inbox/ | WRITE-XXX |
| Paper to read | reading_stack/_inbox/ | PAPER-XXX |
| Paper feedback | papers/<name>/feedback/ | Direct file |

### Priority Levels

When processing, assign priority to action items:

- **P0 (Critical)**: Blocking progress, needs immediate attention
- **P1 (High)**: Important for upcoming deadline
- **P2 (Medium)**: Should be done soon
- **P3 (Low)**: Nice to have, no urgency

---

## ID Conventions

- Feedback entries: `FEEDBACK-001`, `FEEDBACK-002`, etc.
- IDs are assigned sequentially
- Keep the same ID when moving from _inbox to feedback

---

## Integration with Other Stacks

The advisor stack serves as a routing hub, distributing feedback to:

- **idea_stack**: New research directions
- **experiment_stack**: Suggested experiments
- **writer_stack**: Writing and revision tasks
- **reading_stack**: Papers to read
- **papers/**: Paper-specific feedback

---

## Best Practices

1. **Capture immediately**: Create _inbox entry during or right after advisor interaction
2. **Process within 24 hours**: Don't let feedback sit unprocessed
3. **Be specific when routing**: Include enough context in routed entries
4. **Track follow-ups**: Note any required responses with deadlines
5. **Link back**: Reference FEEDBACK-XXX in created entries for traceability
