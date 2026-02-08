import { WEATHER_API_ENDPOINT, weatherMap } from "./const.js";

export const showWeather = async () => {
    const adachiLocation = {
        latitude: 35.76,
        longitude: 139.81,
    };

    const kofuLocation = {
        latitude: 35.65,
        longitude: 138.54,
    };

    const adachiWeatherResponse = await getWeather(adachiLocation);
    const kofuWeatherResponse = await getWeather(kofuLocation);

    displayWeather(adachiWeatherResponse, "kofu");
    displayWeather(kofuWeatherResponse, "adachi");
};

const getWeather = async (location) => {
    const baseParams = {
        current: "temperature_2m,weather_code",
        timezone: "Asia/Tokyo",
    };

    const params = new URLSearchParams({
        ...baseParams,
        ...location,
    });

    const weatherRequest = new Request(`${WEATHER_API_ENDPOINT}?${params}`);

    const response = await fetch(weatherRequest);
    return response.json();
};

const displayWeather = (response, city) => {
    const weather = weatherMap[response.current.weather_code] ?? "-";
    const temperature = response.current.temperature_2m ?? "-";
    document.getElementById(city).innerText = `${weather} / ${temperature}℃`;
};
