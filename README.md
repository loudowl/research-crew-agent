# research-crew-agent

A three-agent AI pipeline built with [CrewAI](https://github.com/joaomdmoura/crewAI) that researches any topic and produces a structured, opinionated brief — automatically.

Give it a topic. Get back a markdown report with current facts, key themes, practical implications, and open questions.

---

## How it works

Three agents run in sequence, each building on the last:

```
Topic input
    │
    ▼
┌─────────────────────────────────────────────┐
│  🔍 Research Specialist                      │
│  Uses web search to gather raw material:     │
│  sources, data points, recent developments  │
└───────────────────┬─────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│  🧠 Insight Analyst                          │
│  Extracts themes, tensions, signal vs noise  │
│  Identifies what matters for practitioners  │
└───────────────────┬─────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│  ✍️  Report Writer                           │
│  Produces a tight markdown brief:           │
│  TL;DR → State → Themes → So What → Sources │
└───────────────────┬─────────────────────────┘
                    │
                    ▼
              report.md
```

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/loudowl/research-crew-agent.git
cd research-crew-agent
```

### 2. Create a virtual environment

> **Requires Python 3.10–3.13.** CrewAI does not yet support Python 3.14+.
> If your default `python3` is 3.14, install 3.12 first: `brew install python@3.12`

```bash
python3.12 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
pip install "crewai[anthropic]"   # native Anthropic provider
```

### 4. Configure API keys

```bash
cp .env.example .env
```

Edit `.env` and add:
- **`ANTHROPIC_API_KEY`** — from [console.anthropic.com](https://console.anthropic.com) (requires credits)
- **`SERPER_API_KEY`** — free tier at [serper.dev](https://serper.dev) (2,500 searches/month free)

---

## Usage

```bash
# Research any topic
python main.py "the current state of edge AI inference"

# Multi-word topics — use quotes
python main.py "open-source LLM fine-tuning in 2026"

# Custom output file
python main.py "agentic AI frameworks" --output agentic_ai_brief.md

# Interactive mode
python main.py
```

The report is saved to `report.md` by default and also printed to the terminal.

---

## Example output structure

```markdown
# Edge AI Inference: A Research Brief

## TL;DR
- ...

## What's Happening Now
...

## Key Themes
### Theme 1: ...
### Theme 2: ...

## What It Means for Builders
...

## Open Questions
...

## Sources
1. ...
```

---

## Configuration

### Swap the LLM

The crew defaults to **Claude Haiku 4.5** (`claude-haiku-4-5-20251001`). Edit `crew.py` to change it:

```python
from crewai import LLM

# Claude Haiku 4.5 — default (fast, low cost, fits Tier-1 rate limits)
llm = LLM(model="claude-haiku-4-5-20251001", provider="anthropic")

# Claude Sonnet 4.6 — better quality, higher cost, needs Tier-2+ for long runs
llm = LLM(model="claude-sonnet-4-6", provider="anthropic")
```

> **Why `provider="anthropic"` is required:** CrewAI 1.14.x resolves the LLM provider
> from a hardcoded model list that only includes Claude 3.x names. Without the explicit
> `provider` argument, `claude-*` model names silently fall back to the OpenAI provider
> and fail. This will likely be fixed in a future CrewAI release.

### Use OpenAI instead

Set `OPENAI_API_KEY` in `.env` and update `crew.py`:

```python
llm = LLM(model="gpt-4o-mini")   # no provider arg needed for OpenAI
```

### Rate limits and Tier-1 accounts

On a freshly funded Anthropic account (Tier 1), the limit is **50k input tokens/minute**
for Haiku and **30k/minute** for Sonnet. The Researcher agent scrapes multiple web pages
per run, which can exceed these limits if unchecked. Two guards are already in place:

- **`TruncatedScraper`** in `agents.py` caps each scraped page at 3,000 characters.
- **`max_iter=8`** on the Researcher caps the total number of tool calls per task.

To upgrade your rate limits, add more credits at [console.anthropic.com/settings/billing](https://console.anthropic.com/settings/billing).

### Run without web search

Remove `tools=[search_tool, web_tool]` from the Researcher in `agents.py` to reason
from training data only — faster, no Serper key needed, but results won't be current.

---

## Stack

- [CrewAI](https://github.com/joaomdmoura/crewAI) — multi-agent orchestration
- [crewai-tools](https://github.com/joaomdmoura/crewAI-tools) — SerperDev search + web scraping
- [Anthropic Claude](https://console.anthropic.com) — LLM backbone (swappable to OpenAI)
- [Serper](https://serper.dev) — Google Search API for agents

---

## What I learned building this

- Sequential agent pipelines work best when each agent has a clearly distinct job. Overlap between researcher and analyst tasks causes redundant output.
- The quality of the final report is mostly determined by the task descriptions — vague tasks produce vague reports regardless of model quality.
- `output_file` in CrewAI tasks is convenient but the final `crew.kickoff()` result string and the file can differ slightly; always check both.
- Serper's free tier (2,500 searches/month) is plenty for experimentation but production use needs a paid plan.
- **CrewAI 1.14.x does not auto-detect Claude 4.x model names** — you must pass `provider="anthropic"` explicitly or it silently routes to OpenAI.
- **Web scraping without a content cap hits rate limits fast.** Scraped pages can be 5–15k tokens each; wrapping the tool to truncate output is the simplest fix.
- `WebsiteSearchTool` (RAG-based) requires an `OPENAI_API_KEY` regardless of your LLM choice. Use `ScrapeWebsiteTool` instead when running on a non-OpenAI provider.

---

## Ideas for extending this

- [ ] Add a `--format` flag for different output styles (executive brief, blog post, Slack digest)
- [ ] Support multiple topics in batch mode
- [ ] Add a 4th agent: a Fact-Checker that validates claims against primary sources
- [ ] Stream output in real time instead of waiting for the full run
- [ ] Build a simple web UI with FastAPI + HTMX

---

## License

MIT
