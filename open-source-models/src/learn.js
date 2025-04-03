// Text to speech

const text = "It's an exciting time to be an A.I. engineer."

const response = await hf.textToSpeech({
  inputs: text,
  model: "espnet/kan-bayashi_ljspeech_vits"
})

console.log(response)

// have an <audio> element in the html
const audioElement = document.getElementById('speech')
const speechUrl = URL.createObjectURL(response)
audioElement.src = speechUrl