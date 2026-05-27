from crewai import Crew, LLM, Process

from agents import make_researcher, make_analyst, make_writer
from tasks import make_research_task, make_analysis_task, make_writing_task

# Use Claude Sonnet 4.6 as the LLM backbone
llm = LLM(model="claude-haiku-4-5-20251001", provider="anthropic")


def build_crew(output_path: str = "report.md") -> Crew:
    """
    Assemble the three-agent research crew.

    Agents run sequentially:
      1. Researcher  — gathers raw information from the web
      2. Analyst     — extracts themes, tensions, and implications
      3. Writer      — produces the final formatted brief

    Each agent receives the outputs of the previous agent as context.
    """
    researcher = make_researcher(llm=llm)
    analyst = make_analyst(llm=llm)
    writer = make_writer(llm=llm)

    tasks = [
        make_research_task(researcher),
        make_analysis_task(analyst),
        make_writing_task(writer, output_path=output_path),
    ]

    return Crew(
        agents=[researcher, analyst, writer],
        tasks=tasks,
        process=Process.sequential,
        verbose=True,
    )


def run(topic: str, output_path: str = "report.md") -> str:
    """Run the crew on a topic and return the final report string."""
    crew = build_crew(output_path=output_path)
    result = crew.kickoff(inputs={"topic": topic})
    return str(result)
