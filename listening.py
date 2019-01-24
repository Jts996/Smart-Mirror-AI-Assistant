import threading
import time
import datetime
import pymongo
import urllib.parse

username = urllib.parse.quote_plus("jts996")
password = urllib.parse.quote_plus("M@serati96!")
myClient = pymongo.MongoClient("mongodb+srv://%s:%s@smart-mirror-log-eo59t.azure.mongodb.net/test" 
                               "?retryWrites=true" % (username, password))
mydb = myClient["mySmartMirror"]
myCol = mydb["request_log"]


class Listening(threading.Thread):

    def run(self):
        print("Listening for request")

    # function which handles the listening for the wake word
    #
    # This will iterate in a loop until the desired wake word is provided by the user.
    # Once this is done the "heard" function is initiated (See heard function for details)
    @staticmethod
    def wake_word_detection():
        from Assistant_responses import start, record_audio

        waiting = True
        print("-------------------------------------------------")
        print("Wake word detection initiated")
        while waiting:
            print("Waiting for wake word")
            wake_word = record_audio()
            print("Checking wake word")
            # print(str(wake_word))
            if wake_word == "hello":
                print("Said")
                start()
                Listening.heard()
                waiting = False

    # Function to deal with the user request
    # Tries 5 times to record and find the best response, after this it will revert back to
    # waiting for the wake word
    #
    # The flow is that it will call the "record_audio" function to record the users voice,
    # this string is then sent to be used to find a response, if a response is found, ask user
    # if that is all they want or else check that the limited number of tries hasn't been reached.
    #
    # Once the max limit is reached or the user has finished with their exchange, return to waiting
    # for the wake word
    @staticmethod
    def heard():
        from Assistant_responses import mirror_mirror, end, speak, record_audio

        request_not_received = True
        print("-------------------------------------------------")
        print("Heard initiated")

        # Keep count of the number of times the program loops for a request
        tries = 1
        # Once it tries up tp this limit the program will go back to waiting for the Wake word
        tries_limit = 5

        while request_not_received:
            print("recording request")
            print("Try number: " + str(tries))
            data = record_audio()

            if data is not None:

                print("The users request was: " + str(data))
                print("Finding response to user request")
                found = mirror_mirror(data)

                # Sleep to wait on the return of the find response to the user and to respond
                #  Then continue on
                print("5 second sleep")
                time.sleep(5)
                if found:
                    request_not_received = False
                else:
                    if tries == tries_limit:
                        break
                    # Try up too receive user input and/or find the response up to limited number
                    # If it reaches this limit, reset back to wake_word_detection
                    else:
                        speak("Sorry, I could not find that, Please try again")
                        time.sleep(3.7)
                        tries += 1
            else:
                if tries == tries_limit:
                    break
                tries += 1

        if tries == tries_limit and request_not_received:
            speak("Sorry I can't help you with that! Try again later")
            time.sleep(3.7)
        else:
            print("User request has been dealt with, now back to waiting for wake word")
        time.sleep(2)
        print("Restarting, going back to wait for wake word")
        end()
        Listening.wake_word_detection()

        #speak("Is that everything?")
        #data = record_audio()
        #if "yes" in data:
         #   end()
          #  Listening.wake_word_detection()
        #if "no" in data:
         #   speak("Ok, What else would you like help with?")
          #  Listening.heard()

    # Function which takes care of storing the user requests to the log
    # I am using a Mongodb to store the JSON objects

    @staticmethod
    def logging(request):

        date = datetime.datetime.now()

        log = {"request": request, "date": date}

        myCol.insert_one(log)
