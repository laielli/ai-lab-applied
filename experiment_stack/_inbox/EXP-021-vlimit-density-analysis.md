# Experiment: V-LIMIT Density Distribution Analysis

- **ID**: EXP-021
- **Paper**: idea-010-v-limit
- **Status**: inbox
- **Source**: SIM-007 (SME Q1, Q2, Q5)
- **Priority**: P2

## Objective

Characterize the density and similarity distributions in the current V-LIMIT benchmark to validate experimental conditions match the intended "uniformly high semantic similarity" scenario from the original LIMIT paper.

## Background

SME questions from SIM-007 raised concerns that d=0.173 may be too low and that template-based queries may not represent real retrieval scenarios. This analysis provides the diagnostic data needed to validate or revise the benchmark.

## Analyses

### 1. Density Distribution Characterization
- Compute histogram of query-caption density values
- Report mean, median, std, min, max
- Compare against estimated LIMIT paper density range

### 2. Synthetic vs Real Query Comparison
- Download MSR-VTT or ActivityNet test queries
- Compare token length distributions
- Compare vocabulary overlap statistics
- Assess lexical diversity (type-token ratio)

### 3. Pairwise Similarity Matrix
- Compute CLIP similarity for all query-video pairs
- Analyze distribution: Is it "uniformly high" or spread out?
- Identify if there are easy vs hard queries skewing results

### 4. BM25 Score Distribution
- Compute BM25 scores for all query-video pairs
- Compare distribution shape to CLIP similarities
- Look for regime where scores become saturated

## Deliverables

1. Density histogram figure (route to figure_stack if needed)
2. Statistical summary table
3. Comparison table: synthetic vs real query statistics
4. Similarity heatmap or distribution plot
5. Recommendations for benchmark revision if issues found

## Estimated Time

- Analysis code: 2 hours
- Compute: 1 hour (mostly CLIP encoding already cached)
- Writeup: 1 hour

## Success Criteria

- Clear documentation of current benchmark properties
- Identification of any validity threats
- Specific recommendations for EXP-020 benchmark construction

## Dependencies

- EXP-002 benchmark data (available)
- MSR-VTT or ActivityNet queries for comparison (download required)
