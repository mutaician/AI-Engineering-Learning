from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from dotenv import load_dotenv
from typing import List, Union
import yaml
import os

load_dotenv()

with open('data/publication-small.md') as f:
    publication_content = f.read()

llm = ChatGroq(
    model='llama-3.1-8b-instant',
    temperature=0.7,
    streaming=True,
    api_key=os.getenv("GROQ_API_KEY") # type: ignore
)

conversation: List[Union[SystemMessage, HumanMessage, AIMessage]] = [
    SystemMessage(f"You are a helpful AI Assistant discussing research publication.\n\nBased your answers only on this publication content: {publication_content}")
]

# user question 1
conversation.append(HumanMessage(content=f"""What are variational autoencoders and list top 5 applications for them?"""))
response1 = llm.invoke(conversation)
print("AI response for question 1")
print(response1.content)

conversation.append(AIMessage(response1.content))

conversation.append(HumanMessage(content="How does it work in the case of anomaly detection?"))
print("AI response for question 2")

for chunk in  llm.stream(conversation):
    print(chunk.content, end='', flush=True)
