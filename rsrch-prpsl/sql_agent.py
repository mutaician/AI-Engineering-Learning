import os
import requests, pathlib
from langchain.chat_models import init_chat_model
from langchain_community.utilities import SQLDatabase
from dotenv import load_dotenv
import re
from langchain_core.tools import tool
# from langchain.agents import create_agent
from langgraph.prebuilt import create_react_agent as create_agent
from langchain_core.messages import SystemMessage
from langchain_cerebras import ChatCerebras


load_dotenv()


# llm = init_chat_model("openai:gpt-5-nano")

llm = ChatCerebras(
    model="qwen-3-coder-480b",
    # other params...
)

# Configure the sample database
url = "https://storage.googleapis.com/benchmarks-artifacts/chinook/Chinook.db"
local_path = pathlib.Path("Chinook.db")

if local_path.exists():
    print(f"{local_path} already exists, skipping download.")
else:
    response = requests.get(url)
    if response.status_code == 200:
        local_path.write_bytes(response.content)
        print(f"File downloaded and saved as {local_path}")
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")

# Tools for database interaction
db = SQLDatabase.from_uri("sqlite:///Chinook.db")
SCHEMA = db.get_table_info() # extract info about the database

# Execute sql queries
DENY_RE = re.compile(r"\b(INSERT|UPDATE|DELETE|ALTER|DROP|CREATE|REPLACE|TRUNCATE)\b", re.I)
HAS_LIMIT_TAIL_RE = re.compile(r"(?is)\blimit\b\s+\d+(\s*,\s*\d+)?\s*;?\s*$")

def _safe_sql(q: str) -> str:
    # normalize
    q = q.strip()
    # block multiple statements (allow one optional trailing ;)
    if q.count(";") > 1 or (q.endswith(";") and ";" in q[:-1]):
        return "Error: multiple statements are not allowed."
    q = q.rstrip(";").strip()

    # read-only gate
    if not q.lower().startswith("select"):
        return "Error: only SELECT statements are allowed."
    if DENY_RE.search(q):
        return "Error: DML/DDL detected. Only read-only queries are permitted."

    # append LIMIT only if not already present at the end (robust to whitespace/newlines)
    if not HAS_LIMIT_TAIL_RE.search(q):
        q += " LIMIT 5"
    return q

@tool
def execute_sql(query: str) -> str:
    """Execute a READ-ONLY SQLite SELECT query and return results."""
    query = _safe_sql(query)
    q = query
    if q.startswith("Error:"):
        return q
    try:
        return db.run(q) # type: ignore
    except Exception as e:
        return f"Error: {e}"

# defining create_agent - ReAct agent that interpret the request and generate SQL command
SYSTEM = f"""You are a careful SQLite analyst.

Authoritative schema (do not invent columns/tables):
{SCHEMA}

Rules:
- Think step-by-step.
- When you need data, call the tool `execute_sql` with ONE SELECT query.
- Read-only only; no INSERT/UPDATE/DELETE/ALTER/DROP/CREATE/REPLACE/TRUNCATE.
- Limit to 5 rows unless user explicitly asks otherwise.
- If the tool returns 'Error:', revise the SQL and try again.
- Limit the number of attempts to 5.
- If you are not successful after 5 attempts, return a note to the user.
- Prefer explicit column lists; avoid SELECT *.
"""

agent = create_agent(
    model=llm,
    tools=[execute_sql],
    prompt=SystemMessage(content=SYSTEM),
)


# Run the agent
# question = "Which genre on average has the longest tracks?"
question = "Which customers are our biggest spenders and what genres do they prefer?"


# for step in agent.stream(
#     {"messages": [{"role": "user", "content": question}]},
#     stream_mode="values",
# ):
#     step["messages"][-1].pretty_print()