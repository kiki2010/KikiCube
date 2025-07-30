'''
I made this program on the raspberry but I will add it here so it's easier to get. 
28/07/2025
Chiara Catalini
'''
#Get libraries
from evdev import InputDevice, categorize, ecodes, list_devices
import RPi.GPIO as GPIO

#-- Setting of GPIO --
GPIO.setmode(GPIO.BCM)

led_up = 17
led_down = 27
led_left = 22
led_right = 23

for pin in [led_up, led_down, led_left, led_right]:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, False)

#-- Get Gamepad --
#get devices
devices = [InputDevice(path) for path in list_devices()]

#show device path and name, here we'll get the path for the gamepad.
for device in devices:
    print(device.path, device.name)

#gamepad, change with the correct path
gamepad = InputDevice('/dev/input/event9')
print("everything ready for LED control")

#--- LED control ---

try: 
    for event in gamepad.read_loop():
        #If movement of the joystick is detected
        if event.type == ecodes.EV_ABS:
            # Y axis
            if event.code == ecodes.ABS_Y:
                if event.value < 128:
                    GPIO.output(led_up, True)
                    GPIO.output(led_down, False)
                elif event.value > 128:
                    GPIO.output(led_up, False)
                    GPIO.output(led_down, True)
                else:
                    GPIO.output(led_up, False)
                    GPIO.output(led_down, False)

            # X axis
            if event.code == ecodes.ABS_X:
                if event.value < 128:
                    GPIO.output(led_left, True)
                    GPIO.output(led_right, False)
                elif event.value > 128:
                    GPIO.output(led_left, False)
                    GPIO.output(led_right, True)
                else:
                    GPIO.output(led_left, False)
                    GPIO.output(led_right, False)

except KeyboardInterrupt:
    print("Bye :D")
    GPIO.cleanup