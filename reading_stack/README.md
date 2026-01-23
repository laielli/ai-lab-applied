# Reading Stack

A system for managing papers to read, generating summaries, and developing research ideas.

## Purpose

- **Inbox**: Queue of papers to read (arXiv links)
- **Summaries**: Processed papers with focus area tags and sparked ideas

## Directory Structure

```
reading_stack/
├── _inbox/          # Papers waiting to be read
└── summaries/       # Processed paper summaries
```

**Note:** Ideas sparked from papers are extracted to `idea_stack/` via the `/extract-ideas` skill. See `idea_stack/README.md` for the idea pipeline.

## Workflow

```
User drops arXiv link → _inbox/PAPER-XXX.md
         ↓
Read and summarize → summaries/PAPER-XXX.md (with focus tags)
         ↓
Extract ideas → idea_stack/_inbox/ (via /extract-ideas)
```

---

## Paper Entry Format (_inbox/)

Filename: `PAPER-XXX-[first-author]-[year].md`

```markdown
# Paper: [Title]

- **ID**: PAPER-XXX
- **arXiv**: 2401.12345
- **Authors**: Smith et al.
- **Year**: 2024
- **Added**: YYYY-MM-DD
- **Status**: unread

## Why Read
Brief note on why this paper is relevant to lab vision.

## Focus Areas
- [ ] Mechanistic DL Theory
- [ ] Feature Learning
- [ ] Knowledge Distillation
- [ ] Theory-Inspired Applications

## Notes
Notes from a first-pass reading.

## Questions
A list of questions about the paper to answer in the summary.
```

---

## Summary Format (summaries/)

Filename: `PAPER-XXX-[first-author]-[year].md`

```markdown
# Summary: [Title]

- **Paper ID**: PAPER-XXX
- **arXiv**: 2401.12345
- **Summarized**: YYYY-MM-DD

## Focus Area Tags
- Mechanistic DL Theory
- Feature Learning

## One-Line Summary
[Single sentence capturing the core contribution]

## Key Contributions
1. ...
2. ...

## Methodology
[Brief description of approach]

## Key Results
- ...

## Answers to First-pass Questions
[Answers for any first-pass questions listed in the Paper Entry file]

## Relevance to Lab Vision
[How this connects to our research direction]

## Potential Connections
- Connection to [other paper/idea]
- Gap this reveals: ...

## Ideas Sparked
- IDEA-XXX: [brief description]
```

---

## Focus Areas (from lab_vision.md)

When tagging papers and ideas, use these focus areas:

1. **Mechanistic DL Theory** - How/why neural networks learn, learning dynamics
2. **Feature Learning** - How representations emerge, what determines features learned
3. **Knowledge Distillation** - Theoretical foundations, student-teacher dynamics
4. **Theory-Inspired Applications** - Applied methods from theoretical understanding

---

## ID Conventions

- Papers: `PAPER-001`, `PAPER-002`, etc.

IDs are assigned sequentially.

---

## Integration with Code Stack

When a paper has an associated code repository:

1. **Add to code_stack**: Create entry in `code_stack/_inbox/REPO-XXX.md`
2. **Cross-reference**: Link PAPER-XXX ↔ REPO-XXX in both summaries
3. **Implementation notes**: Reference code_stack summary in paper's "Potential Connections" section

This creates a bidirectional link between theoretical understanding (paper) and practical implementation (code). See `code_stack/README.md` for the code review workflow.
