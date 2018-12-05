import nltk as nl
import pyaudio
import smart_mirror as sm
import threading
from pygame import mixer
import numpy as np
import time
text = "come to the club, it will be fun dark outside"

noise_words = ['is', "Is", "a", "at", "to", 'it', "be", "the"]


def audio_sensor():
    CHUNK = 2 ** 11
    RATE = 44100

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

    for i in range(int(10 * 44100 / 1024)):  # go for a few seconds
        data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
        peak = np.average(np.abs(data)) * 2
        bars = "#" * int(50 * peak / 2 ** 16)
        print("#" + str(bars))
    # print(i, peak, bars)
    # "%04d %05d %s"

    stream.stop_stream()
    stream.close()
    p.terminate()


def remove_noise(self):
    words = nl.word_tokenize(self)
    noise_free_text = words
    word = 0

    while word < len(words):
        noise = 0
        while noise < len(noise_words):
            if words[word] == noise_words[noise]:
                del noise_free_text[word]
            else:
                noise += 1
        word += 1
    return noise_free_text


""" This Function is used to decide whether the user has said the required wake word"""


def wake_word_detection():
    waiting = True
    mixer.init()
    mixer.music.load("Start_tone.mp3")
    print("-------------------------------------------------")
    print("Wake word detection initiated")
    while waiting:
        print("Waiting for wake word")
        wake_word = sm.record_audio()
        print("Checking wake word")
        # print(str(wake_word))
        if wake_word == "mirror mirror":
            print("Said")
            if sm.interactions == 0:
                mixer.music.play()
                sm.interactions += 1
            else:
                mixer.music.play()
                sm.interactions += 1
            waiting = False

    heard()


def heard():
    request_not_received = True
    print("-------------------------------------------------")
    print("Heard initiated")

    # Keep count of the number of times the program loops for a request
    tries = 0

    # Once it tries up tp this limit the program will go back to waiting for the Wake word
    tries_limit = 5

    while request_not_received:
        print("recording request")
        print("Try number: " + str(tries))
        data = sm.record_audio()
        if data is not None:
            print("The users request was: " + str(data))
            print("Finding response to user request")
            found = sm.mirror_mirror(data)

            # Sleep to wait on the return of the find response to the user and to respond
            # Then continue on
            print("5 second sleep")
            time.sleep(5)
            if found:
                request_not_received = False

            # Try up too receive user input and/or find the response up to limited number
            # If it reaches this limit, reset back to wake_word_detection
            else:
                if tries == tries_limit:
                    break
                tries += 1
        else:
            if tries == tries_limit:
                break
            tries += 1

    if tries == tries_limit:
        sm.speak("Sorry I can't help you with that! Please try again later")
    else:
        print("User request has been dealt with, now back to waiting for wake word")

    mixer.init()
    mixer.music.load("Closing_tone.mp3")
    mixer.music.play()

    wake_word_detection()


wake_word_detection()

