from dotenv import load_dotenv
import os
from smolagents import CodeAgent, LiteLLMModel, DuckDuckGoSearchTool


load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

model = LiteLLMModel(
    model_id="gemini/gemini-2.0-flash",
    api_key=api_key,
    max_tokens=8192
)

agent = CodeAgent(
    tools=[DuckDuckGoSearchTool()],
    model=model)


agent.run("Search for the best music recommendations for a party at the Wayne's mansion.")

