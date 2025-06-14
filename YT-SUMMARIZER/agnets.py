from langchain_community.document_loaders import YoutubeLoader
from langchain_core.prompts import PromptTemplate
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_ollama import ChatOllama
from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq

llm = ChatGroq(
    model="gemma2-9b-it",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)

# llm = ChatOllama(model="mistral:latest")

template = """
You are an AI YouTube video summarizer.
You are provided with the transcript of a YouTube video.
Your task is to summarize the content concisely while maintaining the key points and main ideas.
Here is the transcript:
{content}
Please provide a clear and structured summary of the video content, including important details, main themes, and conclusions.
"""
prompt = PromptTemplate.from_template(template=template)
summarizer_chain = prompt | llm


def yt_transcribeer(url):
    loader = YoutubeLoader.from_youtube_url(
        url,
        add_video_info=False,
        language=["bn", "en", "arabic"],
    )
    docs = loader.load()
    content = "".join([doc.page_content for doc in docs])
    return content


class State(TypedDict):
    url: str
    content: str
    response: str


def transcriber(state: State) -> State:
    print("transcriber")
    content = yt_transcribeer(state["url"])
    return {"content": content}


def summarizer(state: State) -> State:
    print("summarizer")
    # print(state["content"])
    response = summarizer_chain.invoke({"content": state["content"]})

    return {"response": response.content}


builder = StateGraph(State)

builder.add_node("transcriber", transcriber)
builder.add_node("summarizer", summarizer)
builder.add_edge(START, "transcriber")
builder.add_edge("transcriber", "summarizer")
builder.add_edge("summarizer", END)
graph = builder.compile()
