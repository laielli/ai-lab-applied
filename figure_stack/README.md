# Figure Stack

A system for generating figures from experiment results, including plots, charts, diagrams, and tables in various formats (paper, slides, stand-alone).

## Purpose

- **_inbox/**: Figure requests waiting to be generated
- **figures/**: Completed figures in multiple formats

## Directory Structure

```
figure_stack/
├── _inbox/      # Figure requests to process
└── figures/     # Generated figure packages
```

## Workflow

```
Experiment results → _inbox/FIG-XXX.md (request)
         ↓
Generate figure → figures/FIG-XXX/
         ↓
Output formats:
  • papers/<name>/paper/figures/  (paper-ready PDF)
  • papers/<name>/presentation/   (slides PNG)
  • stand-alone images            (PNG, PDF, SVG)
```

---

## Entry Formats

### _inbox/ Format

Figure request specification. Filename: `FIG-XXX-[short-name].md`

```markdown
# Figure Request: [Short Descriptive Name]

- **ID**: FIG-XXX
- **Requested**: YYYY-MM-DD
- **Paper**: [paper-name] (if applicable)
- **Experiment**: EXP-XXX (source experiment)
- **Priority**: P0/P1/P2/P3
- **Status**: requested

## Figure Type

- [ ] Line plot (training curves, ablations)
- [ ] Bar chart (method comparisons)
- [ ] Scatter plot (correlation analysis)
- [ ] Heatmap (attention, confusion matrix)
- [ ] Table (results, ablations)
- [ ] Diagram (architecture, workflow)
- [ ] Other: [describe]

## Data Source

- **Location**: experiment_stack/results/EXP-XXX.md
- **Data format**: [CSV, JSON, inline]
- **Columns/fields**: [list relevant fields]

## Specification

### Content

[What should the figure show? What is the key insight?]

### Axes/Labels

- **X-axis**: [label, units]
- **Y-axis**: [label, units]
- **Legend**: [entries to include]

### Visual Requirements

- **Color scheme**: [default | colorblind-safe | grayscale | custom]
- **Font size**: [default: paper-ready]
- **Dimensions**: [width x height in inches]

## Output Formats Needed

- [ ] Paper figure (PDF, LaTeX labels, column-width)
- [ ] Presentation slide (PNG, larger fonts)
- [ ] Stand-alone image (SVG for editing)
- [ ] LaTeX table (booktabs style)

## Reference

[Link to similar figures or style examples]
```

### figures/ Format

Generated figure package. Directory: `figures/FIG-XXX-[short-name]/`

```
figures/FIG-XXX-[short-name]/
├── README.md           # Figure metadata and usage
├── fig_paper.pdf       # Paper-ready figure
├── fig_paper.tex       # LaTeX code (tables, TikZ)
├── fig_slides.png      # Presentation version (PNG)
├── fig_standalone.svg  # Stand-alone vector
├── slide.tex           # Beamer slide with caption
├── slide.pdf           # Rendered beamer slide
├── data.csv            # Source data
└── generate.py         # Generation script
```

**README.md format:**

```markdown
# Figure: [Title]

- **ID**: FIG-XXX
- **Created**: YYYY-MM-DD
- **Paper**: [paper-name]
- **Experiment**: EXP-XXX

## Description

[What this figure shows and why it matters]

## Files

| File | Format | Use Case |
|------|--------|----------|
| fig_paper.pdf | PDF | Paper submission |
| fig_paper.tex | LaTeX | Tables, editable source |
| fig_slides.png | PNG | Inline in presentations |
| slide.tex | LaTeX | Beamer slide with caption |
| slide.pdf | PDF | Ready-to-present slide |
| fig_standalone.svg | SVG | Web, editing |

## Usage in Paper (LaTeX)

\```latex
\begin{figure}[t]
    \centering
    \includegraphics[width=\columnwidth]{figures/FIG-XXX/fig_paper.pdf}
    \caption{[Caption text]}
    \label{fig:XXX}
\end{figure}
\```

## Usage in Presentation

Option 1: Use `slide.pdf` directly (standalone beamer slide with caption)
Option 2: Include `fig_slides.png` in your own slide deck

## Regeneration

\```bash
python generate.py
\```

## Data Source

Experiment: EXP-XXX
```

---

## Figure Types

### Plots (Matplotlib/Seaborn)

| Type | Use Case |
|------|----------|
| Line plot | Training curves, scaling laws |
| Bar chart | Method comparisons, ablations |
| Scatter plot | Correlation, embedding visualization |
| Heatmap | Attention weights, confusion matrices |
| Box plot | Distribution comparisons |

### Tables (LaTeX)

| Type | Use Case |
|------|----------|
| Results table | Main benchmark comparisons |
| Ablation table | Component contribution analysis |
| Statistics table | Dataset characteristics |

### Diagrams

| Type | Use Case |
|------|----------|
| Architecture | Model structure (TikZ, draw.io) |
| Method overview | High-level approach |
| Pipeline | Data flow visualization |

---

## Style Guidelines

### Paper Figures

```python
# Matplotlib settings for paper-ready figures
plt.rcParams.update({
    'font.size': 10,
    'font.family': 'serif',
    'figure.figsize': (3.25, 2.5),  # Column width
    'figure.dpi': 300,
    'axes.labelsize': 10,
    'legend.fontsize': 8,
    'xtick.labelsize': 8,
    'ytick.labelsize': 8,
})
```

- **Size**: Column width (3.25") or full width (6.5")
- **Format**: PDF (vector)
- **Font**: Serif, matching paper
- **Colors**: Colorblind-safe palette

### Presentation Figures

```python
# Matplotlib settings for slides
plt.rcParams.update({
    'font.size': 18,
    'font.family': 'sans-serif',
    'figure.figsize': (10, 6),
    'figure.dpi': 150,
})
```

- **Size**: 16:9 aspect ratio
- **Format**: PNG (raster)
- **Font**: Sans-serif, large
- **Colors**: High contrast

### Tables (LaTeX)

```latex
\begin{table}[t]
\centering
\caption{Main Results}
\label{tab:main}
\begin{tabular}{lcccc}
\toprule
Method & R@1 & R@5 & R@10 & MedR \\
\midrule
Baseline & 42.1 & 71.3 & 82.5 & 2.0 \\
\textbf{Ours} & \textbf{45.3} & \textbf{74.1} & \textbf{85.2} & \textbf{2.0} \\
\bottomrule
\end{tabular}
\end{table}
```

- **Style**: Booktabs (no vertical lines)
- **Bold**: Best results
- **Precision**: Consistent decimals

### Beamer Slides (LaTeX)

Each figure generates a standalone beamer slide with descriptive caption:

**slide.tex:**
```latex
\documentclass[aspectratio=169]{beamer}
\usetheme{default}
\usecolortheme{default}

% Minimal beamer setup
\setbeamertemplate{navigation symbols}{}
\setbeamertemplate{footline}{}

\usepackage{graphicx}
\usepackage{booktabs}

\begin{document}

\begin{frame}{[Figure Title]}
    \centering
    \includegraphics[width=0.85\textwidth]{fig_paper.pdf}

    \vspace{0.5em}
    \small
    [Descriptive caption explaining the figure, key insights, and takeaways.
    This should be 1-3 sentences that help the audience understand what they're seeing.]
\end{frame}

\end{document}
```

**To render:**
```bash
pdflatex slide.tex
```

- **Aspect ratio**: 16:9 (aspectratio=169)
- **Caption**: Descriptive, explains the insight (not just "Results table")
- **Figure size**: 85% of text width for good margins

---

## Color Palettes

### Colorblind-Safe (Recommended)

```python
# Wong palette
colors = ['#0072B2', '#E69F00', '#009E73', '#CC79A7', '#F0E442', '#56B4E9']
```

### Method Comparison

```python
# Baseline vs Ours
colors = {'baseline': '#888888', 'ours': '#0072B2'}
```

---

## ID Conventions

- Figures: `FIG-001`, `FIG-002`, etc.
- Paper-specific: `FIG-<paper>-001` (e.g., `FIG-temporal-001`)
- IDs persist through the lifecycle

---

## Integration with Other Stacks

### From experiment_stack

Experiment results provide data:
- Metrics from `experiment_stack/results/EXP-XXX.md`
- Training logs for curves
- Ablation results for comparison

### To papers/

Generated figures integrate into papers:
- Copy PDF to `papers/<name>/paper/figures/`
- Copy PNG to `papers/<name>/presentation/`

### To lab_meeting_stack

Presentation-format figures for meetings:
- Use `fig_slides.png` versions
- Higher contrast, larger labels

---

## Best Practices

1. **Reproducibility**: Always include `generate.py` and `data.csv`
2. **Multiple formats**: Generate paper, slides, and stand-alone
3. **Consistent style**: Use templates across figures
4. **Colorblind-safe**: Accessible palettes by default
5. **Vector for paper**: PDF preserves quality at any scale
6. **Label clearly**: Self-explanatory axes and legends
