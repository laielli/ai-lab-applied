# Experiment: Temporal Query Classification Validation

- **ID**: EXP-009
- **Created**: 2026-01-24
- **Paper**: IDEA-009-temporal-fourier-signatures
- **Source**: SIM-003 (SME Q2)
- **Priority**: P2
- **Status**: queued

## Objective

Validate the keyword-based temporal query classification with human annotation to establish inter-annotator agreement and identify any selection bias.

## Hypothesis

Keyword-based classification has > 80% agreement with human annotation, and any disagreements will reveal missed temporal patterns (under-counting) rather than false positives (over-counting).

## Method

### Setup

- **Dataset**: MSR-VTT test queries (2000 total, 136 currently labeled temporal)
- **Sample**: Stratified sample of 200 queries (all 136 temporal + 64 random non-temporal)
- **Annotators**: Manual review (can use LLM as second annotator for agreement)

### Configuration

```yaml
sample_size: 200
stratification:
  current_temporal: all (136)
  current_non_temporal: random (64)
annotation_criteria:
  temporal: "Query requires understanding sequence order or temporal relationships"
  non_temporal: "Query can be answered from any single frame or unordered frames"
```

### Procedure

1. Extract 200 query sample (all labeled temporal + 64 random non-temporal)
2. Blind annotation round 1 (remove original labels)
3. Annotate each query as temporal/non-temporal with confidence
4. Compute agreement with keyword classification
5. Analyze disagreement cases
6. Optionally expand keyword list based on missed patterns

## Metrics

- **Primary**: Classification accuracy vs human labels
- **Secondary**: Precision/recall of keyword approach, missed temporal patterns

## Baselines

- Current keyword classification: 136/2000 = 6.8% temporal rate
- Expected after validation: Possibly higher if keywords under-count

## Compute Budget

- **Estimated time**: 2-4 hours manual annotation
- **Phase**: validation

## Success Criteria

- Agreement > 80% on temporal queries
- Identify any systematic bias in keyword approach
- Produce improved keyword list if needed

## Dependencies

- [x] MSR-VTT query list
- [x] Current keyword list
- [ ] Annotation interface (simple spreadsheet sufficient)
