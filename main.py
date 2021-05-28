from vosk import Model, KaldiRecognizer
import os
import pyaudio
import pyttsx3
import json

## =========== speech synthesis ============
engine = pyttsx3.init()


def speak(text: str) -> None:
    """generates voice for a given text

    Args:
        text ([str]): a text to be generated
    """
    engine.say(text)
    engine.runAndWait()

## =========== speech recognition ==========
model = Model("model")
rec = KaldiRecognizer(model, 16000)

#open microphone for listening
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

while True:
    data = stream.read(4000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        result = rec.Result()
        # result is a string of dict "{}"
        result_dict = json.loads(result)
        text = result_dict['text']
        print(text)
        speak(text)

    