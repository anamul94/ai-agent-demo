from langchain_community.tools.yahoo_finance_news import YahooFinanceNewsTool
from langchain_community.tools import DuckDuckGoSearchRun
from langgraph_supervisor import create_supervisor
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Set up the LLM (Groq + Qwen)
model = ChatGroq(model="qwen-2.5-32b")

# Tools
finance_tool = YahooFinanceNewsTool()
search_tool = DuckDuckGoSearchRun()

# Web Agent - for general queries or extra info
web_agent = create_react_agent(
    tools=[search_tool],
    name="web_agent",
    model=model,
    prompt="You are a web research agent. For queries   search the web and summarize findings.",
)

# Finance Agent - core logic to analyze trends and suggest action
finance_agent = create_react_agent(
    tools=[finance_tool],
    name="finance_agent",
    model=model,
    prompt="""
You are a financial analysis expert.

Your job is to:
1. Analyze the latest financial news using Yahoo Finance News.
2. Detect trends, investor sentiment, or major movements in the market.
3. If a user compares companies (e.g., NVDA vs Microsoft), evaluate both and give a reasoned investment suggestion.
4. Use markdown formatting. Use bullet points or tables where useful.
5. Be honest — if data is limited, say so, and recommend caution.

Focus on being helpful, cautious, and informative.
""",
)

# Supervisor Agent - routes tasks
workflow = create_supervisor(
    [web_agent, finance_agent],
    model=model,
    prompt="""
You are a supervisor agent overseeing two experts:
- web_agent for general online search
- finance_agent for financial news and investment advice
- Use markdown formatting. Use bullet points or tables where useful.

""",
)

# Compile the app
app = workflow.compile()

# Sample Query (can replace this with user input)
# response = app.invoke(
#     {"messages": "Which is a better investment right now, NVDA or Microsoft?"}
# )
# print(response)
