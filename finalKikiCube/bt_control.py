''' 
02/09/2025
Chiara Catalini
Bluetooth control of the motors
'''
from evdev import InputDevice, categorize, ecodes, list_devices
from motor import forward, backward, left, right, stopped

#Center and deadzone
CENTER = 128
DEADZONE = 10

def gamepad_loop():
    gamepad = InputDevice('/dev/input/event14')
    x_joystick = CENTER
    y_joystick = CENTER

    #When a event is detected, see which kind of event and move acordding to the value detected.
    for event in gamepad.read_loop():
        if event.type == ecodes.EV_ABS:
            print(f'X: {x_joystick}, Y: {y_joystick}')
            if event.code == ecodes.ABS_Y:
                y_joystick = event.value
            if event.code == ecodes.ABS_X:
                x_joystick = event.value
            
            if y_joystick < CENTER - DEADZONE:
                forward()
            elif y_joystick > CENTER + DEADZONE:
                backward()
            elif x_joystick < CENTER - DEADZONE:
                left()
            elif x_joystick > CENTER + DEADZONE:
                right()
            else:
                stopped()