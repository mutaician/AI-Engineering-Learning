# Week 1 Assignment: Understanding AI Agents 

## Part 1: Reflection Questions

1. Foundational Understanding
How would you explain the difference between traditional AI systems and AI agents to someone with limited technical background?
Answer: traditional ai systems is like guiding a system on the exact thing to do, it includes predefined steps the AI has to take to achieve a goal while agentic ai is giving the system a goal and necessary tools to use to achieve the goal and let the ai plan, decide on what to do and actually do it

2. Professional Application
Think about your organization or industry. What specific tasks could benefit from AI agents? What would an implementation look like for one of these tasks?
Answer: 

3. Architecture Analysis
The virtual assistance example we discussed in the lecture employs a specific multi-agent architecture. What type of architecture is it, and why is this approach effective for this application?
Answer: centralized networks, for easier communication and coordination -- the orchestrator agent is necessary to determine the intent for the prompt and decide on the appropriate agent to do the task.

4. Components Analysis
Choose one cognitive component of AI agents (Perception, Reasoning, Action, or Feedback & Learning) and explain how it manifests in a real-world AI application of your choice
Answer: Feedback and learning - in real world humans learn by error and correction, you try something it doesn't work you get to know why it didn't work and what you are going to do for the next try

## Part 2: Case Evaluation - When to Use Agentic Systems

For each of the following scenarios, evaluate whether an agentic AI system would be appropriate. Explain your reasoning by discussing the benefits and drawbacks of using an agent versus a non-agentic solution.

1. Simple Data Lookup: A system that retrieves specific information from a structured database in response to direct queries (e.g., "What is the price of Product X?")
Your Answer Here: agent solution because the database requires exact command/language to query values and the input is a natural language so an agent is needed to understand the intent and generate the correct database query

2. Basic Calculator: A tool that performs straightforward mathematical operations like addition and multiplication
Your Answer Here: non-agentic solution, math operations doesn't need any agentic operations. It would be wasting tokens and time to do such operations that doesn't need any reasoning

3. Travel Planning Assistant: A system that needs to coordinate flights, accommodations, transportation, and activities based on user preferences, budget constraints, and real-time availability
Your Answer Here: agentic solution is needed as their are many variables present which are varying (each one is unique based on an individual) the agent needs to consider that so as to coordinate travel operations. Though I am thinking of non-agentic solution specifically machine learning when lots of data is involved (not that sure).

4. Research Synthesis: A system that searches across multiple sources, extracts relevant information, evaluates credibility, and compiles findings into a cohesive report
Your Answer Here: agentic solution, depending on the research topic the it has to be agent to plan on researching multiple sources and getting relevant info and turn it into a cohesive report. 

5. Smart Home Coordinator: A system that manages multiple connected devices, anticipates user needs based on patterns, and proactively adjusts settings accordingly
Your Answer Here: agentic solution, to learn user patterns and adjust accordingly

6. Email Management: A system that sorts incoming emails and drafts responses
Your Answer Here: agentic solution, for the agent to understand type of email and understand the email and draft a specific response to specific intended email

7. Medical Symptom Assessment: A system designed to evaluate described symptoms and provide health information
Your Answer Here: agentic solution, the agent needs to understand the symptoms and generate correct info based on it.

8. Financial Investment Advisor: A system providing investment recommendations based on market conditions and user goals
Your Answer Here: non-agentic solution as its based on data and investment goals

## Part 3: Repository Analysis
Review the codebase at https://github.com/readytensor/rt-repo-assessment. Based on the definition of agentic AI systems we've covered in the lecture, would you classify this solution as agentic? Why or why not? Support your analysis with specific examples from the codebase that either align with or deviate from the key characteristics of AI agents we've discussed.

Answer: ~~Got ratelimited 🥲😅: openai.RateLimitError: Error code: 429 - {'error': {'message': 'Rate limit reached for gpt-5-nano in organization org-5UQGs3k1JQD71z6x5RzWYvaq on tokens per min (TPM): Limit 200000, Used 198168, Requested 5110. Please try again in 983ms. Visit https://platform.openai.com/account/rate-limits to learn more.', 'type': 'tokens', 'param': None, 'code': 'rate_limit_exceeded'}}~~ lowered number of workers in config.json
It aligns with key characteristics of AI Agents, as the repo to be accessed is unique, the agent has access to tools to know more about the repo and get a specific information about the repo. with the content of the repo the agent understands what to do with it considering the final goal of providing final report of the repo. Liked the parallel processing

## Part 4: Future of Work Analysis
Based on what you have understood about agentic AI in Week 1, do you think the following job titles will be eliminated in the next 10 years due to agentic AI? Explain your reasoning for each:
● Software Engineer
● Data Analyst
● Data Scientist
● ML Engineer
● AI Engineer
● Data Engineer
● ML-Ops Engineer
Your Answer Here: I don't think the roles will be eliminated, short why: not every problem needs an agent


## Part 5: Choosing the Right Architecture for an Automated
Peer Review System
Background:
Imagine you are tasked with building a system to automatically review academic papers for a journal submission platform. The system should read the paper identify strengths and weaknesses, and generate a structured review.
Exercise:
Below are two different architectural designs for this system:
● One is a non-agentic workflow,
● One is a multi-agent system,
Your task:
● Carefully study the two architectures.
● Based on what you learned about Workflows vs. Agents, choose the architecture you think
will perform best for this task.
● There is no right or wrong answer - we want you to think strategically about tradeoffs like
flexibility, transparency, cost, complexity, and reliability.
● You can also propose another architecture that you think would be best for this case study.
In 2–8 sentences, explain why you made your choice. 
Your Answer Here: Agentic architecture (multiagent system), to make the sytem more flexible, we can dedicate different models to a specific task powerful one for planning, smaller one for verifying with external knowledge, we can add human in the loop to the agentic system .... with it also we can know where the issue is in debugging agent process, like which agent needs more fixes and features. 