'''
This is the first final base of the project, including voice control and Bluetooth.  
15/08/2025
Chiara Catalini
'''
#Get libraries
from evdev import InputDevice, categorize, ecodes, list_devices
import RPi.GPIO as GPIO
import requests
import asyncio
import websockets
import json

'''
GPIO Control Funtions
'''
GPIO.setmode(GPIO.BCM)

mA1 = 17
mA2 = 27
mB1 = 22
mB2 = 23
# Pin mode
for pin in [mA1, mA2, mB1, mB2]:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, False)

# Funtions for directions
def stopped():
    GPIO.output(mA1, False)
    GPIO.output(mA2, False)
    GPIO.output(mB1, False)
    GPIO.output(mB2, False)

def forwards():
    GPIO.output(mA1, True)
    GPIO.output(mA2, False)
    GPIO.output(mB1, True)
    GPIO.output(mB2, False)

def backward():
    GPIO.output(mA1, False)
    GPIO.output(mA2, True)
    GPIO.output(mB1, False)
    GPIO.output(mB2, True)

def left():
    GPIO.output(mA1, False)
    GPIO.output(mA2, False)
    GPIO.output(mB1, True)
    GPIO.output(mB2, False)

def right():
    GPIO.output(mA1, True)
    GPIO.output(mA2, False)
    GPIO.output(mB1, False)
    GPIO.output(mB2, False)

'''
Bluetooth control
'''
#Get devices 
devices = [InputDevice(path) for path in list_devices()]

#show device path and name, here we'll get the path for the gamepad.
for device in devices:
    print(device.path, device.name)

#gamepad, change with the correct path
gamepad = InputDevice('/dev/input/event9')
print("everything ready for LED control")

async def listen_gamepad():
    try:
        for event in gamepad.read_loop():
            if event.type == ecodes.EV_ABS:
                #Stopped
                stopped()
                
                #Forwards and backward
                if event.code == ecodes.ABS_Y:
                    if event.value < 128:
                        forwards()
                    elif event.value > 128:
                        backward()

                if event.code == ecodes.ABS_X:
                    if event.value < 128:
                        left()
                    elif event.value > 128:
                        right()
    except Exception as e:
        print(f"Bluetooth error: {e}")
        GPIO.cleanup()

'''
Voice Control
'''
rhasspy_ws = "ws://localhost:12101/api/events/intent"

async def listen_intent():
    while True:
        try:
            async with websockets.connect(rhasspy_ws) as websocket:
                print("Connecting")
                async for message in websocket:
                    data = json.loads(message)
                    intent_name = data["intent"]["name"]
                    text = data["text"]
                    print(f"intent: {intent_name} | text: {text}")

                    if intent_name == 'Forwards':
                        forwards()
                        print("Going forwards")
                    elif intent_name == 'Backward':
                        backward()
                        print("Going backward")
                    elif intent_name == 'Left':
                        left()
                        print("Going left")
                    elif intent_name == 'Right':
                        right()
                        print("Going right")
                    else:
                        stopped()

        except (websockets.ConnectionClosedError, OSError) as e:
            print(f"Error: {e}")
            await asyncio.sleep(3)


async def main():
    await asyncio.gather(
        listen_gamepad(),
        listen_intent()
    )

if __name__ == "__main__":
    asyncio.run(main())