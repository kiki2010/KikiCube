# **KikiCube**
[![Athena Award Badge](https://img.shields.io/endpoint?url=https%3A%2F%2Faward.athena.hackclub.com%2Fapi%2Fbadge)](https://award.athena.hackclub.com?utm_source=readme)

### **Day 1: 1 hour and one minute**
Today I experimented with the use and resistance of the H-bridge I'll be using in this project.
A1-A, A1-B, B1-A, and B1-B will be connected to the Raspberry Pi.
VCC will be connected to an external power supply.
All GNDs will be connected together.

😱 This testing period was quite short because at some point I connected something wrong and one of the L9110S integrated circuits burned out.

![day1](https://github.com/user-attachments/assets/f08f4463-372f-419a-82ee-f80b087fa47d)

> We will miss you L9110S 🫠

So, I will try to get another this week so I can continue with this part of the project. But I will need to look more information about how to connect with ChatGPT to talk with it :D

## **Day 2: 1 hour**
First 30 minutes:
I experimented with a bluetooth gamepad, connecting it to the Raspberry Pi and making a simple program to read it.

```
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