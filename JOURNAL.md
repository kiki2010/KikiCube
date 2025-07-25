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

![gamepad](https://github.com/user-attachments/assets/5ffcbdce-be8c-471e-854d-47fa9d50a15d)

### The other 30 minutes:
Looking for the perfect screen, I thought it would be a good idea to find a small screen so I could more easily modify programs on the Raspberry Pi, so I took apart a tablet, although since it's a generic one, I couldn't find an adapter for it. Anyway, I'll try to fix another one later to connect it to the Raspberry Pi conventionally.

![tablet1](https://github.com/user-attachments/assets/0b0efcd2-7b9e-44ba-b572-d1cdf62fbc63)
![tablet2](https://github.com/user-attachments/assets/25714fb3-5f95-4dbc-9a62-56b0b20eb257)