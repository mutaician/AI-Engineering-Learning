export async function getCurrentWeather(){
    const weather = {
        temperature: "25",
        unit: "C",
        forecast: "Raining"
    }

    return JSON.stringify(weather)
}

export async function getLocation(){
    return "Kabarak, Nakuru, Kenya"
}

export const tools = [
    {
        type: 'function',
        function: {
            name: "getCurrentWeather",
            description: "Get the current weather",
            parameters: {
                type: 'object',
                properties: {}
            }
        }
    },
    {
        type: "function",
        function: {
            name: "getLocation",
            description: "Get the user's current location",
            parameters: {
                type: "object",
                properties: {}
            }
        }
    }
]