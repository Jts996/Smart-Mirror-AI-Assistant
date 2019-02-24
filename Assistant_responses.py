from google.cloud import texttospeech
from google.oauth2 import service_account
import speech_recognition as sr
import time
from threading import Thread
from pygame import mixer
import webbrowser
from listening import Listening
import os
import sys
import text_manipulation


# To track how many interactions the user has had with the system
interactions = 0

# Setup Google cloud credentials
GOOGLE_CLOUD_CRED = service_account.Credentials.from_service_account_file(
    '/Users/james/Documents/Fourth Year/Project Module/api-key-speech-recognition.json')


# Setup the voice of the assistant
voice = texttospeech.types.cloud_tts_pb2.VoiceSelectionParams(
    language_code='en-GB',
    ssml_gender=texttospeech.enums.SsmlVoiceGender.MALE,
)


# Create The text-to-speech client with the required credentials
client = texttospeech.TextToSpeechClient(credentials=GOOGLE_CLOUD_CRED)


# setup the configuration of the audio file
audio_config = texttospeech.types.cloud_tts_pb2.AudioConfig(
    audio_encoding=texttospeech.enums.AudioEncoding.MP3
)


def start():
    mixer.init()
    mixer.music.load("Start_tone.mp3")
    mixer.music.play()


def end():
    mixer.init()
    mixer.music.load("Closing_tone.mp3")
    mixer.music.play()


def alert():
    mixer.init()
    mixer.music.load('alarm.mp3')
    mixer.music.play()


""" Method to deal with turning the text response into an audio file for the user feedback """


def speak(self):
    response_text = self

    # Set the text to be said
    input_response = texttospeech.types.cloud_tts_pb2.SynthesisInput(text=response_text)

    # Conduct the text-to-speech request on the specified text response
    response = client.synthesize_speech(input_response, voice, audio_config)

    # Response is in binary format
    with open('response.mp3', 'wb') as r:
        r.write(response.audio_content)
        print("Created the audio file")

    # Loading mixer and then loading audio file and then playing the response to the user
    mixer.init()
    print("Loading audio response")
    mixer.music.load('response.mp3')
    print("Responding")
    mixer.music.play()
    mixer.quit()


""" Method to deal with the speech recognition """


def record_audio():
    r = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("Listening to user")
            data = r.recognize_google(r.listen(source))
            # print("Data in record_audio: " + str(data))
    except sr.UnknownValueError:
        # speak("I'm Sorry, i couldn't understand that")
        return None
    except sr.RequestError as e:
        # speak("Could not request results from Google Speech Recognition service; {0}".format(e))
        return None

    return data


""" Method to deal with finding and deciding what to do with the users request """


def mirror_mirror(self):

    print("-------------------------------------------------")
    print("Finding response in mirror")

    request = self
    found = False
    print(str(request))

    # intents, objs = text_manipulation.remove_noise(request)
    # print(intents)
    # print(objs)

    # Path to chrome browser in MacOS
    chrome_path = 'open -a /Applications/Google\ Chrome.app %s'

    if "what is your name" in request:
        response = "You can call me, Mirror, Mirror"
        speak(response)
        found = True

    elif "where do you live" in request:

        response = "In your heart."
        speak(response)
        found = True

    elif "how" in request:

        response = "I am fine, thank you"
        speak(response)
        found = True

    elif "what" in request:

        from my_time import Times

        if "time" in request:

            response = Times.current_time()
            speak(response)
            found = True

        elif "date" in request:

            response = Times.current_date()
            speak(response)
            found = True

        elif "weather" in request:
            from my_weather import MyWeather
            print("here")
            data = self.split(" ")
            location = data[len(data)]
            response = MyWeather.current_weather(location)
            speak(response)
            found = True

    elif "start" in request:
        print("In here")
        print(str(len(request)))
        from my_time import Timer

        if "timer" in request:
            print("Timer initialisation")
            word = 0

            # If user specifies a time in minutes, we need to convert this to seconds
            # This is because the timer is implemented as a sleep which only takes seconds as
            # its parameters
            if "minutes" in request:
                position = request.index("minutes")
                print("Converting minutes")
                # extracting the time number from the char list
                t = int(request[position-2])
                print(str(t))
                response = "Starting a timer for " + str(t) + " minutes"
                speak(response)
                # Converting the time in minutes to seconds
                sec = t * 60
                # Starts a new thread so that the timer can run in the background, and not disrupt the
                # rest of the application
                thread_timer = Thread(target=Timer.tim,
                                      args=[sec])
                thread_timer.start()
                print("Timer Thread is exiting and rejoining the main listening thread")
                # Makes sure the thread is terminated as to not waste resources
                thread_timer.join()

            # If time is specified in seconds already, no need to do the conversion
            elif "seconds" in request:
                position = request.index("seconds")
                print(str(position))
                print("seconds")
                # extracting the time number from the char list
                sec = int(request[position - 2])
                response = "Starting a timer for " + str(sec) + " seconds"
                speak(response)
                # Starts a new thread so that the timer can run in the background, and not disrupt the
                # rest of the application
                thread_timer = Thread(target=Timer.tim,
                                      args=[sec])
                thread_timer.start()
                print("Timer Thread is exiting and rejoining the main listening thread")
                # Makes sure the thread is terminated as to not waste resources
                thread_timer.join()
            else:
                word += 1
        found = True
        return found

    # NEED TO FIX: DOES NOT WORK
    elif "who" in request:
        data = self.split(" ")
        name = data[2]
        response = "Hold on, I'm finding information about " + name
        speak(response)
        found = True

    elif "where" in request:  # Close screen option
        data = self.split(" ")
        location = data[2]
        response = "Hold on, here is what I have found for you"
        speak(response)
        url = "https://www.google.nl/maps/place/" + location + "/&amp;"
        webbrowser.get(chrome_path).open(url)
        found = True

    elif "open" in request:
        data = self.split(" ")
        application = data[1]
        response = "Hold on, here is what I have found for you"
        speak(response)
        url = "https://www." + application + ".com"
        webbrowser.get(chrome_path).open(url)
        found = True

    else:
        found = False

    if found:
        logging_thread = Thread(target=Listening.logging, args=[request, found])
        logging_thread.start()
        logging_thread.join()
    else:
        logging_thread = Thread(target=Listening.logging, args=[request, found])
        logging_thread.start()
        logging_thread.join()

    return found
