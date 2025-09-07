''' 
06/09/2025
Chiara Catalini
KikiCube AI voice assistance
'''
import ollama
import requests
import espeakng
import sounddevice as sd
import soundfile as sf
import numpy as np
import threading
import os
import time

# Variables:
audioFile = 'audio.wav'
rhasspyUrl = 'http://localhost:12101/api/speech-to-text'
ollamaModel = 'tinyllama'
mic_device = 'plughw:3,0'

stop_event = threading.Event()

# Start speaking
speaker = espeakng.ESpeakNG()
speaker.voice = 'en'
speaker.say("Hi, I am KikiCube. Press A to ask for help.")

# Funtions for audio recording and asking TinyLlama AI

def audiototext(filename=audioFile):
    if not os.path.exists(filename) or os.path.getsize(filename) < 1000:
        print('Error: file too small or does not exist')
        return ''
    try:
        with open(filename, 'rb') as f:
            audio_data = f.read()
        headers = {"Content-Type": "audio/wav"}
        resp = requests.post(rhasspyUrl, data=audio_data, headers=headers)
        return resp.text.strip()

    except requests.RequestException as e:
        print('Error connecting to Rhasspy', e)
        return ''

def asktollama(prompt):
    response = ollama.chat(
        model=ollamaModel,
        messages=[
            {'role': 'system', 'content': '''
             Your name is KikiCube, you are a voice assistance built into a robot with a camera, motors and a H bridge. You are friendly, funny and your responses are short (around 3 sentences), concise and informative. 
             
             You can give tips, recommendations and explanations about python programming or the Raspberry Pi, but as a Voice Assistance you cannot control directly motors or another hardware.
             
             Always clarify you are only an AI voice assistance.

             You were created by Kiki, and you are programmed in python.

             You can provide guidance on python coding, but all physical actions must be done by the user or external scripts.

             For more information about YOUR CAPABILITIES and CODE, refer users to the GitHub of Kiki.
            
             Always confirm actions clearly, inform the user, and ask for clarification when a question is unclear. 
             
             Be friendly and slightly humorous tone, but stay concise and informative, when possible, give examples in just 1 or 2 sentences.
            '''},
            {'role': 'user', 'content': prompt}
        ]
    )
    return response['message']['content']

def speak(text):
    speaker.say(text)

frames = []
recording = False

def recordAudio():
    global frames, recording
    frames = []
    def callback(indata, frames_count, time_info, status):
        if recording:
            frames.append(indata.copy())
        
    with sd.InputStream(channels=1, samplerate=16000, callback=callback):
        while recording:
            stop_event.wait()

def saveAudio():
    if frames:
        data = np.concatenate(frames, axis=0)
        sf.write(audioFile, data, 16000)
    else:
        print('no audio recorded')

def handleRecording():
    global recording
    if not recording:
        speak('Ready for helping')
        print('started recording')
        recording = True
        stop_event.clear()
        threading.Thread(target=recordAudio).start()
    else:
        print('Stopping recording')
        recording = False
        stop_event.set()
        saveAudio()
        text = audiototext()
        print('Transcription:', text)
        if text:
            answer = asktollama(text)
            print('Answer:', answer)
            speak(answer)