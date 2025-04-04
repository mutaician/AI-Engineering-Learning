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

async function processDataAndAddToSupabas(contents) {
  const data = await processContents(contents);
  console.log('Embedding Results:', data);
  // insert data to supabase
  await supabase.from('documents').insert(data)
  console.log("Storing to supabase complete")
}

async function getVectorMatch(query) {
  try {
    const embedding = await embeddingWithOllama(query);
    if (!embedding) {
      console.error('Failed to generate embedding for query');
      return null;
    }

    const queryEmbedding = embedding.embedding;
    const { data } = await supabase.rpc('match_documents', {
      query_embedding: queryEmbedding,
      match_threshold: 0.5,
      match_count: 1
    });

    // Check if we got any matches
    if (!data || data.length === 0) {
      console.log('No matches found for query:', query);
      return null;
    }

    return data[0].content;
  } catch (error) {
    console.error('Error in getVectorMatch:', error);
    return null;
  }
}

async function generatePodcastResponse(context, query) {
  try {
    const systemPrompt = "You are an enthusiastic podcast expert who loves recommending podcasts to people. You will be given two pieces of information - some context about podcasts episodes and a question. Your main job is to formulate a short answer to the question using the provided context. If you are unsure and cannot find the answer in the context, say, \"Sorry, I don't know the answer.\" Please do not make up the answer.";
    
    const response = await ollama.chat({
      model: 'gemma3:1b',
      messages: [
        {
          role: 'system',
          content: systemPrompt
        },
        {
          role: 'user',
          content: `Context: ${context}\nQuestion: ${query}`
        }
      ]
    });

    return response.message.content;
  } catch (error) {
    console.error('Error in generatePodcastResponse:', error);
    return "Sorry, I encountered an error while processing your request.";
  }
}

async function handlePodcastSearch(query) {
  try {
    // Show loading state
    const resultElement = document.getElementById("result");
    resultElement.textContent = "Searching for podcasts...";

    // Get the matching content
    const matchedContent = await getVectorMatch(query);
    if (!matchedContent) {
      resultElement.textContent = "No matching podcasts found. Try a different search.";
      return;
    }

    // Generate AI response
    const aiResponse = await generatePodcastResponse(matchedContent, query);
    
    // Display the response
    resultElement.textContent = aiResponse;
  } catch (error) {
    console.error('Error:', error);
    document.getElementById("result").textContent = 
      "Sorry, something went wrong. Please try again.";
  }
}

async function main() {
  // Get DOM elements
  const searchButton = document.getElementById("generate");
  const searchInput = document.getElementById("podcast-query");

  // Add click event listener to button
  searchButton.addEventListener("click", async () => {
    const query = searchInput.value.trim();
    if (!query) {
      document.getElementById("result").textContent = 
        "Please enter a search query";
      return;
    }
    await handlePodcastSearch(query);
  });

  // Add enter key listener to input
  searchInput.addEventListener("keypress", async (event) => {
    if (event.key === "Enter") {
      const query = searchInput.value.trim();
      if (!query) {
        document.getElementById("result").textContent = 
          "Please enter a search query";
        return;
      }
      await handlePodcastSearch(query);
    }
  });
}

main();

