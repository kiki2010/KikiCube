''' 
02/09/2025
Chiara Catalini
Bluetooth control of the motors
'''
from evdev import InputDevice, categorize, ecodes, list_devices
from motor import forward, backward, left, right, stopped
import aiquestions
import threading

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
                print('moving Foward')
                forward()
            elif y_joystick > CENTER + DEADZONE:
                print('moving Backward')
                backward()
            elif x_joystick < CENTER - DEADZONE:
                print('moving Left')
                left()
            elif x_joystick > CENTER + DEADZONE:
                print('moving Right')
                right()
            else:
                stopped()
        elif event.type == ecodes.EV_KEY:
            if event.code == 304:
                if event.value == 1:
                    print('Recording thread')
                    threading.Thread(target=aiquestions.handleRecording).start()            