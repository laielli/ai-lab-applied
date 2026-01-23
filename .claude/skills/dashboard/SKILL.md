---
name: dashboard
description: "Update dashboard snapshots for idea_stack and papers. Use to get a quick overview of research portfolio status with evaluation scores."
---

# Dashboard

Update status dashboards for ideas and papers with evaluation scores.

## Usage

- `/dashboard` - Update all dashboards (ideas + papers)
- `/dashboard --ideas` - Update only idea_stack/DASHBOARD.md
- `/dashboard --papers` - Update only papers/DASHBOARD.md

## Workflow

### Step 1: Launch Dashboard Agent

Use the Task tool to launch a general-purpose agent with this prompt:

```
Update research portfolio dashboards.

## Scope
$ARGUMENTS (or "all" if empty)

## For Ideas (idea_stack/)

1. Scan all stages: _inbox/, developing/, ready/
2. For each idea, evaluate (1-5 scale):
   - **Novelty**: 1=incremental, 3=new combination, 5=fundamentally new
   - **Impact**: 1=minor gain, 3=notable contribution, 5=shifts field
   - **Scoop Risk**: 1=low competition, 3=moderate, 5=hot topic race
3. Check stage readiness:
   - inbox→developing: clear research question + approach?
   - developing→ready: testable hypothesis + experiment plan + novelty argument?
4. Update idea_stack/DASHBOARD.md

## For Papers (papers/)

1. Scan each paper directory
2. Read STATUS.md, README.md, or prd/paper_requirements.md
3. Evaluate (1-5 scale):
   - **Novelty**: 1=incremental, 5=best paper potential
   - **Impact**: 1=workshop, 3=main conf, 5=oral potential
   - **Scoop Risk**: 1=unique, 5=race condition
   - **Cost**: 1=>500 GPU-hrs, 3=100-500, 5=<100 GPU-hrs
   - **Time**: 1=>6 months, 3=2-4 months, 5=<2 months
4. Update papers/DASHBOARD.md

## Dashboard Format

Use tables with scores, recommendations section, and scoop watch for high-risk items.

Report: items evaluated, key recommendations, items needing attention.
```

### Step 2: Report Results

After the agent completes, summarize:
- Dashboard files updated
- Total ideas/papers evaluated
- Top priority recommendations
- Any scoop risks flagged

## Evaluation Criteria

### Ideas

| Score | Novelty | Impact | Scoop Risk |
|-------|---------|--------|------------|
| 5 | Fundamentally new | Could shift field | Hot topic, high risk |
| 3 | New combination | Notable contribution | Active area |
| 1 | Incremental | Minor gain | Low competition |

### Papers

Same as ideas, plus:

| Score | Cost (GPU-hrs) | Time to Completion |
|-------|----------------|-------------------|
| 5 | <100 | <2 months |
| 3 | 100-500 | 2-4 months |
| 1 | >500 | >6 months |

## Output Files

- `idea_stack/DASHBOARD.md` - Idea portfolio overview
- `papers/DASHBOARD.md` - Paper portfolio overview

## Notes

- Dashboards are point-in-time snapshots
- Run regularly to track progress
- High scoop risk (≥4) items flagged for acceleration
- Scores are subjective estimates—use for relative prioritization
