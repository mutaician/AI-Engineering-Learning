export async function getCurrentWeather(){
    const weather = {
        temperature: "62",
        unit: "F",
        forecast: "Cloudy"
    }

    return JSON.stringify(weather)
}

export async function getLocation(){
    return "Nakuru, Kenya"
}