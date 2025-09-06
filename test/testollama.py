import ollama
from evdev import InputDevice, ecodes, list_devices
import requests
import espeakng
import subprocess
import os
import time
import signal

audioFile = "audio.wav"
rhasspyUrl = "http://localhost:12101/api/speech-to-text"
ollamaModel = "tinyllama"
buttoncode = 304
mic_device = "plughw:3,0"

speaker = espeakng.ESpeakNG()
speaker.voice = 'en'
speaker.speed = 150
speaker.volume = 100
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

def gamepad_loop():
    global recording, proc
    gamepad = InputDevice('/dev/input/event16')

    for event in gamepad.read_loop():
        if event.type == ecodes.EV_KEY:
            if event.code == buttoncode and event.value == 1:
                if not recording:
                    print('Starting recording...')
                    proc = subprocess.Popen([
                        "arecord", "-D", mic_device, "-f", "cd",
                        "-t", "wav", "-r", "16000", "-d", "10", audioFile
                    ])
                    recording = True
                else:
                    print('Stopping recording...')
                    if proc:
                        proc.send_signal(signal.SIGINT)
                        proc.wait()
                        proc = None
                        time.sleep(0.1)
                    recording = False

                    texto = audiototext()
                    print('Transcription:', texto)
                    if texto:
                        answer = askollama(texto)
                        print("Ollama:", answer)
                        hablar(answer)

if __name__ == "__main__":
    gamepad_loop()
