from typing import Optional
from datetime import datetime

from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.genai import types

def before_agent_callback(callback_context: CallbackContext) -> Optional[types.Content]:
    """
    Simple callback that logs when the agent starts processing the  request
    Args: callback_context: contains state and context information
    Returns: None to continue with normal agent processing
    """

    # Get session statee
    state = callback_context.state

    # record timestamp
    timestamp = datetime.now()

    # set agent name if not present
    if "agent_name" not in state:
        state["agent_name"] = "SimpleChatBot"
    
    # initialize request counter
    if "request_counter" not in state:
        state["request_counter"] = 1
    else:
        state["request_counter"] += 1

    # Store start time for duration calculation in after_agent_callback
    state["request_start_time"] = timestamp
    
    # Log the request
    print("=== AGENT EXECUTION STARTED ===")
    print(f"Request #: {state['request_counter']}")
    print(f"Timestamp: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")

    # Print to console
    print(f"\n[BEFORE CALLBACK] Agent processing request #{state['request_counter']}")

    return None

def after_agent_callback(callback_context: CallbackContext) -> Optional[types.Content]:
    """
    Simple callback that logs when the agent finishes processing a request.

    Args:
        callback_context: Contains state and context information

    Returns:
        None to continue with normal agent processing
    """
    # Get the session state
    state = callback_context.state

    # Calculate request duration if start time is available
    timestamp = datetime.now()
    duration = None
    if "request_start_time" in state:
        duration = (timestamp - state["request_start_time"]).total_seconds()

    # Log the completion
    print("=== AGENT EXECUTION COMPLETED ===")
    print(f"Request #: {state.get('request_counter', 'Unknown')}")
    if duration is not None:
        print(f"Duration: {duration:.2f} seconds")

    # Print to console
    print(
        f"[AFTER CALLBACK] Agent completed request #{state.get('request_counter', 'Unknown')}"
    )
    if duration is not None:
        print(f"[AFTER CALLBACK] Processing took {duration:.2f} seconds")

    return None


root_agent = LlmAgent(
    model='gemini-2.0-flash-lite',
    name='root_agent',
    description='A basic agent that demonstrates before and after agent callbacks',
    instruction="""You are a friendly greeting agent. Your name is {agent_name}.
    Your job is to:
    - Greet users politely
    - Respond to basic questions
    - keep your response friendly and concise""",
    before_agent_callback=before_agent_callback,
    after_agent_callback=after_agent_callback,
    
)
