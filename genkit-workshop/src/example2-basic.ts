import { googleAI } from '@genkit-ai/google-genai';
import { genkit } from 'genkit';
import 'dotenv/config';

// Initialize Genkit with Google AI
const ai = genkit({
  plugins: [googleAI()],
});

// Load the prompt from the file
const storyGeneratorPrompt = ai.prompt('story-generator');

async function generateStory() {
  try {
    console.log('=== Generating Story with Prompt File ===');

    const storyInput = {
      character: 'a unfriendly robot',
      setting: 'a unmagical library',
    };

    console.log('Story parameters:');
    console.log(`Character: ${storyInput.character}`);
    console.log(`Setting: ${storyInput.setting}`);

    const response = await storyGeneratorPrompt(storyInput);

    console.log('\n=== Generated Story ===');
    console.log(response.text);
  } catch (error) {
    console.error('Error generating story:', error);
  }
}

// Generate different stories
async function generateDifferentStories() {
  const stories = [
    { character: 'a curious cat', setting: 'a space station' },
    { character: 'a young wizard', setting: 'a bustling marketplace' },
    { character: 'a brave explorer', setting: 'an underwater city' },
  ];

  for (const story of stories) {
    console.log(`\n=== Story: ${story.character} in ${story.setting} ===`);
    const response = await storyGeneratorPrompt(story);
    console.log(response.text);
    console.log('\n' + '='.repeat(50));
  }
}

// Run examples
async function main() {
  await generateStory();
//   await generateDifferentStories();
}

main();