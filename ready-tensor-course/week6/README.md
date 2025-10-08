# Architecting Multiagent systems

1. Design multi-agent systems that operate in sequence or in parallel  
2. Assign clear, non-overlapping roles to agents to avoid confusion and redundancy  
3. Connect agents into a collaborative, fault-tolerant system  
4. Use LangGraph to manage agent state, coordination, and decision-making  
5. Build with modularity, safety, and observability in mind  

## Building blocks of Agentic Systems 

### Primitives 
Logic node - llm, programming logic , it processes input and emit output
Edge - connection between the nodes that defines flow and data transfer, conditional or simple
Tool - callable interface to external functionality - agents to interact with the world
Memory - storage unit for context ,- persistent across steps or sessions

### Workflow Patterns
Chain(Sequential pattern) - straight line, one thing happens then the next
Router - adds decision making, inspect input and choose the next step
Parallelism - if tasks are independent run them in parallel 
Generator-Evaluator Loop - one node creates another critiques
Orchestrator - when task is too complex or dynamic for a chain or router it's time to orchestrate
Retry/Fallback - when things don't go wrong, don't crash try again or try something else

### Agentic Patterns
Assmebly Line - chain of agents each handling a distnct part of the task. each step is handled by a fully-fledged agent
Reflection - mirror generator - evaluator workflow but at the agentic level
Supervisor - one agent oversees the work of others -- assigning tasks, checking outputs or deciding when to intervene
Hierarchial - agents are arranged in a hierarchy- with higher levels agents breaking down tasks and lower agents executing them
Competitive pattern - multiple agents tackle the same task independently,  and the system selects the best result
Network - agents operate in a loose, decentralized network - communicating with each other, sometimes recursively to achieve a desired goal

> Real-World Systems Combine these patterns

### Antipatterns to avoid
1. One Agent to Rule Them All - Designing a single agent to handle everything.
2. Death by a Thousand Agents - Designing one agent per tiny task, too many agents, each doing too little
3. The LLM Hammer - Treating every node like an agent — even when it doesn’t need to be.
4. The Chain of Pain - Designing overly lengthy sequence of agents that depend on each other.
5. Blurred Boundaries - Assigning multiple agents vague or poorly defined roles.
6. Falling Through the Cracks - Leaving parts of the workflow undefined. *Apply MECE Principle
7. No Escape Hatch - Designing loops with no cap, limit, or fail-safe. 

### Designing with purpose
What's the problem?
What's the cleanest, smartest way to solve it?
Where do agents actually make sense?
