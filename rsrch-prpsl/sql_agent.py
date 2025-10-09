import os
import requests, pathlib
import io
import base64
import json
import sqlite3
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
from typing import Optional, List, Tuple
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


load_dotenv()


llm = init_chat_model("openai:gpt-5-nano")

# llm = ChatCerebras(
#     model="qwen-3-coder-480b",
#     # other params...
# )

# Configure the sample database
db = SQLDatabase.from_uri("sqlite:///inventory.db")
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


def _ensure_limit(sql: str, top_n: Optional[int] = None) -> str:
    """Ensure the SELECT query ends with a LIMIT; if already limited, keep the smaller of the two.
    This expects input already sanitized by _safe_sql (single statement, read-only).
    """
    sql = sql.strip().rstrip(";")
    desired = max(1, min(100, top_n or 20))
    # If trailing LIMIT exists, reduce if needed
    m = HAS_LIMIT_TAIL_RE.search(sql)
    if m:
        # Extract the existing limit value
        try:
            tail = sql[m.start():]
            nums = re.findall(r"\d+", tail)
            if nums:
                current = int(nums[0])
                if desired < current:
                    # Replace current with desired
                    sql = re.sub(r"(?is)\blimit\b\s+\d+(\s*,\s*\d+)?\s*$", f"LIMIT {desired}", sql)
            # else keep as-is
        except Exception:
            # On any parsing issue, enforce our limit by appending (safe since rstrip(';'))
            sql = f"{sql} LIMIT {desired}"
    else:
        sql = f"{sql} LIMIT {desired}"
    return sql


def _plot_to_base64(fig) -> str:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=200)
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")


def _fetch_df(sql: str) -> pd.DataFrame:
    with sqlite3.connect("Chinook.db") as conn:
        return pd.read_sql_query(sql, conn)


def _is_numeric(series: pd.Series) -> bool:
    return pd.api.types.is_numeric_dtype(series)


@tool
def visualize_sql(
    query: str,
    chart_type: str,
    x: str,
    y: Optional[str] = None,
    group_by: Optional[str] = None,
    aggregate: Optional[str] = None,
    top_n: Optional[int] = None,
    title: Optional[str] = None,
) -> str:
    """Create a chart from a READ-ONLY SQLite SELECT query and return a JSON payload with base64 PNG image.

    Args:
        query: SELECT-only SQL. No DML/DDL.
        chart_type: one of ["bar","column","line","scatter","pie"].
        x: x-axis / category column.
        y: y-axis column (not required for pie).
        group_by: optional grouping column.
        aggregate: optional aggregation (sum, avg, count, min, max).
        top_n: max rows to visualize (default 20, max 100).
        title: optional chart title.
    Returns:
        JSON string: { summary, image: {format, base64}, title, source: {query, rowCount} }
    """
    try:
        # Sanitize and enforce limit
        safe = _safe_sql(query)
        safe = _ensure_limit(safe, top_n)

        df = _fetch_df(safe)
        row_count = len(df)
        if row_count == 0:
            return json.dumps({
                "summary": "No data matched the query.",
                "title": title or "Empty result",
                "source": {"query": safe, "rowCount": 0}
            })

        # Validate columns
        if x not in df.columns:
            return json.dumps({"error": f"Column '{x}' not found in result.", "source": {"query": safe}})
        if chart_type.lower() != "pie" and (y is None or y not in df.columns):
            return json.dumps({"error": f"Column '{y}' not found in result.", "source": {"query": safe}})

        # Optional aggregation
        plot_df = df.copy()
        agg = (aggregate or "").lower().strip()
        if agg:
            func_map = {"sum": "sum", "avg": "mean", "count": "count", "min": "min", "max": "max"}
            if chart_type.lower() == "pie":
                if group_by:
                    gb = group_by
                    if gb not in plot_df.columns:
                        return json.dumps({"error": f"Column '{gb}' not found in result.", "source": {"query": safe}})
                    # Require numeric column to aggregate; choose y if given, else first numeric
                    target_col = y if (y and y in plot_df.columns) else None
                    if target_col is None:
                        numeric_cols = [c for c in plot_df.columns if _is_numeric(plot_df[c])]
                        if not numeric_cols:
                            return json.dumps({"error": "No numeric column to aggregate for pie chart.", "source": {"query": safe}})
                        target_col = numeric_cols[0]
                    plot_df = plot_df.groupby(gb, dropna=False)[target_col].agg(func_map.get(agg, agg)).reset_index()
                    x_col, y_col = gb, target_col
                else:
                    # Single series pie not grouped is ambiguous; error out
                    return json.dumps({"error": "Pie chart requires group_by with an aggregate.", "source": {"query": safe}})
            else:
                if group_by:
                    if group_by not in plot_df.columns:
                        return json.dumps({"error": f"Column '{group_by}' not found in result.", "source": {"query": safe}})
                    y_col = y if y is not None else ""
                    plot_df = plot_df.groupby([group_by, x], dropna=False)[y_col].agg(func_map.get(agg, agg)).reset_index()
                else:
                    y_col = y if y is not None else ""
                    plot_df = plot_df.groupby(x, dropna=False)[y_col].agg(func_map.get(agg, agg)).reset_index()
        else:
            # No aggregation requested; keep as-is
            pass

        # After aggregation, enforce top_n (e.g., top by y desc when applicable)
        n = max(1, min(100, top_n or 20))
        ctype = chart_type.lower()

        # Prepare figure
        fig, ax = plt.subplots(figsize=(10, 6))

        if ctype in ("bar", "column"):
            if y is None:
                return json.dumps({"error": "Bar/Column chart requires 'y' column.", "source": {"query": safe}})
            # Prefer top by y desc
            if _is_numeric(plot_df[y]):
                plot_df = plot_df.sort_values(by=y, ascending=False).head(n)
            else:
                plot_df = plot_df.head(n)
            ax.bar(plot_df[x].astype(str), plot_df[y])
            ax.set_xlabel(x)
            ax.set_ylabel(y)
            ax.set_title(title or f"{ctype.capitalize()} of {y} by {x}")
            ax.tick_params(axis='x', rotation=60, labelsize=9)
            ax.tick_params(axis='y', labelsize=9)

        elif ctype == "line":
            if y is None:
                return json.dumps({"error": "Line chart requires 'y' column.", "source": {"query": safe}})
            # For time-like x, try parsing; else plot as-is
            try:
                plot_df = plot_df.copy()
                plot_df[x] = pd.to_datetime(arg=plot_df[x], errors='coerce')
            except Exception:
                pass
            plot_df = plot_df.head(n)
            ax.plot(plot_df[x].astype(str), plot_df[y], marker='o', linewidth=1.8)
            ax.set_xlabel(x)
            ax.set_ylabel(y)
            ax.set_title(title or f"{y} over {x}")
            ax.tick_params(axis='x', rotation=45, labelsize=9)
            ax.tick_params(axis='y', labelsize=9)

        elif ctype == "scatter":
            if y is None:
                return json.dumps({"error": "Scatter chart requires 'y' column.", "source": {"query": safe}})
            if not (_is_numeric(plot_df[x]) and _is_numeric(plot_df[y])):
                return json.dumps({"error": "Scatter requires numeric 'x' and 'y'.", "source": {"query": safe}})
            plot_df = plot_df.head(n)
            ax.scatter(plot_df[x], plot_df[y], alpha=0.8)
            ax.set_xlabel(x)
            ax.set_ylabel(y)
            ax.set_title(title or f"Scatter of {y} vs {x}")
            ax.tick_params(axis='x', labelsize=9)
            ax.tick_params(axis='y', labelsize=9)

        elif ctype == "pie":
            # Expect plot_df to have categories in x and values in y or aggregated value
            value_col = y if (y and y in plot_df.columns and _is_numeric(plot_df[y])) else None
            if value_col is None:
                # Try to infer a numeric column other than x
                numeric_cols = [c for c in plot_df.columns if c != x and _is_numeric(plot_df[c])]
                if not numeric_cols:
                    return json.dumps({"error": "Pie chart requires a numeric value column.", "source": {"query": safe}})
                value_col = numeric_cols[0]
            plot_df = plot_df.sort_values(by=value_col, ascending=False).head(n)
            labels_list = list(plot_df[x].astype(str).values)
            ax.pie(plot_df[value_col], labels=labels_list, autopct='%1.1f%%', startangle=90, textprops={"fontsize": 9})
            ax.axis('equal')
            ax.set_title(title or f"Pie of {value_col} by {x}")

        else:
            return json.dumps({"error": f"Unsupported chart_type '{chart_type}'.", "source": {"query": safe}})

        img_b64 = _plot_to_base64(fig)
        summary = {
            "bar": f"Bar chart of top {min(n, row_count)} {x} by {y}.",
            "column": f"Column chart of top {min(n, row_count)} {x} by {y}.",
            "line": f"Line chart of {y} over {x}.",
            "scatter": f"Scatter plot of {y} vs {x}.",
            "pie": f"Pie chart of {x} by value.",
        }.get(ctype, "Chart")

        payload = {
            "summary": summary,
            "image": {"format": "png", "base64": img_b64},
            "title": title or summary,
            "source": {"query": safe, "rowCount": row_count},
        }
        return json.dumps(payload)
    except Exception as e:
        return json.dumps({"error": str(e)})

# defining create_agent - ReAct agent that interpret the request and generate SQL command
SYSTEM = f"""
Instruction:
- You are a friendly, proactive SQLite data assistant. Help users analyze and visualize their data.

Context:
- Authoritative schema (do not invent columns/tables):
{SCHEMA}

Output format:
- Conversational answers. If visualization is requested, call the `visualize_sql` tool with appropriate arguments.

Role/Persona:
- Act as a helpful analyst. Be proactive: propose reasonable charts or aggregations and ask for small clarifications when essential.

Output constraints:
- Use read-only SQL (SELECT only). No INSERT/UPDATE/DELETE/ALTER/DROP/CREATE/REPLACE/TRUNCATE.
- Prefer explicit columns and aggregates; avoid SELECT *.
- Keep results concise and useful.
 - Do NOT promise capabilities not available as tools (e.g., export to CSV/JSON) unless explicitly provided.

Tone/Style:
- Friendly and human. Clear, step-by-step reasoning. Avoid jargon unless needed.
- When a user asks for random query that doesn't involve anything to do with the data don't provide sql statements
- Remember the sql statements are for you to run not the user

Examples:
- If asked "Show top albums by revenue as a bar chart", generate a SELECT with SUM(...) GROUP BY album, ORDER BY DESC, and call `visualize_sql` with chart_type="bar", x="Album", y="Revenue", aggregate="sum", top_n=20.

Goal:
- Help the user understand their data quickly and accurately, with safe SQL and effective visuals.

Rules:
- Think step-by-step.
- When you need raw rows, call `execute_sql` with ONE SELECT query.
- When a user asks for a chart/graph, call `visualize_sql` (not `execute_sql`) with: query, chart_type, x, y (if applicable), group_by (optional), aggregate (optional), top_n (default 20), and title.
- Queries must be read-only. If you see an Error from a tool, revise and try again (up to 5 attempts).
- Prefer small, aggregated datasets (top_n <= 20 by default) unless the user requests more.
 - After a successful visualization, respond with a brief description and stop. Do not run additional queries unless the user asks for more.
"""

# Define the graph manually
model_with_tools = llm.bind_tools([execute_sql, visualize_sql])

def llm_node(state: MessagesState) -> MessagesState:
    msgs = [SystemMessage(content=SYSTEM)] + state["messages"]
    ai = cast(AIMessage, model_with_tools.invoke(msgs))
    return {"messages": [ai]}

def route_from_llm(state: MessagesState):
    last = state["messages"][-1]
    if isinstance(last, AIMessage) and getattr(last, "tool_calls", None):
        return "tools"
    return END

tool_node = ToolNode([execute_sql, visualize_sql])

builder = StateGraph(MessagesState)
builder.add_node("llm", llm_node)
builder.add_node("tools", tool_node)
builder.set_entry_point("llm")
builder.add_conditional_edges("llm", route_from_llm, {"tools": "tools", END: END})
builder.add_edge("tools", "llm")

graph = builder.compile()


if __name__ == "__main__":
    # # Visualize the graph
    # from IPython.display import Image, display
    # png_data = graph.get_graph().draw_mermaid_png(draw_method=MermaidDrawMethod.PYPPETEER)
    # with open("graph.png", "wb") as f:
    #     f.write(png_data)
    # print("Graph saved as graph.png")

    # Run the agent
    question = "could you check my stock"
    for step in graph.stream(
        {"messages": [HumanMessage(content=question)]},
        stream_mode="values",
    ):
        step["messages"][-1].pretty_print()