import './style.css'
import OpenAI from 'openai';
import { getCurrentWeather, getLocation } from './tools';

const openai = new OpenAI({
  baseURL: "https://openrouter.ai/api/v1",
  apiKey: import.meta.env.VITE_OPENROUTER_API_KEY,
  dangerouslyAllowBrowser: true
});

const weather = await getCurrentWeather() 
const location = await getLocation()

async function main() {
  const completion = await openai.chat.completions.create({
    model: "meta-llama/llama-4-maverick:free",
    messages: [
      {
        "role": "user",
        "content": `Give me a list of activity ideas based on my current location of ${location} and weather of ${weather}`
      }
    ],
    
  });

  console.log(completion.choices[0].message.content);
}

main();