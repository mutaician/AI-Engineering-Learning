# Messed up with my local git repo setup test but all credits of this directory/folder goes to https://github.com/readytensor/rt-repo-assessment 

# This folder has all the resources I am using while learning about Agentic AI Developer Certification Program by [readytensor](https://app.readytensor.ai/hubs/ready_tensor_certifications)

## Real-World Applications of Agentic AI

Agentic AI is already making significant impacts across various industries:

### Customer Support
- Chatbots that resolve the majority of queries without human intervention
- Systems that analyze customer sentiment and route complex issues to appropriate departments
- Virtual assistants handling scheduling, cancellations, and basic troubleshooting

### Healthcare
- Diagnostic agents cross-referencing symptoms with medical journals
- Medication management systems that track patient adherence
- Radiology assistants that flag potential abnormalities in medical imaging
- Patient monitoring agents that alert healthcare providers to concerning trends

### Finance
- Fraud-detection agents scanning transactions in real time
- Investment advisors analyzing market trends and portfolio performance
- Algorithmic trading systems that adapt strategies based on market conditions
- Personal finance assistants that provide budgeting recommendations and spending insights

### Logistics
- Warehouse robots coordinating deliveries
- Supply chain optimization systems predicting bottlenecks
- Route optimization agents that adapt to traffic patterns and weather conditions
- Inventory management systems that automatically reorder based on demand forecasting

### Creative Industries
- AI writing teams drafting content
- Design assistants generating mockups based on specifications
- Music composition tools creating original scores based on style parameters
- Video editing assistants that identify and compile highlights from raw footage

### Software Development
- Coding agents like GitHub Copilot suggesting code completions in real time
- Cursor AI generating entire functions or classes based on natural language descriptions
- Debugging assistants that identify potential bugs and suggest fixes
- Documentation generators that automatically create readable explanations of code
- Code refactoring tools that suggest improvements to existing codebases
- Testing agents that generate comprehensive test cases based on function specifications
- DevOps assistants that monitor deployment pipelines and resolve common issues

### Education
- Personalized tutoring agents that adapt to individual learning styles
- Automated grading systems providing detailed feedback on assignments
- Curriculum development assistants suggesting content based on learning objectives
- Student progress monitoring tools identifying areas needing intervention

### Legal
- Contract review agents flagging potential issues in legal documents
- Legal research assistants finding relevant case law for specific situations
- Document automation tools generating standardized legal forms
- Compliance monitoring systems ensuring adherence to regulatory requirements
  

## How to spot an Agentic Use Case

1. The task is ambiguous or goal-driven
2. Multiple tools or Api's are involved
3. It needs reasoning, delegation or decision making

- Agentic AI is not the only solution for every problem
- For repetitive steps, fixed inputs go for RPA(Robot Process Automation), macros, scripts
- for predicting outcomes from labeled tasks go for machine learning
- Go for Agentic AI for open-ended goals involving tools and steps


### Factors for choosing a Framework
1. Use Case: What's your agent's primary purpose? Different frameworks excel at different tasks.
2. Level of Abstraction: Do you want full control over prompts, memory, and workflows, or a higher-level framework that handles those under the hood?
3. Criticality: Is this a mission-critical system? Choose battle-tested tools for essential applications.
4. Team Skills: Do you have Python experts, or would no-code tools be more appropriate?
5. Time/Budget: Need a quick solution or have resources for a more custom approach?
6. Integration Requirements: Will you need to connect with external systems like Slack, Jira, etc.?
7. Scalability Considerations: Think about monitoring, logging, and auto-scaling if you'll serve many users.

- For personal projects don't overthink just go with what's good enough to complete the job
- Don't be a tool expert, it's CLM - Career Limiting Move

## Agents Vs Workflows - still confuses me btw 😅
- Workflows is predefined procees, giving the exact process on how the llm is going to complete a task
  - (systems where LLMs and tools are orchestrated through predefined code paths.)
- Agents is for unsure steps, you have a goal but you don't know the exact steps the llm is going to take when its interacting with tools ...
  - systems where LLMs dynamically direct their own processes and tool usage, maintaining control over how they accomplish tasks.

#### Notes from antropic [article](https://www.anthropic.com/engineering/building-effective-agents)

##### Types of Workflows
1. prompt chaining
2. routing
3. parallelization
4. orchestrator-workers
5. evaluator-optimizer

##### Agents Implementation Principles
1. maintain simplicity in your agent's design
2. prioritize transparency by explicitly showing the agent's planning steps
3. carefully craft your agent-computer interface (ACI) through thorough tool documentation and testing
