import "./style.css";
import ollama from "ollama";
import { GoogleGenAI } from "@google/genai";
import { createClient } from "@supabase/supabase-js";
import podcasts from "./content";

// Supabase config
const privateKey = import.meta.env.VITE_SUPABASE_API_KEY
const url = import.meta.env.VITE_SUPABASE_URL
const supabase = createClient(url, privateKey)

async function embeddingWithOllama(text) {
  try {
    const embedding = await ollama.embeddings({
      model: "nomic-embed-text",
      prompt: text,
    });

    return {
      content: text,
      embedding: embedding.embedding,
    };
  } catch (error) {
    console.error(`Error generating embedding for text: "${text}"`, error);
    return null;
  }
}

async function embeddingWithGoogle(text) {
  try {
    const ai = new GoogleGenAI({ apiKey: import.meta.env.VITE_GEMINI_API_KEY });
    const response = await ai.models.embedContent({
      model: "text-embedding-004",
      contents: text,
    });

    return {
      content: text,
      embedding: response.embeddings[0].values,
    };
  } catch (error) {
    console.error(`Error generating embedding for text: "${text}"`, error);
    return null;
  }
}

async function processContents(contents) {
  const embeddings = [];
  
  for (const text of contents) {
    const result = await embeddingWithOllama(text);
    if (result) {
      embeddings.push(result);
    }
  }
  
  return embeddings;
}

async function getVectorMatch(query) {
  const embedding = await embeddingWithOllama(query)
  const queryEmbedding = embedding.embedding

  const { data } = await supabase.rpc('match_documents', {
    query_embedding: queryEmbedding,
    match_threshold: 0.5,
    match_count: 5
  })

  console.log(data)

}

async function main() {
  // const data = await processContents(podcasts);
  // console.log('Embedding Results:', data);
  // // insert data to supabase
  // await supabase.from('documents').insert(data)
  // console.log("Storing to supabase complete")

  // Query supabase for nearest vector 
  const query = "Training computers"
  await getVectorMatch(query)
  
}

main();

document.querySelector("#app").innerHTML = "<h1>Hello Embedding</h1>";
