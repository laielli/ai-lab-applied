# Summary: nanochat

- **Repo ID**: REPO-001
- **GitHub**: https://github.com/karpathy/nanochat
- **Paper**: N/A (educational/reference implementation)
- **Reviewed**: 2026-01-17

## One-Line Summary

A minimal, full-stack LLM training codebase that demonstrates how principled gradient accumulation and careful hyperparameter scaling enable single-GPU experiments to replicate multi-GPU scaling law behaviors.

## Codebase Overview

### Structure

```
nanochat/
├── nanochat/                 # Core package
│   ├── gpt.py               # Transformer model architecture
│   ├── engine.py            # Inference engine with KV cache
│   ├── dataloader.py        # Distributed tokenizing data loader
│   ├── adamw.py             # Distributed AdamW optimizer
│   ├── muon.py              # Muon optimizer (momentum + orthogonalization)
│   ├── checkpoint_manager.py # Fault-tolerant checkpointing
│   ├── tokenizer.py         # BPE tokenizer (GPT-4 style)
│   ├── core_eval.py         # CORE evaluation framework
│   └── ui.html              # Web interface
├── scripts/                  # Training scripts
│   ├── base_train.py        # Pretraining
│   ├── mid_train.py         # Midtraining phase
│   ├── chat_sft.py          # Supervised fine-tuning
│   ├── chat_rl.py           # Reinforcement learning
│   └── chat_web.py          # Web deployment
├── tasks/                    # Evaluation tasks
│   ├── arc.py, mmlu.py      # Multiple-choice evals
│   ├── gsm8k.py             # Math reasoning
│   ├── humaneval.py         # Code generation
│   └── common.py            # Task composition
├── tests/                    # Test suite
├── speedrun.sh              # $100 tier (~4 hours on 8xH100)
├── run1000.sh               # $1000 tier (~42 hours on 8xH100)
├── scaling_laws.sh          # Scaling law experiments
└── miniseries.sh            # Depth scaling series
```

### Tech Stack

- **Language**: Python 3.10+
- **Framework**: PyTorch >= 2.9.0
- **Distributed**: torchrun + PyTorch DDP
- **Inference**: Flash Attention 3, KV cache
- **Package Manager**: uv
- **Key dependencies**: transformers, tiktoken, datasets, fastapi, wandb

### Size & Complexity

- **Lines of code**: ~5,000 (estimated core)
- **Core modules**: 10
- **Complexity assessment**: moderate (deliberately minimal)

## Quality Assessment

### Code Quality

- **Readability**: excellent - Clean, well-named functions, consistent style, minimal abstraction layers
- **Documentation**: thorough - Extensive README, inline comments explaining non-obvious choices, detailed shell scripts
- **Tests**: minimal - Basic pytest suite, but training scripts are effectively tested by the speedrun
- **Reproducibility**: easy - Complete shell scripts with all hyperparameters, deterministic seeds, public data

### Utility Assessment

- **Reusable components**:
  - Distributed AdamW/Muon optimizers with ZeRO-2-style sharding
  - Checkpoint manager with backward compatibility patching
  - CORE evaluation framework
  - BOS-aligned bestfit packing dataloader
  - KV cache inference engine
- **Adaptation difficulty**: moderate - Clean design but LLM-specific; patterns transfer well
- **Active maintenance**: active - 251 commits, 39 contributors, last updated Jan 16, 2026

---

## Key Implementation Details

### 1. Single-GPU Scaling Law Equivalence

**Location**: `scripts/base_train.py` - gradient accumulation logic

**Summary**: The critical insight enabling single-GPU replication of multi-GPU results is **mathematically equivalent gradient accumulation**. When you reduce GPU count, you increase accumulation steps proportionally, producing identical effective batch sizes and gradients.

**Key Code Pattern**:
```python
# Calculate accumulation steps to reach target batch size
tokens_per_fwdbwd = args.device_batch_size * args.max_seq_len
world_tokens_per_fwdbwd = tokens_per_fwdbwd * ddp_world_size
grad_accum_steps = args.total_batch_size // world_tokens_per_fwdbwd

# Training loop with normalized loss
for micro_step in range(grad_accum_steps):
    with autocast_ctx:
        loss = model(x, y)
    loss = loss / grad_accum_steps  # Normalize for accumulation
    loss.backward()
```

**Key Insights**:
- With 8 GPUs: `grad_accum_steps = 4` (or similar)
- With 1 GPU: `grad_accum_steps = 32` (8x higher)
- Both produce **identical gradients** after accumulation
- Training takes 8x longer on 1 GPU but converges to same loss curve
- This is explicitly stated: "all code will run just fine on even a single GPU... and will produce ~identical results"

**Why This Matters for Scaling Laws**:
- Scaling laws describe loss as a function of compute (FLOPs), data (tokens), and parameters
- The relationships hold regardless of parallelization strategy
- Single-GPU experiments can validate scaling curves that predict multi-GPU outcomes
- Enables cheap hypothesis testing before committing to expensive runs

### 2. Distributed Training Architecture

**Location**: `nanochat/adamw.py`, `nanochat/muon.py`, `scripts/base_train.py`

**Summary**: Implements ZeRO-2-style optimizer sharding where each rank owns a slice of optimizer state, reducing memory by world_size.

**Key Insights**:
- Small parameters (< 1024 elements): `all_reduce()` for gradient averaging
- Large parameters: `reduce_scatter_tensor()` distributes reduced gradients
- Async operations with futures enable computation/communication overlap
- Each rank saves its own optimizer shard: `optim_{step}_rank{rank}.pt`

**Distributed Muon Innovation**:
```python
# Muon applies Newton-Schulz orthogonalization to gradient updates
# Uses "Polar Express" algorithm (2025 paper) for fast orthogonalization
# Only applies to 2D parameters (embeddings/final layer use AdamW)
```

### 3. Memory Optimization Techniques

**Location**: `nanochat/gpt.py`, `scripts/base_train.py`

**Summary**: Multiple techniques minimize memory footprint without sacrificing training fidelity.

**Key Techniques**:
1. **Vocabulary padding to 64**: Aligns with tensor core boundaries
2. **bfloat16 throughout**: Including embeddings and rotary embeddings
3. **Static graph compilation**: `torch.compile(model, dynamic=False)`
4. **Sliding window attention**: Earlier layers use half-context windows
5. **ReLU squared activation**: `x = F.relu(x).square()` instead of GELU
6. **No bias terms**: Removed from attention and most projections

**Memory Arena Configuration**:
```python
os.environ["PYTORCH_ALLOC_CONF"] = "expandable_segments:True"
```

### 4. Training Efficiency Pipeline

**Location**: `speedrun.sh`, `run1000.sh`

**Summary**: Multi-stage training (base -> mid -> SFT -> RL) with Chinchilla-optimal data ratios.

**Stage Details**:

| Stage | Purpose | Data | Key Hyperparameter |
|-------|---------|------|-------------------|
| Base | Language modeling | 370 shards (~54B chars) | token-param-ratio=20 |
| Mid | Capabilities (tools, MC, math) | Curated mixture (~850K rows) | BOS-aligned packing |
| SFT | Conversation adaptation | ~23K examples | Role-masked loss |
| RL | Task optimization | GSM8K | (optional) |

**Scaling Configuration**:
```bash
# $100 tier: 4 hours on 8xH100
--depth=20 --target-param-data-ratio=20

# $1000 tier: 42 hours on 8xH100
--depth=32 --model-dim=2048 --n-heads=16
# Results in ~1.88B parameters, 37.58B tokens
```

### 5. Learning Rate Scaling

**Location**: `scripts/base_train.py`

**Summary**: Implements batch-size-aware LR scaling following square root rule for Adam.

**Key Pattern**:
```python
batch_ratio = args.total_batch_size / reference_batch_size
batch_lr_scale = batch_ratio ** 0.5  # sqrt scaling for Adam/Muon

# Also model-size-aware scaling
model_scale = (model_dim / 768) ** -0.5
```

**Multi-phase Schedule**:
- Warmup: Linear ramp for first N% of steps
- Constant: Full learning rate
- Warmdown: Linear decay to final_lr_frac

### 6. Data Loading for Scaling

**Location**: `nanochat/dataloader.py`

**Summary**: Two loading strategies optimized for different training phases.

**Standard Loader**:
- Flat token buffer, slides window by B*T
- Simple, efficient for pure language modeling

**BOS-aligned Bestfit Packing**:
- Each batch row starts with BOS (conversation boundary)
- Best-fit algorithm packs documents to minimize cropping
- "100% utilization (no padding)" for conversation data
- Critical for mid-training and SFT where conversation structure matters

### 7. Evaluation Framework

**Location**: `nanochat/core_eval.py`, `tasks/`

**Summary**: Implements CORE evaluation from DCLM paper plus standard benchmarks.

**Task Types**:
- Multiple choice: ARC, MMLU with letter-after-choice formatting
- Generative: GSM8K, HumanEval
- Language modeling: Bits-per-byte loss

**Composition Strategies**:
- `TaskMixture`: Interleaved sampling with deterministic shuffle
- `TaskSequence`: Concatenated curriculum learning

---

## Architecture Notes

### Data Flow

```
Raw Text → BPE Tokenizer → Distributed DataLoader →
  → GPT Model (compiled) → Loss → Gradient Accumulation →
  → Distributed Optimizer → Parameter Update → Checkpoint
```

### Key Abstractions

| Component | Role |
|-----------|------|
| `GPTConfig` | Dataclass defining model dimensions |
| `CausalSelfAttention` | GQA with rotary embeddings, sliding window |
| `DistAdamW` | ZeRO-2 sharded AdamW optimizer |
| `DistMuon` | Orthogonalized momentum optimizer for matrices |
| `KVCache` | Flash Attention 3 compatible inference cache |
| `CheckpointManager` | Backward-compatible model persistence |

### Design Decisions

1. **No config factories**: Single cohesive codebase over configurability
   - Rationale: "avoid giant configuration objects, model factories, or if-then-else monsters"
   - Trade-off: Less flexible, but much easier to understand and modify

2. **Separate optimizers for parameter types**:
   - Embeddings: AdamW with low LR
   - 2D matrices: Muon with orthogonalization
   - Scalars: AdamW with very high LR
   - Rationale: Different parameter types benefit from different optimization dynamics

3. **Sliding window attention in early layers**:
   - Pattern: "L" (full) vs "S" (half-context) per layer
   - Rationale: Reduce compute in layers that primarily do local processing

4. **Per-layer learnable scalars** (`resid_lambdas`, `x0_lambdas`):
   - Learned residual stream scaling factors
   - Enables model to adjust information flow per layer

---

## Relevance to Lab Research

### The Core Insight: Idea Validation Scaling

The most important lesson from nanochat for our lab's "AI-Agent First" approach is the **mathematical equivalence between single-GPU and multi-GPU training**. This has profound implications:

**For Scaling Law Validation**:
1. Run experiments on 1 GPU for 8x longer to get identical loss curves
2. Validate that a hypothesis improves scaling before expensive multi-GPU runs
3. The relationship between loss, compute, and model size holds regardless of parallelization

**For Agent-Driven Research**:
- Agents can run single-GPU experiments to validate ideas quickly
- A "scaling law experiment" can be run overnight on 1 GPU instead of requiring 8xH100
- Fail-fast: If an idea doesn't improve the scaling curve on small scale, it won't at large scale

### Applicable Patterns for Video Retrieval

| nanochat Pattern | Video Retrieval Application |
|------------------|---------------------------|
| Gradient accumulation | Same technique works for video encoders; enables single-GPU ablations |
| Multi-stage training | Pretrain video encoder -> Fine-tune for retrieval -> Adapt for temporal |
| BOS-aligned packing | Video-text pair packing for contrastive learning efficiency |
| CORE evaluation framework | Modular eval system for retrieval benchmarks (MSR-VTT, DiDeMo, etc.) |
| Checkpoint backward compat | Long-running experiments with evolving architectures |
| Sliding window attention | Efficient long-video encoding with local + global attention |

### Potential Reuse

- [ ] Can adapt distributed optimizer pattern for video-language model training
- [ ] Can adapt evaluation framework for multi-benchmark video retrieval evaluation
- [ ] Can adapt checkpoint manager for fault-tolerant video experiments
- [ ] Can adopt "scaling law experiment" methodology for validating temporal reasoning hypotheses

### Learnings

1. **Mathematical equivalence is key**: The same gradients mean the same convergence, regardless of how you compute them. This is the foundation of cheap idea validation.

2. **Clean code enables rapid iteration**: The minimal, hackable design allows quick experimentation. No fighting with config systems.

3. **Multi-stage training is practical**: Base -> Mid -> SFT flow maps well to video-language: Pretrain encoder -> Alignment -> Retrieval fine-tuning.

4. **Evaluation discipline matters**: CORE framework plus modular tasks ensures rigorous measurement. We should adopt similar rigor.

5. **Memory optimization is essential**: Even with H100s, techniques like sliding window, bfloat16, and compiled graphs are necessary. Critical for video (larger tensors).

### Gaps or Limitations

- **LLM-specific**: Many patterns transfer, but video introduces spatial dimensions not addressed
- **No multi-modal**: Single modality (text); cross-modal alignment patterns would need to be added
- **Contrastive learning absent**: Video retrieval primarily uses contrastive objectives, not next-token prediction
- **Attention patterns**: Sliding window is temporal, but video needs spatial + temporal attention patterns

---

## Implications for "Idea Validation Scaling"

### The Key Principle

nanochat demonstrates that **compute can be traded for time with mathematical equivalence**. This is the foundation for rapid idea validation:

```
Hypothesis: "Adding X improves model quality"

Traditional approach:
  - Run full-scale experiment (8 GPUs, 4 hours, $100)
  - If wrong, $100 wasted

nanochat-inspired approach:
  - Run single-GPU experiment (1 GPU, 32 hours, ~$12)
  - Get IDENTICAL scaling curve
  - Only scale up if hypothesis validated
```

### Applying to Video Retrieval Research

**Temporal Reasoning Experiments**:
1. Train small video-language model on 1 GPU with gradient accumulation
2. Compare scaling curves: baseline vs temporal-enhanced architecture
3. If temporal architecture shows better compute-efficiency, scale up
4. If not, try next hypothesis

**Cross-Modal Alignment Experiments**:
1. Test contrastive objective variants on small scale
2. Validate that alignment quality scales predictably
3. Only commit expensive compute to validated approaches

**Efficiency Technique Validation**:
1. Test sparse attention, efficient video encoding on single GPU
2. Measure compute-quality trade-off
3. Scale winner to full benchmarks

### Recommended Lab Protocol

Inspired by nanochat's approach, we should adopt:

1. **Scaling Law Validation Stage**: Before any multi-GPU experiment, run single-GPU version to verify compute-efficiency improvement

2. **Gradient Accumulation Standard**: All training code should support arbitrary accumulation, enabling seamless single/multi-GPU switching

3. **Checkpoint Compatibility**: Design checkpoints to survive architecture changes (like nanochat's patching)

4. **Modular Evaluation**: Build task-based eval framework for video retrieval benchmarks

5. **Shell Script Experiments**: Document full experiments as reproducible shell scripts with all hyperparameters

---

## Cross-References

- **Paper Summary**: N/A (educational implementation)
- **Related Repos**: REPO-XXX (future: nanoGPT, llm.c)
- **Lab Papers Using**: Could inform any paper requiring training efficiency

---

## Code Snippets for Reference

### Gradient Accumulation Pattern (transferable)
```python
# Location: scripts/base_train.py
tokens_per_fwdbwd = device_batch_size * max_seq_len
world_tokens_per_fwdbwd = tokens_per_fwdbwd * ddp_world_size
grad_accum_steps = total_batch_size // world_tokens_per_fwdbwd

for micro_step in range(grad_accum_steps):
    x, y = next(dataloader)
    with torch.amp.autocast(device_type, dtype=torch.bfloat16):
        loss = model(x, y)
    loss = loss / grad_accum_steps
    loss.backward()
optimizer.step()
optimizer.zero_grad()
```

### Learning Rate Scaling (transferable)
```python
# Location: scripts/base_train.py
batch_ratio = total_batch_size / reference_batch_size
batch_lr_scale = batch_ratio ** 0.5  # sqrt scaling for Adam

def get_lr_multiplier(step):
    warmup_iters = round(warmup_ratio * num_iterations)
    warmdown_iters = round(warmdown_ratio * num_iterations)
    if step < warmup_iters:
        return (step + 1) / warmup_iters
    elif step <= num_iterations - warmdown_iters:
        return 1.0
    else:
        progress = (num_iterations - step) / warmdown_iters
        return progress + (1 - progress) * final_lr_frac
```

### Distributed Data Sharding (transferable)
```python
# Location: nanochat/dataloader.py
rg_idx = ddp_rank  # Each GPU starts at its rank
while rg_idx < num_row_groups:
    # Process row group
    yield row_group_data
    rg_idx += ddp_world_size  # Stride by world size
```
