from google.cloud import speech as speech
from google.cloud import texttospeech
from google.oauth2 import service_account
import speech_recognition as sr
from pygame import mixer
import subprocess
import os


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


def speak(self):
    print(self)
    response_text = self
    # Create The text-to-speech client with the required credentials
    client = texttospeech.TextToSpeechClient(credentials=GOOGLE_CLOUD_CRED)

    # Set the text to be said
    input_response = texttospeech.types.cloud_tts_pb2.SynthesisInput(text=response_text)

    # setup the configuration of the audio file
    audio_config = texttospeech.types.cloud_tts_pb2.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3
    )

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


def record_audio():
    r = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            data = r.recognize_google(r.listen(source))
            # print("Data in record_audio: " + str(data))
    except sr.UnknownValueError:
        # speak("I'm Sorry, i couldn't understand that")
        return None
    except sr.RequestError as e:
        # speak("Could not request results from Google Speech Recognition service; {0}".format(e))
        return None

    return data


def mirror_mirror(self):

    print("-------------------------------------------------")
    print("Finding response in mirror")

    request = self
    CHROME = os.path.join('Applications/', 'Google Chrome.app')
    google_chrome = 'Google Chrome'

    # if "Mirror Mirror" in data:
    #  speak("Yes, sir ?")
    if "what is your name" in request:
        speak("You can call me, Mirror Mirror")
        found = True

    elif "where do you live" in request:
        speak("In your heart.")
        found = True

    elif "how are you" in request:
        print("Found request, now responding")
        speak("I am fine")
        found = True

    elif "what time is it" in request:
        speak(time.localtime(time.time()))
        found = True

    elif "who is" in self:
        data = self.split(" ")
        name = data[2]
        speak("Hold on, I'm finding information about " + name)
        os.system('killall ' + google_chrome)
        found = True

    elif "where is" in request:
        data = self.split(" ")
        location = data[2]
        speak("Hold on, I will show you where " + location + " is.")
        os.system('killall ' + google_chrome)
        subprocess.call([CHROME, "https://www.google.nl/maps/place/" + location + "/&amp;"])
        found = True

    elif "open" in request:
        data = self.split(" ")
        application = data[1]
        speak("Hold on, I will show you " + application)
        os.system('killall ' + google_chrome)
        subprocess.call([CHROME, "https://www." + application + ".com"])
        found = True

    else:
        found = False

    return found
