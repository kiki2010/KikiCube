# **KikiCube**
## **Total time: 16 hours 50 minutes**

[![Athena Award Badge](https://img.shields.io/endpoint?url=https%3A%2F%2Faward.athena.hackclub.com%2Fapi%2Fbadge)](https://award.athena.hackclub.com?utm_source=readme)


Time per day:

| Day | Sections | Hours |
|-----|----------|-------|
| [1](#day-1-1-hour-and-one-minute)  | 1 | 1 hour and 1 minute |
| [2](#day-2-1-hour)                  | 2 | 1 hour |
| [3](#day-3-1-hour-48-minutes)      | 2 | 1 hour 48 minutes |
| [4](#day-4-1-hour-1-minute)        | 1 | 1 hour 1 minute |
| [5](#day-5-1-hour-19-minutes)      | 1 | 1 hour 19 minutes |
| [6](#day-6-2-hours)                | 2 | 2 hours |
| [7](#day-7-1-hour-32-minutes)      | 2 | 1 hour 32 minutes |
| [8](#day-8-changes)                | - | Not timed. But a summary and clarification is given |
| [9](#day-9-3-hours-24-minutes)     | 3 | 3 hours 24 minutes |
| [10](#day-10-4-hours-and-45-minutes) | 5 | 4 hours and 45 minutes |

----------------------------------

Final Time:

| Activity       | Days                  | minutes | hours            |
|----------------|----------------------|---------|-----------------|
| Test and SetUp | Days 1, 2, 3, 4, 5, 6, 7, 8 | 581     | 9 hours 41 minutes |
| Assembly       | Days 8, 9, 10        | 489     | 8 hours 9 minutes  |

----------------------------------

## **Day 1: 1 hour and one minute**
Today I experimented with the use and resistance of the H-bridge I'll be using in this project.

A1-A, A1-B, B1-A, and B1-B will be connected to the Raspberry Pi.

VCC will be connected to an external power supply.

All GNDs will be connected together.

😱 This testing period was quite short because at some point I connected something wrong and one of the L9110S integrated circuits burned out.

![day1](https://github.com/user-attachments/assets/f08f4463-372f-419a-82ee-f80b087fa47d)

> We will miss you L9110S 🫠

So, I will try to get another this week so I can continue with this part of the project. But I will need to look more information for this project.

----------------------------------

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

----------------------------------

## **Day 3: 1 hour 48 minutes**
### 48 minutes:
Configuration and testing of speakers and microphone. I use the webcam microphone.

![webcam](https://github.com/user-attachments/assets/4d232832-a4ed-453e-83af-b5eeac80d7e1)

### 1 Hour:
Installing and configuring Rhasspy, I haven't tested it yet.

----------------------------------

## **Day 4: 1 hour 1 minute**
I tried testing with a simple Rhasspy test but didn't make any progress :C
I'll continue testing this.

![day 4](https://github.com/user-attachments/assets/f9d3503d-44aa-4064-ace7-95daece816ed)

----------------------------------

## **Day 5: 1 hour 19 minutes**
Test with gamepad and Leds. The X and Y axes of the gamepad joystick are read. In order to reflect the reading on the LEDs.

![kikicubetestled](https://github.com/user-attachments/assets/f4a8b12f-4238-4185-b857-fa6a34ef3d9a)

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
```

<img width="694" height="582" alt="Captura de pantalla 2025-07-28 202012" src="https://github.com/user-attachments/assets/a7596090-8bd6-4c17-b011-41b5d890dc2e" />

----------------------------------

## **Day 6: 2 hours**

### 23 minutes:
Simulate the control of the motors with the LED lights, truly recreating what it would be like if the H bridge were connected instead of the LEDs. The idea is to continue working with voice control.

![kikicubeledacurate](https://github.com/user-attachments/assets/f9669ec0-ef21-4d02-91d4-dfd286c14f57)


```python
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
```

<img width="692" height="626" alt="Captura de pantalla 2025-07-30 193009" src="https://github.com/user-attachments/assets/2bf314b6-8579-4497-8594-baf35d92f329" />

### 1 hour 44 minutes
The truth is that, since this is my first Raspberry Pi project, it's a bit ambitious. After successfully controlling the LEDs with the remote, I wanted to go a step further and start using Rhasspy for voice control. However, installing everything got messy, and now every time I try to launch Rhasspy, I get an error. So, I'll continue tomorrow. But after the fastest hour and forty minutes of my life, I think the most viable solution is to restore my Raspberry Pi and start configuring Rhasspy from scratch.

<img width="676" height="617" alt="Captura de pantalla 2025-07-30 212916" src="https://github.com/user-attachments/assets/2190ceff-7b60-4a6b-9fa9-f770636e5949" />

----------------------------------

## **Day 7: 1 hour 32 minutes**
### 40 minutes:
I formatted the SD and reinstalled Raspberry Pi OS, I was also able to do the initial setup of Rhasspy, installing everything necessary and testing the microphone.

![Video de WhatsApp 2025-08-06 a las 22 40 37_e3f8d59b](https://github.com/user-attachments/assets/db99d565-805b-4a4b-a2b9-14a0e94742f1)
![Video de WhatsApp 2025-08-06 a las 22 40 49_8702dec3](https://github.com/user-attachments/assets/cebe0093-665d-4adf-abb4-446c60c68cbd)

### 52 minutes:
I set up Rhasspy. After a lot of trouble with the setup, I managed to get it to recognize recorded audio. The only thing left to do is get it to work with live audio, as it fails to analyze.

<img width="500" src="https://github.com/user-attachments/assets/e120ee2d-2224-471b-8714-19b09b170a90" />

![Video de WhatsApp 2025-08-06 a las 22 41 52_cf10b836](https://github.com/user-attachments/assets/e81e48fa-2164-4f71-b81e-a9265b1755ca)

<img width="500" src="https://github.com/user-attachments/assets/27ecd006-3b5c-4bc8-932b-f5be05b03387" />

----------------------------------

## **Day 8: Changes**
Even though I was working for several more days, I decided not to time it, so I would just notify you when I made progress.
First, I solved the problem that kept me from accessing the web interface. The problem was that that port was already in use, which is why it wouldn't let me in.
On the other hand, I spent several days trying to read intents using internal MQTT, but after reading a little more, I realized that for what I wanted to achieve, using HTTP and WebSocket is a much simpler connection and serves what I wanted to achieve without the need for a very complex configuration.

Today I managed to send an intent from the terminal and react to it. When asked what time it is, the program returns the current time. These are the two programs.
So today I hope to continue putting everything together to make it work. 😀

----------------------------------

## **Day 9: 3 hours 24 minutes**
I sent a 3D model for the base of my robot to be printed. As it is inspired by a cubesat, I looked for a free-to-use model on Thingverse. This is the link: 

<a href="https://www.thingiverse.com/thing:4096437#Summary">Universal 1U Cubesat by Juliano85</a>
<img width="500" src="https://github.com/user-attachments/assets/ed8dcbdd-16c2-47c5-9c22-3df4bbc2249e" />

### First 1 hour 40 minutes
I looked through my materials for everything I needed to assemble it. I looked for the best screws, nuts, and acrylic robot bases.
So I spent this first hour and forty minutes looking for everything I needed and preparing everything to build the base.

<img width="500" src="https://github.com/user-attachments/assets/0a9bed40-c861-4f34-ab58-964bed2f7224" />

### 53 minutes later
I put the motors in position and assembled the structure of the 3D print. In the image, it is presented on the acrylic base that I will adapt to make it more stable.

<img width="500" src="https://github.com/user-attachments/assets/552493b2-91ce-4286-9c0f-5a109636fa08" />
<img width="500" src="https://github.com/user-attachments/assets/dad0f719-d2f1-408c-abd5-91da729d9c5f" />
<img width="500" src="https://github.com/user-attachments/assets/dc153fb7-6cf2-4aec-aa5f-5ff66d257108" />

### 51 minutes later
I joined the 3D printed base with the acrylic, leaving a space to pass the battery that will be used to power the motors, I also cut the acrylic to the correct size.

<img width="500" src="https://github.com/user-attachments/assets/9c75c3eb-bddb-418b-bded-88fd5e9c516c" />

> [!NOTE]
> Time really flew by doing this 😭
> I couldn't believe it was already dark 🌙

----------------------------------

## **Day 10: 4 hours and 45 minutes**
Today I managed to finish the base, and finally test the engine control.

### 1 hour:
Connection diagram ready 😀😃
I found the necessary materials and attached the H bridge to the motor base 🤖

<img width="500" src="https://github.com/user-attachments/assets/5d1e90ed-18a2-4d4d-b98c-ad6e22e01bad" />
<img width="500" src="https://github.com/user-attachments/assets/d7dc3cb0-66d7-4788-9179-e601f5573139" />
<img height="500" src="https://github.com/user-attachments/assets/5b8ff51e-0f10-4098-b78d-a2608685d68c" />
<img height="500" src="https://github.com/user-attachments/assets/ebdeb779-e391-40d6-819e-b1e8d12d5d5f" />

> Photos taken at 4 p.m. on 08/30

### 1 hour:
Adapt female connectors for the robot.
Especially for recycling components and make it completely custom 😎.

<img width="500" src="https://github.com/user-attachments/assets/74f8e89e-364f-4ab7-85f7-9263ea8c9c7c" />

> Photo taken at 5 p.m on 08/30

> [!NOTE]
> I always try to add recycled components in my projects ♻️
> Obviously, I adapt them 😎

### 1 hour:
Finished cable adapted for H-bridge inputs, cables soldered to the motors.

<img width="500" src="https://github.com/user-attachments/assets/9c06baa7-b14b-4442-b1c7-79ad02f9be03" />

> Photo taken at 6:43 p.m on 08/30

### 1 hour: 
Added a button and adapted connectors for the battery (7.3V, also recycled and adapted from an old laptop). All that's left is to put everything together and test it.

<img width="500" src="https://github.com/user-attachments/assets/27d81c6c-65d3-428e-8e96-507eabe71d86" />
<img width="500" src="https://github.com/user-attachments/assets/e4bf36f3-c850-45dd-9585-ccdb4ef75592" />
<img height="500" src="https://github.com/user-attachments/assets/51aedf72-a71b-42e9-8aaa-f1ca5f611d85" />

> Photo taken at 7:45 p.m on 08/30

### 45 minutes:
Everything's assembled and tested. I'll continue working on the code.

![test, video listo](https://github.com/user-attachments/assets/fccf28da-cf9d-4224-b245-9e7a96fae811)
> Video recorded at 9:38 p.m on 08/30

----------------------------------