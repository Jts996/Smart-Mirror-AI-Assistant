import speech_recognition as sr
from pygame import mixer
import subprocess
import os
from gtts import gTTS

interactions = 0


def speak(self):
    print(self)
    tts = gTTS(text=self, lang='en')
    tts.save("audio.mp3")
    mixer.init()
    mixer.music.load('audio.mp3')
    mixer.music.play()


def record_audio():
    r = sr.Recognizer()
    with sr.Microphone(device_index=None, sample_rate=48000, chunk_size=2048) as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        data = r.recognize_google(audio)
    except sr.UnknownValueError:
        # speak("I'm Sorry, i couldn't understand that")
        return None
    except sr.RequestError as e:
        # speak("Could not request results from Google Speech Recognition service; {0}".format(e))
        return None

    return data


def mirror_mirror(self):

    CHROME = os.path.join('Applications/', 'Google Chrome.app')
    google_chrome = 'Google Chrome'

    # if "Mirror Mirror" in data:
    #  speak("Yes, sir ?")
    if "what is your name" in self:
        speak("You can call me, Mirror Mirror")
    if "where do you live" in self:
        speak("In your heart.")
    if "how are you" in self:
        speak("I am fine")
    if "what time is it" in self:
        speak(time.localtime(time.time()))
    if "who is" in self:
        data = self.split(" ")
        name = data[2]
        speak("Hold on, I'm finding information about " + name)
        os.system('killall ' + google_chrome)
    if "where is" in self:
        data = self.split(" ")
        location = data[2]
        speak("Hold on, I will show you where " + location + " is.")
        os.system('killall ' + google_chrome)
        subprocess.call([CHROME, "https://www.google.nl/maps/place/" + location + "/&amp;"])
    if "open" in self:
        data = self.split(" ")
        application = data[1]
        speak("Hold on, I will show you " + application)
        os.system('killall ' + google_chrome)
        subprocess.call([CHROME, "https://www." + application + ".com"])
