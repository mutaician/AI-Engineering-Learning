from dotenv import load_dotenv
import os
from openai import OpenAI


load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

def use_tool(tool_name, input_text):
    if tool_name == "calculator":
        try:
            result = eval(input_text)
            return str(result)
        except Exception as e:
            return f"Error in calculation: {str(e)}"
    return "Tool not found or invalid input."

messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant.Keep your responses short and concise."
    }
]

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break

    # simulate tool usage detection
    # i.e calculate 2 + 3 * 4
    if user_input.lower().startswith("calculate"):
        expression = user_input[len("calculate "):]
        tool_response = use_tool("calculator", expression)
        print(f"Assistant (tool): {tool_response}")
        messages.append({"role": "user", "content": user_input})
        messages.append({"role": "assistant", "content": tool_response})
    else:
        messages.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model="openrouter/optimus-alpha",
            messages=messages,
        )
        messages.append({"role": "assistant", "content": response.choices[0].message.content})

        print(response.choices[0].message.content)