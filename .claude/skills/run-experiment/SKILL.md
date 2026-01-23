---
name: run-experiment
description: "Move experiments through the experiment_stack lifecycle (_inbox → in_progress → results). Use to start, update, or complete experiments."
---

# Run Experiment

Track experiments through their lifecycle.

## Usage

- `/run-experiment start EXP-XXX` - Start an experiment (move to in_progress)
- `/run-experiment complete EXP-XXX` - Complete an experiment (move to results)
- `/run-experiment update EXP-XXX` - Update progress on running experiment
- `/run-experiment` or `/run-experiment --list` - List all experiments by status

## Workflow

### Step 1: Launch Experiment Runner Agent

Use the Task tool to launch the `experiment-runner` agent with this prompt:

**For starting an experiment:**
```
Start experiment EXP-XXX.

1. Read experiment spec from experiment_stack/_inbox/EXP-XXX-*.md
2. Validate the spec is complete:
   - Objective defined
   - Configuration complete
   - Dependencies satisfied
   - Compute within budget
3. Move to experiment_stack/in_progress/:
   - Add "Started" timestamp
   - Change status to "running"
   - Initialize progress log
4. Report that experiment is ready to run

Experiment: $ARGUMENTS
```

**For completing an experiment:**
```
Complete experiment EXP-XXX.

1. Read experiment from experiment_stack/in_progress/EXP-XXX-*.md
2. Gather results (ask user if not provided):
   - Final metrics
   - Training logs
   - Artifacts locations
3. Move to experiment_stack/results/:
   - Add "Completed" timestamp
   - Add results tables
   - Analyze whether hypothesis was validated
   - Document key findings
4. Report summary of results

Experiment: $ARGUMENTS
```

**For updating progress:**
```
Update progress on experiment EXP-XXX.

1. Read experiment from experiment_stack/in_progress/EXP-XXX-*.md
2. Add progress entry with current status
3. Update metrics table if new results available
4. Update estimated completion if needed

Experiment: $ARGUMENTS
```

**For listing experiments:**
```
List all experiments across the experiment_stack.

1. Check _inbox/ for queued experiments
2. Check in_progress/ for running experiments
3. Check results/ for completed experiments
4. Report summary with:
   - Queued count and names
   - Running count with start dates
   - Completed count with outcomes
```

### Step 2: Report Results

After the agent completes, report to the user:

**For start:**
- Confirmation experiment is started
- Validation results
- What to do while it runs

**For complete:**
- Results summary table
- Whether hypothesis was validated
- Key findings
- Next steps

**For update:**
- Current progress
- Latest metrics
- Estimated completion

**For list:**
- Experiments by stage
- Any blocked experiments
- Recommended next actions

## Experiment Lifecycle

```
_inbox (queued)
    ↓ start
in_progress (running)
    ↓ complete
results (done)
```

## Compute Budget Reference

| Phase | Budget | Description |
|-------|--------|-------------|
| Validation | <8 GPU-hours | Initial hypothesis test |
| Ablation | <24 GPU-hours | Component analysis |
| Full | Varies | Paper-quality results |

## Notes

- Experiments keep their ID through the lifecycle
- Paper-specific experiments live in papers/<name>/experiment_stack/
- The agent validates compute budgets before starting
- Use with paper experiments: `/run-experiment start EXP-temporal-001`
