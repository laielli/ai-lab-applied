# Figure Request: Video Retrieval Benchmark Sparsity Comparison

- **ID**: FIG-002
- **Requested**: 2026-01-24
- **Paper**: idea-010-v-limit
- **Experiment**: EXP-001, EXP-006
- **Priority**: P1
- **Status**: completed
- **Source**: SIM-002 SME Q3, Lay Q1

## Figure Type

- [x] Bar chart (method comparisons)
- [x] Line plot (threshold sensitivity)
- [ ] Scatter plot (correlation analysis)
- [ ] Heatmap (attention, confusion matrix)
- [ ] Table (results, ablations)
- [ ] Diagram (architecture, workflow)
- [ ] Other

## Data Source

- **Location**:
  - EXP-001 results (MSR-VTT, ActivityNet, PE-Video)
  - EXP-006 results (DiDeMo, VATEX) - pending
- **Data format**: Inline from experiment results
- **Columns/fields**: dataset, d_tripartite, num_queries, num_videos

## Specification

### Content

Two-panel figure showing:

**Panel A: Ground-Truth Sparsity Comparison**
- Bar chart comparing d_tripartite across video benchmarks (MSR-VTT, ActivityNet, DiDeMo, VATEX)
- Include LIMIT text benchmark reference values (0.05-0.20 range) as horizontal band
- Key insight: Video benchmarks are 10-100x sparser than text benchmarks

**Panel B: CLIP-Perceived Density by Threshold**
- Line plot showing d_tripartite vs similarity threshold (tau)
- X-axis: tau from 0.70 to 0.95
- Y-axis: d_tripartite (log scale)
- Include both original and shuffled lines (should overlap to demonstrate domain-driven similarity)
- Key insight: Even at loose thresholds, video density remains far below text benchmarks

### Axes/Labels

**Panel A:**
- X-axis: Dataset
- Y-axis: d_tripartite (log scale)
- Legend: Video benchmarks (bars) vs LIMIT text range (shaded band)

**Panel B:**
- X-axis: Similarity threshold (tau)
- Y-axis: d_tripartite (log scale)
- Legend: Original pairings vs Shuffled pairings

### Visual Requirements

- **Color scheme**: colorblind-safe (Wong palette)
- **Font size**: paper-ready (10pt)
- **Dimensions**: Full page width (6.5" x 2.5" for two-panel)

## Output Formats Needed

- [x] Paper figure (PDF, LaTeX labels, full-width)
- [x] Presentation slide (PNG, larger fonts)
- [ ] Stand-alone image (SVG for editing)
- [ ] LaTeX table (booktabs style)

## Reference

- LIMIT paper Figure 2 (sparsity comparison) for style reference
- Use log scale on y-axis to show differences clearly

## Notes

- Wait for EXP-006 results before generating Panel A
- Panel B can be generated immediately from EXP-001 results
- Caption should emphasize: "Video retrieval benchmarks are 10-100x sparser than text benchmarks"
