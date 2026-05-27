from crewai import Task


def make_research_task(researcher):
    return Task(
        description=(
            "Research the topic: **{topic}**\n\n"
            "Your job is to gather raw material — not to analyse or summarise yet.\n\n"
            "Find:\n"
            "1. Current state of the field — what is happening right now\n"
            "2. Key projects, tools, papers, companies, or people driving this space\n"
            "3. Significant developments from the last 6–12 months\n"
            "4. Concrete data points, numbers, or benchmarks where available\n"
            "5. Any disagreement, controversy, or competing approaches\n\n"
            "Use at least 5 distinct sources. Prefer primary sources "
            "(official docs, research papers, founder posts) over secondary coverage."
        ),
        expected_output=(
            "A detailed research dump covering key facts, recent developments, notable "
            "projects or people, data points, and a list of sources with URLs."
        ),
        agent=researcher,
    )


def make_analysis_task(analyst):
    return Task(
        description=(
            "Analyse the research findings about **{topic}**.\n\n"
            "Do not restate the raw research — synthesise it.\n\n"
            "Extract:\n"
            "1. The 3–5 most important themes or trends (with evidence)\n"
            "2. Key tensions or trade-offs: what are the real debates in this space?\n"
            "3. What is overhyped vs. what is genuinely significant?\n"
            "4. What this means practically for builders, engineers, or product people\n"
            "5. The most important open questions — what does nobody know yet?\n\n"
            "Be willing to have a point of view where the evidence supports one."
        ),
        expected_output=(
            "A structured analytical layer: themes with evidence, tensions, "
            "signal vs. noise assessment, practical implications, and open questions."
        ),
        agent=analyst,
    )


def make_writing_task(writer, output_path: str = "report.md"):
    return Task(
        description=(
            "Write a research brief on **{topic}** using the research and analysis.\n\n"
            "Format it exactly like this:\n\n"
            "---\n"
            "# {topic}: A Research Brief\n\n"
            "## TL;DR\n"
            "3 bullet points. Each one should be a standalone insight, not a topic label.\n\n"
            "## What's Happening Now\n"
            "2–3 paragraphs on the current state. Specific and grounded.\n\n"
            "## Key Themes\n"
            "One subsection per theme (### Theme Name). Each with a brief explanation "
            "and why it matters.\n\n"
            "## What It Means for Builders\n"
            "Practical takeaways. What should someone building in this space know or do?\n\n"
            "## Open Questions\n"
            "3–5 questions the field has not answered. Be specific — not 'what is the future?'\n\n"
            "## Sources\n"
            "Numbered list of sources used, with URLs.\n"
            "---\n\n"
            "Tone: direct, confident, no filler. Write for a senior engineer or product lead "
            "who has 5 minutes and no patience for vague summaries."
        ),
        expected_output=(
            "A complete, well-formatted research brief in markdown — "
            "opinionated, specific, and ready to publish."
        ),
        agent=writer,
        output_file=output_path,
    )
