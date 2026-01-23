# Repo: nanochat

- **ID**: REPO-001
- **GitHub**: https://github.com/karpathy/nanochat
- **Paper**: N/A (educational/reference implementation)
- **Added**: 2026-01-17
- **Status**: reviewed
- **Summary**: code_stack/summaries/REPO-001-nanochat.md

## Why Review

While nanochat focuses on LLM training rather than text-to-video retrieval, it offers valuable insights for lab research in several areas:

1. **Cross-modal training pipeline**: The multi-stage training approach (pretraining → midtraining → SFT) could inform video-language model fine-tuning strategies
2. **Efficient inference**: KV cache implementation and efficient attention mechanisms are relevant for scaling video retrieval systems
3. **Evaluation framework**: The modular task system for multi-benchmark evaluation aligns with lab standards for rigorous evaluation
4. **Foundation model utilization**: Demonstrates practical approach to building on existing architectures, consistent with lab strategy of leveraging foundation models rather than pretraining from scratch
5. **Code quality reference**: High-quality, minimal, hackable codebase serves as a standard for clean ML implementations

The repository has 40.4k stars and is actively maintained by Andrej Karpathy, representing production-quality educational code.

## Key Methods to Understand

- [x] Multi-stage training pipeline (pretraining → SFT → RL)
- [x] Efficient inference engine with KV cache (`engine.py`)
- [x] Distributed training setup across 8 GPUs
- [x] Custom optimizer implementations (`adamw.py`, `muon.py`)
- [x] Modular evaluation task system
- [x] Checkpoint management for fault tolerance
- [ ] Web-based deployment architecture (skipped - not relevant to lab)

## Initial Notes

**Tech Stack**:
- Python 74.9%, PyTorch-based
- Model: GPT-style Transformer, 200M-2.2B parameters
- Distributed training: torchrun + PyTorch DDP
- 251 commits, 39 contributors

**Architecture**:
- Core model in `gpt.py`
- Scalable depth (d20 to d34 configurations)
- Custom BPE tokenizer
- Modular task evaluation system

**Deployment**:
- Web UI (`ui.html`) with Python HTTP server
- CLI and streaming inference support
- Live demo at nanochat.karpathy.ai

**Quality Indicators**:
- Pytest test suite
- Clean, minimal, dependency-lite design
- Comprehensive documentation
- Active development (last updated Jan 16, 2026)

**Potential Relevance**:
- Training methodology for video-language models
- Efficient attention/inference patterns for video retrieval
- Multi-benchmark evaluation framework design
- Code organization and quality standards
