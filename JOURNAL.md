# **KikiCube**
[![Athena Award Badge](https://img.shields.io/endpoint?url=https%3A%2F%2Faward.athena.hackclub.com%2Fapi%2Fbadge)](https://award.athena.hackclub.com?utm_source=readme)

## **Day 1: 1 hour and one minute**
Today I experimented with the use and resistance of the H-bridge I'll be using in this project.

A1-A, A1-B, B1-A, and B1-B will be connected to the Raspberry Pi.

VCC will be connected to an external power supply.

All GNDs will be connected together.

😱 This testing period was quite short because at some point I connected something wrong and one of the L9110S integrated circuits burned out.

![day1](https://github.com/user-attachments/assets/f08f4463-372f-419a-82ee-f80b087fa47d)

> We will miss you L9110S 🫠

So, I will try to get another this week so I can continue with this part of the project. But I will need to look more information for this project.

## **Day 2: 1 hour**
### First 30 minutes:
I experimented with a bluetooth gamepad, connecting it to the Raspberry Pi and making a simple program to read it.

```python
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
```

![gamepad](https://github.com/user-attachments/assets/5ffcbdce-be8c-471e-854d-47fa9d50a15d)

### The other 30 minutes:
Looking for the perfect screen, I thought it would be a good idea to find a small screen so I could more easily modify programs on the Raspberry Pi, so I took apart a tablet, although since it's a generic one, I couldn't find an adapter for it. Anyway, I'll try to fix another one later to connect it to the Raspberry Pi conventionally.

![tablet1](https://github.com/user-attachments/assets/0b0efcd2-7b9e-44ba-b572-d1cdf62fbc63)
![tablet2](https://github.com/user-attachments/assets/25714fb3-5f95-4dbc-9a62-56b0b20eb257)

## **Day 3: 1 hour 48 minutes**
### 48 minutes:
Configuration and testing of speakers and microphone. I use the webcam microphone.

![webcam](https://github.com/user-attachments/assets/4d232832-a4ed-453e-83af-b5eeac80d7e1)

### 1 Hour:
Installing and configuring Rhasspy, I haven't tested it yet.

## **Day 4: 1 hour 1 minute**
I tried testing with a simple Rhasspy test but didn't make any progress :C
I'll continue testing this.

![day 4](https://github.com/user-attachments/assets/f9d3503d-44aa-4064-ace7-95daece816ed)

## **Day 5: 1 hour 19 minutes**
Test with gamepad and Leds. The X and Y axes of the gamepad joystick are read. In order to reflect the reading on the LEDs.
![Adobe Express - kikicubetestled (1)](https://github.com/user-attachments/assets/dacff2fb-9c89-4fba-a1da-95bab9f771b0)

This is the program, you can also find it as testgamepadLed.py in test folder.
```python
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
                if event.values < 128:
                    GPIO.output(led_up, True)
                    GPIO.output(led_down, False)
                elif event.values > 128:
                    GPIO.output(led_up, False)
                    GPIO.output(led_down, True)
                else:
                    GPIO.output(led_up, False)
                    GPIO.output(led_down, False)

            # X axis
            if event.code == ecodes.ABS_X:
                if event.values < 128:
                    GPIO.output(led_left, True)
                    GPIO.output(led_right, False)
                elif event.values > 128:
                    GPIO.output(led_left, False)
                    GPIO.output(led_right, True)
                else:
                    GPIO.output(led_left, False)
                    GPIO.output(led_right, False)

except KeyboardInterrupt:
    print("Bye :D")
    GPIO.cleanup
```

<img width="694" height="582" alt="Captura de pantalla 2025-07-28 202012" src="https://github.com/user-attachments/assets/a7596090-8bd6-4c17-b011-41b5d890dc2e" />
