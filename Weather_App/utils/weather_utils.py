import requests
from datetime import datetime

def get_weather_emoji(weather_main):
    emoji_map = {
        "Clear": "☀️", "Clouds": "☁️", "Rain": "🌧️", "Drizzle": "🌦️",
        "Thunderstorm": "⛈️", "Snow": "❄️", "Mist": "🌫️", "Smoke": "🌫️",
        "Haze": "🌫️", "Dust": "🌪️", "Fog": "🌫️", "Sand": "🌪️",
        "Ash": "🌋", "Squall": "🌀", "Tornado": "🌪️"
    }
    return emoji_map.get(weather_main, "❓")

def get_weather_data(city, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    url = f"{base_url}q={city}&appid={api_key}&units=metric&lang=en"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        print(f"Request timed out for city: {city}")
        return None
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err} - Status: {response.status_code}")
        if response.status_code == 401:
            print("Error: Invalid API Key. Please check your API_KEY in config.py.")
        elif response.status_code == 404:
            print(f"Error: City '{city}' not found.")

        return None
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return None

    api_json_data = response.json()

    try:
        if not (isinstance(api_json_data.get("weather"), list) and
                len(api_json_data["weather"]) > 0 and
                isinstance(api_json_data.get("main"), dict) and
                isinstance(api_json_data.get("sys"), dict) and
                "name" in api_json_data):
            print(f"API response format is unexpected or incomplete: {api_json_data}")
            return None

        main_weather_info = api_json_data["weather"][0]

        processed_data = {
            "city": api_json_data.get("name", "N/A"),
            "temp": api_json_data["main"].get("temp", "N/A"),
            "feels_like": api_json_data["main"].get("feels_like", "N/A"),
            "humidity": api_json_data["main"].get("humidity", "N/A"),
            "description": main_weather_info.get("description", "N/A"),
            "icon_id": main_weather_info.get("icon", ""),
            "weather_main": main_weather_info.get("main", "Unknown"),
            "sunrise": "N/A",
            "sunset": "N/A",
            "emoji": get_weather_emoji(main_weather_info.get("main", "Unknown"))
        }

        if "sunrise" in api_json_data.get("sys", {}):
            processed_data["sunrise"] = datetime.fromtimestamp(api_json_data["sys"]["sunrise"]).strftime('%H:%M')
        if "sunset" in api_json_data.get("sys", {}):
            processed_data["sunset"] = datetime.fromtimestamp(api_json_data["sys"]["sunset"]).strftime('%H:%M')

        return processed_data

    except (KeyError, IndexError, TypeError) as e:
        print(f"Error parsing API response data: {e}")
        print(f"Problematic API Response was: {api_json_data}")
        return None