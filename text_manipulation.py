import nltk as nl
import pyaudio
import numpy as np
import speech_recognition as sr


text = "come to the club, it will be fun dark outside"

noise_words = ['is', "Is", "a", "at", "to", 'it', "be", "the"]


def remove_noise(input_text):
    words = nl.word_tokenize(input_text)
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


def wake_word_detection():
    r = sr.Recognizer()
    mic = sr.Microphone()
    wake_word_not_said = True
    wake_word = "hi"

    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    while wake_word_not_said:

        try:
            received_word = r.recognize_google(audio)

            if received_word == wake_word:
                print("I have heard the wake word! What do you want?")
                wake_word_not_said = False
        except sr.UnknownValueError:
            print("Could not make out audio")
            exit(1)
        except sr.RequestError as e:
            print("Could not request results {0}".format(e))
            exit(1)


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


wake_word_detection()
