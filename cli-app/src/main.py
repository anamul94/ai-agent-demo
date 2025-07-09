from agno.models.ollama import Ollama
from agno.models.aws import Claude
from agno.agent import Agent

from agent_app import create_agent

from dotenv import load_dotenv
load_dotenv(".env")

ollama = Ollama(id="qwen3:latest")
claude = model=Claude(
        inference_profile_id="apac.anthropic.claude-sonnet-4-20250514-v1:0",  # Use the inference profile ID
    )

agent_app = create_agent(model=claude)
print("Agent created successfully!")
# response = agent_app.run("hi, tell me a joke")
# print(f"Agent response: {response.content}")

dirname = "/home/aa/Desktop/WORK/ARCGEN/PHISHING/rocket-lms/codecanyon-gTRuCdpU-rocket-lms-learning-management-academy-script/Source/Source"

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Exiting the agent app. Goodbye!")
        break
    
    for res in agent_app.run(user_input, stream=True):
        print(res.content, end="", flush=True)
    print()  # New line after the response
