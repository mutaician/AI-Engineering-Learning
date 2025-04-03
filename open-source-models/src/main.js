import './style.css'

// HuggingFace.js Inference
import { HfInference } from '@huggingface/inference'

const hf = new HfInference(import.meta.env.VITE_HF_ACCESS_TOKEN)

// Text Generation 
document.getElementById('generate-btn').addEventListener("click", async () => {
  const textToGenerate = document.getElementById('text-to-generate').value

  const response = await hf.textGeneration({
      inputs: textToGenerate,
      model: "HuggingFaceH4/zephyr-7b-beta",
      max_tokens: 100
  })
  document.getElementById('text-result').textContent = response.generated_text

})

// Text Classification
document.getElementById("classify-btn").addEventListener("click", async () => {
  const textToClassify = document.getElementById("text-to-classify").value

  const response = await hf.textClassification({
    model: "SamLowe/roberta-base-go_emotions",
    inputs: textToClassify
  })

  document.getElementById("classify-result").textContent = response[0].label
  console.log(response)
})







