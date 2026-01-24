# Experiment: d_tripartite Analysis for DiDeMo and VATEX

- **ID**: EXP-006
- **Created**: 2026-01-24
- **Paper**: idea-010-v-limit
- **Priority**: P1
- **Status**: queued
- **Source**: SIM-002 Advisor Q1

## Objective

Extend the d_tripartite sparsity analysis from EXP-001 to two additional video retrieval benchmarks (DiDeMo, VATEX) to strengthen the universality claim for the V-LIMIT paper.

## Hypothesis

DiDeMo and VATEX will show similarly sparse relevance patterns (d_tripartite < 0.01) as MSR-VTT (0.001) and ActivityNet (0.0002), confirming that sparsity is a universal property of current video retrieval benchmarks rather than dataset-specific.

## Method

### Setup

- **Datasets**: DiDeMo, VATEX
- **Analysis**: Ground-truth d_tripartite computation (same as EXP-001 Part A)
- **Hardware**: CPU only (annotation file processing)

### Procedure

1. Download DiDeMo annotation files from official release
2. Download VATEX annotation files from official release
3. Parse query-video relevance mappings
4. Compute d_tripartite = (relevant pairs) / (queries x videos)
5. Report alongside MSR-VTT and ActivityNet results

## Metrics

- **Primary**: d_tripartite value
- **Secondary**: Number of queries, videos, query-video pairs, structure (1:1, 1:N, M:N)

## Baselines

- MSR-VTT: d_tripartite = 0.001 (from EXP-001)
- ActivityNet: d_tripartite = 0.0002 (from EXP-001)

## Compute Budget

- **Estimated time**: <1 hour (annotation processing only)
- **Phase**: validation (<8h)

## Success Criteria

- Both DiDeMo and VATEX show d_tripartite < 0.01
- Results provide 4+ benchmark data points for universality claim

## Dependencies

- [ ] DiDeMo annotation files available
- [ ] VATEX annotation files available
- [ ] d_tripartite computation code from EXP-001
