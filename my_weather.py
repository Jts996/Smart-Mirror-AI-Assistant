#!/usr/bin/python3

from pyowm import OWM


class MyWeather:

    @staticmethod
    def current_weather(loc):

        owm = OWM()

        weather = owm.weather_at_place(loc)
        print(weather)

