# Simulation Stack

Pre-meeting rehearsal system that simulates lab meetings with synthetic feedback from multiple perspectives.

## Purpose

Unlike real lab meetings (`lab_meeting_stack`) or advisor feedback (`advisor_stack`), this system provides **simulated feedback** before actual meetings. It helps identify weaknesses and prepare answers.

| Existing System | Purpose | This System |
|-----------------|---------|-------------|
| `advisor_stack` | Process real advisor feedback | Simulate advisor perspective |
| `lab_meeting_stack` | Prepare/process real meetings | Simulate full meeting Q&A |
| `meeting-facilitator` | Aggregate status | Generate synthetic feedback |

## Directory Structure

```
simulation_stack/
├── README.md           # This file
├── _inbox/             # Presentation specs to simulate
└── sessions/           # Completed simulation transcripts
```

## Three Personas

### 1. Advisor
- **Focus**: Strategic positioning, resource allocation, publication venues
- **Questions**: "Is this enough for CVPR?" "How does this position us vs competition?"
- **Feedback style**: Direct, strategic

### 2. Subject Matter Expert (SME)
- **Focus**: Experimental methodology, statistical validity, implementation details
- **Questions**: "Did you control for X?" "What about confound Y?" "Baseline seems unfair"
- **Feedback style**: Rigorous, technical

### 3. Lay Researcher
- **Focus**: Fundamental assumptions, clarity, motivation
- **Questions**: "Why would we expect this to work?" "How is this better than simple baseline?"
- **Feedback style**: Questioning assumptions, jargon detection

---

## Input Format

File: `_inbox/SIM-XXX-[topic].md`

```markdown
# Simulation Request: [Topic]

- **ID**: SIM-XXX
- **Paper**: [paper-name]
- **Type**: experiment-update | paper-review | idea-pitch

## Presentation Content

### Context
[Problem setup, 1-2 paragraphs]

### Experiments
[What was run]

### Results
| Experiment | Metric | Baseline | Ours | Delta |
|------------|--------|----------|------|-------|

### Analysis
[Interpretation]

### Open Questions
1. [Question for feedback]

## Focus Areas
- [ ] Methodology
- [ ] Statistical validity
- [ ] Narrative
- [ ] Next steps
```

---

## Output Format

File: `sessions/SIM-XXX-[topic].md`

```markdown
# Simulation Session: [Topic]

- **ID**: SIM-XXX
- **Paper**: [paper-name]
- **Date**: YYYY-MM-DD
- **Type**: experiment-update | paper-review | idea-pitch

---

## Q&A Transcript

### Advisor Questions

#### Q1: [Question]
**Suggested Answer**: [Response]
**Action if Weak**: [What to do if answer is insufficient]

#### Q2: [Question]
**Suggested Answer**: [Response]
**Action if Weak**: [What to do]

### SME Questions

#### Q1: [Technical Question]
**Suggested Answer**: [Response]
**Follow-up Risk**: [Likely follow-up question]

#### Q2: [Technical Question]
**Suggested Answer**: [Response]
**Follow-up Risk**: [Likely follow-up]

### Lay Researcher Questions

#### Q1: [Fundamental Question]
**Suggested Answer**: [Response]

#### Q2: [Clarity Question]
**Suggested Answer**: [Response]

---

## Feedback Synthesis

### Strengths
- [What works well]

### Weaknesses/Gaps
- [What needs work]

### Contested Points
- [Areas of potential disagreement]

---

## Action Items

| Priority | Description | Source | Route To |
|----------|-------------|--------|----------|
| P1 | [Action] | [Persona Q#] | [stack/_inbox/] |
| P2 | [Action] | [Persona Q#] | [stack/_inbox/] |

---

## Routing Log

| Action | Routed To | Entry Created |
|--------|-----------|---------------|
| [Description] | [stack/_inbox/] | [ID] |
```

---

## Workflow

### Creating a Simulation Request

1. Create file in `_inbox/SIM-XXX-[topic].md`
2. Fill in the presentation content
3. Mark focus areas for feedback

### Running a Simulation

```
/simulate-meeting SIM-XXX     # Run simulation for specific ID
/simulate-meeting --create    # Create new presentation spec
/simulate-meeting --list      # List pending simulations
```

### After Simulation

1. Review Q&A transcript
2. Prepare answers for weak spots
3. Act on routed items before real meeting

---

## Feedback Routing

Simulations route actionable items to appropriate stacks:

```
simulation_stack/sessions/
    ├── Experiments ────► experiment_stack/_inbox/
    ├── Writing ────────► writer_stack/_inbox/
    ├── Papers ─────────► reading_stack/_inbox/
    └── Figures ────────► figure_stack/_inbox/
```

---

## ID Assignment

Simulation IDs follow the pattern `SIM-XXX`:
- Check existing files in `_inbox/` and `sessions/`
- Assign next sequential number

---

## Integration Points

- **Inputs**: `experiment_stack/results/`, `figure_stack/`, `papers/`
- **Outputs**: Action items to `experiment_stack/`, `writer_stack/`, `reading_stack/`, `figure_stack/`
- **Workflow**: Fits between experiment completion and real lab meeting
