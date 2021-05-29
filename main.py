from vosk import Model, KaldiRecognizer
import os
import pyaudio
import pyttsx3
import json
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch


## =========== speech synthesis ============
engine = pyttsx3.init()

def speak(text: str) -> None:
    """generates voice for a given text

    Args:
        text ([str]): a text to be generated
    """
    engine.say(text)
    engine.runAndWait()

## =========== question answering ==========
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
qa_model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

## =========== speech recognition ==========
model = Model("model")
rec = KaldiRecognizer(model, 16000)

#open microphone for listening
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

step = 0
while True:
    data = stream.read(4000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        #TODO: the bot answers it's own voice and answers it.
        #TODO: make some pause or sth to first get user command and then answer it and repeat it again
        '''convert speech to text'''
        result = rec.Result()
        # result is a string of dict "{}" -> covert it to text and get the text only
        result_dict = json.loads(result)
        text = result_dict['text']

        print(f'User input: {text}')

        if 'isaac' in text:
            ''' encode user input and feed it into QA model'''
            new_user_input_ids = tokenizer.encode(text + tokenizer.eos_token, return_tensors='pt')
            # append the new user input tokens to the chat history
            bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if step > 0 else new_user_input_ids
            # generated a response while limiting the total chat history to 1000 tokens, 
            chat_history_ids = qa_model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
            answer = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
            print(f"bot's answer: {answer}")

            '''convert answer to speech'''
            speak(answer)

        step += 1 # increase step for next user input
    