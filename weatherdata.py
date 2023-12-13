import json
import time
import urllib.request

API='JoZpeCmsptmiRaBXJv59aVz1BVxApjLX'

def getLocation(city):
    search_address="http://dataservice.accuweather.com/locations/v1/cities/search?apikey="+API+"&q="+city+"&details=true"
    with urllib.request.urlopen(search_address) as search_address:
        data=json.loads(search_address.read().decode())
        loaction_key=data[0]['Key']
        return(loaction_key)

#city='mumbai'
#locationkey=getLocation(city)

def getforecast(locationkey):
    daily_forecastURL="http://dataservice.accuweather.com/forecasts/v1/daily/1day/"+locationkey+"?apikey="+API+""
    #print(daily_forecastURL)
    with urllib.request.urlopen(daily_forecastURL) as daily_forecastURL:
        data=json.loads(daily_forecastURL.read().decode())
        #print(data["DailyForecasts"])
        return(data["DailyForecasts"])
    #print(data)

# =============================================================================
#     for key1 in data["DailyForecasts"]:
#         print("Weather Forecast for "+key1['Date']+"is:")
#         print("Temperature in F (minimum) is: "+str(key1['Temperature']['Minimum']['Value']))
#         print("Temperature in F (maximum) is: " + str(key1['Temperature']['Maximum']['Value']))
#         print("Day Forecast "+str(key1['Day']['IconPhrase']))
#         print("Day Forecast "+str(key1['Night']['IconPhrase']))
#         print("------------------------------------------------------------------------")
# 
# =============================================================================
#getforecast(locationkey)
