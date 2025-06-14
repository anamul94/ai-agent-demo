from agno.agent import Agent
from agno.models.aws import Claude
from agno.models.groq import Groq
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.calculator import CalculatorTools
from agno.storage.sqlite import SqliteStorage
from agno.file import File

from agno.storage.postgres import PostgresStorage
from agno.memory.v2.db.postgres import PostgresMemoryDb
from agno.memory.v2.memory import Memory




from dotenv import load_dotenv
load_dotenv()

db_file = "tmp/agent.db"
db_url = "postgresql+psycopg://postgres:1234@192.168.0.103:5433/agnodb"

# storage = SqliteStorage(table_name="agent_sessions", db_file=db_file)
storage = PostgresStorage(
    # store sessions in the ai.sessions table
    table_name="agent_sessions",
    # db_url: Postgres database URL
    db_url=db_url,
    auto_upgrade_schema=True,
)
memory_db = PostgresMemoryDb(table_name="memory", db_url=db_url)
memory = Memory(model=Groq(id="gemma2-9b-it"),
                db=memory_db)


agent = Agent(
    model=Claude(
        id="apac.anthropic.claude-sonnet-4-20250514-v1:0",  # Use the inference profile ID
    ),
    tools=[DuckDuckGoTools()],
    memory=memory,
    storage=storage,
    enable_agentic_memory=True,
    enable_user_memories=True,
    add_history_to_messages=True,
    markdown=True
)

# Print the response on the terminal
# agent.print_response("who am i", stream=True, user_id="anamul")
# print(agent.get_s())
