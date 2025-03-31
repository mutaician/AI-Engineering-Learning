import OpenAI from 'openai';

// --- Configuration ---
// IMPORTANT: Replace "YOUR_API_KEY_HERE" with your actual OpenRouter API key.
// Never commit API keys directly into your frontend code in production!
const OPENROUTER_API_KEY = "YOUR_API_KEY_HERE";
const API_BASE_URL = 'https://openrouter.ai/api/v1';
const MODEL_NAME = 'deepseek/deepseek-chat-v3-0324:free';

// --- OpenAI Client Setup ---
let openai;
if (OPENROUTER_API_KEY === "YOUR_API_KEY_HERE") {
    console.warn("OpenRouter API Key not set. Please replace 'YOUR_API_KEY_HERE' in index.js");
    // Display a message to the user in the UI?
} else {
    openai = new OpenAI({
        baseURL: API_BASE_URL,
        apiKey: OPENROUTER_API_KEY,
        dangerouslyAllowBrowser: true, // Required for browser usage
    });
}

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
    if (!openai) {
        alert("API client is not configured. Please add your API key to index.js.");
        return;
    }

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

    originalText = textToTranslate; // Store the original text
    const targetLanguageName = languageMap[selectedLanguageValue];
    const prompt = `Translate the following English text to ${targetLanguageName}:\n\n"${textToTranslate}"\n\nTranslation:`;

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
        const completion = await openai.chat.completions.create({
            model: MODEL_NAME,
            messages: [
                { role: 'system', content: `You are a helpful translation assistant. Translate the user's text accurately to the specified language. Provide only the translation, without any extra explanations or introductory phrases.` },
                { role: 'user', content: prompt },
            ],
            temperature: 0.7,
        });

        const translation = completion.choices[0]?.message?.content?.trim() || 'Translation not available.';

        // --- Update UI with Result ---
        translationResultDisplay.textContent = translation;
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
        isShowingResult = true; // Treat error state like result state for reset logic

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
