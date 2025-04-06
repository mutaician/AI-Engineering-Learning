import './style.css'
import OpenAI from 'openai';
import { getCurrentWeather, getLocation } from './tools';

const openai = new OpenAI({
  baseURL: "https://openrouter.ai/api/v1",
  apiKey: import.meta.env.VITE_OPENROUTER_API_KEY,
  dangerouslyAllowBrowser: true
});

/**
 * Goal - build an agent that can answer any questions that might reguire knowledge about my current location and the curent weather at my location
 */

/**
 * PLAN:
 * 1. Design a well-written ReAct prompt
 * 2. Build a loop for my agent to run in
 * 3. Parse any actions that my agent to run in
 * 4. End Condition - final Answer is given
 */


// async function main() {
//   const completion = await openai.chat.completions.create({
//     model: "meta-llama/llama-4-maverick:free",
//     messages: [
//       {
//         "role": "user",
//         "content": `Give me a list of activity ideas based on my current location of ${location} and weather of ${weather}`
//       }
//     ],
    
//   });

//   console.log(completion.choices[0].message.content);
// }

// main();