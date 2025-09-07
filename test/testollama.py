import ollama
from evdev import InputDevice, ecodes, list_devices
import requests
import espeakng
import sounddevice as sd
import soundfile as sf
import numpy as np
import threading
import os
import time

audioFile = "audio.wav"
rhasspyUrl = "http://localhost:12101/api/speech-to-text"
ollamaModel = "tinyllama"
buttoncode = 304
mic_device = "plughw:3,0"

stop_event = threading.Event()

speaker = espeakng.ESpeakNG()
speaker.voice = 'en'
speaker.say("Hi, I am KikiCube. Press A to ask for help.")

def audiototext(filename=audioFile):
    if not os.path.exists(filename) or os.path.getsize(filename) < 1000:
        print("Error: audio file too small or does not exist")
        return ""
    try:
        with open(filename, "rb") as f:
            resp = requests.post(rhasspyUrl, files={"file": f})
        return resp.text.strip()
    except requests.RequestException as e:
        print("Error connecting to Rhasspy:", e)
        return ""

def askollama(prompt):
    response = ollama.chat(
        model=ollamaModel,
        messages=[
            {'role': 'system', 'content': 'Voice assistant, called KikiCube, you are on a Raspberry Pi 4 and are controlled by Python, a gamepad, and voice.'},
            {'role': 'user', 'content': prompt}
        ]
    )
    return response['message']['content']

def hablar(texto):
    speaker.say(texto)

recording = False
proc = None
frames = []

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


def gamepad_loop():
    global recording, proc
    gamepad = InputDevice('/dev/input/event16')

    for event in gamepad.read_loop():
        if event.type == ecodes.EV_KEY:
            if event.code == buttoncode and event.value == 1:
                if not recording:
                    print('started recording')
                    recording = True
                    stop_event.clear()
                    audio_thread = threading.Thread(target=recordAudio)
                    saveAudio()
                else:
                    print('stopping recording')
                    recording = False
                    stop_event.set()
                    audio_thread.join()
                    saveAudio()

                    texto = audiototext()
                    print("Transcription:", texto)
                    if texto:
                        answer = askollama(texto)
                        print("Ollama:", answer)
                        hablar(answer)

if __name__ == "__main__":
    gamepad_loop()
