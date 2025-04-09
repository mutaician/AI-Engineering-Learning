import './style.css'
import OpenAI from 'openai'
import { getCurrentWeather, getLocation, tools } from "./tools";


const openai = new OpenAI({
  baseURL: "https://openrouter.ai/api/v1",
  apiKey: import.meta.env.VITE_OPENROUTER_API_KEY,
  dangerouslyAllowBrowser: true,
})

const availableFunctions = {
  getCurrentWeather,
  getLocation
}

async function agent(query) {
  const messages = [
      { role: "system", content: "You are a helpful AI agent. Give highly specific answers based on the information you're provided. Prefer to gather information with the tools provided to you rather than giving basic, generic answers." },
      { role: "user", content: query }
  ]
  
  const MAX_ITERATIONS = 5
  
  for (let i = 0; i < MAX_ITERATIONS; i++) {
      console.log(`Iteration #${i + 1}`)
      const response = await openai.chat.completions.create({
          model: "openrouter/quasar-alpha",
          messages,
          tools
      })

      // console.log(JSON.stringify(response.choices[0],null,2))

      const {finish_reason: finishReason, message} = response.choices[0]
      const {tool_calls: toolCalls} = message
      // console.log(JSON.striangify(toolCalls))
      messages.push(message)

      if (finishReason === "stop"){
        console.log("AGENT STOPPED")
        return message.content
      }
      if (finishReason === "tool_calls"){
        for (const toolCall of toolCalls) {
          const functionName = toolCall.function.name
          const functionToCall = availableFunctions[functionName]
          const functionArgs = JSON.parse(toolCall.function.arguments)
          const functionResponse = await functionToCall(functionArgs)
          console.log(functionResponse)

          messages.push({
            role: 'tool',
            tool_call_id: toolCall.id,
            name: functionName,
            content: functionResponse
          })
        }
      }
      // console.log(response)
  }
}

async function main(){
  console.log("stating")
  console.log(await agent("whats the current weather"))
  console.log("End")
}

main()

document.querySelector('#app').innerHTML = 'Hello I am learning about OpenAI Functions Agent'
