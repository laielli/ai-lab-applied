# AI-Lab Workflow Schematic

This document provides visual diagrams of how content flows through the various stacks in the ai-lab-t2v repository.

## Table of Contents

1. [Main Workflow](#main-workflow)
2. [Experiment Feedback Cycle](#experiment-feedback-cycle)
3. [Complete Research Cycle](#complete-research-cycle)
4. [Feedback Routing Reference](#feedback-routing-reference)
5. [Skill Commands](#skill-commands)
6. [Idea Lifecycle](#idea-lifecycle)
7. [Stack Summary](#stack-summary)

---

## Main Workflow

```
┌──────────────────────────────────────────────────────────────────────────────────────┐
│                          AI-LAB-T2V WORKFLOW SCHEMATIC                               │
└──────────────────────────────────────────────────────────────────────────────────────┘

                            ╔═══════════════════════════╗
                            ║     EXTERNAL INPUTS       ║
                            ╚═══════════════════════════╝
                                        │
          ┌─────────────────────────────┼─────────────────────────────┐
          │                             │                             │
          ▼                             ▼                             ▼
 ┌─────────────────┐         ┌─────────────────┐           ┌─────────────────┐
 │  arXiv/PDF URL  │         │   GitHub URL    │           │ Advisor Meeting │
 └────────┬────────┘         └────────┬────────┘           └────────┬────────┘
          │                           │                             │
          ▼                           ▼                             ▼
┌─────────────────────┐   ┌─────────────────────┐     ┌────────────────────────┐
│   READING_STACK     │   │     CODE_STACK      │     │     ADVISOR_STACK      │
├─────────────────────┤   ├─────────────────────┤     ├────────────────────────┤
│ _inbox/             │   │ _inbox/             │     │ _inbox/                │
│   │ /read           │   │   │ code-inbox-     │     │   │ advisor-processor  │
│   ▼                 │   │   │ reader          │     │   ▼                    │
│ summaries/          │   │   ▼                 │     │ feedback/              │
│   │                 │   │ summaries/          │     │   │                    │
│   │ "Ideas Sparked" │   │                     │     │   │ routes to:         │
│   │                 │   │                     │     │   │ • ideas            │
└───┼─────────────────┘   └─────────────────────┘     │   │ • experiments      │
    │                                                 │   │ • writing tasks    │
    │ /extract-ideas                                  └───┼────────────────────┘
    │                                                     │
    ▼                                                     ▼
┌────────────────────────────────────────────────────────────────────────────────────┐
│                                   IDEA_STACK                                       │
├────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                    │
│  ┌──────────┐     /promote-idea     ┌─────────────┐    /promote-idea   ┌─────────┐ │
│  │  _inbox/ │ ───────────────────▶  │ developing/ │ ────────────────▶  │ ready/  │ │
│  └──────────┘                       └─────────────┘                    └────┬────┘ │
│       ▲                                   ▲                                 │      │
│       │ new ideas from feedback           │                                 │      │
│       │                                   │                                 │      │
└───────┼───────────────────────────────────┼─────────────────────────────────┼──────┘
        │                                   │                                 │
        │                                   │                          /launch-paper
        │                                   │                                 │
        │                                   │                                 ▼
┌───────┼───────────────────────────────────┼───────────────────────────────────────┐
│       │                                   │         PAPERS/<name>/                │
├───────┼───────────────────────────────────┼───────────────────────────────────────┤
│       │                                   │                                       │
│  ┌────┴────────┐  ┌───────────┐  ┌────────┴──────┐  ┌───────────┐  ┌────────────┐ │
│  │ README.md   │  │ STATUS.md │  │ prd/          │  │ src/      │  │ paper/     │ │
│  │ (overview)  │  │ (tracking)│  │ (requirements)│  │ (code)    │  │ (LaTeX)    │ │
│  └─────────────┘  └───────────┘  └───────────────┘  └───────────┘  └─────▲──────┘ │
│                                                                          │        │
│  ┌───────────────────────────────────────────────────────────────────────┼──────┐ │
│  │                      experiment_stack/ (per-paper)                    │      │ │
│  │                                                                       │      │ │
│  │   ┌─────────┐    start    ┌──────────────┐   complete   ┌──────────┐  │      │ │
│  │   │ _inbox/ │ ─────────▶  │ in_progress/ │ ───────────▶ │ results/ │──┘      │ │
│  │   └────▲────┘             └──────────────┘              └────┬─────┘         │ │
│  │        │                                                     │               │ │
│  │        │ new experiments from feedback                       │               │ │
│  │        │                                                     │               │ │
│  └────────┼─────────────────────────────────────────────────────┼───────────────┘ │
│           │                                                     │                 │
└───────────┼─────────────────────────────────────────────────────┼─────────────────┘
            │                                                     │
            │                                                     │ SHARE RESULTS
            │                                                     │
            │         ┌───────────────────────────────────────────┴───────────┐
            │         │                                                       │
            │         ▼                                                       ▼
            │  ┌────────────────────────────┐               ┌────────────────────────────┐
            │  │     LAB_MEETING_STACK      │               │       ADVISOR_STACK        │
            │  ├────────────────────────────┤               ├────────────────────────────┤
            │  │ _inbox/                    │               │ _inbox/                    │
            │  │   │ meeting-facilitator    │               │   │ advisor-processor      │
            │  │   ▼                        │               │   ▼                        │
            │  │ feedback/                  │               │ feedback/                  │
            │  │   │                        │               │   │                        │
            │  │   │ action items:          │               │   │ action items:          │
            │  │   │ • experiments ─────────┼───────────────┼───┼──┐                     │
            │  │   │ • ideas ───────────────┼───────────────┼───┼──┼──┐                  │
            │  │   │ • writing tasks ───────┼───────────────┼───┼──┼──┼──┐               │
            │  │   │                        │               │   │  │  │  │               │
            │  └───┼────────────────────────┘               └───┼──┼──┼──┼───────────────┘
            │      │                                            │  │  │  │
            │      └────────────────────────────────────────────┘  │  │  │
            │                           │                          │  │  │
            └───────────────────────────┼──────────────────────────┘  │  │
                                        │                             │  │
                    ┌───────────────────┼─────────────────────────────┘  │
                    │                   │                                │
                    ▼                   ▼                                ▼
          ┌─────────────────┐  ┌─────────────────┐            ┌─────────────────────┐
          │ experiment_stack│  │   idea_stack    │            │    WRITER_STACK     │
          │ /_inbox         │  │   /_inbox       │            ├─────────────────────┤
          │ (new experiments│  │   (new ideas)   │            │ _inbox/             │
          │  queued)        │  │                 │            │   │ writer agent    │
          └─────────────────┘  └─────────────────┘            │   ▼                 │
                                                              │ summaries/          │
                                                              │   │                 │
                                                              │   ▼                 │
                                                              │ papers/paper/       │
                                                              └─────────────────────┘

                    ┌─────────────────────────────────────────────────────────────┐
                    │                       FIGURE_STACK                          │
                    ├─────────────────────────────────────────────────────────────┤
                    │  _inbox/ (figure requests)                                  │
                    │    │ figure-builder                                         │
                    │    ▼                                                        │
                    │  figures/ (plots, tables, diagrams)                         │
                    │    ├── fig_paper.pdf ────────▶  papers/paper/figures/       │
                    │    ├── fig_slides.png ───────▶  inline in presentations     │
                    │    └── slide.pdf ────────────▶  beamer slide w/ caption     │
                    └─────────────────────────────────────────────────────────────┘
```

---

## Experiment Feedback Cycle

The critical insight: **experiment results don't just go to the paper—they cycle through advisor reviews and lab meetings, generating new experiments, ideas, and writing tasks**.

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                        EXPERIMENT FEEDBACK CYCLE                                    │
└─────────────────────────────────────────────────────────────────────────────────────┘

                       ┌─────────────────────────────────┐
                       │    experiment_stack/results/    │
                       │    (completed experiments)      │
                       └───────────────┬─────────────────┘
                                       │
                     ┌─────────────────┴─────────────────┐
                     │                                   │
                     ▼                                   ▼
       ┌─────────────────────────┐         ┌─────────────────────────┐
       │     ADVISOR REVIEW      │         │      LAB MEETING        │
       │                         │         │                         │
       │  • Share results        │         │  • Present findings     │
       │  • Discuss implications │         │  • Get group feedback   │
       │  • Get strategic input  │         │  • Discuss next steps   │
       └───────────┬─────────────┘         └───────────┬─────────────┘
                   │                                   │
                   ▼                                   ▼
       ┌─────────────────────────┐         ┌──────────────────────────┐
       │ advisor_stack/feedback/ │         │lab_meeting_stack/feedback│
       └───────────┬─────────────┘         └───────────┬──────────────┘
                   │                                   │
                   └─────────────┬─────────────────────┘
                                 │
                                 ▼
                 ┌───────────────────────────────┐
                 │       FEEDBACK ROUTING        │
                 ├───────────────────────────────┤
                 │                               │
                 │  "Run ablation on X"          │
                 │         │                     │
                 │         ▼                     │
                 │  ┌─────────────────────────┐  │
                 │  │ experiment_stack/_inbox │◀─┼── NEW EXPERIMENT
                 │  └─────────────────────────┘  │
                 │                               │
                 │  "Try approach Y"             │
                 │         │                     │
                 │         ▼                     │
                 │  ┌─────────────────────────┐  │
                 │  │ idea_stack/_inbox       │◀─┼── NEW IDEA
                 │  └─────────────────────────┘  │
                 │                               │
                 │  "Clarify section Z"          │
                 │         │                     │
                 │         ▼                     │
                 │  ┌─────────────────────────┐  │
                 │  │ writer_stack/_inbox     │◀─┼── NEW WRITING TASK
                 │  └─────────────────────────┘  │
                 │                               │
                 │  "Read paper W"               │
                 │         │                     │
                 │         ▼                     │
                 │  ┌─────────────────────────┐  │
                 │  │ reading_stack/_inbox    │◀─┼── NEW PAPER TO READ
                 │  └─────────────────────────┘  │
                 │                               │
                 └───────────────────────────────┘
                                 │
                                 │
                                 ▼
                 ┌───────────────────────────────┐
                 │   experiment_stack/_inbox     │
                 │   (new experiments queued)    │
                 └───────────────┬───────────────┘
                                 │
                                 │ /run-experiment start
                                 ▼
                           ┌───────────┐
                           │  REPEAT   │◀──── CONTINUOUS CYCLE
                           └───────────┘
```

---

## Complete Research Cycle

The research process is iterative, not linear. Within a paper project, the primary cycle is:
**experiment → results → feedback → new experiments**.

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                           COMPLETE RESEARCH CYCLE                                   │
└─────────────────────────────────────────────────────────────────────────────────────┘

                                  ┌──────────┐
                                  │   IDEA   │
                                  └────┬─────┘
                                       │
                                       ▼
                                  ┌──────────┐
                                  │  PAPER   │
                                  │ PROJECT  │
                                  └────┬─────┘
                                       │
                       ┌───────────────┼────────────────┐
                       │               │                │
                       │               ▼                │
                       │         ┌───────────┐          │
                       │         │EXPERIMENT │◀─────────┤
                       │         └─────┬─────┘          │
                       │               │                │
                       │               ▼                │
                       │          ┌──────────┐          │
                       │          │ RESULTS  │          │
                       │          └────┬─────┘          │
                       │               │                │
                       │         ┌─────┴─────┐          │
                       │         ▼           ▼          │
                       │      ┌───────┐   ┌───────┐     │
                       │      │ADVISOR│   │  LAB  │     │
                       │      │REVIEW │   │MEETING│     │
                       │      └───┬───┘   └───┬───┘     │
                       │          │           │         │
                       │          └─────┬─────┘         │
                       │                ▼               │
                       │          ┌───────────┐         │
                       │          │ FEEDBACK  │         │
                       │          └─────┬─────┘         │
                       │                │               │
                       │                │        new experiments
                       │                │               │
                       └────────────────┴───────────────┘

            The cycle continues until the paper is ready for submission
```

---

## Simulation Stack (Pre-Meeting Rehearsal)

The simulation stack provides **pre-meeting rehearsal** before real lab meetings or advisor reviews.

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                           SIMULATION STACK WORKFLOW                                  │
└─────────────────────────────────────────────────────────────────────────────────────┘

                       ┌─────────────────────────────────┐
                       │    experiment_stack/results/    │
                       │    figure_stack/figures/        │
                       │    papers/<name>/               │
                       └───────────────┬─────────────────┘
                                       │
                                       │ Create presentation spec
                                       ▼
                       ┌─────────────────────────────────┐
                       │   simulation_stack/_inbox/      │
                       │   SIM-XXX-[topic].md            │
                       └───────────────┬─────────────────┘
                                       │
                                       │ /simulate-meeting SIM-XXX
                                       ▼
                       ┌─────────────────────────────────────────────────────────────┐
                       │                THREE PERSONAS SIMULATE Q&A                  │
                       ├─────────────────────────────────────────────────────────────┤
                       │                                                             │
                       │  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐   │
                       │  │   ADVISOR   │ │     SME     │ │   LAY RESEARCHER    │   │
                       │  ├─────────────┤ ├─────────────┤ ├─────────────────────┤   │
                       │  │ Strategy    │ │ Methodology │ │ Assumptions         │   │
                       │  │ Positioning │ │ Statistics  │ │ Clarity             │   │
                       │  │ Venues      │ │ Baselines   │ │ Motivation          │   │
                       │  └─────────────┘ └─────────────┘ └─────────────────────┘   │
                       │                                                             │
                       │  Output: 9-15 questions with suggested answers              │
                       │                                                             │
                       └───────────────────────────┬─────────────────────────────────┘
                                                   │
                       ┌───────────────────────────┼───────────────────────────┐
                       │                           │                           │
                       ▼                           ▼                           ▼
          ┌─────────────────────┐   ┌─────────────────────┐   ┌─────────────────────┐
          │ simulation_stack/   │   │   ACTION ITEMS      │   │  PREPARATION        │
          │ sessions/           │   │   ROUTED TO:        │   │                     │
          │ SIM-XXX-[topic].md  │   │                     │   │  • Review Q&A       │
          │                     │   │  experiment_stack/  │   │  • Prepare answers  │
          │  • Q&A transcript   │   │  writer_stack/      │   │  • Address gaps     │
          │  • Feedback summary │   │  reading_stack/     │   │                     │
          │  • Action items     │   │  figure_stack/      │   └──────────┬──────────┘
          └─────────────────────┘   └─────────────────────┘              │
                                                                         │
                                                                         │ Ready for real meeting
                                                                         ▼
                                    ┌─────────────────────────────────────────────────┐
                                    │     REAL LAB MEETING / ADVISOR REVIEW           │
                                    │                                                 │
                                    │  • Better prepared                              │
                                    │  • Weak spots addressed                         │
                                    │  • Answers practiced                            │
                                    └─────────────────────────────────────────────────┘
```

### Simulation vs Real Feedback

| System | Input | Output | Purpose |
|--------|-------|--------|---------|
| `simulation_stack` | Presentation spec | Synthetic Q&A | Pre-meeting rehearsal |
| `advisor_stack` | Real meeting notes | Real action items | Process actual feedback |
| `lab_meeting_stack` | Real presentation | Real feedback | Facilitate real meetings |

---

## Feedback Routing Reference

| Source | Feedback Type | Routes To |
|--------|---------------|-----------|
| Advisor Review | "Run more ablations" | `experiment_stack/_inbox` (PAPER-XXX-EXP-XXX) |
| Advisor Review | "Try different baseline" | `experiment_stack/_inbox` (PAPER-XXX-EXP-XXX) |
| Advisor Review | "Explore direction X" | `idea_stack/_inbox` (IDEA-XXX) |
| Advisor Review | "Strengthen related work" | `writer_stack/_inbox` (PAPER-XXX-WRITE-XXX) |
| Advisor Review | "Read paper Y" | `reading_stack/_inbox` (READ-XXX) |
| Lab Meeting | "What if you tried Z?" | `experiment_stack/_inbox` (PAPER-XXX-EXP-XXX) |
| Lab Meeting | "Compare with method W" | `experiment_stack/_inbox` (PAPER-XXX-EXP-XXX) |
| Lab Meeting | "Interesting new angle" | `idea_stack/_inbox` (IDEA-XXX) |
| Lab Meeting | "Clarify motivation" | `writer_stack/_inbox` (PAPER-XXX-WRITE-XXX) |
| Lab Meeting | "Check paper V" | `reading_stack/_inbox` (READ-XXX) |

---

## Skill Commands

| Command | Description |
|---------|-------------|
| `/read <url>` | Add paper from URL → read → summarize |
| `/extract-ideas` | Paper summaries → idea_stack/_inbox |
| `/promote-idea <ID>` | Evaluate & promote idea to next stage |
| `/launch-paper <ID>` | Ready idea → papers/\<name\>/ project |
| `/run-experiment <cmd>` | Track experiments: start \| complete \| update \| list |
| `/simulate-meeting <ID>` | Simulate lab meeting Q&A: create \| list \| run |

---

## Idea Lifecycle

The complete journey from paper to publication:

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                           COMPLETE IDEA LIFECYCLE                                   │
└─────────────────────────────────────────────────────────────────────────────────────┘

  Paper URL ───▶ reading_stack/_inbox ───▶ summaries ───▶ "Ideas Sparked"
                                                                │
                                                /extract-ideas  │
                                                                ▼
                                                      idea_stack/_inbox
                                                                │
                                                /promote-idea   │  • clear question
                                                                │  • lab vision alignment
                                                                │  • not scooped
                                                                ▼
                                                      idea_stack/developing
                                                                │
                                                /promote-idea   │  • hypothesis
                                                                │  • novelty validated
                                                                │  • experiment plan
                                                                │  • target venue
                                                                ▼
                                                      idea_stack/ready
                                                                │
                                                /launch-paper   │
                                                                ▼
                                                      papers/<name>/
                                                                │
                                                                │
                              ┌─────────────────────────────────┘
                              │
                              ▼
           ┌─────────────────────────────────────────────────────────────┐
           │                    EXPERIMENT CYCLE                         │
           │                                                             │
           │   experiment_stack/_inbox ──▶ in_progress ──▶ results       │
           │          ▲                                        │         │
           │          │                                        │         │
           │          │    ┌───────────────────────────────────┘         │
           │          │    │                                             │
           │          │    ▼                                             │
           │          │  advisor review / lab meeting                    │
           │          │    │                                             │
           │          │    ▼                                             │
           │          └── feedback (new experiments)                     │
           │                                                             │
           └─────────────────────────────────────────────────────────────┘
                              │
                              │ (repeat until done)
                              ▼
                         SUBMISSION
```

---

## Stack Summary

| Stack | Structure | Purpose |
|-------|-----------|---------|
| `reading_stack/` | _inbox → summaries | Paper reading queue |
| `idea_stack/` | _inbox → developing → ready | Idea development pipeline |
| `code_stack/` | _inbox → summaries | Code repo review |
| `advisor_stack/` | _inbox → feedback | Advisor feedback processing |
| `experiment_stack/` | _inbox → in_progress → results | Experiment lifecycle |
| `lab_meeting_stack/` | _inbox → feedback | Lab meeting workflow |
| `simulation_stack/` | _inbox → sessions | Pre-meeting rehearsal with simulated Q&A |
| `figure_stack/` | _inbox → figures | Plots, charts, tables, diagrams |
| `writer_stack/` | _inbox → summaries | Writing tasks |

---

## Global vs Paper-Specific Stacks

Some stacks exist at two levels:

| Stack | Global Location | Paper-Specific Location |
|-------|-----------------|-------------------------|
| `experiment_stack/` | `experiment_stack/` (lab-wide validation) | `papers/<name>/experiment_stack/` |
| `figure_stack/` | `figure_stack/` (general presentations) | `papers/<name>/presentation/` |

**When to use which:**
- **Global**: Early validation experiments, lab meeting figures, general exploration
- **Paper-specific**: Experiments for a specific paper, paper figures
