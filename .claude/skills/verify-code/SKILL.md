---
name: verify-code
description: "Review experiment code before execution. Checks that code implements the spec correctly and is safe to run."
---

# Verify Code

Review experiment code to ensure it correctly implements the spec and is ready for execution.

## Usage

- `/verify-code EXP-XXX` - Verify code for experiment in current paper context
- `/verify-code EXP-XXX --paper <paper-name>` - Verify for specific paper
- `/verify-code papers/<paper>/src/expXXX/` - Verify by code path

## Workflow

### Step 1: Parse Arguments

Extract:
- **Experiment ID**: e.g., `EXP-001`
- **Paper name**: From `--paper` flag, path, or context
- **Code path**: Direct path or infer from experiment ID

### Step 2: Locate Code and Spec

Find:
```
papers/<paper>/src/expXXX/              (code directory)
papers/<paper>/experiment_stack/*/EXP-XXX-*.md  (spec)
```

If code not found, suggest running `/implement-experiment` first.

### Step 3: Launch Code Verifier Agent

Use the Task tool to launch the `code-verifier` agent:

```
Verify code for experiment EXP-XXX.

Paper: papers/<paper-name>/
Code path: papers/<paper-name>/src/expXXX/

Review the code against the experiment spec:

1. Read experiment spec to understand requirements
2. Read all code files (run.py, data.py, metrics.py, config.yaml)
3. Verify spec compliance:
   - Correct dataset and split
   - All required metrics implemented
   - Configuration matches spec
4. Check for issues:
   - Memory estimates vs requirements
   - Reproducibility (seeds, logging)
   - Error handling
   - Result persistence
5. Render verdict: READY or NEEDS REVISION

Arguments: $ARGUMENTS
```

### Step 4: Report Results

After the agent completes:
- Display verdict (READY / NEEDS REVISION)
- Summarize any issues found
- Provide next steps

## Examples

```
User: /verify-code EXP-001
Agent: Verdict: READY
       - Spec compliance: OK
       - Memory estimate: <1GB (safe)
       - Reproducibility: Seeds set, logging configured
       Next: /execute-experiment EXP-001
```

```
User: /verify-code EXP-002
Agent: Verdict: NEEDS REVISION
       Critical issue: similarity matrix materialization will OOM
       - Change compute_similarity() to use chunked computation
       Fix and re-verify before running.
```

## Verification Checklist

The agent checks:

1. **Spec Compliance**
   - Dataset matches spec
   - All metrics implemented
   - Configuration correct

2. **Memory Estimates**
   - Fits in target GPU memory
   - Large computations chunked

3. **Reproducibility**
   - Seeds set
   - Environment logged
   - Deterministic operations

4. **Result Persistence**
   - Results saved to JSON
   - Timestamps and IDs included
   - Checkpointing for long runs

5. **Error Handling**
   - Exceptions logged
   - Graceful failure modes

6. **Dependencies**
   - Imports are standard packages
   - No hidden dependencies

## Verdict Meanings

| Verdict | Meaning | Action |
|---------|---------|--------|
| READY | No critical issues | Proceed to `/execute-experiment` |
| NEEDS REVISION | Critical issues found | Fix issues, then re-verify |

## Notes

- Review depth scales with compute cost
- Assumes `/implement-experiment` was run first
- Uses Sonnet for efficient review
- Critical issues must be fixed before execution
- Moderate/minor issues are logged but don't block
