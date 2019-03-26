#!/usr/bin/python3

from google.cloud import texttospeech
from google.oauth2 import service_account
import time
from multiprocessing import Process
from pygame import mixer
import webbrowser
from Logs import Logging
import os
import sys
import text_manipulation



# To track how many interactions the user has had with the system
interactions = 0

# Setup Google cloud credentials
GOOGLE_CLOUD_CRED = service_account.Credentials.from_service_account_file(
    '/Users/james/Documents/Fourth Year/Project Module/api-key-speech-recognition.json')


# Tone to provide feedback to user that the device is ready for their request
def start():
    mixer.init()
    mixer.music.load("Start_tone.mp3")
    mixer.music.play()


# Tone to provide feedback to user that the device has finished the interaction
def end():
    mixer.init()
    mixer.music.load("Closing_tone.mp3")
    mixer.music.play()


# Tone to alert the user to that their timer has finished
def alert():
    mixer.init()
    mixer.music.load('alarm.mp3')
    mixer.music.play()


# Method to deal with turning the text response into an audio file for the user feedback
def speak(self, weather):
    response_text = self

    print("Speaking")

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
    if weather:
        time.sleep(10)
    else:
        time.sleep(5)
    os.remove("response.mp3")
    mixer.quit()


# Method to deal with finding and deciding what to do with the users request
def mirror_mirror(self):

    print("-------------------------------------------------")
    print("Finding response in mirror")

    request = self
    found = False
    print(str(request))

    objects, intents = text_manipulation.request_processing(request)
    print(intents)
    print(objects)

    if "what" in intents:

        from my_time import Times

        if "time" in objects:

            response = Times.current_time()
            speak(response, False)
            found = True

        elif "date" in objects:

            response = Times.current_date()
            speak(response, False)
            found = True

        elif "weather" in objects:
            from my_weather import MyWeather
            if len(objects) > 2:
                # date = objects[len(objects) - 1]
                location = objects[len(objects) - 2]
            else:
                location = objects(len(objects) - 1)
            response = MyWeather.current_weather(location)
            speak(response, True)
            found = True

        else:
            response = "You can call me, Mirror, Mirror"
            speak(response, False)
            found = True

    elif "where" in intents:

        response = "In your heart."
        speak(response, False)
        found = True

    elif "how" in intents:

        response = "I am fine, thank you"
        speak(response, False)
        found = True

    elif "start" or "set" in intents:
        from my_time import Timer

        if "timer" in objects:
            print("Timer initialisation")
            word = 0

            # If user specifies a time in minutes, we need to convert this to seconds
            # This is because the timer is implemented as a sleep which only takes seconds as
            # its parameters
            if "minut" in objects:

                print("Converting minutes")

                # extracting the time number from the char list
                t = int(objects[len(objects) - 2])

                response = "Starting a timer for " + str(t) + " minutes"
                speak(response, False)

                # Converting the time in minutes to seconds
                sec = t * 60

                # Starts a new thread so that the timer can run in the background, and not disrupt the
                # rest of the application
                thread_timer = Process(target=Timer.tim, args=[sec])
                thread_timer.start()

            # If time is specified in seconds already, no need to do the conversion
            elif "second" in objects:
                # extracting the time number from the char list
                sec = int(objects[len(objects) - 2])

                response = "Starting a timer for " + str(sec) + " seconds"
                speak(response, False)

                # Starts a new thread so that the timer can run in the background, and not disrupt the
                # rest of the application
                thread_timer = Process(target=Timer.tim, args=[sec])
                thread_timer.start()

            else:
                word += 1
        found = True

    else:
        found = False

    print("-------------------------------------------------")
    Logging.log(request, found)
    return found
