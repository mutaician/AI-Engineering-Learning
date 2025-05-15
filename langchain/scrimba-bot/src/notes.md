const answerTemplate = `You are a helpful and enthusiastic support bot who can answer a given question about Scrimba based on the context provided. Try to find the answer in the context. If you really don't know the answer, say "I'm sorry, I don't know the answer to that." And direct the questioner to email help@scrimba.com. Don't try to make up an answer. Always speak as if you were chatting to a friend.
context: {context}
question: {question}
answer:
`


const chain = standaloneQuestionPrompt.pipe(llm).pipe(new StringOutputParser()).pipe(retriever).pipe(combineDocuments).pipe(answerQuestionPrompt)
RunnableSequence.from([answerQuestionPrompt, llm, new StringOutputParser()]) is same as answerQuestionPrompt.pipe(llm).pipe(new StringOutputParser())

##### Improving Performance
1. Chunk Size
2. Overlap size
3. Number of chunks retrieved, default is 4 for current code
4. prompt engineering
5. AI Settings - temperature, model, frequency and presence penalty 