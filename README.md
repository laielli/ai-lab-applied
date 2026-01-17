# AI Lab — Text-to-Video Retrieval

An agent-driven applied research lab focused on **text-to-video retrieval**, with emphasis on **temporal reasoning** and **cross-modal alignment**. Optimized for publishing papers at top-tier AI conferences (CVPR, ICCV, NeurIPS, ACL, EMNLP).

## Quick Start

1. **Define priorities**: Update `agents/context/priorities.md`
2. **Create a paper**: Follow structure in `papers/README.md`
3. **Create tasks**: Add to `agents/tasks/backlog/`
4. **Track progress**: Update `execution/roadmap.md`

## Structure

```
ai-lab/
├── standards/          # Constraints all agents follow
├── shared_stack/       # Common technical assets
├── papers/             # Paper-specific work (one per paper)
├── execution/          # Roadmap, submissions, metrics
└── agents/             # Agent charters, tasks, context
```

## Agent System

Work is organized by functional agents:
- **orchestrator** — Prioritization and coordination
- **explorer** — Literature search and discovery
- **paper** — Requirements and specs
- **engineering** — Implementation and code review
- **ml** — Models, training, evaluation
- **communication** — Writing and presentations

See `agents/charters/` for detailed agent responsibilities.

## Workflow

1. Tasks flow: `backlog/` → `active/` → `review/` → done
2. All agents read `agents/context/` for coordination
3. Standards in `standards/` apply to all work
4. Papers live in `papers/<paper_name>/`

## Getting Started

- Read `CLAUDE.md` for AI assistant guidance
- Review `ai_lab_framework.md` for design philosophy
- Check `agents/context/priorities.md` for current focus
