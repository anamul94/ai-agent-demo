from phi.agent import Agent
# from phi.model.ollama import Ollama
from phi.tools.yfinance import YFinanceTools
from phi.model.groq import Groq

from dotenv import load_dotenv
from portkey_ai import PORTKEY_GATEWAY_URL, createHeaders

import os
load_dotenv()

os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"


# Define the model to be used by the agent
model = Groq(
    id="qwen-2.5-32b",
    default_headers=createHeaders(
        provider="groq",
        api_key=os.getenv("PORTKEY_API_KEY"),  # Replace with your Portkey API key
    ),
)  # Replace with your preferred model
# llm = GroqChat(
#     base_url=PORTKEY_GATEWAY_URL,
#     api_key=os.getenv("GROQ_API_KEY"),  # Replace with Your Groq API Key
#     default_headers=createHeaders(
#         provider="groq",
#         api_key=os.getenv("PORTKEY_API_KEY"),  # Replace with your Portkey API key
#     ),
# )

# Create the Finance Agent
finance_agent = Agent(
    name="Finance Agent",
    role="Get financial data",
    model=model,
    tools=[
        YFinanceTools(
            stock_price=True,
            analyst_recommendations=True,
            company_info=True,
            company_news=True,
            historical_prices=True,
            stock_fundamentals=True,
        )
    ],
    instructions=["Use tables to display data"],
    show_tool_calls=True,
    markdown=True,
)

# Example query to retrieve financial data
# finance_agent.print_response("Summarize analyst recommendations for NVDA", stream=True)
