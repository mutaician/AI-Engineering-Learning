import "./style.css";
import OpenAI from "openai";
import { getCurrentWeather, getLocation } from "./tools";

const openai = new OpenAI({
  baseURL: "https://openrouter.ai/api/v1",
  apiKey: import.meta.env.VITE_OPENROUTER_API_KEY,
  dangerouslyAllowBrowser: true,
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

const availableFunctions = {
  getCurrentWeather,
  getLocation,
};

const systemPrompt = `
You cycle through Thought, Action, PAUSE, Observation. At the end of the loop you output a final Answer. Your final answer should be highly specific to the observations you have from running
the actions.
1. Thought: Describe your thoughts about the question you have been asked.
2. Action: run one of the actions available to you - then return PAUSE.
3. PAUSE
4. Observation: will be the result of running those actions.

Available actions:
- getCurrentWeather: 
    E.g. getCurrentWeather: Salt Lake City
    Returns the current weather of the location specified.
- getLocation:
    E.g. getLocation: null
    Returns user's location details. No arguments needed.

Example session:
Question: Please give me some ideas for activities to do this afternoon.
Thought: I should look up the user's location so I can give location-specific activity ideas.
Action: getLocation: null
PAUSE

You will be called again with something like this:
Observation: "New York City, NY"

Then you loop again:
Thought: To get even more specific activity ideas, I should get the current weather at the user's location.
Action: getCurrentWeather: New York City
PAUSE

You'll then be called again with something like this:
Observation: { location: "New York City, NY", forecast: ["sunny"] }

You then output:
Answer: <Suggested activities based on sunny weather that are highly specific to New York City and surrounding areas.>
`;
// Set up agent function
async function agent(query) {
  const messages = [
    {
      role: "system",
      content: systemPrompt,
    },
    {
      role: "user",
      content: query,
    },
  ];

  const MAX_ITERATIONS = 5;
  const actionRegex = /^Action: (\w+): (.*)$/


  for (let i = 0; i < MAX_ITERATIONS; i++) {
    console.log(`Iteration: `, i + 1)

    const response = await openai.chat.completions.create({
      model: "meta-llama/llama-4-maverick:free",
      messages,
    });

    const responseText = response.choices[0].message.content;
    console.log(responseText)
    messages.push({ role: "assistant", content: responseText });

    const responseLines = responseText.split("\n");
    const actionMatch = responseLines.find(line => actionRegex.test(line))

    if (actionMatch) {
      const actions = actionRegex['exec'](actionMatch)
      const [_, action, actionArg] = actions;

      if (!availableFunctions.hasOwnProperty(action)) {
        throw new Error(`Unknown action: ${action}: ${actionArg}`);
      }

      console.log(`Calling function: ${action} with argument ${actionArg}`)
      const observation = await availableFunctions[action](actionArg);
      messages.push({
        role: "assistant",
        content: `Observation: ${observation}`,
      });
    } else {
      console.log("Agent finished with task")
      return responseText
    }
  }
}

async function main() {
  console.log(await agent("I am a student. Could you list for me some activity ideas that I can do today based on my location and weather?"))
}

main();
