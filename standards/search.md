# Literature Search Standards

Guidelines for systematic literature search in text-to-video retrieval and vision-language research.

## Search Process

### 1. Start with Anchor Papers

Identify 3-5 highly-cited recent papers in your specific area:
- Check papers with 100+ citations from last 2-3 years
- Look for best paper awards at target venues
- Find papers from top labs (see Key Research Groups below)

### 2. Citation Mining

**Backward search** (references):
- Read related work sections of anchor papers
- Identify foundational papers they all cite
- Track methodology lineage

**Forward search** (citations):
- Use Google Scholar "Cited by" or Semantic Scholar
- Filter by recent years
- Look for papers that improve on or critique anchor papers

### 3. Keyword Search

Use multiple sources with domain-specific queries:

**Primary sources:**
- [arXiv](https://arxiv.org) - cs.CV, cs.CL, cs.MM sections
- [Google Scholar](https://scholar.google.com)
- [Semantic Scholar](https://semanticscholar.org) - good for related papers
- [Papers With Code](https://paperswithcode.com) - includes benchmarks

**Search query templates:**
```
"text-to-video retrieval" + [specific aspect]
"video-text matching" + transformer
"temporal" + "video" + "language"
"cross-modal" + "video" + "retrieval"
[benchmark name] + "state of the art"
```

### 4. Venue-Specific Search

Check proceedings from target venues for last 2-3 years:

| Venue | Focus | Proceedings |
|-------|-------|-------------|
| CVPR/ICCV/ECCV | Computer Vision | CVF Open Access |
| NeurIPS/ICML/ICLR | Machine Learning | OpenReview, NeurIPS Proceedings |
| ACL/EMNLP/NAACL | NLP/Language | ACL Anthology |
| AAAI/IJCAI | AI General | AAAI Library |
| MM (ACM) | Multimedia | ACM DL |

## Domain-Specific Keywords

### Core Topics

**Text-to-Video Retrieval:**
- text-to-video retrieval, video-text retrieval, cross-modal retrieval
- video-text matching, video-language matching
- dense video retrieval, video search

**Temporal Reasoning:**
- temporal modeling, temporal reasoning, temporal grounding
- moment retrieval, video moment localization
- action localization, temporal action detection
- video temporal understanding

**Cross-Modal Learning:**
- vision-language pretraining, video-language models
- cross-modal alignment, multimodal learning
- contrastive learning video, video-text contrastive

**Architecture Components:**
- video transformer, temporal transformer
- cross-attention video, video encoder
- frame aggregation, temporal pooling

### Key Model Families

Track papers building on these foundations:
- **CLIP-based**: CLIP4Clip, X-CLIP, VideoCLIP, CLIP-ViP
- **Dual-encoder**: Frozen, MILES, InternVideo
- **Cross-encoder**: VIOLET, All-in-one, mPLUG-2
- **Foundation models**: VideoMAE, InternVideo2, LanguageBind

## Key Benchmarks

Papers often cluster around benchmarks. Search for recent SOTA on:

| Benchmark | Task | Size | Key Metric |
|-----------|------|------|------------|
| MSR-VTT | Retrieval | 10K videos | R@1, R@5, R@10 |
| DiDeMo | Moment retrieval | 10K videos | R@1 |
| ActivityNet Captions | Dense retrieval | 20K videos | R@1, R@5 |
| LSMDC | Movie retrieval | 118K clips | R@1 |
| VATEX | Multilingual | 41K videos | R@1 |
| QuerYD | Query-focused | 10K videos | mAP |

**Temporal-focused benchmarks** (prioritize for our lab):
- Charades-STA (temporal grounding)
- TACoS (temporal action)
- YouCook2 (procedural understanding)

## Key Research Groups

Track publications from labs with consistent output in our area:

| Group | Institution | Focus |
|-------|-------------|-------|
| Microsoft Research Asia | MSRA | Video understanding, retrieval |
| Meta FAIR | Meta | Foundation models, video |
| Google DeepMind | Google | Multimodal, video |
| Shanghai AI Lab | OpenGVLab | InternVideo series |
| UNC Chapel Hill | | Vision-language |
| UT Austin | | Video understanding |

## Relevance Evaluation

When reviewing a paper, assess against lab_vision.md:

### High Relevance (add to reading_stack)
- Directly addresses text-to-video retrieval
- Proposes temporal modeling innovations
- Achieves SOTA on target benchmarks
- Introduces new benchmark or evaluation protocol

### Medium Relevance (skim, maybe add)
- General video-language pretraining
- Related cross-modal retrieval (image-text)
- Efficiency improvements for video models
- Relevant architectural innovations

### Low Relevance (skip unless specific need)
- Video generation/synthesis
- Image-only methods
- Task-specific (captioning, QA) without retrieval angle
- Compute-heavy methods (100+ GPU days)

## Documentation

### Adding to Reading Stack

For each relevant paper found:

1. Create entry in `reading_stack/_inbox/` using format from README
2. Note why it's relevant in "Why Read" section
3. Tag with focus areas (Temporal Reasoning, Cross-Modal Alignment, etc.)
4. List specific questions to answer when reading

### Tracking Search Sessions

Keep notes on searches performed:
```markdown
## Search: [Date] - [Topic]

**Queries used:**
- "temporal video retrieval" site:arxiv.org
- ...

**Papers found:**
- [Paper title] - [Relevance: High/Med/Low] - [Action: Added/Skipped]
- ...

**Gaps identified:**
- No recent work on [X]
- [Y] approach hasn't been tried for retrieval
```

## Search Automation

### arXiv Alerts

Set up daily/weekly alerts for key terms:
1. Go to [arxiv-sanity](http://arxiv-sanity-lite.com/) or use arXiv API
2. Track categories: cs.CV, cs.CL, cs.MM
3. Filter by keywords from Domain-Specific Keywords above

### Google Scholar Alerts

Create alerts for:
- Key author names
- "text-to-video retrieval"
- Specific benchmark names + "state of the art"

### Semantic Scholar Research Feeds

Create a feed combining:
- Papers citing your anchor papers
- Papers from followed authors
- Papers matching keyword filters

## Anti-Patterns

**Avoid:**
- Only searching one source (cross-reference!)
- Stopping at first page of results
- Ignoring papers without code (theory can be valuable)
- Only reading papers from top venues (workshops have gems)
- Forgetting to check very recent arXiv (last 30 days)

**Watch for:**
- Papers claiming SOTA but using outdated baselines
- Benchmark results that don't match other papers' reported numbers
- Methods requiring resources far beyond our capacity
