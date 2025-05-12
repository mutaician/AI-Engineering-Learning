# Tutorial on Building AI Agents using Agent Development Kit (ADK)

- install requirements
```bash
 uv pip install -r requirements.txt
 ```

### notes
root agent is important - intro to other agents
name of subagent should be same as folder the agent code is in 

#### Tools
Types:
1. Function - methods, agents as tools, long running
2. Built in tools - googlesearch, code execution, rag (only work with gemini)
3. third-party tools - crewai, langchain

on using tools you can only pass one tool per agent     
Custom tools - define return type(dict is preferred), docstring