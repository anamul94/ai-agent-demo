from langchain_core.messages import AIMessage
from langchain_core.tools import tool

from langgraph.prebuilt import ToolNode
from langchain_community.tools.pubmed.tool import PubmedQueryRun
from langgraph.checkpoint.memory import InMemorySaver
from agents.models import nova_model
from typing import Literal
from langgraph.graph import StateGraph, MessagesState, START, END

tools = [PubmedQueryRun()]
tool_node = ToolNode(tools)
model_with_tools = nova_model.bind_tools(tools=tools)


def should_continue(state: MessagesState):
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tools"
    return END


def call_model(state: MessagesState):
    messages = state["messages"]
    response = model_with_tools.invoke(messages)
    # result = response.get("messages")[-1]
    # print(response)
    return {"messages": [response]}


workflow = StateGraph(MessagesState)

# Define the two nodes we will cycle between
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", should_continue, ["tools", END])
workflow.add_edge("tools", "agent")

checkpointer = InMemorySaver()
app = workflow.compile(checkpointer=checkpointer)
