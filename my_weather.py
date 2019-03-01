#!/usr/bin/python3

from pyowm import OWM
import pymongo
import urllib.parse

owm_api_key = "7efd54737b3e8f9e8f8567014b77a354"

owm = OWM(owm_api_key)

username = urllib.parse.quote_plus("jts996")
password = urllib.parse.quote_plus("*****")
myClient = pymongo.MongoClient(
    'mongodb+srv://%s:%s@log-3kku0.mongodb.net/test?retryWrites=true' % (username, password))
mydb = myClient["Locations"]
myCol = mydb["cities"]

loc = "stirling"


class MyWeather:

    @staticmethod
    def current_weather(loc):
        doc = myCol.find_one({"city": loc})
        print(doc)

        try:
            city_id = int(doc["_id"])
            observation = owm.weather_at_id(city_id)
            weather = observation.get_weather()
            print(weather)

            forecast = weather.get_detailed_status()
            print(forecast)
            temp = weather.get_temperature('celsius')
            print(temp)

            current_temp = int(temp['temp'])
            max_temp = int(temp['temp_max'])
            min_temp = int(temp['temp_min'])
            return ("The forecast in %s today is %s with a current temperature of %d Celsius, and a high of %d "
                    "Celsius and a low of %d Celsius" % (loc, forecast, current_temp, max_temp, min_temp))
        except:
            return "Sorry I can not find that location"
