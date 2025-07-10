from textwrap import dedent

from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.models.aws import Claude,AwsBedrock 
from agno.tools.youtube import YouTubeTools

model=Claude(
        id="apac.anthropic.claude-3-5-sonnet-20240620-v1:0",
        max_tokens=8192),
nova = AwsBedrock(id="apac.amazon.nova-pro-v1:0")
ollama = Ollama(id="mistral-small3.2:latest")
agent = Agent(
    model=nova,
    tools=[YouTubeTools()],
    instructions=dedent("""\
       You are an expert blog post writer.
Your task is to craft a well-structured, informative, and engaging blog post based on the captions (transcript) of a YouTube video.

Guidelines:

    Analyze the transcript carefully to understand the topic, structure, and key points covered in the video.

    Use a clear, conversational tone suitable for a general audience.

    Ensure the blog content closely aligns with the video’s message and flow, preserving the intent and context of the speaker.

    The blog should not be a direct copy of the transcript but a coherent and refined narrative based on it.

The blog post must include:

    A compelling introduction that hooks the reader and sets up the topic.

    Clear subheadings for different sections (where applicable).

    Well-developed paragraphs that explain key ideas with clarity.

    A concise conclusion or call-to-action that wraps up the content effectively.

Optional (but recommended):

    Highlight any important takeaways, examples, or tips shared in the video.

    Maintain the educational or storytelling tone used by the speaker, depending on the context.
    
**Must Follow
    ***Return only blog***
        """
        ),
    markdown=True,
)