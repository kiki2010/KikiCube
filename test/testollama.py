'''
06/09/2025
Chiara Catalini
In this test I will try to use voice control to ask thinks to an AI by using ollama and rhasspy
'''
import ollama
from evdev import InputDevice, categorize, ecodes, list_devices
import requests
import espeakng
import subprocess

audioFile = "audio.wav"
rhasspyUrl = "http://localhost:12101/api/speech-to-text"
ollamaModel = "tinyllama"
buttoncode = 304

speaker = espeakng.ESpeakNG()
speaker.voice = 'en'
speaker.say("Hi, I am KikiCube press A to ask for help")

def audiototext(filename=audioFile):
    with open(filename, "rb") as f:
        resp = requests.post(rhasspyUrl, files={"file": f})
    return resp.text.strip()

def askollama(prompt):
    response = ollama.chat(
        model=ollamaModel,
        messages=[
            {'role': 'system', 'content': 'Voice asistance, called KikiCube, you are on a raspberry pi 4 and you are a robot controled by using python code, a gamepad and voice control'},
            {'role': 'user', 'content': prompt}
        ]
    )
    return response['message']['content']

def hablar(texto):
    speaker.say(texto)

recording = False
proc = None

def gamepad_loop():
    global recording
    gamepad = InputDevice('/dev/input/event14')

    for event in gamepad.read_loop():
        if event.type == ecodes.EV_KEY:
            if event.code == buttoncode and event.value == 1:
                if not recording:
                    print('started recording')
                    proc = subprocess.Popen([
                        "arecord", "-D", "plughw:3,0", "-f", "cd",
                        "-t", "wav", "-r", "16000", audioFile
                    ])
                    recording = True
                else:
                    print('stopping recording')
                    if proc:
                        proc.terminate()
                        proc.wait()
                    recording = False

                    texto = audiototext()
                    print('text', texto)
                    if texto:
                        answer = askollama(texto)
                        print("ollama", answer)
                        hablar(answer)

if __name__ == "__main__":
    gamepad_loop()