---
name: simulate-meeting
description: "Simulate a lab meeting with three personas (Advisor, SME, Lay Researcher) to prepare for real meetings. Generates Q&A feedback and routes action items."
---

# Simulate Meeting

Pre-meeting rehearsal with synthetic feedback from multiple perspectives.

## Usage

- `/simulate-meeting SIM-XXX` - Run simulation for specific ID
- `/simulate-meeting --create` - Create new presentation spec
- `/simulate-meeting --list` - List pending simulations
- `/simulate-meeting` - List pending simulations (default)

## Workflow

### For Running a Simulation (`/simulate-meeting SIM-XXX`)

Use the Task tool to launch the `lab-meeting-simulator` agent with this prompt:

```
Run simulation SIM-XXX.

1. Read simulation_stack/README.md for formats
2. Read simulation_stack/_inbox/SIM-XXX-*.md
3. Generate Q&A from three personas:
   - Advisor: 3-5 strategic questions
   - SME: 3-5 technical questions
   - Lay Researcher: 3-5 clarity questions
4. Synthesize feedback (strengths, weaknesses, contested points)
5. Extract action items and route to appropriate stacks
6. Create session transcript in simulation_stack/sessions/
7. Delete processed request from _inbox
8. Report summary

Simulation ID: $ARGUMENTS
```

### For Creating a New Spec (`/simulate-meeting --create`)

Create an interactive workflow:

1. Ask user for:
   - Topic/title
   - Associated paper (if any)
   - Type: experiment-update, paper-review, or idea-pitch

2. Determine next SIM-XXX ID by checking existing files

3. Create template file in `simulation_stack/_inbox/SIM-XXX-[topic].md`:

```markdown
# Simulation Request: [Topic]

- **ID**: SIM-XXX
- **Paper**: [paper-name or "none"]
- **Type**: [type]

## Presentation Content

### Context
[TODO: Problem setup, 1-2 paragraphs]

### Experiments
[TODO: What was run]

### Results
| Experiment | Metric | Baseline | Ours | Delta |
|------------|--------|----------|------|-------|
| TODO | | | | |

### Analysis
[TODO: Interpretation]

### Open Questions
1. [TODO: Question for feedback]

## Focus Areas
- [ ] Methodology
- [ ] Statistical validity
- [ ] Narrative
- [ ] Next steps
```

4. Report file location and prompt user to fill in content

### For Listing Simulations (`/simulate-meeting --list` or `/simulate-meeting`)

1. Check `simulation_stack/_inbox/` for pending simulations
2. Check `simulation_stack/sessions/` for completed simulations
3. Report:

```markdown
## Simulation Stack Status

### Pending (_inbox/)
| ID | Topic | Paper | Type |
|----|-------|-------|------|
| SIM-XXX | [topic] | [paper] | [type] |

### Completed (sessions/)
| ID | Topic | Date | Action Items |
|----|-------|------|--------------|
| SIM-XXX | [topic] | [date] | [count] |

### Recommended Action
[Next step based on status]
```

## Three Personas

The simulation generates questions from three perspectives:

| Persona | Focus | Style |
|---------|-------|-------|
| Advisor | Strategy, venues, positioning | Direct, strategic |
| SME | Methodology, validity, details | Rigorous, technical |
| Lay Researcher | Assumptions, clarity, motivation | Questioning, jargon-detecting |

## Output

Session transcripts include:
- 9-15 questions with suggested answers
- Feedback synthesis (strengths, weaknesses, contested points)
- Action items routed to appropriate stacks
- Routing log

## Feedback Routing

Action items are automatically routed:

| Type | Destination |
|------|-------------|
| Experiments | `experiment_stack/_inbox/` |
| Writing | `writer_stack/_inbox/` |
| Papers to read | `reading_stack/_inbox/` |
| Figures | `figure_stack/_inbox/` |

## Examples

```bash
# Prepare for presenting temporal modeling results
/simulate-meeting --create
# Fill in the template, then:
/simulate-meeting SIM-001

# Check what simulations are pending
/simulate-meeting --list

# Run a specific simulation
/simulate-meeting SIM-003
```

## Notes

- Use before real lab meetings for rehearsal
- Honest feedback helps identify weak spots early
- Action items should be addressed before real presentation
- Sessions are preserved for reference
