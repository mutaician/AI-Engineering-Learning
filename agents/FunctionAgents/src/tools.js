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