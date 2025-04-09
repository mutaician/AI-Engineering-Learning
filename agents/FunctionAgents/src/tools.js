export async function getCurrentWeather({ location, unit = "celcius" }) {

  const weather = {
    location,
    temperature: "34",
    unit,
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
      name: "getCurrentWeather",
      description: "Get the current weather",
      parameters: {
        type: "object",
        properties: {
          location: {
            type: "string",
            description: "The location from where to get the weather",
          },
          unit: { type: "string", enum: ["celcius", "fahrenheit"] },
        },
        required: ["location"],
      },
    },
  },
  {
    type: "function",
    function: {
      name: "getLocation",
      description: "Get the user's current location",
      parameters: {
        type: "object",
        properties: {},
      },
    },
  },
];
