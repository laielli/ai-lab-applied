# Figure Request: Temporal Attention Visualization

- **ID**: FIG-001
- **Created**: 2026-01-23
- **Source**: SIM-001 (Advisor Q2)
- **Priority**: P1
- **Status**: pending

## Request

Create qualitative visualization showing learned temporal attention patterns for different query types.

## Specifications

1. **Figure Type**: Multi-panel visualization (4-6 examples)
2. **Content per panel**:
   - Video frames (8-16 sampled frames as thumbnails)
   - Attention weights as bar chart or heatmap overlay
   - Query text
   - Highlighted frame(s) with peak attention
3. **Example selection**:
   - 2 action queries (e.g., "person picks up object")
   - 2 scene/state queries (e.g., "outdoor sunny day")
   - 2 complex queries (e.g., "man walks to car then drives away")
4. **Comparison**: Show how different queries produce different attention patterns on same video

## Purpose

Demonstrates that the model learns meaningful query-conditioned attention, not just static saliency. Key evidence for the "query-specific temporal structure" insight. Essential for elevating the contribution from incremental to insightful.

## Technical Requirements

- Extract attention weights from trained model
- Select examples that clearly illustrate the phenomenon
- Ensure high visual quality for publication
