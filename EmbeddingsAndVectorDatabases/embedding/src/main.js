import "./style.css";
import ollama from "ollama";
import { GoogleGenAI } from "@google/genai";

const contents = [
  "Beyond Mars: speculating life on distant planets.",
  "Jazz under stars: a night in New Orleans' music scene.",
  "Mysteries of the deep: exploring uncharted ocean caves.",
  "Rediscovering lost melodies: the rebirth of vinyl culture.",
  "Tales from the tech frontier: decoding AI ethics.",
];

async function embeddingWithOllama(text) {
  try {
    const embedding = await ollama.embeddings({
      model: "nomic-embed-text",
      prompt: text,
    });

    return {
      text,
      embedding: embedding.embedding,
      dimension: embedding.embedding.length
    };
  } catch (error) {
    console.error(`Error generating embedding for text: "${text}"`, error);
    return null;
  }
}

async function embeddingWithGoogle() {
  const ai = new GoogleGenAI({ apiKey: import.meta.env.VITE_GEMINI_API_KEY });

  const response = await ai.models.embedContent({
    model: "text-embedding-004",
    contents: "Hello, World",
  });

  console.log(response.embeddings);
}

async function processContents() {
  const embeddings = [];
  
  for (const text of contents) {
    const result = await embeddingWithOllama(text);
    if (result) {
      embeddings.push(result);
    }
  }
  
  return embeddings;
}

async function main() {
  const results = await processContents();
  console.log('Embedding Results:', results);
  
  results.forEach(({text, embedding, dimension}) => {
    console.log('\n---');
    console.log(`Text: ${text}`);
    console.log(`Dimension: ${dimension}`);
    console.log(`First 5 values: [${embedding.slice(0, 5).join(', ')}]`);
  });
}

main();

document.querySelector("#app").innerHTML = "<h1>Hello Embedding</h1>";
