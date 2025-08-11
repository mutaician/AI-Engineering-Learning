from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-5-nano", temperature=0, streaming=True)
output_parser = StrOutputParser()

question_prompt = PromptTemplate(
    input_variables=["topic"], template="Generate 3 questions about {topic}"
)

answer_prompt = PromptTemplate(
    input_variables=["questions"],
    template="Answer the folowing questions: \n {questions}\n your response should contain question and answer to it. Answer each question briefly.",
)

question_chain = question_prompt | llm | output_parser
answer_chain = answer_prompt | llm | output_parser
def create_answer_input(out):
    return {'questions': out}

qa_chain = question_chain | create_answer_input | answer_chain

# questions = qa_chain.invoke({"topic": "Artificial Intelligence"})
# print(questions)
for chunk in qa_chain.stream({'topic': 'Artificial Intelligence'}):
    print(chunk, end="", flush=True)