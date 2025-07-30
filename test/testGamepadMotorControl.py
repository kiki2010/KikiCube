''' 
30/07/2025
Chiara Catalini
'''
#Get libraries
from evdev import InputDevice, categorize, ecodes, list_devices
import RPi.GPIO as GPIO

#-- Setting of GPIO --
GPIO.setmode(GPIO.BCM)

mA1 = 17
mA2 = 27
mB1 = 22
mB2 = 23

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

#-- Get Gamepad --
#get devices
devices = [InputDevice(path) for path in list_devices()]

#show device path and name, here we'll get the path for the gamepad.
for device in devices:
    print(device.path, device.name)

#gamepad, change with the correct path
gamepad = InputDevice('/dev/input/event9')
print("everything ready for LED control")

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


except KeyboardInterrupt:
    print("Bye :D")
    GPIO.cleanup