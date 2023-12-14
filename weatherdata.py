import json  # Import the json module to parse JSON data.
import time  # Import the time module (unused in this code snippet).
import urllib.request  # Import urllib.request to make HTTP requests.

API = 'JoZpeCmsptmiRaBXJv59aVz1BVxApjLX'  # AccuWeather API key.

def getLocation(city):
    # Construct the URL to search for a city using the AccuWeather API.
    search_address = "http://dataservice.accuweather.com/locations/v1/cities/search?apikey=" + API + "&q=" + city + "&details=true"
    with urllib.request.urlopen(search_address) as search_address:
        # Open the URL and read the response.
        data = json.loads(search_address.read().decode())
        # Extract the location key from the response.
        location_key = data[0]['Key']
        return location_key  # Return the location key.

def getforecast(locationkey):
    # Construct the URL to get the daily forecast using the AccuWeather API and the location key.
    daily_forecastURL = "http://dataservice.accuweather.com/forecasts/v1/daily/1day/" + locationkey + "?apikey=" + API
    with urllib.request.urlopen(daily_forecastURL) as daily_forecastURL:
        # Open the URL and read the response.
        data = json.loads(daily_forecastURL.read().decode())
        # Return the 'DailyForecasts' part of the response.
        return data["DailyForecasts"]
