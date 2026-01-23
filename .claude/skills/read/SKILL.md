---
name: read
description: "Add a research paper from a PDF URL to the reading stack and generate a full summary. Use when the user wants to read a paper from a URL."
---

# Read Paper from URL

When invoked with a paper PDF URL, execute the following steps in sequence:

## Step 1: Add Paper to Inbox
Use the Task tool to launch the `paper-inbox-reader` agent with this prompt:

"Add this paper to the reading stack: $ARGUMENTS"

Wait for the agent to complete. It will create an entry in `reading_stack/inbox/` and report the filename (e.g., `PAPER-XXX-author-year.md`).

## Step 2: Read and Summarize the Paper
After Step 1 completes, use the Task tool to launch the `paper-reader` agent with this prompt:

"Read and summarize the paper that was just added to the inbox: `PAPER-XXX-author-year.md`"

The agent will create a summary in `reading_stack/summaries/`.

## Step 3: Report Results
After both agents complete, report to the user:
1. The paper's title and ID
2. Location of the inbox entry
3. Location of the summary
4. Key contributions (2-3 bullet points from the summary)
