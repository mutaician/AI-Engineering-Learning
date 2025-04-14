import { ChatOllama } from "@langchain/ollama";
import { PromptTemplate } from "@langchain/core/prompts";

const llm = new ChatOllama({
    model: "gemma3:1b",
})

const tweetTemplate = 'Generate a promotional tweet for a product, from this product description: {productDesc}'

const tweetPrompt = PromptTemplate.fromTemplate(tweetTemplate)
console.log(JSON.stringify(tweetPrompt, null, 2))