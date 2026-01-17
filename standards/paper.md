# Paper Standards

## Paper Requirements Document (PRD) Template

Each paper should have a PRD that includes:

1. **Research Question** — What problem are we solving?
2. **Hypothesis** — What do we expect to discover?
3. **Success Metrics** — How will we measure success?
4. **Target Venue** — Which conference/journal?
5. **Timeline** — Key milestones and deadlines

## Acceptance Criteria

- Novel contribution clearly articulated
- Experimental validation demonstrates claimed improvements
- Results are reproducible
- Writing is clear and follows venue guidelines

## Computational Efficiency Requirements

Every paper PRD must include a compute strategy that follows the lab's scaling methodology.

### Required in PRD

1. **Single-GPU Validation Strategy**
   - How will the core hypothesis be tested in <8 GPU-hours?
   - What metrics will indicate go/no-go for full experiments?

2. **Scaling Prediction Methodology**
   - What scaling curve will be traced during validation?
   - How will small-scale results predict full-scale outcomes?

3. **Compute Budget by Phase**
   | Phase | GPU-Hours | Deliverable |
   |-------|-----------|-------------|
   | Validation | <8 | Proof of concept |
   | Ablations | <24 | Component analysis |
   | Full experiments | (estimate) | Paper-quality results |

### Rationale

This ensures:
- Ideas are validated cheaply before major compute investment
- Failed hypotheses are identified early (fail fast, fail cheap)
- Compute resources are allocated to promising directions
- Agent-driven experimentation can run autonomously

See `standards/ml.md` for detailed scaling law methodology.