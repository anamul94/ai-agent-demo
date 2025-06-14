import streamlit as st
from agno.agent import Agent
from agno.models.aws import Claude
from agno.models.groq import Groq
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.calculator import CalculatorTools
from agno.storage.sqlite import SqliteStorage
from agno.memory.v2.db.sqlite import SqliteMemoryDb

from agno.memory.v2.memory import Memory
from agno.file import File
import os

from agent import agent
from dotenv import load_dotenv

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
db_file = "tmp/agent.db"

# Setup agent
storage = SqliteStorage(
    # store sessions in the ai.sessions table
    table_name="agent_sessions_storage",
    # db_file: Sqlite database file
    db_file=db_file,
)
memory = Memory(
    # Use any model for creating memories
    model=Groq(id="gemma2-9b-it"),
    db=SqliteMemoryDb(table_name="user_memories", db_file=db_file),
)

# agent = Agent(
#     model=Claude(id="apac.anthropic.claude-sonnet-4-20250514-v1:0"),
#     tools=[DuckDuckGoTools(), CalculatorTools()],
#     enable_user_memories=True,
#     memory=memory,
#     storage=storage,
#     enable_agentic_memory=True,
#     add_history_to_messages=True,
#     num_history_runs=3,
#     markdown=True
# )

st.set_page_config(page_title="AI Chatbot", layout="wide")
st.title("🤖 AI Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm your AI assistant. How can I help you today?"}
    ]

# File uploader in sidebar
with st.sidebar:
    st.subheader("📎 Upload Files")
    uploaded_files = st.file_uploader(
        "Choose files", 
        accept_multiple_files=True, 
        type=['txt', 'pdf', 'docx', 'csv', 'json', 'py', 'md'],
        help="Upload files to analyze or reference"
    )

    if uploaded_files:
        st.subheader("Uploaded Files")
        for file in uploaded_files:
            st.write(f"• {file.name} ({file.size} bytes)")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input (automatically handles Enter key)
if user_input := st.chat_input("Type your message here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Process files if uploaded
    files = None
    if uploaded_files:
        try:
            converted_files = convert_to_custom_files(uploaded_files)
            files = converted_files
            st.success(f"Uploaded {len(converted_files)} file(s) successfully!")
        except Exception as e:
            st.error(f"Error processing files: {str(e)}")

    # Generate assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = agent.run(
                    message=user_input,
                    files=files,
                    user_id="anamul",
                    session_id="session_1",
                    stream_intermediate_steps=True
                )
                st.markdown(response.content)

                # Add assistant response to chat history
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": response.content
                })

            except Exception as e:
                error_msg = f"Sorry, I encountered an error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": error_msg
                })