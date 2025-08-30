''' 
18/08/2025
Chiara Catalini
This is a small test to control GPIO pins using voice commands and a Bluetooth controller.
'''
import RPi.GPIO as GPIO
from evdev import InputDevice, categorize, ecodes, list_devices
import asyncio
import websockets
import json
import time
import requests

# GPIO Setup
GPIO.setmode(GPIO.BCM)

m1a = 17
m2a = 27
m1b = 22
m2b = 23

led1 = 24
led2 = 25

GPIO.setup(m1a, GPIO.OUT)
GPIO.setup(m2a, GPIO.OUT)
GPIO.setup(m1b, GPIO.OUT)
GPIO.setup(m2b, GPIO.OUT)
GPIO.setup(led1, GPIO.OUT)
GPIO.setup(led2, GPIO.OUT)

GPIO.output(m1a, False)
GPIO.output(m2a, False)
GPIO.output(m1b, False)
GPIO.output(m2b, False)
GPIO.output(led1, False)
GPIO.output(led2, False)

# Motor Funtions
def stopped():
    GPIO.output(m1a, False)
    GPIO.output(m2a, False)
    GPIO.output(m1b, False)
    GPIO.output(m2b, False)

def forward():
    GPIO.output(m1a, True)
    GPIO.output(m2a, False)
    GPIO.output(m1b, True)
    GPIO.output(m2b, False)

def backward():
    GPIO.output(m1a, False)
    GPIO.output(m2a, True)
    GPIO.output(m1b, False)
    GPIO.output(m2b, True)

def left():
    GPIO.output(m1a, False)
    GPIO.output(m2a, False)
    GPIO.output(m1b, True)
    GPIO.output(m2b, False)

def right():
    GPIO.output(m1a, True)
    GPIO.output(m2a, False)
    GPIO.output(m1b, False)
    GPIO.output(m2b, False)

def LED1on():
    GPIO.output(led1, True)

def LED1off():
    GPIO.output(led1, False)

def sendWhatTime():
    Rhasspy_URL = "http://localhost:12101/api/text-to-intent"
    text = "what time is it"
    response = requests.post(Rhasspy_URL, data=text.encode("utf-8"))
    print(response.json())


# Bluetooth Control
CENTER = 68
DEADZONE = 5

def gamepad_loop():
    gamepad = InputDevice('/dev/input/event15')
    for event in gamepad.read_loop():
        if event.type == ecodes.EV_ABS:

            if event.code == ecodes.ABS_Y:
                if event.value < CENTER - DEADZONE:
                    forward()
                elif event.value > CENTER + DEADZONE:
                    backward()
                else:
                    stopped()
            
            if event.code == ecodes.ABS_X:
                if event.value < CENTER - DEADZONE:
                    left()
                elif event.value > CENTER + DEADZONE:
                    right()
                else:
                    stopped()

        elif event.type == ecodes.EV_KEY:
            if event.code == 304:
                if event.value == 1:
                    LED1on()
                    sendWhatTime()
                if event.value == 0:
                    LED1off()

# Voice Control

rhasspy_ws = "ws://localhost:12101/api/events/intent"

async def voice_control():
    while True:
        try:
            async with websockets.connect(rhasspy_ws) as websocket:
                async for message in websocket:
                    data = json.loads(message)
                    intent_name = data["intent"]["name"]
                    text = data["text"]

                    if intent_name == 'GetTime':
                        LED1on()
                        time.sleep(2)
                        LED1off()
                    
                    elif intent_name == 'Forwards':
                        forward()
                    
                    elif intent_name == 'Backward':
                        backward()
                    
                    elif intent_name == 'Left':
                        left()
                    
                    elif intent_name == 'Right':
                        right()
                    
                    elif intent_name == 'Stopped':
                        stopped()

        except Exception as e:
            print(e)
            await asyncio.sleep(3)

async def main():
    task_gamepad = asyncio.to_thread(gamepad_loop)
    task_voice = voice_control()
    await asyncio.gather(task_gamepad, task_voice)

try:
    asyncio.run(main())
except KeyboardInterrupt:
    GPIO.cleanup()
    print("Bye :(")
