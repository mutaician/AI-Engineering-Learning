# Workflows to Agents

AI agent are systems where LLM reasoning determines the next steps in a dynamic workflow
AI Agents Include:
1. multiple LLM calls
2. Tool use to search, calculate, write, fetch or manipulate
3. A reasoning loop that can reflect and revise
4. A planner / controller - coordinate what happens
5. Autonomy - decides how to achieve the goal

- most real world systems fall between agent and workflows
LangGraph is an open-source framework designed specifically for graph-based orchestration of agentic workflows — think of it as a way to give your agents a map, some structure, and a few ground rules... so they don’t wander off into chaos.

Langchain - building block - prompts, chains, tools, memory
Langgraph - flow control- how those blocks connect, branch, retry, loop and evolve over time
LangChain is great for predictable flows.
LangGraph is built for dynamic, multi-agent systems that adapt and evolve.

#### Core comppnents of langchain
1. state - context of your workflow represented as pydantic object/typed dict
2. nodes - function that receives current state and perform step of work and return 3. new version of the state
4. edges - define flow from one node to another
5. graph - structure of everything together, 

#### 5-step Langgraph Workflow
1. define state - what information needs to carry throughout the workflow
2. write node functions , receive current state and return updated version
3. create a graph builder, instatiate a Stategraph specifying the state type
4. Add nodes and edges - register the node functions and define how they connect
5. Compile and run the graph

#### How State Updates Work: Reducer Functions
- overwrite (default)
- append to messages (LLM Chat apps)
- append to generic lists
- sum or count
- custom merge logic 