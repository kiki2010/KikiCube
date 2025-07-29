'''
I made this program on the raspberry but I will add it here so it's easier to get. 
16/07/2025
Chiara Catalini
'''
#Get libraries
from evdev import InputDevice, categorize, ecodes, list_devices

#get devices
devices = [InputDevice(path) for path in list_devices()]

#show device path and name, here we'll get the path for the gamepad.
for device in devices:
    print(device.path, device.name)

#gamepad, change with the correct path
gamepad = InputDevice('/dev/input/event9')

#Show what it reads.
for event in gamepad.read_loop():
    if event.type in [ecodes.EV_KEY, ecodes.EV_ABS]:
        print(categorize(event))