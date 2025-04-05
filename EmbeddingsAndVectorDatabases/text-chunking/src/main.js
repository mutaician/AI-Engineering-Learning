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
  try {
    console.log(`Starting to split document: ${document}`);
    const response = await fetch(document);
    
    if (!response.ok) {
      throw new Error(`Failed to fetch document: ${response.status} ${response.statusText}`);
    }
    
    const text = await response.text();
    console.log(`Successfully fetched document, length: ${text.length} characters`);

    const splitter = new RecursiveCharacterTextSplitter({
      chunkSize: 500,
      chunkOverlap: 250
    })

    const output = await splitter.splitText(text);
    console.log(`Document successfully split into ${output.length} chunks`);
    return output;
  } catch (error) {
    console.error('Error in splitDocument:', error.message);
    throw error;
  }
}

// Embedding
// initialise embedding pipeline
let generateEmbedding = await pipeline('feature-extraction', 'Xenova/all-MiniLM-L6-v2');

async function embeddingWithMiniLM(text) {
  try {
    if (!generateEmbedding) {
      console.log("Initializing the embedding pipeline...");
      generateEmbedding = await pipeline('feature-extraction', 'Xenova/all-MiniLM-L6-v2');
    }

    console.log(`Generating embedding for text of length: ${text.length}`);
    const output = await generateEmbedding(text, {
      pooling: 'mean',
      normalize: true,
    });

    const embedding = Array.from(output.data);
    console.log(`Successfully generated embedding of length: ${embedding.length}`);

    return {
      content: text,
      embedding: embedding,
    };
  } catch (error) {
    console.error(`Error generating embedding:`, error);
    return null;
  }
}

async function createAndStoreEmbeddings(contents) {
  try {
    console.log(`Starting embedding creation for ${contents.length} chunks`);
    const embeddings = [];
    let successCount = 0;
    let failCount = 0;

    for (const text of contents) {
      const result = await embeddingWithMiniLM(text);
      if (result) {
        embeddings.push(result);
        successCount++;
      } else {
        failCount++;
      }
    }

    console.log(`Embedding generation complete. Success: ${successCount}, Failed: ${failCount}`);
    
    if (embeddings.length > 0) {
      console.log('Storing embeddings in Supabase...');
      const { data, error } = await supabase.from('documentstwo').insert(embeddings);
      
      if (error) {
        throw new Error(`Supabase storage error: ${error.message}`);
      }
      
      console.log(`Successfully stored ${embeddings.length} embeddings in Supabase`);
    } else {
      console.warn('No embeddings to store in database');
    }
  } catch (error) {
    console.error('Error in createAndStoreEmbeddings:', error);
    throw error;
  }
}

async function processMovies() {
  try {
    console.log('Starting movie processing pipeline...');
    const contentSplits = await splitDocument('/src/movies.txt');
    console.log(`Document splitting complete. Generated ${contentSplits.length} splits`);
    
    await createAndStoreEmbeddings(contentSplits);
    console.log('Movie processing pipeline completed successfully');
  } catch (error) {
    console.error('Error in processMovies:', error);
    throw error;
  }
}

async function main() {
  try {
    console.log('Starting main application...');
    await processMovies();
    console.log('Application completed successfully');
  } catch (error) {
    console.error('Application failed:', error);
  }
}

main()
document.querySelector('#app').innerHTML = "Embedding, Vector Databases and Text Chunking"

