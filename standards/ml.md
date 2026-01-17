# ML Standards

## Evaluation Discipline

- Always establish baseline metrics before experimentation
- Track all experiment parameters and results
- Use consistent evaluation metrics across experiments

## Dataset Management

- Version all datasets
- Document data sources and preprocessing steps
- Track dataset statistics and distributions

## Reproducibility

- Set random seeds for reproducible results
- Log hyperparameters for all training runs
- Save model checkpoints with metadata

## Scaling Law Methodology

### Principle: Single-GPU Equivalence

Gradient accumulation provides mathematical equivalence for scaling validation:

```
8 GPUs × 4 accumulation steps = 1 GPU × 32 accumulation steps
→ IDENTICAL gradients, IDENTICAL scaling curves
```

**Key insight**: The loss curve traced is identical—just slower. This means scaling laws can be validated on single-GPU before committing expensive multi-GPU compute.

### Requirements

- All training code MUST support arbitrary gradient accumulation
- Experiments MUST be designed with configurable batch size and accumulation steps
- Validation experiments target **<8 GPU-hours** total compute
- Document effective batch size (micro_batch × accumulation × num_gpus)

### Validation Protocol

1. **Design**: Configure experiment with adjustable batch size and gradient accumulation
2. **Small-scale run**: Execute on 1 GPU overnight to trace initial scaling curve
3. **Evaluate curve**: If curve shows promise → approve multi-GPU budget
4. **Iterate cheap**: If curve shows failure → revise hypothesis (cheap failure, fast iteration)
5. **Scale up**: Only after small-scale validation, commit to full compute budget

### Confidence Metrics for Extrapolation

Before predicting large-scale outcomes from small-scale runs:

- Require **3+ data points** on the scaling curve before extrapolation
- Log-linear fit **R² > 0.95** for confident prediction
- Always validate **1 point at larger scale** before full commitment
- Track loss variance to ensure stable training dynamics

### Compute Budget Guidelines

| Phase | Target Compute | Purpose |
|-------|----------------|---------|
| Idea validation | <8 GPU-hours | Prove concept is viable |
| Ablation studies | <24 GPU-hours | Identify key components |
| Full experiment | Budget varies | Final results for paper |

### What This Enables

- **Fail fast, fail cheap**: Invalid hypotheses identified in hours, not days
- **More ideas explored**: 10× more concepts tested per compute budget
- **Confident scaling**: Predictable results when scaling up
- **Agent-friendly**: Autonomous agents can run validation loops overnight
