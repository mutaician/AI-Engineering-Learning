# Q&A sql Agent

I am testing how to read sql database with AI
To manage complex sql queries, basically talking to your database without having to use sql

This readme was all written by human(me😅). Expect human nuisances if you want to explore this project

### To test it out (might work or not)
- have uv installed and set venv
- this project is inside a bigger directory so figure out how to get the code in [qa-sql.py](./qa-sql.py) and get dependencies in [pyproject.toml](./pyproject.toml) installed 
- have OPENAI_API_KEY or GOOGLE_API_KEY in [.env](.env)
- run **uv run qa-sql.py**
- if you want to know how the agent outputs check [agent-process](./agent-process-log.txt)
- Don't mind about other files

The whole project was from [langchain tutorial](https://python.langchain.com/docs/tutorials/sql_qa/)
Check it out to find clear instruction of creating a simple question answering system
