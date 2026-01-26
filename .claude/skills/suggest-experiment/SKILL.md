---
name: suggest-experiment
description: "Suggest the next experiment for a paper's experiment_stack. Analyzes paper requirements, schedule, and status to identify what experiment should run next."
---

# Suggest Experiment

Generate the next appropriate experiment spec for a paper project.

## Usage

- `/suggest-experiment <paper-name>` - Suggest next experiment for a paper
- `/suggest-experiment idea-010-v-limit` - Example with specific paper

## Workflow

### Step 1: Validate Paper Exists

Check that `papers/<paper-name>/` exists with required structure:
- `prd/paper_requirements.md`
- `EXPERIMENT_SCHEDULE.md`
- `experiment_stack/_inbox/`

If paper not found, list available papers in `papers/`.

### Step 2: Launch Experiment Planner Agent

Use the Task tool to launch the `experiment-planner` agent:

```
Analyze the paper project and suggest the next experiment.

Paper: papers/<paper-name>/

1. Read paper requirements from prd/paper_requirements.md
2. Read experiment schedule from EXPERIMENT_SCHEDULE.md
3. Check STATUS.md for current phase and blockers
4. Scan experiment_stack/ for existing experiments
5. Identify the next logical experiment based on:
   - Current phase (validation → ablation → full)
   - Go/no-go criteria status
   - Dependencies between experiments
6. Create experiment spec in experiment_stack/_inbox/

Output:
- Created experiment ID and filename
- Brief rationale for why this experiment is next
- Dependencies on prior experiments
- Estimated GPU-hours
```

### Step 3: Report Results

After the agent completes:
- Confirm experiment spec was created
- Show the experiment ID and title
- Display estimated compute cost
- Note any dependencies or prerequisites

## Examples

```
User: /suggest-experiment idea-010-v-limit
Agent: Created EXP-001-dtripartite-msrvtt.md
       "Compute d_tripartite for MSR-VTT" (2 GPU-hrs)
       Phase 1 validation experiment - no dependencies
```

```
User: /suggest-experiment
Agent: Available papers:
       - idea-010-v-limit
       Run: /suggest-experiment <paper-name>
```

## Experiment Phases

The agent respects the phased approach:

| Phase | Budget | Description |
|-------|--------|-------------|
| Validation | <8 GPU-hours | Quick test of core hypothesis |
| Ablation | <24 GPU-hours | Systematic component analysis |
| Full | Varies | Paper-quality results |

## Notes

- Experiments follow the pattern: `EXP-XXX-<descriptive-name>.md`
- Agent respects phased approach (validation → ablation → full)
- Won't suggest Phase 2 experiments until Phase 1 go/no-go passed
- Links experiments to paper requirements and success metrics
- Paper-specific experiments live in `papers/<name>/experiment_stack/`
