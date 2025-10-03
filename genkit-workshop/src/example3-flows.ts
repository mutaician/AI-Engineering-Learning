import { googleAI } from '@genkit-ai/google-genai';
import { genkit, z } from 'genkit';
import 'dotenv/config';

// Initialize Genkit with Google AI
const ai = genkit({
  plugins: [googleAI()],
  model: googleAI.model("gemini-2.5-flash-lite")
});

// Define a simple greeting flow
export const greetingFlow = ai.defineFlow(
  {
    name: 'greeting',
    inputSchema: z.object({
      name: z.string().describe("The person's name"),
      language: z.enum(['english', 'spanish', 'french']).describe('Language for greeting'),
    }),
    outputSchema: z.object({
      greeting: z.string().describe('The generated greeting'),
    }),
  },
  async ({ name, language }) => {
    // Generate the greeting
    const response = await ai.generate({
      prompt: `Create a friendly greeting for ${name} in ${language}. Keep it warm and welcoming.`,
    });

    return {
      greeting: response.text.trim(),
    };
  },
);

// Define a joke generator flow
export const jokeFlow = ai.defineFlow(
  {
    name: 'jokeGenerator',
    inputSchema: z.object({
      topic: z.string().describe('The topic for the joke'),
    }),
    outputSchema: z.object({
      joke: z.string().describe('The generated joke'),
    }),
  },
  async ({ topic }) => {
    // Generate a clean, family-friendly joke
    const response = await ai.generate({
      prompt: `Create a clean, family-friendly joke about ${topic}. Keep it short and funny.`,
    });

    return {
      joke: response.text.trim(),
    };
  },
);

// Example usage function
async function demonstrateFlows() {
  try {
    console.log('=== Testing Greeting Flow ===');

    const greetingResult = await greetingFlow({
      name: 'Alice',
      language: 'english',
    });

    console.log('Greeting Result:');
    console.log(greetingResult.greeting);

    console.log('\n=== Testing Joke Flow ===');

    const jokeResult = await jokeFlow({
      topic: 'programming',
    });

    console.log('Joke Result:');
    console.log(jokeResult.joke);

    console.log('\n=== Testing Multiple Greetings ===');
    const people = [
      { name: 'Bob', language: 'spanish' as const },
      { name: 'Claire', language: 'french' as const },
    ];

    for (const person of people) {
      const result = await greetingFlow(person);
      console.log(`${person.name} (${person.language}): ${result.greeting}`);
    }
  } catch (error) {
    console.error('Error running flows:', error);
  }
}

// Run the demonstration
demonstrateFlows();