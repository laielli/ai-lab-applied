# Engineering Standards

## Code Quality

- Write clean, readable code with clear variable names
- Include tests for core functionality
- Document complex logic with inline comments

## Code Review

- All code changes should be reviewable
- Focus on correctness, performance, and maintainability

## Version Control

- Use meaningful commit messages
- Keep commits atomic and focused

## Efficiency Standards

### Single-GPU Default

- All training code MUST run on single GPU with gradient accumulation
- Multi-GPU is an optimization, not a requirement
- Target: validation experiments complete in **<8 hours on 1 GPU**
- Code that requires multi-GPU for basic functionality is a design flaw

### Memory Budget

- Default target: **24GB GPU memory** (A10G/RTX 3090 tier)
- Use mixed precision (**bfloat16**) by default for all training
- Profile memory usage before scaling batch size
- Gradient checkpointing for memory-intensive models

### Reproducibility as Code

- Experiments = **shell scripts** (not notebooks, not ad-hoc commands)
- Every experiment must be reproducible via a single script
- Scripts capture: hyperparameters, data paths, random seeds, git commit
- Example structure:
  ```
  papers/<paper_name>/src/
  ├── train.py           # Main training code
  ├── scripts/
  │   ├── exp_001.sh     # Baseline experiment
  │   ├── exp_002.sh     # Ablation: no temporal
  │   └── exp_003.sh     # Full model
  ```

### Checkpoint Evolution

- Checkpoints must survive minor architecture changes
- Use **patch-based loading**: load what matches, initialize what's new
- Document checkpoint compatibility in training code
- Tag checkpoints with model version metadata

### Compute Awareness

- Log wall-clock time and GPU utilization for all runs
- Track compute cost (GPU-hours) alongside metrics
- Include efficiency metrics in experiment logs (samples/sec, memory peak)