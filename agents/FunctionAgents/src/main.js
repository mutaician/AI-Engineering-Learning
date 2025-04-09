import "./style.css";
import OpenAI from "openai";
import { getCurrentWeather, getLocation, tools } from "./tools";
import { marked } from "marked";

const openai = new OpenAI({
  baseURL: "https://openrouter.ai/api/v1",
  apiKey: import.meta.env.VITE_OPENROUTER_API_KEY,
  dangerouslyAllowBrowser: true,
});

const availableFunctions = {
  getCurrentWeather,
  getLocation,
};

marked.setOptions({
  breaks: true,
  gfm: true
})

// Chat UI Elements
const messagesContainer = document.getElementById("messages");
const chatForm = document.getElementById("chat-form");
const userInput = document.getElementById("user-input");
const clearChatButton = document.getElementById("clear-chat");

// Keep track of chat history
let chatHistory = [
  {
    role: "system",
    content:
      "You are a helpful AI agent. Give highly specific answers based on the information you're provided. Prefer to gather information with the tools provided to you rather than giving basic, generic answers.",
  },
];

// Initialize the UI
function initUI() {
  chatForm.addEventListener("submit", handleSubmit);
  clearChatButton.addEventListener("click", clearChat);
  userInput.focus();
  
  // Add a welcome message
  addMessageToUI("Hello! How can I help you today?", "ai");
}

// Handle form submission
async function handleSubmit(e) {
  e.preventDefault();
  const query = userInput.value.trim();
  
  if (!query) return;
  
  // Add user message to UI
  addMessageToUI(query, "user");
  
  // Clear input
  userInput.value = "";
  
  // Show loading indicator
  showLoadingIndicator();
  
  try {
    // Add user message to chat history
    chatHistory.push({ role: "user", content: query });
    
    // Get response from agent
    const response = await agent(query);
    
    // Add AI response to UI
    addMessageToUI(response, "ai");
    
    // Add response to chat history
    chatHistory.push({ role: "assistant", content: response });
  } catch (error) {
    console.error("Error:", error);
    addMessageToUI("Sorry, there was an error processing your request.", "ai");
  } finally {
    // Remove loading indicator
    hideLoadingIndicator();
  }
}

// Clear chat history
function clearChat() {
  chatHistory = [chatHistory[0]]; // Keep the system message
  messagesContainer.innerHTML = "";
  
  // Add a welcome message
  addMessageToUI("Chat cleared. How can I help you?", "ai");
}

// Add a message to the UI
function addMessageToUI(content, role) {
  const messageElement = document.createElement("div");
  messageElement.classList.add("message");
  messageElement.classList.add(role === "user" ? "user-message" : "ai-message");
  
  if (role === "ai") {
    // Parse and render markdown for AI messages
    messageElement.innerHTML = marked.parse(content);
  } else {
    // For user messages, just use text
    messageElement.textContent = content;
  }
  
  messagesContainer.appendChild(messageElement);
  
  // Scroll to bottom
  messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Show loading indicator
function showLoadingIndicator() {
  const loadingElement = document.createElement("div");
  loadingElement.classList.add("message", "ai-message", "loading");
  loadingElement.id = "loading-indicator";
  
  const loadingDots = document.createElement("div");
  loadingDots.classList.add("loading-dots");
  
  for (let i = 0; i < 3; i++) {
    const dot = document.createElement("div");
    dot.classList.add("dot");
    loadingDots.appendChild(dot);
  }
  
  loadingElement.appendChild(loadingDots);
  messagesContainer.appendChild(loadingElement);
  
  // Scroll to bottom
  messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Hide loading indicator
function hideLoadingIndicator() {
  const loadingIndicator = document.getElementById("loading-indicator");
  if (loadingIndicator) {
    loadingIndicator.remove();
  }
}

// Agent function to process queries
async function agent(query) {
  const messages = [...chatHistory]; // Use the complete chat history
  
  // If it's a new conversation, add the user message
  if (messages.length === 1) {
    messages.push({ role: "user", content: query });
  }

  const runner = openai.beta.chat.completions.runTools({
    model: "openrouter/quasar-alpha",
    messages,
    tools,
  });
  
  const finalContent = await runner.finalContent();
  const runnerMessages = await runner.messages
  console.log(JSON.stringify(runnerMessages,null, 2))

  return finalContent;
}

// Initialize the UI when the DOM is loaded
document.addEventListener("DOMContentLoaded", initUI);
