import os
from dotenv import load_dotenv

load_dotenv()

from typing import Iterator, Optional
from pydantic import BaseModel, Field
from langchain_aws import ChatBedrock

from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
import datetime
from langchain_core.messages import SystemMessage, HumanMessage
from typing_extensions import TypedDict
from langchain_tavily import TavilySearch
from datetime import datetime
from langchain_ollama import ChatOllama


IDEA_CLARIFICATION_NODE = "idea_clarification_node"
MARKET_RESEARCH_NODE = "market_research_node"
COMPETITOR_ANALYSIS_NODE = "competitor_analysis_node"
REPORT_GENERATION_NODE = "report_generation_node"

class IdeaClarification(BaseModel):
    originality: str = Field(..., description="Originality of the idea.")
    mission: str = Field(..., description="Mission of the company.")
    objectives: str = Field(..., description="Objectives of the company.")
    current_date: str = Field(..., description="Current Date")


class MarketResearch(BaseModel):
    total_addressable_market: str = Field(
        ..., description="Total addressable market (TAM)."
    )
    serviceable_available_market: str = Field(
        ..., description="Serviceable available market (SAM)."
    )
    serviceable_obtainable_market: str = Field(
        ..., description="Serviceable obtainable market (SOM)."
    )
    target_customer_segments: str = Field(..., description="Target customer segments.")


class CompetitorAnalysis(BaseModel):
    competitor_analysis: str = Field(
        ..., description="Competitor analysis report for startup"
    )

# model = ChatGroq(model="qwen-qwq-32b", temperature=0.1)
noav = ChatBedrock(
    model_id="apac.amazon.nova-pro-v1:0",  # Use the inference profile ID
    region_name=os.getenv("AWS_REGION"),  # Specify your AWS region
    beta_use_converse_api=True,  # Enable the Converse API
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    cache=None,
    temperature=0.1,
    verbose=False,
)

model = ChatOllama(model="mistral:latest", temperature=0.4)


class State(TypedDict):
    startup_idea: str
    idea_clarification: IdeaClarification
    market_research: MarketResearch
    competitor_analysis: str
    final_report: str


# @tool
def get_datetime():
    """Return current date in yyyy-mm-dd format"""
    return datetime.now().strftime("%Y-%m-%d")


def idea_clarifier_agent(state: State) -> State:
    system_msg = SystemMessage(
        content="""
        "Given a user's startup idea, its your goal to refine that idea. ",
        "Evaluates the originality of the idea by comparing it with existing concepts. ",
        "Define the mission and objectives of the startup."
        Add datetime to response,
        """
    )
    formated_idea = f"startup_idea: {state["startup_idea"]}"
    user_msg = HumanMessage(content=formated_idea)
    messages = [system_msg, user_msg]
    llm_with_structured_output = model.with_structured_output(IdeaClarification)
    response = llm_with_structured_output.invoke(messages)
    response.current_date = get_datetime()
    state["idea_clarification"] = response
    return state


def market_research_node(state: State) -> State:
    market_research_agent = create_react_agent(
        name="market_research_agent",
        model=model,
        prompt="""You are provided with a startup idea and the company's mission and objectives. ",
            -Estimate the total addressable market (TAM), serviceable available market (SAM), and serviceable obtainable market (SOM),
            -Define target customer segments and their characteristics.,
            -Search the web for resources if you need to.""",
        tools=[TavilySearch()],
        response_format=MarketResearch,
    )
    message = """
    startup_idea: {startup_idea}
    idea_clarification: {idea_clarification}
    """
    message.format(
        startup_idea=state["startup_idea"],
        idea_clarification=state["idea_clarification"],
    )
    # response = market_research_agent.invoke(message)
    response = market_research_agent.invoke({"message": message})
    state["market_research"] = response["structured_response"]
    return state

from langchain_core.output_parsers import StrOutputParser


def competitor_analysis_node(state: State):
    # yield "competitor_analysis"
    tavil = TavilySearch(max_results=5, search_depth="advanced")
    competitor_analysis_agent = create_react_agent(
        name="competitor_analysis",
        model=model,
        prompt="""
             You are provided with a startup idea and some market research related to the idea.
            - Identify existing competitors in the market.
            - Perform Strengths, Weaknesses, Opportunities, and Threats (SWOT) analysis for each competitor.
            - Assess the startup’s potential positioning relative to competitors.
            """.strip(),
        tools=[tavil],
        response_format=CompetitorAnalysis,
    )
    message = """
        startup_idea: {startup_idea}
        market_research: {market_research}
        """
    message.format(
        startup_idea=state["startup_idea"], market_research=state["market_research"]
    )
    response = competitor_analysis_agent.invoke({"messge": message})
    state["competitor_analysis"] = response["structured_response"]
    return state


def report_agent_node(state: State):
    system_msg = SystemMessage(
        content="""
 You are provided with a startup idea and other data about the idea.,
- Summarise everything into a single report.
- Keep the tone professional and data-driven.
""".strip()
    )

    template = """startup_idea: {startup_idea}
idea_clarification: {idea_clarification}
market_research: {market_research}
competitor_analysis_report: {competitor_analysis_report}
"""
    formated_template = template.format(
        startup_idea=state["startup_idea"],
        idea_clarification=state["idea_clarification"],
        market_research=state["market_research"],
        competitor_analysis_report=state["competitor_analysis"],
    )
    print(formated_template)
    user_msg = HumanMessage(content=formated_template)
    messages = [system_msg, user_msg]
    response = model.invoke(messages)
    state["final_report"] = response.content
    return state


from langgraph.graph import StateGraph, START, END

builder = StateGraph(State)

builder.add_node(IDEA_CLARIFICATION_NODE, idea_clarifier_agent)
builder.add_node(MARKET_RESEARCH_NODE, market_research_node)
builder.add_node(COMPETITOR_ANALYSIS_NODE, competitor_analysis_node)
builder.add_node(REPORT_GENERATION_NODE, report_agent_node)

builder.add_edge(IDEA_CLARIFICATION_NODE, MARKET_RESEARCH_NODE)
builder.add_edge(MARKET_RESEARCH_NODE, COMPETITOR_ANALYSIS_NODE)
builder.add_edge(COMPETITOR_ANALYSIS_NODE, REPORT_GENERATION_NODE)

builder.add_edge(START, IDEA_CLARIFICATION_NODE)
builder.add_edge(REPORT_GENERATION_NODE, END)

graph = builder.compile()

# graph.invoke({"startup_idea": startup_idea})
