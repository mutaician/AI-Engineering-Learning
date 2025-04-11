import './style.css'
import OpenAI from 'openai'

const openai = new OpenAI({
  baseURL: "https://openrouter.ai/api/v1",
  apiKey: import.meta.env.VITE_OPENROUTER_API_KEY,
  dangerouslyAllowBrowser: true
})

// upload file with assistants purpose
async function uploadFileforAssistant(){
  // Fetch the file and convert it to a Blob
  const response = await fetch("/src/movies.txt");
  const fileBlob = await response.blob();
  
  // Create a File object from the Blob
  const file = new File([fileBlob], "movies.txt", { type: "text/plain" });
  
  // Upload the file
  const uploadedFile = await openai.files.create({
    file: file,
    purpose: "assistants",
  });

  return uploadedFile;
}

// Create a movie assistant
async function createAssistant(){
  const myAssistant = await openai.beta.assistants.create({
    name: "Movie Expert",
    instructions: "You are great at recommending movies. When asked a question, use the information in the provided file to form a friendly response. If you cannot find the answer in the file, do your best to infer what the answer should be.",
    tools: [{type: "file_search"}],
    model: "openrouter/quasar-alpha"
  })
}

async function main(){
  const file = await uploadFileforAssistant();
  console.log(JSON.stringify(file, null, 2))
}

main()

document.querySelector('#app').innerHTML = ''