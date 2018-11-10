import nltk as nl
import pyaudio
import smart_mirror as sm
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


def wake_word_detection():
    waiting = True
    while waiting:
        wake_word = sm.record_audio()
        if wake_word == "hi":
            if sm.interactions == 0:
                sm.speak("Hello, What I do for you ?")
                sm.interactions += 1
                heard()
            else:
                sm.speak("Hello again, what can I do ?")
                sm.interactions += 1
                heard()


def heard():
    request_not_received = True
    data = ""
    while request_not_received:
        data = sm.record_audio()
        if data is not None:
            request_not_received = False

    sm.mirror_mirror(data)
    time.sleep(2)
    wake_word_detection()

wake_word_detection()


