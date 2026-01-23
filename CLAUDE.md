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

There are three stacks maintained at the top tier to facilitate exploration and high influx of new ideas

### Reading Stack

For paper reading queue, summaries, and idea pipeline, see `reading_stack/README.md`. Papers flow through: inbox → summaries → `idea_stack`

### Idea Stack

For idea queue, see `idea_stack/README.md`. Ideas flow through: nascent → developing → launched / new project in `papers`

### Code Stack

For code repository review queue and implementation analysis, see `code_stack/README.md`. Repos flow through: inbox → summaries (with quality assessment and key implementation details). Cross-references with reading_stack when repos correspond to papers.

## Key Directory Layout

```
ai-lab-t2v/
├── standards/          # Constraints all agents follow (engineering, ml, paper, writing, search, decisions)
├── reading_stack/      # Paper reading queue, and summaries. Ideas resulting from paper summaries are added to idea_stack
├── idea_stack/         # 3-stage idea development queue: nascent → developing → launched
├── code_stack/         # Code repo review queue and implementation analysis
├── papers/             # Paper-specific work (one subdirectory per paper)
├── group_sync/         # Simulates a research group where ideas and progress are presented and feedback is receieved
```

## Structure of `papers/`

Each paper lives in `papers/<paper_name>/` with:
- `STATUS.md` - A up-to-date assessment of overall paper status and probability of meeting submission deadlines
- `EXPERIMENT_SCHEDULE.md` - A master schedule of experiments, continually updated to reflect latests developments
- `experiment_stack/` - 3-stage experiment pipeline: waiting → in_progress → completed
- `log/` — Experiment log and results
- `src/` — Experiment source code
- `paper/` — Paper drafts in LaTeX
- `datasets/` — Paper-specific datasets

## Structure of `group_sync`

Simulates a research group where paper-specific ideas and progress are presented, discussed and valuable feedback is receieved and incorporated back into the respective paper project

- `presentation_stack/` - 3-stage presentation pipeline: presentation → discussion → feedback

## Standards to Follow

Before working on specific areas, consult the relevant standards documents:
- `standards/engineering.md` — Coding conventions, reviews, CI
- `standards/ml.md` — Evaluation discipline, dataset versioning
- `standards/paper.md` — PRD template, success metrics
- `standards/writing.md` — Paper writing formats and styles
- `standards/search.md` — Literature search best practices
- `standards/decisions.md` — ADR-style decision log

## When Creating New Work

1. Check `agents/context/priorities.md` for current focus
2. Review relevant agent charter in `agents/charters/`
3. Create task file in appropriate queue (`backlog/`, `active/`, or `review/`)
4. Follow the task file format with clear acceptance criteria
5. Update shared context files when blocking issues arise

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
