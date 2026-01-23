# Experiment Stack

A system for tracking experiments through their lifecycle, from specification to results.

## Purpose

- **_inbox/**: Experiment specs waiting to be run
- **in_progress/**: Experiments currently running
- **results/**: Completed experiments with analysis

## Directory Structure

```
experiment_stack/
├── _inbox/          # Experiment specs queued to run
├── in_progress/     # Currently running experiments
└── results/         # Completed experiments with results
```

## Workflow

```
Define experiment → _inbox/EXP-XXX.md
         ↓
Start running → in_progress/EXP-XXX.md (status: running)
         ↓
Complete & analyze → results/EXP-XXX.md
         ↓
Integrate into paper → papers/<name>/log/
```

---

## Entry Formats

### _inbox/ Format

Experiment specification ready to run. Filename: `EXP-XXX-[short-name].md`

```markdown
# Experiment: [Short Descriptive Name]

- **ID**: EXP-XXX
- **Created**: YYYY-MM-DD
- **Paper**: [paper-name] (if applicable)
- **Idea**: IDEA-XXX (if applicable)
- **Priority**: P0/P1/P2/P3
- **Status**: queued

## Objective

[What question does this experiment answer?]

## Hypothesis

[Expected outcome and why]

## Method

### Setup

- **Model**: [architecture/checkpoint]
- **Dataset**: [dataset name and split]
- **Hardware**: [GPU type, count]

### Configuration

```yaml
# Key hyperparameters
batch_size: 32
learning_rate: 1e-4
epochs: 10
...
```

### Procedure

1. [Step 1]
2. [Step 2]
3. ...

## Metrics

- **Primary**: [main metric to optimize]
- **Secondary**: [other metrics to track]

## Baselines

- [Baseline 1]: [expected/reported performance]
- [Baseline 2]: [expected/reported performance]

## Compute Budget

- **Estimated time**: X GPU-hours
- **Phase**: validation (<8h) / ablation (<24h) / full (varies)

## Success Criteria

- [Specific threshold or comparison that defines success]

## Dependencies

- [ ] Dataset prepared
- [ ] Model checkpoint available
- [ ] Code implemented
- [ ] Baseline results obtained
```

### in_progress/ Format

Currently running experiment. Filename: `EXP-XXX-[short-name].md`

```markdown
# Experiment: [Short Descriptive Name]

- **ID**: EXP-XXX
- **Created**: YYYY-MM-DD
- **Started**: YYYY-MM-DD
- **Paper**: [paper-name]
- **Status**: running

## Objective

[What question does this experiment answer?]

## Hypothesis

[Expected outcome]

## Configuration

[Same as _inbox, locked at start time]

## Progress Log

### YYYY-MM-DD HH:MM

[Update on progress, any issues encountered]

### YYYY-MM-DD HH:MM

[Another update]

## Current Metrics

| Epoch | Train Loss | Val Loss | Primary Metric |
|-------|------------|----------|----------------|
| 1     | X.XX       | X.XX     | X.XX           |
| 2     | X.XX       | X.XX     | X.XX           |

## Issues Encountered

- [Issue 1]: [resolution or workaround]

## Estimated Completion

YYYY-MM-DD HH:MM
```

### results/ Format

Completed experiment with analysis. Filename: `EXP-XXX-[short-name].md`

```markdown
# Experiment: [Short Descriptive Name]

- **ID**: EXP-XXX
- **Created**: YYYY-MM-DD
- **Started**: YYYY-MM-DD
- **Completed**: YYYY-MM-DD
- **Paper**: [paper-name]
- **Status**: completed / failed

## Objective

[What question did this experiment answer?]

## Hypothesis

[What we expected]

## Configuration

[Final configuration used]

## Results

### Primary Metrics

| Method | R@1 | R@5 | R@10 | MedR |
|--------|-----|-----|------|------|
| Baseline | X.X | X.X | X.X | X.X |
| Ours | X.X | X.X | X.X | X.X |
| Delta | +X.X | +X.X | +X.X | -X.X |

### Secondary Metrics

[Other relevant measurements]

### Learning Curves

[Description or link to plots]

## Analysis

### Key Findings

1. [Finding 1]
2. [Finding 2]
3. ...

### Hypothesis Validated?

[Yes/No/Partial - with explanation]

### Unexpected Observations

- [Observation 1]
- [Observation 2]

## Compute Used

- **Total GPU-hours**: X.X
- **Hardware**: [GPU type]
- **Duration**: X hours Y minutes

## Artifacts

- **Checkpoints**: [path or link]
- **Logs**: [path or link]
- **Plots**: [path or link]
- **Config**: [path or link]

## Conclusions

[2-3 sentences on what we learned and implications]

## Next Steps

- [ ] [Follow-up experiment or action]
- [ ] [Integration into paper]

## Paper Integration

- [ ] Results added to paper tables
- [ ] Analysis written up
- [ ] Figures generated
```

---

## Experiment Phases

Following the lab's single-GPU scaling methodology:

### Phase 1: Validation (<8 GPU-hours)

- Quick test of core hypothesis
- Can run overnight on single GPU
- Go/no-go decision based on results

### Phase 2: Ablations (<24 GPU-hours)

- Test which components matter
- Identify optimal configurations
- Run after validation shows promise

### Phase 3: Full Experiments (varies)

- Paper-quality results on full datasets
- Multiple benchmarks
- Only after validation and ablations

---

## Status Values

- **queued**: In _inbox, waiting to be started
- **running**: In in_progress, currently executing
- **completed**: In results, finished successfully
- **failed**: In results, terminated with errors
- **blocked**: In _inbox, waiting on dependencies

---

## ID Conventions

- Experiments: `EXP-001`, `EXP-002`, etc.
- IDs are assigned sequentially
- Keep the same ID throughout the lifecycle

---

## Integration with Other Stacks

### From idea_stack

Validation experiments test hypotheses from developing ideas:
- Create EXP-XXX referencing IDEA-XXX
- Results inform promotion decisions

### To papers/

Completed experiments feed into paper projects:
- Copy final results to `papers/<name>/log/`
- Reference EXP-XXX in paper experiment sections

### With advisor_stack

Advisor suggestions for experiments route here:
- Create EXP-XXX from FEEDBACK-XXX action items

---

## Commands

- `/run-experiment EXP-XXX`: Move experiment through lifecycle
- `/run-experiment --list`: Show all experiments and their status
