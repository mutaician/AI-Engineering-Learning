import './style.css'

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
    chunkSize: 150,
    chunkOverlap: 15
  })

  const output = await splitter.splitText(text) 
  return output
}

async function main() {
  const contentSplits = await splitDocument('/src/movies.txt')
  console.log(contentSplits)

}

main()


document.querySelector('#app').innerHTML = "Embedding, Vector Databases and Text Chunking"

