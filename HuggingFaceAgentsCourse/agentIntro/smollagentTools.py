from smolagents import Tool, CodeAgent, LiteLLMModel, tool
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

model = LiteLLMModel(
    model_id="openrouter/openrouter/optimus-alpha",
    api_key=api_key,
    max_tokens=8192
)

@tool
def catering_service_tool(query: str) -> str:
    """
    This tool returns the highest-rated catering service in Gotham City.

    Args:
        query: A search term for finding catering services.
    """
    # Example list of catering services and their ratings
    services = {
        "Gotham Catering Co.": 4.9,
        "Wayne Manor Catering": 4.8,
        "Gotham City Events": 4.7,
    }

    # Find the highest rated catering service (simulating search query filtering)
    best_service = max(services, key=services.get)

    return best_service

def simple_tool_function():
    agent = CodeAgent(tools=[catering_service_tool], model=model)

    # Run the agent to find the best catering service
    result = agent.run(
        "Can you give me the name of the highest-rated catering service in Gotham City?"
    )

    print(result) 

# simple_tool_function()

# Creating a subclass of Tool for more complex functionality
class SuperheroPartyThemeTool(Tool):
    name = "superhero_party_theme_generator"
    description = """
    This tool suggests creative superhero-themed party ideas based on a category.
    It returns a unique party theme idea."""

    inputs = {
        "category": {
            "type": "string",
            "description": "The type of superhero party (e.g., 'classic heroes', 'villain masquerade', 'futuristic Gotham').",
        }
    }

    output_type = "string"

    def forward(self, category: str):
        themes = {
            "classic heroes": "Justice League Gala: Guests come dressed as their favorite DC heroes with themed cocktails like 'The Kryptonite Punch'.",
            "villain masquerade": "Gotham Rogues' Ball: A mysterious masquerade where guests dress as classic Batman villains.",
            "futuristic Gotham": "Neo-Gotham Night: A cyberpunk-style party inspired by Batman Beyond, with neon decorations and futuristic gadgets."
        }

        return themes.get(category.lower(), "Themed party idea not found. Try 'classic heroes', 'villain masquerade', or 'futuristic Gotham'.")

def complex_tool_function():
    party_theme_tool = SuperheroPartyThemeTool()
    agent = CodeAgent(tools=[party_theme_tool], model=model)
    result = agent.run("What would be a good superhero party idea for a 'villain masquerade' theme?")
    print(result)

# complex_tool_function()

"""
    Default ToolBox
        PythonInterpreterTool
        FinalAnswerTool
        UserInputTool
        DuckDuckGoSearchTool
        GoogleSearchTool
        VisitWebpageTool
"""