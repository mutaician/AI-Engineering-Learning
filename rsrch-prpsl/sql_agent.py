import os
import requests, pathlib
from langchain.chat_models import init_chat_model
from langchain_community.utilities import SQLDatabase
from dotenv import load_dotenv
import re
from langchain_core.tools import tool
# from langchain.agents import create_agent
# from langgraph.prebuilt import create_react_agent as create_agent
from langchain_core.messages import SystemMessage
from langchain_core.messages import AIMessage
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, MessagesState, END
from langchain_core.runnables.graph import MermaidDrawMethod
from langgraph.prebuilt import ToolNode
from langchain_cerebras import ChatCerebras
from typing import cast


load_dotenv()


llm = init_chat_model("openai:gpt-5-nano")

# llm = ChatCerebras(
#     model="qwen-3-coder-480b",
#     # other params...
# )

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

# Define the graph manually
model_with_tools = llm.bind_tools([execute_sql])

def llm_node(state: MessagesState) -> MessagesState:
    msgs = [SystemMessage(content=SYSTEM)] + state["messages"]
    ai = cast(AIMessage, model_with_tools.invoke(msgs))
    return {"messages": [ai]}

def route_from_llm(state: MessagesState):
    last = state["messages"][-1]
    if isinstance(last, AIMessage) and getattr(last, "tool_calls", None):
        return "tools"
    return END

tool_node = ToolNode([execute_sql])

builder = StateGraph(MessagesState)
builder.add_node("llm", llm_node)
builder.add_node("tools", tool_node)
builder.set_entry_point("llm")
builder.add_conditional_edges("llm", route_from_llm, {"tools": "tools", END: END})
builder.add_edge("tools", "llm")

graph = builder.compile()


if __name__ == "__main__":
    # Visualize the graph
    from IPython.display import Image, display
    png_data = graph.get_graph().draw_mermaid_png(draw_method=MermaidDrawMethod.PYPPETEER)
    with open("graph.png", "wb") as f:
        f.write(png_data)
    print("Graph saved as graph.png")

    # Run the agent
    # question = "Which genre on average has the longest tracks?"
    question = "What are the top 10 best-selling albums by total revenue and Which customers have spent the most money in the last year?"
    for step in graph.stream(
        {"messages": [HumanMessage(content=question)]},
        stream_mode="values",
    ):
        step["messages"][-1].pretty_print()