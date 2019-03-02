#!/usr/bin/python3

import datetime
import pymongo
import urllib.parse

print("-------------------------------------------------")
print("Setting up Log database connection")
print("-------------------------------------------------")
username = urllib.parse.quote_plus("jts996")
password = urllib.parse.quote_plus("*******")
myClient = pymongo.MongoClient(
    'mongodb+srv://jts996:%s@log-3kku0.mongodb.net/test?retryWrites=true' % password)
mydb = myClient["Logs"]
myCol = mydb["log"]


class Logging:

    # Function which takes care of storing the user requests to the log
    # I am using a Mongodb to store the JSON objects

    @staticmethod
    def log(request, found):
        print("------------------------------------------")
        print("DATABASE: Logging request")
        date = datetime.datetime.now()

        if found:

            log = {"request": request, "date": date}

            myCol.insert_one(log)
        else:

            log = {"request": request, "date": date, "failed_request": "true"}

            myCol.insert_one(log)

        print("DATABASE: Logging complete")
        print("------------------------------------------")
