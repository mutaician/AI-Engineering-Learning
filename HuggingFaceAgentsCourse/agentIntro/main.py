from dotenv import load_dotenv
import os
from smolagents import CodeAgent, LiteLLMModel, DuckDuckGoSearchTool, tool, ToolCallingAgent
import datetime


load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

model = LiteLLMModel(
    model_id="openrouter/openrouter/optimus-alpha",
    api_key=api_key,
    max_tokens=8192
)

def example1():
    agent = CodeAgent(
        tools=[DuckDuckGoSearchTool()],
        model=model)


    agent.run("Search for the best music recommendations for a party at the AI's mansion.")

# Custom tool
@tool
def suggest_menu(occasion: str) -> str:
    """
    Suggests a menu based on the occasion.
    Args:
        occasion (str): The type of occasion for the party. Allowed values are:
                        - "casual": Menu for casual party.
                        - "formal": Menu for formal party.
                        - "superhero": Menu for superhero party.
                        - "custom": Custom menu.
    """
    if occasion == "casual":
        return "Pizza, snacks, and drinks."
    elif occasion == "formal":
        return "3-course dinner with wine and dessert."
    elif occasion == "superhero":
        return "Buffet with high-energy and healthy food."
    else:
        return "Custom menu for the butler."
    
def custom_tool():
    agent = CodeAgent(tools=[suggest_menu], model=model)

    agent.run("Prepare a formal menu for the party.")

# Using python import inside the agent
def agent_with_import():
    agent = CodeAgent(tools=[], model=model, additional_authorized_imports=['datetime'])

    agent.run(
        """
        Alfred needs to prepare for the party. Here are the tasks:
        1. Prepare the drinks - 30 minutes
        2. Decorate the mansion - 60 minutes
        3. Set up the menu - 45 minutes
        4. Prepare the music and playlist - 45 minutes

        If we start right now, at what time will the party be ready?
        """
    )

# Tool calling agent
def tool_calling_agent():
    agent = ToolCallingAgent(tools=[DuckDuckGoSearchTool()], model=model)
    agent.run("Search for the best music recommendations for a party at the Wayne's mansion.")

tool_calling_agent()

