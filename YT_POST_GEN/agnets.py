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
You are an expert blog post writer.

Your task is to craft a well-structured, engaging, and informative blog post based on the content provided below. 
Use a clear and conversational tone suitable for a general audience. The final blog post should include:

- A compelling introduction
- Clear subheadings (if applicable)
- Well-developed paragraphs
- A concise conclusion or call-to-action

Here is the content to base the blog post on:

{content}

Please generate the blog post accordingly.
"""

prompt = PromptTemplate.from_template(template=template)
blog_gen_chain = prompt | llm


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
    response = blog_gen_chain.invoke({"content": state["content"]})

    return {"response": response.content}


builder = StateGraph(State)

builder.add_node("transcriber", transcriber)
builder.add_node("summarizer", summarizer)
builder.add_edge(START, "transcriber")
builder.add_edge("transcriber", "summarizer")
builder.add_edge("summarizer", END)
graph = builder.compile()
