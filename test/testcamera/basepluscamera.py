''' 
02/09/2025
Chiara Catalini
Base using Bluetooth controller, voice control and a camera, because in this way is more cooler
'''
import RPi.GPIO as GPIO

# GPIO Setup
GPIO.setmode(GPIO.BCM)

m1a = 17
m2a = 27
m1b = 22
m2b = 23

GPIO.setup(m1a, GPIO.OUT)
GPIO.setup(m2a, GPIO.OUT)
GPIO.setup(m1b, GPIO.OUT)
GPIO.setup(m2b, GPIO.OUT)

GPIO.output(m1a, False)
GPIO.output(m2a, False)
GPIO.output(m1b, False)
GPIO.output(m2b, False)

# Motor Funtions
def stopped():
    GPIO.output(m1a, False)
    GPIO.output(m2a, False)
    GPIO.output(m1b, False)
    GPIO.output(m2b, False)

def forward():
    GPIO.output(m1a, True)
    GPIO.output(m2a, False)
    GPIO.output(m1b, True)
    GPIO.output(m2b, False)

def backward():
    GPIO.output(m1a, False)
    GPIO.output(m2a, True)
    GPIO.output(m1b, False)
    GPIO.output(m2b, True)

def left():
    GPIO.output(m1a, False)
    GPIO.output(m2a, False)
    GPIO.output(m1b, True)
    GPIO.output(m2b, False)

def right():
    GPIO.output(m1a, True)
    GPIO.output(m2a, False)
    GPIO.output(m1b, False)
    GPIO.output(m2b, False)

# Bluetooth Control
# Voice Control
# Camera