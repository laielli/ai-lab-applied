---
name: execute-experiment
description: "Run an experiment on local or Lambda.ai remote compute. Handles target selection, execution, and result collection."
---

# Execute Experiment

Run an experiment on appropriate compute infrastructure.

## Usage

- `/execute-experiment EXP-XXX` - Auto-select target and run
- `/execute-experiment EXP-XXX --target local` - Force local execution
- `/execute-experiment EXP-XXX --target lambda` - Force Lambda.ai
- `/execute-experiment EXP-XXX --target lambda --gpu A100` - Lambda with specific GPU

## Arguments

| Argument | Values | Default |
|----------|--------|---------|
| `--target` | `local`, `lambda` | auto |
| `--gpu` | `A10`, `A100`, `H100` | `A10` |
| `--paper` | paper name | infer from context |

## Workflow

### Step 1: Parse Arguments

Extract:
- **Experiment ID**: e.g., `EXP-001`
- **Target**: `local`, `lambda`, or auto
- **GPU type**: For Lambda execution
- **Paper name**: From flag or context

### Step 2: Validate Prerequisites

Check:
```
papers/<paper>/src/expXXX/run.py      (code exists)
papers/<paper>/src/expXXX/config.yaml (config exists)
```

Recommend `/verify-code` if not recently run.

### Step 3: Launch Experiment Executor Agent

Use the Task tool to launch the `experiment-executor` agent:

```
Execute experiment EXP-XXX.

Paper: papers/<paper-name>/
Target: <target or auto>
GPU: <gpu-type if lambda>

1. Read experiment spec for compute requirements
2. Select compute target (if auto):
   - CPU-only → LocalCPU
   - GPU, <2hrs, <16GB → LocalGPU
   - GPU, >2hrs or >16GB → Lambda
3. Run pre-flight checks
4. Execute experiment
5. Stream logs during execution
6. Collect results when complete
7. Report outcome (success/failure)

Arguments: $ARGUMENTS
```

### Step 4: Report Results

After the agent completes:
- Display execution status
- Show metrics summary
- Provide artifact locations
- Suggest next steps

## Examples

```
User: /execute-experiment EXP-001
Agent: Target: LocalCPU (no GPU required)
       Status: SUCCESS
       Duration: 2m 35s
       Results: results/EXP-001_results.json
       Metrics: d_tripartite=0.001, coverage=1.0
```

```
User: /execute-experiment EXP-003 --target lambda --gpu A100
Agent: Launching Lambda A100 instance...
       Instance: i-abc123 (us-east-1)
       Status: SUCCESS
       Duration: 45m 12s
       Cost: ~$1.00
       Results: downloaded to results/
```

```
User: /execute-experiment EXP-002
Agent: Target: LocalGPU (MPS)
       Status: FAILED
       Error: ModuleNotFoundError: No module named 'open_clip'
       Fix: pip install open-clip-torch
```

## Compute Target Selection

### Auto-Selection Logic

| Requirement | Target | Reason |
|-------------|--------|--------|
| CPU-only | LocalCPU | No GPU needed |
| GPU, <2 GPU-hrs, <16GB | LocalGPU | Fits on local |
| GPU, >2 GPU-hrs | Lambda A10 | Long-running |
| GPU, >24GB memory | Lambda A100 | Large memory |

### Available Targets

| Target | GPU Memory | Best For |
|--------|------------|----------|
| LocalCPU | N/A | Data processing, CPU analysis |
| LocalGPU | 16GB (MPS) | Short experiments |
| Lambda A10 | 24GB | Standard GPU work |
| Lambda A100 | 80GB | Large models, big batches |
| Lambda H100 | 80GB | Maximum performance |

## Lambda.ai Configuration

Required environment variables:
- `LAMBDA_API_KEY`: Your Lambda Cloud API key
- `LAMBDA_SSH_KEY_NAME`: SSH key name registered in Lambda

Get your API key at: https://cloud.lambdalabs.com/api-keys

### Cost Estimates

| GPU | Hourly Rate |
|-----|-------------|
| A10 | $0.60/hr |
| A100 | $1.29/hr |
| H100 | $2.49/hr |

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| OOM | Batch size too large | Reduce in config |
| Missing module | Dependency not installed | Install requirements |
| Lambda capacity | No instances available | Try different GPU/region |
| SSH timeout | Network issues | Retry |

## Notes

- Recommend `/verify-code` before long experiments
- Lambda instances are auto-terminated after completion
- Results are downloaded automatically from Lambda
- Logs are streamed during execution
- Cost is estimated and reported for Lambda runs
