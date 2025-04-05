import './style.css'


import { RecursiveCharacterTextSplitter } from "langchain/text_splitter";


// LangChain text splitter
async function splitDocument() {
  const response = await fetch('/src/podcasts.txt');
  const text = await response.text();
  // console.log(text);

  const splitter = new RecursiveCharacterTextSplitter({
    separator: " ",
    chunkSize: 150,
    chunkOverlap: 15
  })

  const output = await splitter.createDocuments([text]) 
  console.log(output)
}
splitDocument()

document.querySelector('#app').innerHTML = "Embedding and Vector Databases"

