import streamlit as st
from agents import app
from phi_agents import finance_agent

import os
from dotenv import load_dotenv

load_dotenv()

os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"


st.set_page_config(page_title="📈 Finance Analysis Bot", layout="centered")
st.title("📈 Finance Investment Advisor")

st.markdown(
    """
Ask anything about financial markets, company trends, or investment decisions.
- Compare stocks like **NVDA vs MSFT**
- Ask if it's a good time to invest
"""
)

user_input = st.text_input(
    "💬 Enter your finance question:",
    placeholder="e.g., Should I invest in Microsoft or Nvidia?",
)

if st.button("🔍 Analyze"):
    if user_input:
        with st.spinner("Analyzing financial data..."):
            # response = app.invoke({"messages": user_input})
            # final_response = response.get("messages")
            # st.write(final_response)
            # for message in final_response:
            #     st.write(message.content)
            st.markdown(finance_agent.run(user_input, markdown=True,).content)
    else:
        st.warning("Please enter a question to analyze.")
