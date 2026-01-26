# Experiment: Temporal Query Classifier Validation

- **ID**: EXP-013
- **Created**: 2026-01-24
- **Paper**: IDEA-009-temporal-fourier-signatures
- **Idea**: IDEA-009
- **Priority**: P2
- **Status**: queued
- **Source**: SIM-004 (SME Q2)

## Objective

Manually validate the accuracy of the keyword-based temporal query classifier used in TFS experiments. Determine if the classifier correctly identifies queries that require temporal reasoning.

## Hypothesis

The current keyword-based classifier has moderate accuracy (~70-80%) but misses implicit temporal queries (false negatives) and incorrectly flags non-temporal uses of temporal words (false positives).

## Method

### Setup

- **Dataset**: MSR-VTT test split (1000 captions)
- **Classifier**: Current keyword-based approach
- **Annotator**: Manual review of sample

### Current Classifier Definition

```python
TEMPORAL_KEYWORDS = [
    "first", "then", "finally", "before", "after",
    "while", "begins", "ends", "starts", "stops",
    "initially", "eventually", "next", "later"
]

def is_temporal(caption):
    return any(kw in caption.lower() for kw in TEMPORAL_KEYWORDS)
```

### Configuration

```yaml
# Sampling
total_queries: 1000
sample_size: 100  # Manual review is time-consuming
sampling_strategy: "stratified"  # 50 classified-temporal, 50 classified-non-temporal

# Annotation
annotator: "researcher"
annotation_guide:
  temporal: "Query requires understanding when events occur or their order"
  non_temporal: "Query can be answered by identifying presence of objects/actions"
```

### Procedure

1. **Sample selection**:
   - 50 queries classified as "temporal" by keyword method
   - 50 queries classified as "non-temporal" by keyword method

2. **Manual annotation**:
   For each query, answer:
   - Does this query require temporal reasoning to answer correctly?
   - If misclassified, what type of error? (FP/FN)
   - What keyword (if any) caused the classification?

3. **Compute metrics**:
   - Precision: True temporal / Classified temporal
   - Recall: True temporal / All temporal (estimated from sample)
   - F1 score

4. **Error analysis**:
   - Categorize false positives (e.g., "then" used non-temporally)
   - Categorize false negatives (e.g., implicit temporal structure)

### Example Classifications

**True Positive** (correctly identified as temporal):
- "A person first opens the door, then enters the room"
- Classification: temporal (keyword: "first", "then")
- Ground truth: temporal (requires order understanding)

**False Positive** (incorrectly identified as temporal):
- "The chef then adds some salt"
- Classification: temporal (keyword: "then")
- Ground truth: non-temporal (single action, "then" is filler word)

**False Negative** (missed temporal query):
- "A car drives up and parks"
- Classification: non-temporal (no keywords)
- Ground truth: temporal (requires understanding sequence of driving then parking)

**True Negative** (correctly identified as non-temporal):
- "A dog plays in the grass"
- Classification: non-temporal
- Ground truth: non-temporal

## Metrics

- **Primary**: Precision, Recall, F1 for temporal classification
- **Secondary**: Error type distribution (FP types, FN types)
- **Confidence interval**: Bootstrap 95% CI on sample estimates

## Success Criteria

**Classifier is acceptable if**:
- Precision > 0.70 (at least 70% of flagged queries are truly temporal)
- Recall > 0.50 (captures at least half of temporal queries)

**Classifier needs improvement if**:
- Precision < 0.50 (too many false positives)
- Recall < 0.30 (missing too many temporal queries)

## Compute Budget

- **Annotation time**: ~2-3 hours (100 queries at ~1-2 min each)
- **Compute**: Negligible (text processing only)
- **Phase**: validation

## Dependencies

- [x] MSR-VTT captions file
- [x] Current classifier implementation
- [ ] Annotation spreadsheet template

## Implications for TFS Project

If classifier accuracy is low:
1. TFS results may be measuring something other than temporal reasoning
2. Need to improve classifier or use different evaluation approach
3. May explain inconsistent results across seeds (noisy labels)

If classifier accuracy is high:
1. Current evaluation methodology is sound
2. Focus should be on feature quality, not classification

## Deliverables

1. Annotated sample spreadsheet (100 queries)
2. Precision/Recall/F1 estimates with confidence intervals
3. Error analysis report (common FP and FN patterns)
4. Recommended classifier improvements (if needed)
