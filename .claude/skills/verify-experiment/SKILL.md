---
name: verify-experiment
description: "Verify experiment soundness before running. Questions assumptions about datasets, models, baselines, metrics, compute scale, and identifies potential issues or missing elements."
---

# Verify Experiment

Critical review of an experiment spec before execution. Acts as a devil's advocate to catch issues before compute is spent.

## Usage

- `/verify-experiment EXP-XXX` - Verify a specific experiment
- `/verify-experiment papers/idea-010-v-limit/experiment_stack/_inbox/EXP-001-*.md` - Verify by path

## What Gets Checked

### 1. Dataset Appropriateness
- Is this the right dataset for the hypothesis?
- Are there better alternatives?
- Is the split (train/val/test) appropriate?
- Any known dataset issues or biases?

### 2. Model & Method Selection
- Is this the right model architecture?
- Are there simpler alternatives that would work?
- Does the method actually test the hypothesis?
- Are hyperparameters reasonable?

### 3. Baseline Adequacy
- Are baselines appropriate and competitive?
- Missing any obvious baselines?
- Are baseline numbers sourced correctly?

### 4. Metric Correctness
- Do the metrics measure what we claim?
- Are we using standard evaluation protocols?
- Missing any important metrics?

### 5. Compute Scale
- Is the budget appropriate for the goal?
- Could this be run at smaller scale first?
- Is this over-engineered for a validation experiment?

### 6. Potential Issues
- Hidden assumptions that might not hold?
- Implementation pitfalls?
- Data leakage risks?
- Reproducibility concerns?

### 7. Simplification Opportunities
- Can any components be removed?
- Are we over-complicating the experiment?
- What's the minimal version that tests the hypothesis?

### 8. Missing Elements
- Dependencies not listed?
- Success criteria unclear?
- Missing ablations or controls?

## Workflow

### Step 1: Locate Experiment

Find the experiment spec in:
- `experiment_stack/_inbox/EXP-XXX-*.md`
- `papers/<name>/experiment_stack/_inbox/EXP-XXX-*.md`

### Step 2: Launch Experiment Verifier Agent

Use the Task tool to launch the `experiment-verifier` agent with the experiment path.

### Step 3: Report Verification Results

Output includes:
- **Verdict**: READY / NEEDS REVISION / BLOCKED
- **Issues Found**: Critical, moderate, minor
- **Questions to Resolve**: Assumptions that need validation
- **Suggested Changes**: Specific edits to the experiment spec

## Output Format

```markdown
## Experiment Verification: EXP-XXX

**Verdict**: READY / NEEDS REVISION / BLOCKED

### Critical Issues (must fix)
- [Issue description and suggested fix]

### Moderate Issues (should address)
- [Issue description and suggested fix]

### Minor Issues (nice to have)
- [Issue description and suggested fix]

### Questions to Resolve
1. [Assumption that needs validation]
2. [Decision that needs confirmation]

### Suggested Simplifications
- [What could be removed or simplified]

### Missing Elements
- [What should be added]

### Verdict Explanation
[Why the experiment is/isn't ready to run]
```

## Examples

```
User: /verify-experiment EXP-001
Agent: ## Experiment Verification: EXP-001
       **Verdict**: NEEDS REVISION

       ### Critical Issues
       - Baseline R@1 numbers from wrong paper version

       ### Questions to Resolve
       1. Should we use the full test set or the 1k subset?
```

## Notes

- Run verification BEFORE `/run-experiment start`
- Verification doesn't block execution - it's advisory
- For quick experiments (<2 GPU-hrs), lighter review is acceptable
- For expensive experiments (>8 GPU-hrs), thorough review recommended
