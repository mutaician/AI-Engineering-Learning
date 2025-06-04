from typing import Annotated, Sequence, TypedDict
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage # foundational class for all message types in Langraph
from langchain_core.messages import ToolMessage 
from langchain_core.messages import SystemMessage
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from elements_combinations import get_combination_result


# Annotated - provides additional context without affecting the type itself
# Sequence - automatically handle the state updates for sequences such as adding new messages to a chat history

load_dotenv()

# llm = ChatAnthropic(
#     model_name="claude-3-5-haiku-latest",
#     timeout=60,  # specify timeout in seconds
#     stop=None    # or provide a list of stop sequences if needed
# )

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

@tool
def gap_to_enlightment(n: int) -> str:
    """
    Calculates how far a given number is from the ultimate answer (42),
    and returns a playful explanation.

    Parameters:
        n (int): Any integer input.

    Returns:
        str: A message describing how close or far the number is from 42,
             the so-called 'Answer to the Ultimate Question of Life, the Universe, and Everything'.
    """
    diff = 42 - n
    if diff == 0:
        return "You have achieved perfect balance in the cosmos. 🌌"
    direction = "below" if diff > 0 else "above"
    return f"You are {abs(diff)} units {direction} the Great Answer."

@tool
def elemental_fusion(element1: str, element2: str) -> str:
    """
    Mixes two primal elements and returns the resulting creation.
    Inspired by ancient alchemy and sandbox fusion games.

    Returns:
        The product of the elemental combination if known, or a message like Combination not found! 

    This tool is meant to spark curiosity, creativity, and play. Ideal for use in interactive or fantasy-themed agents.
    """
    return get_combination_result([element1, element2])



tools = [gap_to_enlightment, elemental_fusion]

# model = ChatAnthropic(
#     model_name="claude-3-5-haiku-latest", timeout=60, stop=None, max_retries=3
# ).bind_tools(tools)

model = ChatGoogleGenerativeAI(model="gemini-2.0-flash").bind_tools(tools)


def model_call(state: AgentState) -> AgentState:
    system_prompt = SystemMessage(content="You are my Personal AI assistant, please answer my query to the est of your ability")
    response = model.invoke([system_prompt] + list(state['messages'])) 
    return {"messages": [response]}

def should_continue(state: AgentState):
    messages = state['messages']
    last_message = messages[-1]
    # Check if the last_message has the 'tool_calls' attribute and if it is non-empty
    if hasattr(last_message, "tool_calls") and getattr(last_message, "tool_calls", None):
        return "continue"
    else:
        return "end"

graph = StateGraph(AgentState)
graph.add_node("our_agent", model_call)

tool_node = ToolNode(tools=tools)
graph.add_node("tools", tool_node)

graph.set_entry_point("our_agent")
graph.add_conditional_edges(
    "our_agent",
    should_continue,
    {
        "continue": "tools",
        "end": END
    }
)

graph.add_edge("tools", "our_agent")

app = graph.compile()

def print_stream(stream):
    for s in stream:
        message = s['messages'][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()

inputs = {"messages": [("user", " what do i get when i combine the elements,  life and fire and tell me a joke about it")]}
print_stream(app.stream(inputs, stream_mode="values"))