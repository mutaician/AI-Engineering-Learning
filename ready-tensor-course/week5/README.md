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

### Langsmith
- platform that brings observabillity to language model-powered systems   

. Full-system traceability. Every action your system takes — LLM calls, tool invocations, node transitions — is logged in sequence, so you can see how things actually ran.
. Live state visibility. For each step, LangSmith shows you the exact input, output, and state updates — letting you debug without guesswork.
. Visual timeline. Traces are displayed as interactive, navigable timelines. You can inspect branches, loops, retries, and conditional paths at a glance.
. Performance and cost insights. LangSmith tracks token usage, latency, and per-call costs. No more wondering where the slowdowns or expenses are coming from.
. Automated evaluations. With built-in LLM-powered grading, you can define test sets and measure output quality over time — no manual spot-checking required.
. Searchable, organized runs. Tag, filter, and explore past runs by user, version, or use case — perfect for regression testing, debugging, or collaboration.

## Learning project

### Simple Joke Bot with LangGraph

This project includes a simple CLI-based joke bot implemented using LangGraph, demonstrating agentic workflows with LLM integration.

#### Setup
1. Install dependencies: `uv sync`
2. Add necessary API keys to your `.env` file:
   - `OPENAI_API_KEY`: For the critic LLM (ChatOpenAI)
   - `CEREBRAS_API_KEY`: For the writer LLM (ChatCerebras)

#### Running the Bot
Run the joke bot with: `uv run joke.py`

The bot allows users to:
- Generate jokes using an LLM (via writer and critic nodes)
- Change joke categories and languages
- Reset jokes
- Quit the session

#### LangGraph Implementation
- **State**: `JokeState` (Pydantic model) tracks jokes, user choices, categories, languages, and approval status.
- **Nodes**: 
  - `show_menu`: Displays options and gets user input.
  - `writer`: Generates jokes using Cerebras LLM.
  - `critic`: Approves/rejects jokes using OpenAI LLM, with retry logic.
  - `show_final_joke`: Displays approved jokes and adds to state.
  - Other nodes for category/language changes, reset, and exit.
- **Edges**: Conditional routing based on user choices and approval status.
- **Flow**: User selects "n" → writer → critic → show_final_joke (if approved) → back to menu.

#### Important Files
- `joke.py`: Main bot implementation with LangGraph graph.
- `utils.py`: Utility functions (e.g., loading prompt configs).
- `prompt_builder.py`: Builds prompts for LLMs.
- `.env`: Environment variables for API keys (not committed to repo).