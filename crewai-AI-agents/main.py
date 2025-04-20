from crewai import Agent, Task, Crew, LLM, Process

llm = LLM(model="gemini/gemini-2.0-flash",temperature=0.5)
# llm2=LLM(model="ollama/llama3.2", base_url="http://localhost:11434")

# Create agents
question_generator = Agent(
    role="Question Generator",
    goal="Generate a simple math question for the human to answer",
    backstory="You are an expert at formulating math questions.",
    llm=llm
)

answer_processor = Agent(
    role="Answer Processor",
    goal="Analyze and process the human's answer to determine its correctness",
    backstory="You are skilled at marking human's answer to a math question to ensure its right or wrong",
    llm=llm
)

# Create tasks
task1 = Task(
    description="Generate a simple math question for the human to answer",
    agent=question_generator,
    expected_output="one question, starting with the word 'QuestionAI: ' ",
    human_input=False
)

task2 = Task(
    description="Process the human's answer to ensure its correct",
    agent=answer_processor,
    expected_output="Human's answer in Quotes. Right or wrong with short explanations, Starting with the word 'AnswerAI: '",
    human_input=True
)

# Create and run the crew
crew = Crew(
    agents=[question_generator, answer_processor],
    tasks=[task1, task2],
    process=Process.sequential,
    verbose=True
)

result = crew.kickoff()
print("######################")
print(result)