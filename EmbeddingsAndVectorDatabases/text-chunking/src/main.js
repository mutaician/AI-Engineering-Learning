import './style.css'
import { pipeline } from '@xenova/transformers';
import { createClient } from "@supabase/supabase-js";
import { RecursiveCharacterTextSplitter } from "langchain/text_splitter";


// Supabase config
const privateKey = import.meta.env.VITE_SUPABASE_API_KEY
const url = import.meta.env.VITE_SUPABASE_URL
const supabase = createClient(url, privateKey)

// LangChain text splitter
async function splitDocument(document) {
  const response = await fetch(document);
  const text = await response.text();

  const splitter = new RecursiveCharacterTextSplitter({
    chunkSize: 500,
    chunkOverlap: 250
  })

  const output = await splitter.splitText(text) 
  return output
}

// Embedding
// initialise embedding pipeline
let generateEmbedding = await pipeline('feature-extraction', 'Xenova/all-MiniLM-L6-v2')

async function embeddingWithMiniLM(text) {
  try {
    if (!generateEmbedding) {
      console.log("Initializing the pipeline")
      generateEmbedding = await pipeline('feature-extraction', 'Xenova/all-MiniLM-L6-v2')
    }

    const output = await generateEmbedding(text, {
      pooling: 'mean', // Average the token embeddings
      normalize: true, // Normalize the resulting vector
    });

    const embedding = Array.from(output.data);

    return {
      content: text,
      embedding: embedding,
    };
  } catch (error) {
    console.error(`Error generating embedding for text: "${text}"`, error);
    return null;
  }
}

async function createAndStoreEmbeddings(contents) {
  const embeddings = []

  for  (const text of contents){
    const result = await embeddingWithMiniLM(text)
    if (result){
      embeddings.push(result)
    }
  }

  await supabase.from('documentstwo').insert(embeddings)
  console.log("Embeddings creation and storage complete.")
}

async function processMovies(){
  const contentSplits = await splitDocument('/src/movies.txt')
  console.log("Splitting contents Complete")
  await createAndStoreEmbeddings(contentSplits)
  console.log("Done")
}


async function main() {
  // await processMovies()


}


main()
document.querySelector('#app').innerHTML = "Embedding, Vector Databases and Text Chunking"

