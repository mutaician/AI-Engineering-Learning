import './style.css'
import { RecursiveCharacterTextSplitter } from 'langchain/text_splitter'
import { createClient } from '@supabase/supabase-js'
import { OllamaEmbeddings } from '@langchain/ollama'
import { SupabaseVectorStore } from '@langchain/community/vectorstores/supabase'
// import { ChatOllama } from '@langchain/ollama'
import { PromptTemplate } from "@langchain/core/prompts";
import { ChatDeepSeek } from "@langchain/deepseek";
import { StringOutputParser } from '@langchain/core/output_parsers'
import { RunnableSequence, RunnablePassthrough } from "@langchain/core/runnables";


// const llm = new ChatOllama({
//   model: "gemma3:1b",
// })

const llm = new ChatDeepSeek({
  model: "deepseek-chat",
  apiKey: import.meta.env.VITE_DEEPSEEK_API_KEY,
})

const sbApiKey = import.meta.env.VITE_SUPABASE_API_KEY
const sburl = import.meta.env.VITE_SUPABASE_URL_LC_CHATBOT
const client = createClient(sburl,sbApiKey)

const embeddings = new OllamaEmbeddings({model: "mxbai-embed-large"})

const vectorStore = new SupabaseVectorStore(embeddings, {
  client,
  tableName: "documents",
  queryName: "match_documents"
})

const retriever = vectorStore.asRetriever()

const standaloneQuestionTemplate = "Given a question, convert it to a standalone question. Don't add any extra explanations. Only return the standalone question question: {userQuestion} standalone question: "
const standaloneQuestionPrompt = PromptTemplate.fromTemplate(standaloneQuestionTemplate)

// my prompt 😅
const answerQuestionTemplate = "You are a helpful chatbot that helps to answer questions regarding an online course platform called Scrimba. Your task is to respond to the user using provided context and user's conversation History. Be friendly. Only answer from the information provided and never make up answers. Apologise if you don't know the answer and advise the user to email help@scrimba.com. question: {userQuestion}, usersConversationHistory: {convhistory}, context: {context}, answer: "

const answerQuestionPrompt = PromptTemplate.fromTemplate(answerQuestionTemplate)

function combineDocuments(docs){
  return docs.map((doc)=>doc.pageContent).join('\n\n')
}

const standaloneQuestionChain = RunnableSequence.from([standaloneQuestionPrompt, llm, new StringOutputParser()])
const retrieverChain = RunnableSequence.from([({standalone_question}) => standalone_question,retriever, combineDocuments])
const answerChain = RunnableSequence.from([answerQuestionPrompt, llm, new StringOutputParser()])

const chain = RunnableSequence.from([
  {
    standalone_question: standaloneQuestionChain,
    original_input: new RunnablePassthrough()
  },
  {
    context: retrieverChain,
    userQuestion: ({original_input}) => original_input.userQuestion,
    convhistory: ({original_input}) => original_input.convhistory
  },
  answerChain
])


async function processAndStoreDataEmbeddings() {
  try {
    const data = await fetch('/data/scrimba-info.txt')
    const data_text = await data.text()
  
    const splitter = new RecursiveCharacterTextSplitter({
      chunkSize: 500,
      chunkOverlap: 50
    })
  
    const output = await splitter.createDocuments([data_text])

  
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

function formatConvHistory(messages) {
    return messages.map((message, i) => {
        if (i % 2 === 0){
            return `Human: ${message}`
        } else {
            return `AI: ${message}`
        }
    }).join('\n')
}

const convhistory = []

// Chatbot UI implementation
document.addEventListener('DOMContentLoaded', () => {
  const userInput = document.getElementById('user-input');
  const submitButton = document.getElementById('submit-btn');

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

    try {
      // Call the real chatbot chain
      const response = await chain.invoke({ userQuestion: question, convhistory: formatConvHistory(convhistory) });
      typingIndicator.textContent = response;
      convhistory.push(question)
      convhistory.push(response)
    } catch (err) {
      typingIndicator.textContent = "Sorry, something went wrong. Please try again.";
      console.error(err);
    }
    chatbotConversation.scrollTop = chatbotConversation.scrollHeight;
  }
});

// Clear the default content
document.querySelector('#app').innerHTML = document.querySelector('#app').innerHTML;