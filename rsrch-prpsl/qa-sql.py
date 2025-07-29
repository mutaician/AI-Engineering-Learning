from langchain_community.utilities import SQLDatabase
from typing_extensions import TypedDict, Annotated
from dotenv import load_dotenv
import os
import getpass
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.tools.sql_database.tool import QuerySQLDatabaseTool
from langgraph.graph import START, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

load_dotenv()

if not os.getenv("GOOGLE_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter API key for google gemini: ")

# llm = init_chat_model("gemini-2.5-flash-lite", model_provider="google_genai")
llm = init_chat_model("gpt-4.1-mini", model_provider="openai")

db = SQLDatabase.from_uri("sqlite:///Chinook.db")
# print(db.dialect)
# print(db.get_usable_table_names())
# print(db.run("SELECT * FROM Artist LIMIT 10;"))


class State(TypedDict):
    question: str
    query: str
    result: str
    answer: str


class QueryOutput(TypedDict):
    """Generated SQL query."""

    query: Annotated[str, ..., "Syntactically valid SQL query."]


def write_query(state: State):
    """Generate SQL query to fetch information"""
    prompt = query_prompt_template.invoke(
        {
            "dialect": db.dialect,
            "top_k": 10,
            "table_info": db.get_table_info(),
            "input": state["question"],
        }
    )
    structured_llm = llm.with_structured_output(QueryOutput)
    result = structured_llm.invoke(prompt)
    return {"query": result["query"]}  # type: ignore


def execute_query(state: State):
    """Execute SQL query"""
    execute_query_tool = QuerySQLDatabaseTool(db=db)
    return {"result": execute_query_tool.invoke(state["query"])}


def generate_answer(state: State):
    """Answer question using retrieved information as context"""
    prompt = (
        "Given the following question, corresponding SQL query, and SQL result, answer the user question.\n\n"
        f"Question: {state['question']}"
        f"SQL Query: {state['query']}"
        f"SQL Result: {state['result']}"
    )
    response = llm.invoke(prompt)
    return {"answer": response.content}


system_message = """
Given an input question, create a syntactically correct {dialect} queery to
run to help find the answer. Unless the user specifies in his question a specific number of examples
they wish to obtain, always limit your query to at most {top_k} results. You can order the results by
a relevant column to return the most interesting examples in the database.

Never query for all the colummns from a specific table, only ask for a few relevant columns given the question

Pay attention to use only the column names that you can see in the schema description.Be careful to not query for
columns that do not exist. Also, pay attention to which column is in which table.

Only use the following tables:
{table_info}
"""

user_prompt = "Question: {input}"

query_prompt_template = ChatPromptTemplate(
    [("system", system_message), ("user", user_prompt)]
)


# ==================================================================
#                           CHAIN
# ==================================================================

# graph_builder = StateGraph(State).add_sequence(
#     [write_query, execute_query, generate_answer]
# )

# graph_builder.add_edge(START, "write_query")
# memory = MemorySaver()
# graph = graph_builder.compile(checkpointer=memory, interrupt_before=["execute_query"])

# config = {"configurable": {"thread_id": "1"}}

# for step in graph.stream(
#     {"question": "Tell me the employees in IT"}, config, stream_mode="updates"
# ):
#     print(step)

# try:
#     user_approval = input("Do you want to go to execute query? (yes/no): ")
# except Exception:
#     user_approval = "no"

# if user_approval.lower() == "yes":
#     for step in graph.stream(None, config, stream_mode="updates"):
#         print(step)
# else:
#     print("Operation cancelled by user.")

# ==================================================================
#                           Agent
# ==================================================================

toolkit = SQLDatabaseToolkit(db=db, llm=llm)

tools = toolkit.get_tools()
# print(tools)

system_message = """
You are an agent designed to interact with a SQL database.
Given an input question, create a syntactically correct {dialect} query to run,
then look at the results of the query and return the answer. Unless the user
specifies a specific number of examples they wish to obtain, always limit your
query to at most {top_k} results.

You can order the results by a relevant column to return the most interesting
examples in the database. Never query for all the columns from a specific table,
only ask for the relevant columns given the question.

You MUST double check your query before executing it. If you get an error while
executing a query, rewrite the query and try again.

DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the
database.

To start you should ALWAYS look at the tables in the database to see what you
can query. Do NOT skip this step.

Then you should query the schema of the most relevant tables.
""".format(
    dialect="SQLite",
    top_k=5,
)

agent_executor = create_react_agent(llm, tools, prompt=system_message)

question = "Describe the playlist track table?"
# uncomment below code to run agent_executor
# for step in agent_executor.stream(
#     {"messages": [{"role": "user", "content": question}]},
#     stream_mode="values"
# ):
#     step["messages"][-1].pretty_print()

import ast
import re


def query_as_list(db, query):
    res = db.run(query)
    res = [el for sub in ast.literal_eval(res) for el in sub if el]
    res = [re.sub(r"\b\d+\b", "", string).strip() for string in res]
    return list(set(res))


artists = query_as_list(db, "SELECT Name FROM Artist")
albums = query_as_list(db, "SELECT Title FROM Album")
# print(albums[:5])

from langchain_google_genai import GoogleGenerativeAIEmbeddings

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

from langchain_chroma import Chroma

vector_store = Chroma(
    collection_name="example_collection",
    embedding_function=embeddings,
    persist_directory="./chroma_langchain_db",  # Where to save data locally, remove if not necessary
)

from langchain.agents.agent_toolkits import create_retriever_tool

# _ = vector_store.add_texts(artists + albums)
retriever = vector_store.as_retriever(search_kwargs={"k": 5})
description = (
    "Use to look up values to filter on. Input is an approximate spelling "
    "of the proper noun, output is valid proper nouns. Use the noun most "
    "similar to the search."
)
retriever_tool = create_retriever_tool(
    retriever,
    name="search_proper_nouns",
    description=description,
)

# print(retriever_tool.invoke("Alice Chains"))

# Add to system message
suffix = (
    "If you need to filter on a proper noun like a Name, you must ALWAYS first look up "
    "the filter value using the 'search_proper_nouns' tool! Do not try to "
    "guess at the proper name - use this function to find similar ones."
)

system = f"{system_message}\n\n{suffix}"

tools.append(retriever_tool)

agent = create_react_agent(llm, tools, prompt=system)

# question = "Find albums by that band that sounds like 'Metallico' or something similar"  # passed
# question = "Which months show unusual spikes in jazz purchases compared to normal patterns?"
question = "Which customers are our biggest spenders and what genres do they prefer?"

for step in agent.stream(
    {"messages": [{"role": "user", "content": question}]},
    stream_mode="values",
):
    step["messages"][-1].pretty_print()
