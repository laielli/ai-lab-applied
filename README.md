# AI Lab — Text-to-Video Retrieval

An agent-driven applied research lab focused on **text-to-video retrieval**. Optimized for publishing papers at top-tier AI conferences (CVPR, ICCV, NeurIPS, ACL, EMNLP).

## Structure

```
ai-lab-t2v/
├── .claude/            # Agent charters and skill definitions
│   ├── agents/         # Agent system prompts
│   └── skills/         # Slash command definitions
├── standards/          # Constraints all agents follow
├── reading_stack/      # Paper reading queue → summaries → ideas
├── idea_stack/         # Idea pipeline: _inbox → developing → ready
├── code_stack/         # Code repo review and analysis
├── simulation_stack/   # Pre-meeting rehearsal with simulated Q&A
├── experiment_stack/   # Lab-wide experiments: _inbox → in_progress → results
├── figure_stack/       # Figure/visualization requests
├── writer_stack/       # Writing tasks
├── papers/             # Paper projects (independent git repos)
└── docs/               # Workflow diagrams and documentation
```

## Stack-Based Workflow

Content flows through stacks with defined stages:

| Stack | Flow | Purpose |
|-------|------|---------|
| `reading_stack` | _inbox → summaries | Paper reading and summarization |
| `idea_stack` | _inbox → developing → ready | Idea development pipeline |
| `code_stack` | _inbox → summaries | Code repository analysis |
| `simulation_stack` | _inbox → sessions | Pre-meeting Q&A rehearsal |
| `experiment_stack` | _inbox → in_progress → results | Experiment lifecycle |

## Skills (Slash Commands)

| Command | Description |
|---------|-------------|
| `/read <url>` | Add paper from URL, read, and summarize |
| `/extract-ideas` | Extract ideas from paper summaries |
| `/promote-idea <ID>` | Evaluate and promote idea to next stage |
| `/launch-paper <ID>` | Create paper project from ready idea |
| `/run-experiment <cmd>` | Track experiments through lifecycle |
| `/simulate-meeting <ID>` | Simulate lab meeting Q&A with 3 personas |
| `/dashboard` | Update evaluation dashboards |

## Research Cycle

```
Paper URL → reading_stack → idea_stack → papers/<name>/
                                              ↓
                              ┌───────────────┴───────────────┐
                              ↓                               ↓
                      experiment_stack              simulation_stack
                              ↓                               ↓
                          results ──────────────────→ real lab meeting
                              ↓
                         SUBMISSION
```

See `docs/workflow-schematic.md` for detailed diagrams.

## Key Files

- `CLAUDE.md` — Agent guidance and repository conventions
- `lab_vision.md` — Research focus, scope, and taste
- `standards/*.md` — Engineering, ML, paper, and writing standards

## Papers

Each paper lives in `papers/<paper_name>/` as an independent git repository with:
- `STATUS.md` — Current status and deadline probability
- `experiment_stack/` — Paper-specific experiments
- `src/` — Experiment code
- `paper/` — LaTeX drafts
