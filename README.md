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

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API keys

```bash
cp .env.example .env
```

Edit `.env` and add:
- **`OPENAI_API_KEY`** — from [platform.openai.com](https://platform.openai.com)
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

CrewAI uses GPT-4o by default. To use a different model, edit `crew.py`:

```python
# Use GPT-4o mini (cheaper, faster)
from crewai import LLM
llm = LLM(model="gpt-4o-mini")

# Or use Claude
llm = LLM(model="claude-sonnet-4-6")
```

Pass `llm=llm` to each `Agent(...)` call in `agents.py`.

### Run without web search

Remove `tools=[search_tool, web_tool]` from the Researcher in `agents.py` if you want the crew to reason from training data only (faster, no API key needed for search — but less current).

---

## Stack

- [CrewAI](https://github.com/joaomdmoura/crewAI) — multi-agent orchestration
- [crewai-tools](https://github.com/joaomdmoura/crewAI-tools) — SerperDev search + web scraping
- [OpenAI API](https://platform.openai.com) — LLM backbone (swappable)
- [Serper](https://serper.dev) — Google Search API for agents

---

## What I learned building this

- Sequential agent pipelines work best when each agent has a clearly distinct job. Overlap between researcher and analyst tasks causes redundant output.
- The quality of the final report is mostly determined by the task descriptions — vague tasks produce vague reports regardless of model quality.
- `output_file` in CrewAI tasks is convenient but the final `crew.kickoff()` result string and the file can differ slightly; always check both.
- Serper's free tier (2,500 searches/month) is plenty for experimentation but production use needs a paid plan.

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
