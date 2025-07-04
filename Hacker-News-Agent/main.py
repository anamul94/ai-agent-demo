from typing import List

from agno.agent import Agent
from agno.models.aws import Claude
from agno.models.aws import AwsBedrock
from agno.models.groq import Groq
from agno.models.ollama import Ollama

from agno.team import Team
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.tavily import TavilyTools

from agno.tools.hackernews import HackerNewsTools
from agno.tools.newspaper4k import Newspaper4kTools
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()

# model = Claude(id="apac.anthropic.claude-3-5-sonnet-20240620-v1:0")
model = AwsBedrock(id="apac.amazon.nova-pro-v1:0")
ollama = Ollama(id="qwq:latest")
groq = Groq(id="qwen-qwq-32b")
# nova =

class Article(BaseModel):
    title: str
    summary: str
    reference_links: List[str]


hn_researcher = Agent(
    name="HackerNews Researcher",
    model=model,
    # exponential_backoff=True,
    # delay_between_retries=5,
    # retry_delay=2,
    role="Gets top stories from hackernews.",
    tools=[HackerNewsTools()],
)

web_searcher = Agent(
    name="Web Searcher",
    model=model,
    # exponential_backoff=True,
    # delay_between_retries=5,
    # retry_delay=2,
    role="Searches the web for information on a topic",
    tools=[TavilyTools()],
    add_datetime_to_instructions=True,
)

article_reader = Agent(
    name="Article Reader",
    model=model,
    role="Reads articles from URLs.",
    tools=[Newspaper4kTools()],
)


hn_team = Team(
    name="HackerNews Team",
    mode="coordinate",
    model=model,
    # exponential_backoff=True,
    # delay_between_retries=2,
    # retry_delay=2,
    members=[hn_researcher, web_searcher, article_reader],
    instructions=[
        "First, search hackernews for what the user is asking about.",
        "Then, ask the article reader to read the links for the stories to get more information.",
        "Important: you must provide the article reader with the links to read.",
        "Then, ask the web searcher to search for each story to get more information.",
        "Finally, provide a thoughtful and engaging summary.",
    ],
    response_model=Article,
    show_tool_calls=True,
    markdown=True,
    # debug_mode=True,
    # show_members_responses=True,
)

# hn_team.print_response("Write an article about the top 2 stories on hackernews")
