# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This is an AI Lab framework designed for agent-driven applied research in **text-to-video retrieval**. The goal is publishing papers at top-tier AI conferences (CVPR, ICCV, NeurIPS, ACL, EMNLP)

## Research Direction

For lab research focus, scope, and taste, see `lab_vision.md`. All agents should consult this document when making decisions about research direction, evaluating paper proposals, or prioritizing work

## Directory Structure Philosophy

The directory hierarchy is split into two tiers:
1. Top tier is where ideas are born, nurtured, and developed into paper projects
2. Bottom tier is where individual paper projects are further developed into submissions are top conferences

The repository follows these design principles:

1. **Flat over nested** — Despite the initial two-tier structure, we still aim to avoid deep directory hierarchies
2. **Minimal ceremony** — Add structure only when needed

## Stacks

Stacks are queues with defined stages that items flow through. Each stack has a README.md documenting its format and workflow.

### Reading Stack

For paper reading queue, summaries, and idea pipeline, see `reading_stack/README.md`. Papers flow through: _inbox → summaries → `idea_stack`

### Idea Stack

For idea queue, see `idea_stack/README.md`. Ideas flow through: _inbox → developing → ready → launched (new project in `papers`)

### Code Stack

For code repository review queue and implementation analysis, see `code_stack/README.md`. Repos flow through: _inbox → summaries (with quality assessment and key implementation details). Cross-references with reading_stack when repos correspond to papers.

### Simulation Stack

For pre-meeting rehearsal with simulated lab meeting Q&A, see `simulation_stack/README.md`. Generates synthetic feedback from three personas (Advisor, SME, Lay Researcher) and routes action items to appropriate stacks. Flow: _inbox → sessions

### Experiment Stack

For lab-wide experiment tracking, see `experiment_stack/README.md`. Experiments flow through: _inbox → in_progress → results

### Figure Stack

For figure and visualization requests, see `figure_stack/README.md`. Requests flow through: _inbox → figures

### Writer Stack

For writing tasks (paper sections, abstracts, responses), see `writer_stack/README.md`. Tasks flow through: _inbox → completed

### Advisor Stack

For processing advisor feedback and routing action items, see `advisor_stack/README.md`. Feedback flows through: _inbox → processed (with items routed to appropriate stacks)

### Lab Meeting Stack

For tracking lab meeting presentations and outcomes, see `lab_meeting_stack/README.md`. Meetings flow through: _inbox → completed (with follow-ups routed to appropriate stacks)

## Key Directory Layout

```
ai-lab-t2v/
├── .claude/            # Agent charters and skill definitions
│   ├── agents/         # Agent system prompts (e.g., lab-meeting-simulator.md)
│   └── skills/         # Skill definitions for slash commands (e.g., simulate-meeting/)
├── standards/          # Constraints all agents follow (engineering, ml, paper, writing, search, decisions)
├── shared/             # Shared Python modules (compute targets, utilities)
│   └── compute/        # ComputeTarget abstraction for local/remote execution
├── reading_stack/      # Paper reading queue and summaries → idea_stack
├── idea_stack/         # 3-stage idea pipeline: _inbox → developing → ready
├── code_stack/         # Code repo review queue and implementation analysis
├── simulation_stack/   # Pre-meeting rehearsal with simulated Q&A: _inbox → sessions
├── experiment_stack/   # Lab-wide experiment tracking: _inbox → in_progress → results
├── figure_stack/       # Figure/visualization requests: _inbox → figures
├── writer_stack/       # Writing tasks: _inbox → completed
├── advisor_stack/      # Advisor feedback processing: _inbox → processed
├── lab_meeting_stack/  # Lab meeting tracking: _inbox → completed
├── papers/             # Paper-specific work (one subdirectory per paper, gitignored)
├── docs/               # Documentation including workflow-schematic.md
```

## Structure of `papers/`

Each paper lives in `papers/<paper_name>/` with:
- `STATUS.md` - A up-to-date assessment of overall paper status and probability of meeting submission deadlines
- `EXPERIMENT_SCHEDULE.md` - A master schedule of experiments, continually updated to reflect latests developments
- `experiment_stack/` - 3-stage experiment pipeline: _inbox → in_progress → results
- `log/` — Experiment log and results
- `src/` — Experiment source code
- `paper/` — Paper drafts in LaTeX
- `datasets/` — Paper-specific datasets

## Skills (Slash Commands)

Skills are invoked via slash commands. Key skills:

| Command | Description |
|---------|-------------|
| `/read <url>` | Add paper from URL → read → summarize |
| `/extract-ideas` | Paper summaries → idea_stack/_inbox |
| `/promote-idea <ID>` | Evaluate & promote idea to next stage |
| `/launch-paper <ID>` | Ready idea → papers/<name>/ project |
| `/run-experiment <cmd>` | Track experiments: start \| complete \| update \| list |
| `/suggest-experiment <paper>` | Generate next experiment spec for paper |
| `/verify-experiment <EXP-ID>` | Review experiment soundness before running |
| `/implement-experiment <EXP-ID>` | Generate Python code from experiment spec |
| `/verify-code <EXP-ID>` | Review code before execution |
| `/execute-experiment <EXP-ID>` | Run on local or Lambda.ai remote compute |
| `/simulate-meeting <ID>` | Simulate lab meeting Q&A: create \| list \| run |
| `/dashboard` | Update evaluation dashboards for ideas and papers |

See `docs/workflow-schematic.md` for visual diagrams of how content flows through stacks.

## Standards to Follow

Before working on specific areas, consult the relevant standards documents:
- `standards/engineering.md` — Coding conventions, reviews, CI
- `standards/ml.md` — Evaluation discipline, dataset versioning
- `standards/paper.md` — PRD template, success metrics
- `standards/writing.md` — Paper writing formats and styles
- `standards/search.md` — Literature search best practices
- `standards/decisions.md` — ADR-style decision log

## When Creating New Work

1. Check `lab_vision.md` for current research focus and priorities
2. Review relevant agent in `.claude/agents/` for task-specific guidance
3. Add items to the appropriate stack's `_inbox/` directory
4. Follow the entry format specified in each stack's README.md
5. Use skills (slash commands) to process items through the pipeline

## Git Workflow

### Repository Structure
- **Main repo** (ai-lab): Lab infrastructure, standards, agents, execution
- **Paper repos**: Independent git repositories in `papers/` directory (not tracked by main repo)

The `papers/` directory is in `.gitignore`. Each paper is its own git repository, fully independent from the main repo.

### Working on Lab Infrastructure

When modifying files in the main repo (standards, agents, execution, shared_stack):

```bash
git add <files>
git commit -m "Description of changes"
git push
```

### Working on a Paper

Papers have their own git repositories. Work directly in the paper directory:

```bash
cd papers/<paper_name>
git add .
git commit -m "Description of changes"
git push
```

No changes to the main repo are needed — papers are fully independent.

### Adding a New Paper

To add a new paper, create or clone a git repository in the `papers/` directory:

```bash
cd papers
git clone <paper-repo-url>
# or: mkdir <paper_name> && cd <paper_name> && git init
```

The main repo will not track it (papers/ is gitignored).
