import OpenAI from 'openai';

const openai = new OpenAI({
  baseURL: 'https://openrouter.ai/api/v1',
  apiKey: process.env.OPENROUTER_API_KEY, // Required. Get your API key from https://openrouter.ai,
});

async function main() {
  const completion = await openai.chat.completions.create({
    model: 'deepseek/deepseek-chat-v3-0324:free',
    messages: [
      {
        role: 'user',
        content: 'What is vibe coding?',
      },
    ],
    stream: true,
    temperature: 1,
  });

  for await (const chunk of completion) {
    process.stdout.write(chunk.choices[0]?.delta?.content || '')
  }


}

main();
