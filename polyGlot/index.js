
// --- DOM Elements ---
const textInputLabel = document.getElementById('text-input-label');
const textInput = document.getElementById('text-input');
const languageSectionLabel = document.getElementById('language-section-label');
const languageOptionsContainer = document.getElementById('language-options-container');
const translationResultDisplay = document.getElementById('translation-result-display');
const actionButton = document.getElementById('action-button');

// --- State ---
let isShowingResult = false;
let originalText = ''; // Store original text for display

// --- Language Mapping ---
const languageMap = {
    fr: 'French',
    es: 'Spanish',
    jp: 'Japanese',
    sw: 'Swahili'
};

// --- Event Listeners ---
actionButton.addEventListener('click', handleActionButtonClick);
// Prevent actual form submission if the button is somehow triggered as submit
document.getElementById('translation-form').addEventListener('submit', (e) => e.preventDefault());


// --- Functions ---
function handleActionButtonClick() {
    if (isShowingResult) {
        handleStartOver();
    } else {
        handleTranslate();
    }
}

async function handleTranslate() {

    const textToTranslate = textInput.value.trim();
    const selectedLanguageValue = document.querySelector('input[name="language"]:checked')?.value;

    if (!textToTranslate) {
        alert('Please enter text to translate.');
        return;
    }
    if (!selectedLanguageValue) {
        alert('Please select a language.');
        return;
    }

    originalText = textToTranslate; 
    const targetLanguageName = languageMap[selectedLanguageValue];
    const prompt = `Translate the following English text to ${targetLanguageName}:\n\n"${textToTranslate}"\n\nTranslation:`;
    const messages = [
        { role: 'system', content: `You are a helpful translation assistant. Translate the user's text accurately to the specified language. Provide only the translation, without any extra explanations or introductory phrases. and not in quotes. The translation must be in plain text format.` },
        { role: 'user', content: prompt },
      ]

    // --- Update UI for Loading State ---
    actionButton.disabled = true;
    actionButton.textContent = 'Translating...';
    // Clear previous result and show processing message
    translationResultDisplay.textContent = 'Processing...';
    translationResultDisplay.classList.remove('hidden'); // Show result area
    languageOptionsContainer.classList.add('hidden'); // Hide language options
    languageSectionLabel.textContent = 'Your translation 👇'; // Change label early
    textInputLabel.textContent = 'Original text 👇'; // Change label early
    textInput.readOnly = true; // Make input read-only

    try {

        // make a fetch request to worker url
        const WorkerUrl = "https://translation-api-worker.cypriankiplangat.workers.dev/message"

        const response = await fetch(WorkerUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(messages)
        })

        // Check if the response is OK
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `API returned status ${response.status}`);
        }

        const data = await response.json();
        
        // Check if data is a string (successful translation) or an object (error)
        if (typeof data === 'object' && data !== null) {
            if (data.error) {
                throw new Error(data.error);
            }
            // If we get here, it's an unexpected object response
            throw new Error('Received unexpected response format from the API');
        }


        // --- Update UI with Result ---
        translationResultDisplay.textContent = data;
        actionButton.textContent = 'Start Over';
        isShowingResult = true;

    } catch (error) {
        console.error('Error calling OpenRouter API:', error);
        translationResultDisplay.textContent = 'Error: Could not get translation.';
        alert(`An error occurred: ${error.message || 'Unknown error'}`);
        // Revert UI partially on error? Or leave as is until "Start Over"?
        // For simplicity, we'll leave the UI in the 'result' state but show error.
        // User must click "Start Over" to try again.
        actionButton.textContent = 'Start Over'; // Allow starting over even on error
        isShowingResult = true; 

    } finally {
        // Re-enable button regardless of success or error
        actionButton.disabled = false;
    }
}

function handleStartOver() {
    // --- Reset UI to Initial State ---
    textInputLabel.textContent = 'Text to translate 👇';
    textInput.value = ''; // Clear the input
    textInput.readOnly = false; // Make editable again

    languageSectionLabel.textContent = 'Select language 👇';
    languageOptionsContainer.classList.remove('hidden'); // Show language options
    translationResultDisplay.classList.add('hidden'); // Hide result area
    translationResultDisplay.textContent = ''; // Clear result text

    actionButton.textContent = 'Translate';
    isShowingResult = false;

    // Reset radio button selection? Optional, default is French checked in HTML.
    // document.getElementById('lang-fr').checked = true;
}

// --- Initial State Check ---
// Ensure the UI starts in the correct state (form view)
handleStartOver(); // Call once on load to set initial state correctly
