from django.shortcuts import render

import json
import urllib.request
import urllib.parse
import urllib.error
import os

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")


def index(request):

    data = {}
    city = ""
    error = ""

    if request.method == "POST":

        city = request.POST.get("city", "").strip()

        if not city:
            error = "Please enter a city name."

        else:
            try:

                encoded_city = urllib.parse.quote(city)

                weather_url = (
                    "https://api.weatherapi.com/v1/current.json"
                    f"?key={API_KEY}"
                    f"&q={encoded_city}"
                    "&aqi=no"
                    "&lang=en"
                )

                response = urllib.request.urlopen(weather_url)

                response_data = response.read()

                weather_data = json.loads(response_data)

                location = weather_data["location"]
                current = weather_data["current"]

                data = {
                    "name": location["name"],
                    "region": location["region"],
                    "country": location["country"],
                    "latitude": location["lat"],
                    "longitude": location["lon"],
                    "timezone": location["tz_id"],
                    "localtime": location["localtime"],

                    "temp": current["temp_c"],
                    "feels_like": current["feelslike_c"],

                    "weather": current["condition"]["text"],
                    "icon": current["condition"]["icon"],

                    "pressure": current["pressure_mb"],
                    "humidity": current["humidity"],

                    "wind_speed": current["wind_kph"],
                    "wind_direction": current["wind_dir"],
                    "wind_degree": current["wind_degree"],

                    "clouds": current["cloud"],
                    "precipitation": current["precip_mm"],
                    "visibility": current["vis_km"],
                    "uv": current["uv"],

                    "last_updated": current["last_updated"],
                }

            except urllib.error.HTTPError as e:

                if e.code == 401:
                    error = "Invalid API key."

                elif e.code == 400:
                    error = "City not found or invalid request."

                elif e.code == 403:
                    error = "API access denied or monthly quota exceeded."

                else:
                    error = f"WeatherAPI error: {e.code}"

            except urllib.error.URLError:
                error = "Could not connect to WeatherAPI."

            except KeyError as e:
                error = f"Unexpected API response. Missing field: {e}"

            except json.JSONDecodeError:
                error = "Invalid response received from WeatherAPI."

            except Exception as e:
                error = f"An unexpected error occurred: {e}"

    return render(
        request,
        "index.html",
        {
            "data": data,
            "city": city,
            "error": error,
        },
    )