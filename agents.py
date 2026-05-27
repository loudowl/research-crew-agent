from crewai import Agent
from crewai_tools import ScrapeWebsiteTool, SerperDevTool
from crewai.tools import BaseTool
from pydantic import Field

# Tools available to the Researcher
search_tool = SerperDevTool()

# Wrap the scraper to cap output at ~3,000 chars so scraped pages
# don't blow the Tier-1 token-per-minute rate limit.
class TruncatedScraper(BaseTool):
    name: str = "read_website_content"
    description: str = (
        "Scrapes the text content of a URL. Returns up to 3,000 characters."
    )
    scraper: ScrapeWebsiteTool = Field(default_factory=ScrapeWebsiteTool)

    def _run(self, website_url: str) -> str:
        result = self.scraper._run(website_url=website_url)
        return result[:3000] if isinstance(result, str) else str(result)[:3000]

web_tool = TruncatedScraper()


def make_researcher(llm=None):
    return Agent(
        role="Research Specialist",
        goal=(
            "Find comprehensive, accurate, and current information about {topic} "
            "from multiple credible sources."
        ),
        backstory=(
            "You are a relentless researcher with a talent for surfacing what actually "
            "matters. You dig past the first page of results, cross-reference sources, "
            "and know when a claim needs more than one citation to be trusted. "
            "You prioritize recency and specificity over general overviews."
        ),
        tools=[search_tool, web_tool],
        llm=llm,
        verbose=True,
        allow_delegation=False,
        max_iter=8,  # cap tool calls to avoid rate limit flooding
    )


def make_analyst(llm=None):
    return Agent(
        role="Insight Analyst",
        goal=(
            "Analyse the research findings about {topic} and extract the patterns, "
            "tensions, and implications that a smart practitioner would care about."
        ),
        backstory=(
            "You are a sharp analytical thinker who separates signal from noise. "
            "You find the themes hiding in raw information, identify what is genuinely "
            "new versus recycled hype, and surface the questions that remain open. "
            "You think like a senior engineer who also reads the business press."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )


def make_writer(llm=None):
    return Agent(
        role="Report Writer",
        goal=(
            "Transform the analysis into a tight, well-structured research brief on "
            "{topic} that a busy expert can read in under five minutes."
        ),
        backstory=(
            "You write for smart, time-pressed readers — engineers, product leads, "
            "technical founders. You cut every word that does not earn its place. "
            "Your reports are opinionated where the evidence supports it and honest "
            "about uncertainty where it does not."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )
