import OpenAI from "openai";

export default {
	async fetch(request, env, ctx) {
		const url = new URL(request.url);
		switch (url.pathname) {
			case '/message':
				const  openai = new OpenAI({
						baseURL: 'https://openrouter.ai/api/v1',
						apiKey: env.OPENROUTER_API_KEY,
				})
				try {
					const completion = await openai.chat.completions.create({
						model: 'google/gemma-3-4b-it:free',
						messages: [
							{ role: 'system', content: `You are a helpful translation assistant. Translate the user's text accurately to the specified language. Provide only the translation, without any extra explanations or introductory phrases. and not in quotes. The translation must be in plain text format.` },
							{ role: 'user', content: 'Language: Swahili \n\n Text: I am learning AI Enginering' },
						],
						temperature: 0.7,
					})

					const response = completion.choices[0].message?.content?.trim() || 'Translation not available.';

					return new Response(JSON.stringify(response));


				} catch (error) {
					return new Response(error)
				}


			case '/random':
				return new Response(crypto.randomUUID());
			default:
				return new Response('Not Found', { status: 404 });
		}
	},
};
