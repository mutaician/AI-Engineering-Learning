import './style.css'

// HuggingFace.js Inference
import { HfInference } from '@huggingface/inference'
import { pipeline } from '@huggingface/transformers'
// import { pipeline, env } from "https://cdn.jsdelivr.net/npm/@huggingface/transformers";

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

// AI models in browser with transformer.js
// Object detection


const fileUpload = document.getElementById("file-upload");
const imageContainer = document.getElementById("image-container");
const status = document.getElementById("status");

document.getElementById("detect-btn").addEventListener("click", async () => {
  const imageToBeDetected = imageContainer.querySelector("img");

  if (imageToBeDetected === null){
    status.textContent = "Please upload image first"
    return
  }
  status.textContent = 'Loading model...'

  const detector = await pipeline("object-detection", "Xenova/detr-resnet-50");
  status.textContent = "Ready"

  status.textContent = "Analysing..."
  const output = await detector(imageToBeDetected.src, {
    threshold: 0.95,
    percentage: true
  })

  console.log("Output: ", output)
  status.textContent = `Detected ${output.length} objects`;

  output.forEach(renderBox)

  
})


fileUpload.addEventListener("change", function (e) {
  const file = e.target.files[0];
  if (!file) {
    return;
  }

  const reader = new FileReader();

  // Set up a callback when the file is loaded
  reader.onload = function (e2) {
    imageContainer.innerHTML = "";
    const image = document.createElement("img");
    image.src = e2.target.result;
    imageContainer.appendChild(image);
  };
  reader.readAsDataURL(file);
});


// Render a bounding box and label on the image
function renderBox({ box, label }) {
  const { xmax, xmin, ymax, ymin } = box;

  // Generate a random color for the box
  const color = "#" + Math.floor(Math.random() * 0xffffff).toString(16).padStart(6, 0);

  // Draw the box
  const boxElement = document.createElement("div");
  boxElement.className = "bounding-box";
  Object.assign(boxElement.style, {
    borderColor: color,
    left: 100 * xmin + "%",
    top: 100 * ymin + "%",
    width: 100 * (xmax - xmin) + "%",
    height: 100 * (ymax - ymin) + "%",
  });

  // Draw the label
  const labelElement = document.createElement("span");
  labelElement.textContent = label;
  labelElement.className = "bounding-box-label";
  labelElement.style.backgroundColor = color;

  boxElement.appendChild(labelElement);
  imageContainer.appendChild(boxElement);
}