# Figure Request: Layer Probing Accuracy Curve

- **ID**: FIG-004
- **Requested**: 2026-01-24
- **Paper**: idea-003-avg-pooling
- **Experiment**: Exp 3.1 (Intermediate Layer Temporal Probing)
- **Source**: SIM-005 (SME Q3)
- **Priority**: P2
- **Status**: requested

## Figure Type

- [x] Line plot (training curves, ablations)
- [ ] Bar chart (method comparisons)
- [ ] Scatter plot (correlation analysis)
- [ ] Heatmap (attention, confusion matrix)
- [ ] Table (results, ablations)
- [ ] Diagram (architecture, workflow)
- [ ] Other

## Data Source

- **Location**: Exp 3.1 results (to be formatted)
- **Data format**: inline

```csv
layer,accuracy
0,52.0
1,62.9
8,63.6
10,64.3
11,64.0
15,55.6
17,51.7
19,60.0
23,57.4
```

## Specification

### Content

Show temporal ordering probe accuracy across PE transformer layers. Key insight: accuracy peaks at layer 10 (~64%) and decays to ~57% at output layer 23. This visualizes the "temporal information loss" phenomenon.

Highlight:
- Layer 10 as peak (annotate)
- Layer 23 as output (annotate)
- Random baseline at 50% (dashed line)

### Axes/Labels

- **X-axis**: Layer index (0-23)
- **Y-axis**: Validation Accuracy (%)
- **Legend**: None needed (single series)
- **Annotations**: "Peak" at layer 10, "Output" at layer 23, "Random" baseline line

### Visual Requirements

- **Color scheme**: colorblind-safe (single color for line, distinct for baseline)
- **Font size**: paper-ready
- **Dimensions**: column width (3.25" x 2.5")
- **Error bars**: Add once bootstrap CIs available (placeholder for now)

## Output Formats Needed

- [x] Paper figure (PDF, LaTeX labels, column-width)
- [x] Presentation slide (PNG, larger fonts)
- [ ] Stand-alone image (SVG for editing)
- [ ] LaTeX table

## Additional Notes

- Consider shading the region between peak and output to emphasize the gap
- May need to add more layers to the curve if additional probing is done
- Error bars are critical for publication - placeholder without them for now
