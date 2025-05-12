from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from.sub_agents.funny_nerd.agent import funny_nerd
from .sub_agents.stock_analyst.agent import stock_analyst
from .sub_agents.news_analyst.agent import news_analyst
from .tools.tools import get_current_time

root_agent = Agent(
    model='gemini-2.0-flash',
    name='manager',
    description='Manager agent',
    instruction="""
    You are a manager agent responsible for overseeing the operations of other agents.
    
    Always delegate tasks to the appropriate agents based on their expertise.Use your best judgment 
    to determine which agent to delgate the task to.
    
    You are responsible for delegating tasks to the following agent:
    - stock_analyst
    - funny_nerd
    
    You also have access to the following tools:
    - news_analyst
    - get_current_time
    """,
    sub_agents=[funny_nerd, stock_analyst],
    tools=[AgentTool(news_analyst), get_current_time]
)
