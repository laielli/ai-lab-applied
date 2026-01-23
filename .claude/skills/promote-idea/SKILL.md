---
name: promote-idea
description: "Evaluate an idea against promotion criteria and move it to the next stage in the idea pipeline. Use with idea ID (e.g., /promote-idea IDEA-008) or without arguments to list promotable ideas."
---

# Promote Idea

Evaluate and promote ideas through the idea_stack pipeline.

## Usage

- `/promote-idea IDEA-XXX` - Evaluate specific idea for promotion
- `/promote-idea` - List all ideas and their promotion readiness

## Workflow

### Step 1: Launch Idea Promoter Agent

Use the Task tool to launch the `idea-promoter` agent with this prompt:

**If idea ID provided:**
```
Evaluate IDEA-XXX for promotion to the next stage in the idea pipeline.

1. Read the idea file from idea_stack/
2. Determine its current stage (_inbox, developing, or ready)
3. Evaluate against the promotion criteria for that stage
4. If criteria met: promote to next stage and report success
5. If criteria not met: report specific blockers and recommended actions

Idea ID: $ARGUMENTS
```

**If no arguments:**
```
List all ideas in the idea_stack and assess their promotion readiness.

1. List ideas in each stage (_inbox, developing, ready)
2. For each idea, briefly assess promotion readiness
3. Highlight any ideas that appear ready for promotion
4. Note any ideas that are blocked and why
```

### Step 2: Report Results

After the agent completes, report to the user:

**For successful promotion:**
- The idea ID and new stage
- Brief summary of how criteria were met
- Next steps for the idea

**For blocked ideas:**
- The specific criteria not met
- Recommended actions to address blockers

**For listing:**
- Summary of ideas by stage
- Any ideas ready for promotion
- Blocked ideas and their blockers

## Examples

### Promote Specific Idea
```
User: /promote-idea IDEA-008
Agent: Evaluates IDEA-008, checks criteria, promotes if ready or reports blockers
```

### List Ideas
```
User: /promote-idea
Agent: Lists all ideas by stage with promotion readiness assessment
```

## Notes

- Ideas progress: _inbox → developing → ready
- Ready ideas can be launched as papers with `/launch-paper`
- The agent performs literature checks when promoting to ensure novelty
