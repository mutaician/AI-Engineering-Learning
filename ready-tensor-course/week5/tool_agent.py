from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_community.tools import TavilySearchResults
from langchain_openai import ChatOpenAI
from langchain_core.runnables.graph import MermaidDrawMethod
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-5-mini", temperature=0)
# llm2 = 


# Define Agent's Memory and Tools
class State(TypedDict):
    messages: Annotated[list, add_messages]


def get_tools():
    return [TavilySearchResults(max_results=3, search_depth="basic")]

def llm_node(state: State):
    """Your Agent's brain - decides whether to use tools or respond"""
    
    tools = get_tools()
    llm_with_tools = llm.bind_tools(tools)
    
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}

def tols_node(state: State):
    """Your agent's hands - executes the chosen tools"""
    tools = get_tools()
    tool_registry = {tool.name: tool for tool in tools}
    
    last_message = state["messages"][-1]
    tool_messages = []
    
    # execute each tool the agent requested
    for tool_call in last_message.tool_calls:
        tool = tool_registry[tool_call["name"]]
        result = tool.invoke(tool_call["args"])
        
        tool_messages.append(ToolMessage(
            content=str(result),
            tool_call_id=tool_call["id"]
        ))
    
    return {"messages": tool_messages}

def should_continue(state: State):
    """Decides whether to use tools or provide final answer"""
    last_message = state["messages"][-1]
    
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return END

def create_agent():
    graph = StateGraph(State)
    
    graph.add_node("llm", llm_node)
    graph.add_node("tools", tols_node)
    
    graph.set_entry_point("llm")
    
    graph.add_conditional_edges("llm", should_continue, {"tools": "tools", END: END})
    graph.add_edge("tools", "llm")
    
    return graph.compile()

agent = create_agent()

print(agent.get_graph().draw_ascii())

initial_state = {
    "messages": [
        SystemMessage(content="You are a helpful assistant with access to web search. Use the search tool when you need current information."),
        HumanMessage(content="What's the latest new about AI developments in 2025?")
    ]
}

result = agent.invoke(initial_state)
print(result["messages"][-1].content)
