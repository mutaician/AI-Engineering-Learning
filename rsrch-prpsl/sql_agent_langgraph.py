# initialize an LLM
from langchain.chat_models import init_chat_model

llm = init_chat_model("openai:gpt-5")

import pathlib
import requests

# Initialize the database
from langchain_community.utilities import SQLDatabase

url = "https://storage.googleapis.com/benchmarks-artifacts/chinook/Chinook.db"
local_path = pathlib.Path("Chinook.db")

if local_path.exists():
    print(f"{local_path} already exists, skipping download.")
else:
    response = requests.get(url)
    if response.status_code == 200:
        local_path.write_bytes(response.content)
        print(f"File downloaded and saved as {local_path}")
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")

db = SQLDatabase.from_uri("sqlite:///Chinook.db")
SCHEMA = db.get_table_info()

# Graph State
from typing import Optional

class GraphState(MessagesState):
    first_name: Optional[str]
    last_name: Optional[str]
    customer: bool
    customer_id: Optional[int]