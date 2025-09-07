''' 
02/09/2025
Chiara Catalini
Motor control and setup
'''
import RPi.GPIO as GPIO

#Pin numbers
m1a = 17
m2a = 27
m1b = 22
m2b = 23

#PWM values
pwm_m1a = None
pwm_m2a = None
pwm_m1b = None
pwm_m2b = None

# GPIO Setup
def setUp():
    global pwm_m1a, pwm_m1b, pwm_m2a, pwm_m2b
    GPIO.setmode(GPIO.BCM)

    for pwm in [pwm_m1b, pwm_m1a, pwm_m2a, pwm_m2b]:
        if pwm is not None:
            pwm.stop() 

    #All outputs
    GPIO.setup(m1a, GPIO.OUT)
    GPIO.setup(m2a, GPIO.OUT)
    GPIO.setup(m1b, GPIO.OUT)
    GPIO.setup(m2b, GPIO.OUT)

    pwm_m1a = GPIO.PWM(m1a, 1000)
    pwm_m2a = GPIO.PWM(m2a, 1000)
    pwm_m1b = GPIO.PWM(m1b, 1000)
    pwm_m2b = GPIO.PWM(m2b, 1000)

    for pwm in [pwm_m1b, pwm_m1a, pwm_m2a, pwm_m2b]:
        pwm.start(0)

# Motor Funtions
def stopped():
    for pwm in [pwm_m1b, pwm_m1a, pwm_m2a, pwm_m2b]:
        pwm.ChangeDutyCycle(0)

def forward(speed=100):
    pwm_m1a = GPIO.PWM(m1a, speed)
    pwm_m2a = GPIO.PWM(m2a, 0)
    pwm_m1b = GPIO.PWM(m1b, speed)
    pwm_m2b = GPIO.PWM(m2b, 0)

def backward(speed=100):
    pwm_m1a = GPIO.PWM(m1a, 0)
    pwm_m2a = GPIO.PWM(m2a, speed)
    pwm_m1b = GPIO.PWM(m1b, 0)
    pwm_m2b = GPIO.PWM(m2b, speed)

def left(speed=100):
    pwm_m1a = GPIO.PWM(m1a, 0)
    pwm_m2a = GPIO.PWM(m2a, 0)
    pwm_m1b = GPIO.PWM(m1b, speed)
    pwm_m2b = GPIO.PWM(m2b, 0)

def right(speed=100):
    pwm_m1a = GPIO.PWM(m1a, speed)
    pwm_m2a = GPIO.PWM(m2a, 0)
    pwm_m1b = GPIO.PWM(m1b, 0)
    pwm_m2b = GPIO.PWM(m2b, 0)