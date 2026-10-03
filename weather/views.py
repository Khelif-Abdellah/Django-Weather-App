from django.shortcuts import render

import json
import urllib.request
import urllib.parse
import urllib.error


API_KEY = "edc2a10b081e411ab82123337260310"


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
                # ---------------------------------------------
                # WeatherAPI - Current Weather
                # ---------------------------------------------

                encoded_city = urllib.parse.quote(city)

                weather_url = (
                    "https://api.weatherapi.com/v1/current.json"
                    f"?key={API_KEY}"
                    f"&q={encoded_city}"
                    "&aqi=no"
                    "&lang=en"
                )

                # Send request to WeatherAPI
                response = urllib.request.urlopen(weather_url)

                # Read response
                response_data = response.read()

                # Convert JSON -> Python dictionary
                weather_data = json.loads(response_data)

                # ---------------------------------------------
                # Location information
                # ---------------------------------------------

                location = weather_data["location"]

                # ---------------------------------------------
                # Current weather information
                # ---------------------------------------------

                current = weather_data["current"]

                # ---------------------------------------------
                # Prepare data for Django template
                # ---------------------------------------------

                data = {
                    # Location
                    "name": location["name"],
                    "region": location["region"],
                    "country": location["country"],
                    "latitude": location["lat"],
                    "longitude": location["lon"],
                    "timezone": location["tz_id"],
                    "localtime": location["localtime"],

                    # Temperature
                    "temp": current["temp_c"],
                    "feels_like": current["feelslike_c"],

                    # Weather
                    "weather": current["condition"]["text"],
                    "icon": current["condition"]["icon"],

                    # Pressure
                    "pressure": current["pressure_mb"],

                    # Humidity
                    "humidity": current["humidity"],

                    # Wind
                    "wind_speed": current["wind_kph"],
                    "wind_direction": current["wind_dir"],
                    "wind_degree": current["wind_degree"],

                    # Clouds
                    "clouds": current["cloud"],

                    # Rain
                    "precipitation": current["precip_mm"],

                    # Visibility
                    "visibility": current["vis_km"],

                    # UV
                    "uv": current["uv"],

                    # Last update
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