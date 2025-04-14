import './style.css'
import { RecursiveCharacterTextSplitter } from 'langchain/text_splitter'
import { createClient } from '@supabase/supabase-js'
import { OllamaEmbeddings } from '@langchain/ollama'
import { SupabaseVectorStore } from '@langchain/community/vectorstores/supabase'
import { ChatOllama } from '@langchain/ollama'
import { PromptTemplate } from "@langchain/core/prompts";


const llm = new ChatOllama({
  model: "gemma3:1b",
})

console.log("Starting ")
const standaloneQuestionTemplate = "Given a question, convert it to a standalone question. question: {userQuestion} standalone question: "

const standaloneQuestionPrompt = PromptTemplate.fromTemplate(standaloneQuestionTemplate)

const standaloneQuestionChain = standaloneQuestionPrompt.pipe(llm)

const response = await standaloneQuestionChain.invoke({
  userQuestion: "What are the technical requirements for running Scrimba? I only have a very old laptop which is not that powerful."
})

console.log(JSON.stringify(response))

async function processAndStoreDataEmbeddings() {
  try {
    const data = await fetch('/data/scrimba-info.txt')
    const data_text = await data.text()
  
    const splitter = new RecursiveCharacterTextSplitter({
      chunkSize: 500,
      chunkOverlap: 50
    })
  
    const output = await splitter.createDocuments([data_text])
  
    const sbApiKey = import.meta.env.VITE_SUPABASE_API_KEY
    const sburl = import.meta.env.VITE_SUPABASE_URL_LC_CHATBOT
  
    const client = createClient(sburl,sbApiKey)
  
    await SupabaseVectorStore.fromDocuments(
      output,
      new OllamaEmbeddings({
        model: "mxbai-embed-large"
      }),
      {
        client,tableName: "documents"
      }
    )
  
    console.log("Done")
  } catch (err) {
    console.error(err)
  }
}

// Chatbot UI implementation
document.addEventListener('DOMContentLoaded', () => {
  const userInput = document.getElementById('user-input');
  const submitButton = document.getElementById('submit-btn');
  
  // Add mock response for demonstration
  const mockResponses = [
    "Scrimba is an interactive coding platform where you can learn frontend development through interactive courses.",
    "Scrimba offers courses on HTML, CSS, JavaScript, React, and more.",
    "Scrimba's interactive screencasts let you edit the code while watching the tutorial.",
    "The Scrimba community includes both beginners and experienced developers learning new skills.",
    "Scrimba has both free and premium courses available to users."
  ];
  
  // Event listeners
  submitButton.addEventListener('click', () => progressConversation());
  
  userInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
      progressConversation();
    }
  });
  
  // Initialize with a welcome message
  const chatbotConversation = document.getElementById('chatbot-conversation-container');
  const welcomeMessage = document.createElement('div');
  welcomeMessage.classList.add('speech', 'speech-ai');
  welcomeMessage.textContent = "Hi there! I'm Scrimba Bot. How can I help you today?";
  chatbotConversation.appendChild(welcomeMessage);
  
  async function progressConversation() {
    const userInput = document.getElementById('user-input');
    const chatbotConversation = document.getElementById('chatbot-conversation-container');
    const question = userInput.value.trim();
    
    // Don't process empty inputs
    if (!question) return;
    
    userInput.value = '';

    // Add human message
    const newHumanSpeechBubble = document.createElement('div');
    newHumanSpeechBubble.classList.add('speech', 'speech-human');
    chatbotConversation.appendChild(newHumanSpeechBubble);
    newHumanSpeechBubble.textContent = question;
    chatbotConversation.scrollTop = chatbotConversation.scrollHeight;

    // Add typing indicator
    const typingIndicator = document.createElement('div');
    typingIndicator.classList.add('speech', 'speech-ai');
    typingIndicator.textContent = "Thinking...";
    chatbotConversation.appendChild(typingIndicator);
    chatbotConversation.scrollTop = chatbotConversation.scrollHeight;
    
    // Simulate AI thinking
    setTimeout(() => {
      // For now, just choose a random response from our mock data
      const result = mockResponses[Math.floor(Math.random() * mockResponses.length)];
      
      // Replace typing indicator with AI response
      typingIndicator.textContent = result;
      typingIndicator.classList.remove('typing');
      chatbotConversation.scrollTop = chatbotConversation.scrollHeight;
    }, 1000);
  }
});

// Clear the default content
document.querySelector('#app').innerHTML = document.querySelector('#app').innerHTML;