export async function getCurrentWeather({ location }) {

  const weather = {
    location,
    temperature: "34",
    unit: "C",
    forecast: "partly cloudy",
  };

  return JSON.stringify(weather);
}

export async function getLocation() {
  return "Kabarak, Nakuru, Kenya";
}

export const tools = [
  {
    type: "function",
    function: {
        function: getCurrentWeather,
        parameters: {
            type: 'object',
            properties: {
                location: {
                    type: 'string',
                    description: 'The location to get the weather'
                }
            },
            required: ["location"]
        }
    }
  },
  {
    type: "function",
    function: {
        function: getLocation,
        parameters: {
            type: 'object',
            properties: {}
        }
    }
  },
];
