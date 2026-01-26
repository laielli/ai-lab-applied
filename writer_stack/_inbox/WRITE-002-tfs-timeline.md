# Writing Task: TFS Project Timeline with Kill Criteria

- **ID**: WRITE-002
- **Created**: 2026-01-24
- **Paper**: IDEA-009-temporal-fourier-signatures
- **Section**: project-management
- **Priority**: P2
- **Status**: pending
- **Source**: SIM-004 (Advisor Q3)

## Task Description

Create an explicit timeline for the TFS project with:
1. Clear milestones and deadlines
2. Kill criteria at each checkpoint
3. Resource allocation decisions
4. Escalation path if ambiguous results

## Context

### Paper Overview

TFS is at a critical decision point. The main result (+8.8pp on temporal queries) does not replicate. A pilot experiment with real features (EXP-012) will determine project viability.

### Why This Document is Needed

Without a clear timeline, the project risks:
- Indefinite debugging
- Sunk cost fallacy
- Opportunity cost of blocking other work
- Missing publication deadlines

## Source Materials

- SIM-004 simulation session
- EXP-012 pilot experiment spec
- WRITE-001 decision document

## Requirements

### Must Include

1. **Timeline with specific dates**
   - Start date: 2026-01-24
   - Key checkpoints
   - Decision deadline

2. **Kill criteria at each checkpoint**
   - Quantitative thresholds
   - Who decides

3. **Resource allocation**
   - GPU hours per phase
   - Person-hours per phase
   - Opportunity cost assessment

4. **Contingency plans**
   - What if pilot is ambiguous?
   - What if we need more time?

### Must Avoid

- Open-ended timelines ("when we're ready")
- Vague criteria ("if results look good")
- Scope creep ("maybe we should also try X")

### Tone/Style

Direct, actionable, decision-focused.

## Suggested Timeline Structure

```markdown
# TFS Project Timeline

## Phase 1: Pilot (Jan 24-27)
- [ ] Set up feature extraction (Jan 24)
- [ ] Extract features for 100 videos (Jan 25)
- [ ] Run EXP-012 pilot (Jan 26)
- [ ] Analyze results (Jan 27)

**Kill criteria at end of Phase 1:**
- If TFS improvement < 1pp: KILL
- If TFS improvement > 2pp: PROCEED to Phase 2
- If ambiguous (1-2pp): Extend pilot to 200 videos

## Phase 2: Full Experiment (Jan 28-31)
- [ ] Extract features for all 1000 videos (Jan 28-29)
- [ ] Run full EXP with 5 seeds (Jan 30)
- [ ] Analyze results (Jan 31)

**Kill criteria at end of Phase 2:**
- If TFS improvement < 2pp with p > 0.05: KILL
- If TFS improvement > 3pp with p < 0.05: PROCEED to paper
- If ambiguous: Lab meeting discussion

## Phase 3: Paper Decision (Feb 1)
- [ ] Go/no-go decision
- [ ] If GO: Begin paper draft
- [ ] If NO-GO: Document learnings, shelve

## Total Timeline
- Decision deadline: Feb 1, 2026
- Max extension if ambiguous: +3 days
- Hard kill date: Feb 4, 2026
```

## Key Points to Make

1. **1 week maximum** for decision
2. **Quantitative thresholds** at each checkpoint
3. **No extensions** without explicit lab meeting approval
4. **Document decision** regardless of outcome
