
import { PromptTemplate } from "@langchain/core/prompts";
import { StringOutputParser } from "@langchain/core/output_parsers";
import { RunnableSequence, RunnablePassthrough } from "@langchain/core/runnables";
import { ChatOllama } from '@langchain/ollama'

console.log("working")
const llm = new ChatOllama({
  model: "gemma3:1b",
})

const punctuationTemplate = `Given a sentence, add punctuation where needed. 
    sentence: {sentence}
    sentence with punctuation:  
    `
const punctuationPrompt = PromptTemplate.fromTemplate(punctuationTemplate)

const grammarTemplate = `Given a sentence correct the grammar.
    sentence: {punctuated_sentence}
    sentence with correct grammar: 
    `
const grammarPrompt = PromptTemplate.fromTemplate(grammarTemplate)

const translationTemplate = `Given a sentence, translate that sentence into {language}
    sentence: {grammatically_correct_sentence}
    translated sentence:
    `
const translationPrompt = PromptTemplate.fromTemplate(translationTemplate)

const punctuationChain = RunnableSequence.from([
    punctuationPrompt,
    llm,
    new StringOutputParser()
])
const grammarChain = RunnableSequence.from([
    grammarPrompt,
    llm,
    new StringOutputParser()
])
const translationChain = RunnableSequence.from([
    translationPrompt,
    llm,
    new StringOutputParser()
])

const chain = RunnableSequence.from([
    {
        punctuated_sentence: punctuationChain,
        original_input: new RunnablePassthrough()
    },
    {
        grammatically_correct_sentence: grammarChain,
        language: ({ original_input }) => original_input.language
    },
    translationChain
])

const response = await chain.invoke({
    sentence: 'i dont liked mondays',
    language: 'french'
})

console.log(response)
