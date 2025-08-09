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


