from dotenv import load_dotenv
import os
from openai import OpenAI


load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

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
    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="openrouter/optimus-alpha",
        messages=messages,
    )
    messages.append({"role": "assistant", "content": response.choices[0].message.content})

    print(response.choices[0].message.content)