import './style.css'
import OpenAI from 'openai';

const openai = new OpenAI({
  baseURL: "https://openrouter.ai/api/v1",
  apiKey: import.meta.env.VITE_OPENROUTER_API_KEY,
  dangerouslyAllowBrowser: true
});



async function main() {
  const completion = await openai.chat.completions.create({
    model: "openrouter/quasar-alpha",
    messages: [
      {
        "role": "user",
        "content": "Give me a list of activity ideas based on my current location and weather"
      }
    ],
    
  });

  console.log(completion.choices[0].message.content);
}

main();