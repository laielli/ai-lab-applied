# Writing Standards

Guidelines for writing research papers, with focus on text-to-video retrieval and vision-language research.

## Paper Structure

### Abstract (150-250 words)

Structure: Context → Problem → Approach → Results → Impact

```
[1-2 sentences: Context and motivation]
[1 sentence: Specific problem addressed]
[2-3 sentences: Our approach and key insight]
[1-2 sentences: Main results with numbers]
[1 sentence: Broader impact or availability]
```

**Checklist:**
- [ ] States the problem clearly
- [ ] Highlights the key insight/contribution
- [ ] Includes concrete performance numbers
- [ ] Mentions benchmarks by name

### Introduction (1-1.5 pages)

**Paragraph structure:**
1. **Hook**: Why does this problem matter? (broad motivation)
2. **Problem**: What specific challenge are we addressing?
3. **Gap**: What's missing in current approaches?
4. **Insight**: What's our key observation/idea?
5. **Approach**: How do we address it? (high-level)
6. **Results**: What did we achieve? (preview key numbers)
7. **Contributions**: Bullet list of 3-4 contributions

**Common pitfalls:**
- Starting with "Recently, ..." (overused)
- Vague motivation ("Video understanding is important")
- Listing contributions that aren't novel

### Related Work (1-1.5 pages)

**Organization options:**
1. **By approach**: Group methods by technique (attention-based, contrastive, etc.)
2. **By problem**: Group by subproblem (temporal modeling, cross-modal alignment, etc.)
3. **Chronological**: For rapidly evolving areas (use sparingly)

**For each group:**
- Summarize the common approach
- Cite 3-5 representative papers
- State how our work differs

**Tone:** Respectful but clear about limitations. Never dismissive.

### Method (2-3 pages)

**Structure:**
1. **Overview**: Figure + 1 paragraph explaining the full pipeline
2. **Problem formulation**: Notation, input/output specification
3. **Component sections**: One subsection per key component
4. **Training objective**: Loss functions, optimization details

**Writing tips:**
- Lead with intuition, follow with formalism
- Every equation should be explained in words
- Use consistent notation throughout
- Reference the overview figure when describing components

### Experiments (2-3 pages)

**Required elements:**
1. **Datasets**: Describe each benchmark (size, task, metrics)
2. **Baselines**: List and briefly describe comparison methods
3. **Implementation details**: Enough to reproduce (or cite appendix)
4. **Main results**: Tables comparing to SOTA
5. **Ablations**: Isolate contribution of each component
6. **Analysis**: Qualitative examples, failure cases, insights

**Table guidelines:**
- Bold best results, underline second-best
- Include standard deviations for non-deterministic results
- Specify if results are from our runs or cited from papers

### Conclusion (0.5 pages)

- Restate the problem and approach (briefly)
- Summarize key findings
- Acknowledge limitations honestly
- Suggest future directions

## Style Guidelines

### Voice and Tone

- **Active voice**: "We propose X" not "X is proposed"
- **Precise language**: "improves by 3.2%" not "significantly improves"
- **Confident but measured**: Avoid overclaiming

### Technical Writing

**Do:**
- Define acronyms on first use: "text-to-video retrieval (T2VR)"
- Use consistent terminology (pick one term, stick with it)
- Write equation references as "Eq. (1)" or "Equation 1" consistently
- Use present tense for general truths, past for your experiments

**Don't:**
- Start sentences with "It" without clear antecedent
- Use vague quantifiers ("many", "significant", "large")
- Mix American/British spelling
- Use colloquialisms or clichés

### Figures and Tables

**Figures:**
- Vector graphics (PDF) for diagrams
- High DPI for visualizations
- Readable at 50% zoom
- Self-contained captions

**Tables:**
- Align decimal points
- Use consistent precision (e.g., all 1 decimal place)
- Caption above table
- Minimize lines/borders

## Common Pitfalls for Our Domain

### Text-to-Video Retrieval Papers

**Avoid:**
- Claiming "temporal reasoning" without testing on temporal benchmarks
- Comparing to outdated baselines only
- Ignoring efficiency/scalability concerns
- Overclaiming from single-benchmark improvements

**Include:**
- Multiple benchmarks (MSR-VTT, DiDeMo, ActivityNet, etc.)
- Both R@1 and R@5/R@10 metrics
- Inference time comparisons
- Analysis of temporal vs. appearance features

### Vision-Language Papers

**Avoid:**
- Training/test contamination (especially with CLIP-based models)
- Cherry-picked qualitative examples
- Missing ablations on pretraining data

**Include:**
- Zero-shot vs. fine-tuned results
- Comparison at similar model scales
- Analysis of what the model learns

## Revision Strategies

### Self-Review Checklist

Before sending for review:
- [ ] Read abstract and intro aloud
- [ ] Check all numbers match between text and tables
- [ ] Verify all figures are referenced
- [ ] Confirm all citations are accurate
- [ ] Run spell check and grammar check
- [ ] Check venue formatting requirements

### Responding to Reviews

**Structure:**
1. Thank reviewer for feedback
2. Summarize changes made
3. Address each point with specific responses
4. Quote added/changed text

**Tone:**
- Grateful, not defensive
- Direct answers, not deflection
- Acknowledge valid criticisms

## Venue-Specific Notes

### CVPR/ICCV/ECCV

- 8 pages + references
- Heavy emphasis on visual results
- Supplementary video demos valued

### NeurIPS/ICML

- 9 pages + references
- More tolerance for theory
- Reproducibility checklist required

### ACL/EMNLP

- 8 pages + references
- Emphasis on language understanding
- Error analysis expected

## LaTeX Tips

```latex
% Consistent spacing for equations
\usepackage{amsmath}
\DeclareMathOperator*{\argmax}{arg\,max}

% Good table formatting
\usepackage{booktabs}
\begin{tabular}{lcc}
\toprule
Method & R@1 & R@5 \\
\midrule
Baseline & 42.1 & 68.3 \\
Ours & \textbf{45.7} & \textbf{71.2} \\
\bottomrule
\end{tabular}

% Figure references
\usepackage{cleveref}
\cref{fig:overview}  % "Figure 1"
```
