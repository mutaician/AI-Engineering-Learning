import "./style.css";
import OpenAI from "openai";
import { getCurrentWeather, getLocation, tools } from "./tools";

const openai = new OpenAI({
  baseURL: "https://openrouter.ai/api/v1",
  apiKey: import.meta.env.VITE_OPENROUTER_API_KEY,
  dangerouslyAllowBrowser: true,
});

const availableFunctions = {
  getCurrentWeather,
  getLocation,
};

async function agent(query) {
  const messages = [
    {
      role: "system",
      content:
        "You are a helpful AI agent. Give highly specific answers based on the information you're provided. Prefer to gather information with the tools provided to you rather than giving basic, generic answers.",
    },
    { role: "user", content: query },
  ];

  const runner = openai.beta.chat.completions.runTools({
    model: "openrouter/quasar-alpha",
    messages,
    tools,
  }).on('message', (message) => console.log(JSON.stringify(message)))

  const finalContent = await runner.finalContent();
  return finalContent;
}

async function main() {
  console.log("stating");
  console.log(await agent("whats the current weather"));
  console.log("End");
}

main();

document.querySelector("#app").innerHTML =
  "Hello I am learning about OpenAI Functions Agent";
