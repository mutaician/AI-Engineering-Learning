import './style.css'
import ollama from 'ollama'
import { GoogleGenAI } from '@google/genai'

const content = [
  "Beyond Mars: speculating life on distant planets.",
  "Jazz under stars: a night in New Orleans' music scene.",
  "Mysteries of the deep: exploring uncharted ocean caves.",
  "Rediscovering lost melodies: the rebirth of vinyl culture.",
  "Tales from the tech frontier: decoding AI ethics.",
];

async function embeddingWithOllama() {
  const embedding = await ollama.embeddings({
    model: 'nomic-embed-text',
    prompt: "Hello Embedding"
  })

  console.log(embedding["embedding"])
}

async function embeddingWithGoogle() {
  const ai = new GoogleGenAI({apiKey: import.meta.env.VITE_GEMINI_API_KEY})

  const response = await ai.models.embedContent({
    model: "text-embedding-004",
    contents: content
  })

  console.log(response.embeddings[0])
}

// embeddingWithGoogle()
embeddingWithOllama()

document.querySelector('#app').innerHTML = "<h1>Hello Embedding</h1>"
