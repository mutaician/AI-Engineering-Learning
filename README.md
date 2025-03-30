# AI Engineer Learning Projects

This repository contains projects exploring various concepts in AI Engineering.

## Projects

### 1. Intro To AI Engineering (`introToAIEngineering/`)

A simple Node.js script demonstrating interaction with an AI model via the OpenRouter API.

**Functionality:**
*   Connects to the OpenRouter API (using the `deepseek/deepseek-chat-v3-0324:free` model).
*   Asks the model the question: "What is vibe coding?".
*   Streams the model's response directly to the console.

**Setup:**
1.  Navigate to the `introToAIEngineering` directory:
    ```bash
    cd introToAIEngineering
    ```
2.  Install dependencies:
    ```bash
    # Using pnpm (based on lock file)
    pnpm install
    # Or using npm if you prefer
    # npm install
    ```
3.  Set the required API key as an environment variable. You can get a key from [https://openrouter.ai/](https://openrouter.ai/).
    ```bash
    export OPENROUTER_API_KEY="YOUR_API_KEY_HERE"
    ```
    *(Replace `"YOUR_API_KEY_HERE"` with your actual key)*

**Running:**
1.  Make sure you have `ts-node` installed (`npm install -g ts-node` or `pnpm add -g ts-node`) or compile the TypeScript first.
2.  Execute the script:
    ```bash
    # Using ts-node
    ts-node index.ts
    # Or compile and run
    # tsc index.ts
    # node index.js
    ```

### 2. PolyGlot Translator (`polyGlot/`)

A web-based translation tool using the OpenRouter API.

**Functionality:**
*   Provides a user interface to enter text.
*   Allows selection of a target language (French, Spanish, Japanese).
*   Uses the OpenRouter API (`deepseek/deepseek-chat-v3-0324:free` model) to translate the text.
*   Displays the translation on the webpage.

**Setup:**
1.  Navigate to the `polyGlot` directory:
    ```bash
    cd polyGlot
    ```
2.  Install dependencies:
    ```bash
    # Using pnpm (based on lock file)
    pnpm install
    # Or using npm if you prefer
    # npm install
    ```
3.  Create a `.env` file in the `polyGlot` directory.
4.  Add your OpenRouter API key to the `.env` file:
    ```env
    VITE_OPENROUTER_API_KEY="YOUR_API_KEY_HERE"
    ```
    *(Replace `"YOUR_API_KEY_HERE"` with your actual key)*

**Running:**
1.  Start the Vite development server:
    ```bash
    # Using pnpm
    pnpm run dev
    # Or using npm (check package.json for the exact script name, likely 'dev' or 'start')
    # npm run dev
    ```
2.  Open your web browser to the local address provided by Vite (usually `http://localhost:5173`).
