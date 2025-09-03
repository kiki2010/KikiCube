''' 
02/09/2025
Chiara Catalini
Base using Bluetooth controller, voice control and a camera, because in this way is more cooler
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

GPIO.setup(m1a, GPIO.OUT)
GPIO.setup(m2a, GPIO.OUT)
GPIO.setup(m1b, GPIO.OUT)
GPIO.setup(m2b, GPIO.OUT)

GPIO.output(m1a, False)
GPIO.output(m2a, False)
GPIO.output(m1b, False)
GPIO.output(m2b, False)

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

# Bluetooth Control
CENTER = 128
DEADZONE = 10

def gamepad_loop():
    gamepad = InputDevice('/dev/input/event14')
    x_joystick = CENTER
    y_joystick = CENTER

    for event in gamepad.read_loop():
        if event.type == ecodes.EV_ABS:
            print(f'X: {x_joystick}, Y: {y_joystick}')
            if event.code == ecodes.ABS_Y:
                x_joystick = event.value
            if event.code == ecodes.ABS_X:
                y_joystick = event.value
            
            if y_joystick < CENTER - DEADZONE:
                forward()
            elif y_joystick > CENTER - DEADZONE:
                backward()
            elif x_joystick < CENTER - DEADZONE:
                left()
            elif x_joystick > CENTER - DEADZONE:
                right()
            else:
                stopped()

# Voice Control
rhasspy_ws = 'ws://localhost:12101/api/events/intent'

async def voice_control():
    while True:
        try:
            async with websockets.connect(rhasspy_ws) as websocket:
                async for message in websocket:
                    data = json.loads(message)
                    intent_name = data['intent']['name']
                    text = data['text']

                    if intent_name == 'Forwards':
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

# Camera

# Main
async def main():
    task_gamepad = asyncio.to_thread(gamepad_loop)
    task_voice = voice_control()
    await asyncio.gather(task_gamepad, task_voice)

try:
    asyncio.run(main())
except KeyboardInterrupt:
    GPIO.cleanup()
    print('Kiki Saludos :)')