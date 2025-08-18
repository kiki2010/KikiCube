''' 
17/08/2025
Chiara Catalini
This is a small test to control GPIO pins using voice commands and a Bluetooth controller.
'''

import RPi.GPIO as GPIO
from evdev import InputDevice, categorize, ecodes, list_devices
import asyncio
import websockets
import json
from datetime import datetime
import time

# - Control pins via Bluetooth -

GPIO.setmode(GPIO.BCM)

LED = 24

GPIO.setup(LED, GPIO.OUT)
GPIO.output(LED, False)

# - LED on and off functions -
def LEDon():
    GPIO.output(LED, True)

def LEDoff():
    GPIO.output


# - If button A is touched, the LED will turn on -
def gamepad_loop():
    gamepad = InputDevice('/dev/input/event15')
    for event in gamepad.read_loop():
        if event.type == ecodes.EV_KEY:
            if event.code == 304:
                if event.value == 1:
                    LEDon()
                elif event.value == 0:
                    LEDoff()


# - Control pins by Rhasspy (voice control) -

rhasspy_ws = "ws://localhost:12101/api/events/intent"

# - When the GetTime intent is detected, the LED will turn on for 2 seconds and then turn off. -
async def voice_control():
    while True:
        try:
            async with websockets.connect(rhasspy_ws) as websocket:
                async for message in websocket:
                    data = json.loads(message)
                    intent_name = data["intent"]["name"]
                    text = data["text"]

                    if intent_name == 'GetTime':
                        LEDon()
                        time.sleep(2)
                        LEDoff()

        except Exception as e:
            print(e)
            await asyncio.sleep(3)

# - Run the two loops in parallel - 
async def main():
    task_gamepad = asyncio.to_thread(gamepad_loop)
    task_voice = voice_control()
    await asyncio.gather(task_gamepad, task_voice)

# Run the entire program
try:
    asyncio.run(main())
except KeyboardInterrupt:
    GPIO.cleanup()
    print("KIKI SALUDOS :)")

''' 
Kiki Saludos :D
'''