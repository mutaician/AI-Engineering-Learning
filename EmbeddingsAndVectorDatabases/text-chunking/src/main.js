import './style.css'
import { pipeline } from '@xenova/transformers';
import { createClient } from "@supabase/supabase-js";
import { RecursiveCharacterTextSplitter } from "langchain/text_splitter";
import ollama from "ollama";

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
      chunkOverlap: 50
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
    // Check if there's existing data in the table
    console.log('Checking for existing data in the database...');
    const { data: existingData, error: checkError } = await supabase
      .from('documentstwo')
      .select('content')
      .limit(1);

    if (checkError) {
      throw new Error(`Error checking existing data: ${checkError.message}`);
    }

    if (existingData && existingData.length > 0) {
      console.log('Data already exists in the database. Skipping embedding creation.');
      return;
    }

    // If no existing data, proceed with embedding creation
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

async function getVectorMatch(query) {
  try {
    console.log('Generating embedding for query:', query);
    const embedding = await embeddingWithMiniLM(query);
    if (!embedding) {
      console.error('Failed to generate embedding for query');
      return null;
    }

    console.log('Querying Supabase for matches...');
    const { data, error } = await supabase.rpc('match_documentstwo', {
      query_embedding: embedding.embedding,
      match_threshold: 0.2,
      match_count: 3
    });

    if (error) {
      console.error('Supabase query error:', error);
      return null;
    }

    if (!data || data.length === 0) {
      console.log('No matches found for query:', query);
      return null;
    }

    console.log(`Found matching movie contents`, data);
    return data.map(match => match.content).join('\n');
  } catch (error) {
    console.error('Error in getVectorMatch:', error);
    return null;
  }
}

async function generateMovieResponse(context, query) {
  try {
    console.log('Generating movie response...');
    const systemPrompt = `You are an enthusiastic movie expert who loves recommending movies to people. You will be given two pieces of information - some context about movies and a question. Your main job is to formulate a short answer to the question using the provided context. If you are unsure and cannot find the answer in the context, do not make up the answer else be friendly and caring. DON"T recommend any specific movie not mentioned in the context even if you know that movie. But provide a helpful answer to the user.`;
    
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

    console.log('Successfully generated response');
    return response.message.content;
  } catch (error) {
    console.error('Error in generateMovieResponse:', error);
    return "I'm having a moment! Let me gather my thoughts about movies and try again.";

  }
}

async function handleMovieSearch(query) {
  try {
    const resultElement = document.getElementById("result");
    resultElement.textContent = "Thinking...";

    const matchedContent = await getVectorMatch(query);

    const aiResponse = await generateMovieResponse(matchedContent, query);
    resultElement.textContent = aiResponse;
  } catch (error) {
    console.error('Error:', error);
    document.getElementById("result").textContent = 
      "Sorry, something went wrong. Please try again.";
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
    
    // Set up the initial embedding process
    // await processMovies();
    
    // Set up the search interface
    const searchButton = document.getElementById("search");
    const searchInput = document.getElementById("movie-query");

    searchButton.addEventListener("click", async () => {
      const query = searchInput.value.trim();
      if (!query) {
        document.getElementById("result").textContent = 
          "Please enter a question about movies";
        return;
      }
      await handleMovieSearch(query);
    });

    searchInput.addEventListener("keypress", async (event) => {
      if (event.key === "Enter") {
        const query = searchInput.value.trim();
        if (!query) {
          document.getElementById("result").textContent = 
            "Please enter a question about movies";
          return;
        }
        await handleMovieSearch(query);
      }
    });
    

    console.log('Application setup completed successfully');
  } catch (error) {
    console.error('Application failed:', error);
    document.getElementById("result").textContent = 
      "Sorry, the application failed to initialize properly.";
  }
}

main()


