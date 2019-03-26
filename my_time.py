#!/usr/bin/python3

import threading
import time
import datetime


class Times:

    # Function which provides the response of the current time when the user requests
    @staticmethod
    def current_time():
        t = time.localtime(time.time())
        hour = t[3]
        minute = t[4]

        # After half past changes "too" the next hour
        if minute > 30:
            minute = 60 - t[4]
            # Afternoon
            if 11 < hour < 17:
                hour = hour - 12
                current_t = "It is " + str(minute) + " minutes too " + str(hour) + " in the afternoon"

            # Evening
            elif 17 <= hour < 24:
                hour = hour - 12
                current_t = "It is " + str(minute) + " minutes too " + str(hour) + " in the evening"
            # Morning
            else:
                current_t = "It is " + str(minute) + " minutes too " + str(hour + 1) + " in the morning"
            # Before half past changes to "past" the previous hour
        else:
            # Afternoon
            if 11 < hour < 17:
                hour = hour - 12
                current_t = "It is " + str(minute) + " minutes past " + str(hour) + " in the afternoon"
            # Evening
            elif 17 <= hour < 24:
                hour = hour - 12
                current_t = "It is " + str(minute) + " minutes past " + str(hour) + " in the evening"
            # Morning
            else:
                current_t = "It is " + str(minute) + " minutes past " + str(hour) + " in the morning"

        return current_t

    # Function which provides the response of the current date when the user requests
    @staticmethod
    def current_date():

        date = datetime.datetime.now()

        current_d = date.strftime("it is %A the %d of %B %Y")

        return current_d


# Class for containing the different timer functions
class Timer(threading.Thread):

    # Function for dealing with creating a basic timer
    @staticmethod
    def tim(seconds):
        print("Starting timer")
        from Assistant_responses import alert
        # the timer is a sleep for the specified length of time
        time.sleep(seconds)
        print("Timer has finished")
        # Make alert the user to the timer finishing
        alert()
        alert()
        print("Closing timer thread")
        return 1
