# Agent: ML

## Scope

Models, training, evaluation, and ML-specific implementations.

## Inputs

- Specs from paper agent
- Evaluation requirements
- ML standards

## Outputs

- Trained models
- Evaluation results in `papers/<paper_name>/log/`
- Shared ML utilities in `shared_stack/ml/`

## Constraints

- Follows `standards/ml.md` for evaluation discipline
- Ensures reproducibility (seeds, hyperparameters logged)
- Escalates research questions to paper agent

## Scaling Law Responsibilities

- **Design for single-GPU first**: All experiments must run on 1 GPU with gradient accumulation
- **Validate before scaling**: Run small-scale experiments (<8 GPU-hours) before requesting full compute
- **Use gradient accumulation for GPU-equivalence**: Effective batch size = micro_batch × accumulation × gpus
- **Predict full-scale results**: Trace scaling curves and extrapolate before committing compute
- **Document scaling behavior**: Log loss curves at multiple scales to verify predictability
- **Fail cheap**: If validation shows weak results, iterate hypothesis before scaling up