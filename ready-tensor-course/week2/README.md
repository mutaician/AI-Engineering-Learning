## Building prompts for Agentic AI Systems

### Core components
- Instruction -> What you want the AI to do
- Input -> the content to work with
### Optional but game changing components
- Context -> Background information
- Output format -> structure of the result
- Role/Persona -> who the ai should act as
- output constraints -> length, style
- Tone/Style -> voice and approach to use
- Examples
- Goal -> underlying objective/purpose

## Advanced reasoning techniques

> Ask an LLM to solve a complex problem, and you might get a decent answer. Ask it to show its work first, and you'll often get a brilliant one.

1. Chain of Thought
- step by step, break problem into smaller parts and work through them logically
- introduced by the paper [Chain-of-Thought Prompting Elicits Reasoning in Large Language Models](https://arxiv.org/pdf/2201.11903)
- good for: multi-step problems, logical reasoning, analytical tasks or situation where path to the answer matters
- bad for simple tasks, illdefined problems and may produce convicing answers that are  wrong

2. ReAct Reason and Acting
- alternating between reasoning and taking actions to solve complex problems
- introduced by the paper [REACT: SYNERGIZING REASONING AND ACTING IN LANGUAGE MODELS](https://arxiv.org/pdf/2210.03629)
- good for: external-dependant problems, more than thinking , need actions and tools, immediate results guide the next step
- pattern: Think -> Act -> Observe -> Reflect

3. Self-Ask
- Generate sub-questions answer them one by one then synthesize the final answer
- good for: problems than needs to be broken down, explore multiple angles before decision

Examples: https://app.readytensor.ai/publications/3jI5t1hwF8wM

##### Training data connection with the advanced reasoning
- Chain of Thought: Math textbooks, tutorial explanations, step-by-step guides where humans write "First... then... therefore..."
- ReAct: Technical documentation, troubleshooting guides, research methodologies that follow "assess the situation → take action → evaluate results"
- Self-Ask: Academic papers, investigative journalism, educational content that breaks complex topics into sub-questions

## LLM Output Parsing

1. Regular prompting with format hints
- Explicit Format Instructions, Demonstrate with an Example, Be Precise and Predictable, Standardize Field Names and Types
2. Model-Native Structured Output
- 