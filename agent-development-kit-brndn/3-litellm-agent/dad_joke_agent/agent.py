import os
import random

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

model = LiteLlm(
    model="openrouter/mistralai/mistral-small-3.1-24b-instruct:free",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

def get_dad_joke():
    """Get a random dad joke."""
    jokes = [
        "Why don't skeletons fight each other? They don't have the guts.",
        "I'm reading a book on anti-gravity. It's impossible to put down!",
        "Did you hear about the claustrophobic astronaut? He just needed a little space.",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "I would tell you a joke about an elevator, but it's an uplifting experience.",
    ]
    return random.choice(jokes)

root_agent = Agent(
    model=model,
    name='dad_joke_agent',
    description='A dad joke generator agent.',
    instruction="""
    You are a helpful assistant that can tell dad jokes.
    Only use the tool `get_dad_joke` to tell jokes.""",
    tools=[get_dad_joke]
)
