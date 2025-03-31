import OpenAI from "openai";

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type'
};

export default {
  async fetch(request, env, ctx) {
    // Handle CORS preflight requests
    if (request.method === "OPTIONS") {
      return new Response(null, { headers: corsHeaders });
    }
    
    try {
      const response = await handleRequest(request, env);
      // Add CORS headers to the response
      return addCorsHeaders(response);
    } catch (error) {
      return new Response(JSON.stringify({ error: error.message }), {
        status: 500,
        headers: { 
          'Content-Type': 'application/json',
          ...corsHeaders 
        }
      });
    }
  },
};

async function handleRequest(request, env) {
  const url = new URL(request.url);
  
  switch (url.pathname) {
    case '/message':
		if (request.method !== 'POST'){
			return new Response('Method Not Allowed', {status: 405})
		}
		
		let requestData;
		try {
			requestData = await request.json()
		} catch (error) {
			return new Response(JSON.stringify({error: 'Invalid JSON body'}), {
				status: 400,
				headers: {'Content-Type': 'application/json'}
			})
		}

		if (!Array.isArray(requestData)) {
			return new Response(JSON.stringify({ error: 'Request body must be an array of messages' }), {
			  status: 400,
			  headers: { 'Content-Type': 'application/json' }
			});
		  }

      const openai = new OpenAI({
        baseURL: 'https://openrouter.ai/api/v1',
        apiKey: env.OPENROUTER_API_KEY,
      });
      
      try {
        const completion = await openai.chat.completions.create({
          model: 'google/gemma-3-4b-it:free',
          messages: requestData,
          temperature: 0.7,
        });

        const responseText = completion.choices[0].message?.content?.trim() || 'Translation not available.';

        return new Response(JSON.stringify(responseText), {
          headers: { 'Content-Type': 'application/json' }
        });
      } catch (error) {
        return new Response(JSON.stringify({ error: error.message }), {
          status: 500,
          headers: { 'Content-Type': 'application/json' }
        });
      }

    case '/random':
      return new Response(crypto.randomUUID());
      
    default:
      return new Response('Not Found', { status: 404 });
  }
}

// Helper function to add CORS headers to responses
function addCorsHeaders(response) {
  const newHeaders = new Headers(response.headers);
  Object.entries(corsHeaders).forEach(([key, value]) => {
    newHeaders.set(key, value);
  });
  
  return new Response(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers: newHeaders
  });
}
