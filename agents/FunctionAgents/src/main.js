import './style.css'
import OpenAI from 'openai'
import { getCurrentWeather, getLocation } from "./tools";


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
      })

      const responseText = response.choices[0].message.content
      console.log(responseText)
  }
}

document.querySelector('#app').innerHTML = ''
