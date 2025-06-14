import streamlit as st
from agno.agent import Agent
from agno.models.aws import Claude
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.calculator import CalculatorTools
from agno.storage.sqlite import SqliteStorage
from agno.file import File
import os
from dotenv import load_dotenv
import os

load_dotenv()
os.makedirs("tmp/uploads", exist_ok=True)
def convert_to_custom_files(uploaded_files):
    saved_files = []
    for file in uploaded_files:
        file_path = os.path.join("tmp/uploads", file.name)
        with open(file_path, "wb") as f:
            f.write(file.read())
        saved_files.append(File(name=file.name, path=file_path))
    return saved_files

# Setup agent
storage = SqliteStorage(table_name="agent_sessions", db_file="tmp/agent.db")
agent = Agent(
    model=Claude(id="apac.anthropic.claude-sonnet-4-20250514-v1:0"),
    tools=[DuckDuckGoTools(), CalculatorTools()],
    storage=storage,
    enable_agentic_memory=True,
    markdown=True
)

st.set_page_config(page_title="AI Chatbot", layout="wide")
st.title("🤖 AI Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm your AI assistant. How can I help you today?"}
    ]

# Display messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Layout for input
upload_col, input_col, mic_col, send_col = st.columns([1, 7, 1, 1])

with upload_col:
    uploaded_files = st.file_uploader("", accept_multiple_files=True, label_visibility="collapsed")

with input_col:
    user_input = st.text_area("Type your message...", key="input_box", label_visibility="collapsed")

with send_col:
    send_clicked = st.button("➤", key="send")

# Handle response
if send_clicked and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        files = convert_to_custom_files(uploaded_files) if uploaded_files else None
        response = agent.run(message=user_input, user_id="anamul")
        st.markdown(response.content)
        st.session_state.messages.append({"role": "assistant", "content": response.content})