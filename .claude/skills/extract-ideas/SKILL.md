---
name: extract-ideas
description: "Extract research ideas from paper summaries in reading_stack/summaries/ and create entries in idea_stack/_inbox/. Use to process Ideas Sparked sections from paper reading."
---

# Extract Ideas

Extract ideas from paper summaries and create idea_stack entries.

## Usage

- `/extract-ideas` - Scan all paper summaries and extract new ideas
- `/extract-ideas PAPER-XXX` - Extract ideas from a specific paper summary

## Workflow

### Step 1: Launch Idea Extractor Agent

Use the Task tool to launch the `idea-extractor` agent with this prompt:

**If no arguments (scan all):**
```
Scan all paper summaries in reading_stack/summaries/ and extract ideas.

1. Search for summaries with "Ideas Sparked" sections
2. For each idea found:
   a. Check if it already exists in idea_stack
   b. If new, create entry in idea_stack/_inbox/
   c. Link back to source paper
3. Report summary of extraction

Process all summaries and create idea entries for any new ideas found.
```

**If paper ID provided:**
```
Extract ideas from a specific paper summary.

1. Read reading_stack/summaries/PAPER-XXX-*.md
2. Find the "Ideas Sparked" section
3. For each idea:
   a. Check if it already exists in idea_stack
   b. If new, create entry in idea_stack/_inbox/
   c. Link back to source paper
4. Report what was extracted

Paper ID: $ARGUMENTS
```

### Step 2: Report Results

After the agent completes, report to the user:

1. Number of summaries scanned
2. Number of ideas extracted
3. List of created idea entries with their IDs
4. Any papers that had no Ideas Sparked section
5. Any ideas that were skipped (already existed)

## Output Format

```
## Ideas Extracted

**Summaries Processed**: X
**New Ideas Created**: Y

| Source Paper | Idea Created | Title |
|--------------|--------------|-------|
| PAPER-001 | IDEA-XXX | [title] |
| PAPER-002 | IDEA-YYY | [title] |

**Skipped**:
- PAPER-003: No Ideas Sparked section
- Idea from PAPER-004: Already exists as IDEA-ZZZ
```

## Notes

- Ideas are created in idea_stack/_inbox/ (first stage)
- Each idea links back to its source paper
- The agent avoids creating duplicate ideas
- Use `/promote-idea` to move ideas through the pipeline
