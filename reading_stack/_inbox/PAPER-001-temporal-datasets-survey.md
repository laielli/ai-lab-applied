# Paper: Survey of Datasets with High Temporal Query Density

- **ID**: PAPER-001
- **Added**: 2026-01-24
- **Source**: SIM-004 (Lay Q2, Synthesis)
- **Status**: unread

## Why Read

Current TFS evaluation uses MSR-VTT (~7% temporal queries) and VATEX (~30% temporal queries). With such low density, detecting improvements on temporal queries is statistically difficult. We need to identify datasets with higher temporal query density for more robust evaluation.

**Key question**: Are there text-to-video retrieval datasets where >50% of queries require temporal reasoning?

## Focus Areas

- [x] Temporal Reasoning
- [x] Benchmark and Evaluation
- [ ] Cross-Modal Alignment
- [ ] Efficient Video Representation

## Datasets to Investigate

### Action Recognition Datasets (may have retrieval variants)

1. **ActivityNet Captions**
   - Long videos with dense captions
   - Likely higher temporal density due to activity descriptions
   - Check: Is there a retrieval benchmark?

2. **Charades**
   - Multi-action videos with compositional descriptions
   - Actions have temporal relationships
   - Check: Retrieval split exists?

3. **Something-Something V2**
   - Very temporal: "moving X from A to B"
   - But: Text queries are template-based
   - Check: Natural language retrieval version?

4. **COIN (Instructional videos)**
   - Step-by-step instructions
   - Inherently temporal (first do A, then B)
   - Check: Retrieval benchmark?

### Video QA Datasets (temporal reasoning focus)

5. **NExT-QA**
   - Explicitly tests temporal reasoning
   - Has "temporal" question category
   - Check: Can be adapted for retrieval?

6. **Temporal Reasoning QA (TRQ)**
   - Designed for temporal understanding
   - Check: Dataset availability?

### Dense Video Captioning Datasets

7. **YouCook2**
   - Cooking videos with step-by-step captions
   - Temporal structure in recipes
   - Check: Retrieval setup possible?

8. **ViTT (Video Timeline Tags)**
   - Dense temporal annotations
   - Check: Retrieval benchmark?

## Questions to Answer

1. What % of queries in each dataset require temporal reasoning?
2. Is there an existing retrieval benchmark, or do we need to create one?
3. What is the video domain (open-domain, cooking, sports, etc.)?
4. How many videos/queries? Is it large enough for reliable evaluation?
5. Are pre-extracted features available (to save compute)?

## Priority Assessment Criteria

| Criterion | Weight |
|-----------|--------|
| >50% temporal queries | High |
| Existing retrieval benchmark | High |
| Pre-extracted features available | Medium |
| Video domain overlap with MSR-VTT | Low |

## Deliverables

1. Summary table of datasets with temporal query density estimates
2. Recommendation for 1-2 datasets to add to TFS evaluation
3. Feasibility assessment (data access, compute requirements)

## Notes

If no suitable dataset exists with high temporal density, consider:
1. Creating a temporal subset from multiple datasets
2. Designing a synthetic temporal retrieval benchmark
3. Accepting that temporal retrieval is inherently a small-sample problem
