from datetime import datetime
from google.adk.agents import Agent
from google.adk.tools import google_search

def get_current_time() -> dict:
    """
    Get the current time in the format YYYY-MM-DD HH:MM:SS
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {"current_time": current_time}

root_agent = Agent(
    model='gemini-2.0-flash-001',
    name='tool_agent',
    description='Tool agent',
    instruction='Answer user questions to the best of your knowledge,you can use the following tools - google_search, get_current_time',
    tools=[google_search],
)
