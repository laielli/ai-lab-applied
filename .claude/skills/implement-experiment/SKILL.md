---
name: implement-experiment
description: "Generate Python code from an experiment spec. Creates executable modules in the paper's src/ directory."
---

# Implement Experiment

Generate executable Python code from an experiment specification.

## Usage

- `/implement-experiment EXP-XXX` - Implement experiment in current paper context
- `/implement-experiment EXP-XXX --paper <paper-name>` - Implement for specific paper

## Workflow

### Step 1: Parse Arguments

Extract:
- **Experiment ID**: e.g., `EXP-001`
- **Paper name**: From `--paper` flag or infer from context

If paper not specified, check for active paper context or list available papers.

### Step 2: Validate Spec Exists

Check for experiment spec in:
```
papers/<paper>/experiment_stack/_inbox/EXP-XXX-*.md
papers/<paper>/experiment_stack/in_progress/EXP-XXX-*.md
```

If not found, report error with available experiments.

### Step 3: Launch Experiment Implementer Agent

Use the Task tool to launch the `experiment-implementer` agent:

```
Generate Python code for experiment EXP-XXX.

Paper: papers/<paper-name>/
Experiment: EXP-XXX

1. Read experiment spec from experiment_stack/
2. Read paper requirements for context
3. Analyze existing code patterns in src/
4. Generate modular Python code:
   - src/expXXX/data.py - Dataset loading
   - src/expXXX/metrics.py - Metric computation
   - src/expXXX/run.py - Orchestrator
   - src/expXXX/config.yaml - Default config
5. Create shell wrapper in scripts/expXXX.sh
6. Update spec with code paths

Arguments: $ARGUMENTS
```

### Step 4: Report Results

After the agent completes:
- Confirm code was generated
- Show file locations
- Display next steps

## Examples

```
User: /implement-experiment EXP-001
Agent: Generated code for EXP-001 in papers/idea-010-v-limit/src/exp001/
       Files: data.py, metrics.py, run.py, config.yaml
       Script: scripts/exp001.sh
       Next: /verify-code EXP-001
```

```
User: /implement-experiment EXP-002 --paper idea-010-v-limit
Agent: Generated code for EXP-002 in papers/idea-010-v-limit/src/exp002/
       Files: data.py, metrics.py, run.py, config.yaml
       Next: /verify-code EXP-002
```

## Generated Code Structure

The agent creates:

```
papers/<paper>/src/
├── expXXX/
│   ├── __init__.py        # Package marker
│   ├── data.py            # Dataset loading
│   ├── metrics.py         # Metric computation
│   ├── run.py             # Main orchestrator
│   └── config.yaml        # Default configuration
├── common/                # Shared utilities (if needed)
│   ├── __init__.py
│   ├── datasets.py
│   └── embeddings.py
└── scripts/
    └── expXXX.sh          # Shell wrapper
```

## Code Standards

Generated code follows `standards/engineering.md`:
- Single-GPU default with gradient accumulation
- 24GB memory budget, bfloat16 by default
- Reproducible via single script
- Comprehensive logging

## Notes

- Recommend running `/verify-experiment EXP-XXX` before implementing
- Code generation uses Opus model for quality
- Existing code patterns are analyzed and reused
- Shell scripts are made executable automatically
