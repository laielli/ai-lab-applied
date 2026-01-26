# Figure Request: Order Preservation Intuition Diagram

- **ID**: FIG-003
- **Requested**: 2026-01-24
- **Paper**: IDEA-009-temporal-fourier-signatures
- **Experiment**: N/A (conceptual)
- **Source**: SIM-003 (Lay Q1)
- **Priority**: P2
- **Status**: requested

## Figure Type

- [ ] Line plot (training curves, ablations)
- [ ] Bar chart (method comparisons)
- [ ] Scatter plot (correlation analysis)
- [ ] Heatmap (attention, confusion matrix)
- [ ] Table (results, ablations)
- [x] Diagram (architecture, workflow)
- [ ] Other: [describe]

## Data Source

- **Location**: Conceptual diagram (no data source)
- **Data format**: N/A
- **Columns/fields**: N/A

## Specification

### Content

A visual explanation of how TFS preserves temporal order through rotation-based encoding. Should convey the core intuition without mathematical notation:

1. **Left panel**: Mean pooling loses order
   - Show 3 frame embeddings as arrows
   - Show average as single arrow
   - Show that permuting frames gives same average

2. **Right panel**: TFS preserves order
   - Show same 3 frame embeddings
   - Show rotation applied to each (different angle per position)
   - Show final average depends on rotation pattern
   - Show that permuting frames gives DIFFERENT average

Key insight: "The rotation pattern acts as a fingerprint of sequence order"

### Axes/Labels

- **Panels**: "Mean Pooling" vs "TFS (Ours)"
- **Arrows**: Label frames as "Frame 1", "Frame 2", "Frame 3"
- **Rotations**: Show rotation angles visually (curved arrows or theta symbols)
- **Results**: "Same output" vs "Different output" for permutation

### Visual Requirements

- **Color scheme**: colorblind-safe (use Wong palette)
- **Font size**: paper-ready
- **Dimensions**: full page width (6.5" x 3.5")
- **Style**: Clean, minimal, no 3D effects

## Output Formats Needed

- [x] Paper figure (PDF, LaTeX labels, column-width)
- [x] Presentation slide (PNG, larger fonts)
- [x] Stand-alone image (SVG for editing)
- [ ] LaTeX table (booktabs style)

## Reference

Similar in spirit to:
- Transformer positional encoding visualizations
- RoPE (Rotary Position Embedding) diagrams
- "Before/After" comparison figures in method papers

## Notes

This figure is critical for accessibility and reviewer understanding. The mathematical formulation is precise but abstract; this visual should make the intuition immediately graspable. Consider animation potential for presentations (frames rotating one by one).
