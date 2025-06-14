import streamlit as st
from agno.agent import Agent
from agno.models.aws import Claude
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.calculator import CalculatorTools
from agno.storage.sqlite import SqliteStorage
from agno.file import File
import os
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

# Setup agent (move inside main execution to avoid recreation)
@st.cache_resource
def get_agent():
    storage = SqliteStorage(table_name="agent_sessions", db_file="tmp/agent.db")
    return Agent(
        model=Claude(id="apac.anthropic.claude-sonnet-4-20250514-v1:0"),
        tools=[DuckDuckGoTools(), CalculatorTools()],
        storage=storage,
        enable_agentic_memory=True,
        markdown=True
    )

st.set_page_config(page_title="AI Chatbot", layout="wide")
st.title("🤖 AI Chatbot")

# Get cached agent
agent = get_agent()

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
upload_col, input_col, send_col = st.columns([2, 6, 1])

with upload_col:
    uploaded_files = st.file_uploader(
        "Upload files", 
        accept_multiple_files=True, 
        type=['txt', 'pdf', 'docx', 'csv', 'json', 'py', 'md'],
        help="Upload files to analyze or reference",
        key="file_uploader"  # Add unique key
    )

with input_col:
    user_input = st.text_area(
        "Type your message...", 
        key="input_box", 
        label_visibility="collapsed",
        height=100,
        value=""  # Reset value to prevent sticky input
    )

with send_col:
    send_clicked = st.button("Send ➤", key="send", use_container_width=True)

# Handle response
if send_clicked and user_input.strip():
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Process files if uploaded
    files = None
    if uploaded_files:
        try:
            files = convert_to_custom_files(uploaded_files)
            st.success(f"Uploaded {len(files)} file(s) successfully!")
        except Exception as e:
            st.error(f"Error processing files: {str(e)}")

    # Generate and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = agent.run(
                    message=user_input, 
                    files=files,
                    user_id="anamul"
                )

                # Handle response content properly
                response_content = response.content if hasattr(response, 'content') else str(response)

                st.markdown(response_content)
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": response_content
                })

            except Exception as e:
                error_msg = f"Sorry, I encountered an error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": error_msg
                })

    # Clear the input and rerun
    st.session_state.input_box = ""  # Clear the text area
    st.rerun()

# Display uploaded files info in sidebar
if uploaded_files:
    with st.sidebar:
        st.subheader("📎 Uploaded Files")
        for file in uploaded_files:
            # Get file size properly
            file_size = len(file.read()) if hasattr(file, 'read') else file.size
            file.seek(0)  # Reset file pointer after reading
            st.write(f"• {file.name} ({file_size} bytes)")

# Add clear chat button
with st.sidebar:
    if st.button("🗑️ Clear Chat", key="clear_chat"):
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I'm your AI assistant. How can I help you today?"}
        ]
        st.rerun()