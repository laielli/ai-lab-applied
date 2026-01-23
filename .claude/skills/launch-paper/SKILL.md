---
name: launch-paper
description: "Create a new paper project from a ready idea in idea_stack/ready/. Sets up the full paper directory structure with requirements, experiment tracking, and git repository."
---

# Launch Paper

Create a paper project from a ready idea.

## Usage

- `/launch-paper IDEA-XXX` - Launch paper from specific ready idea
- `/launch-paper` - List ideas in ready stage

## Workflow

### Step 1: Launch Paper Launcher Agent

Use the Task tool to launch the `paper-launcher` agent with this prompt:

**If idea ID provided:**
```
Create a new paper project from a ready idea.

1. Read idea_stack/ready/IDEA-XXX-*.md
2. Verify the idea is complete and ready for paper launch
3. Create paper directory structure in papers/:
   - README.md (paper overview)
   - STATUS.md (deadline tracking)
   - EXPERIMENT_SCHEDULE.md (experiment planning)
   - prd/paper_requirements.md (from idea content)
   - specs/ (technical specifications)
   - experiment_stack/{_inbox,in_progress,results}/
   - log/ (experiment logs)
   - src/ (source code)
   - evals/ (evaluation scripts)
   - paper/ (LaTeX drafts)
   - presentation/ (slides and materials)
4. Initialize git repository
5. Mark idea as launched with link to paper

Idea ID: $ARGUMENTS
```

**If no arguments:**
```
List all ideas that are ready to be launched as papers.

1. Check idea_stack/ready/ for ideas
2. For each idea, show:
   - ID and title
   - Target venue and deadline
   - Brief description
3. Suggest which to launch first based on deadlines

If no ideas are ready, show what's in developing stage.
```

### Step 2: Report Results

After the agent completes, report to the user:

**For successful launch:**
- Paper directory name and location
- Target venue and deadline
- Key next steps to begin work

**For listing:**
- Ready ideas with their deadlines
- Recommendation for which to launch

## Directory Structure Created

```
papers/<paper-name>/
├── README.md
├── STATUS.md
├── EXPERIMENT_SCHEDULE.md
├── prd/
│   └── paper_requirements.md
├── specs/
├── experiment_stack/
│   ├── _inbox/
│   ├── in_progress/
│   └── results/
├── log/
├── src/
├── evals/
├── paper/
└── presentation/
```

## Notes

- Only ideas in idea_stack/ready/ can be launched
- The paper requirements are generated from the idea content
- A git repository is initialized in the paper directory
- The original idea is marked as "launched" but not deleted
- Use `/promote-idea` first if the idea is not yet in ready stage
