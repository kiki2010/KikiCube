''' 
02/09/2025
Chiara Catalini
'''
import RPi.GPIO as GPIO
from evdev import InputDevice, categorize, ecodes, list_devices
import asyncio
import threading

from motor import setUp
from bt_control import gamepad_loop
from voice_control import voice_loop
from app import socketio, app

def run_web():
    socketio.run(app, host='0.0.0.0', port=5000)

async def main():
    task_gamepad = asyncio.to_thread(gamepad_loop)
    task_voice = voice_loop()
    await asyncio.gather(task_gamepad, task_voice)

if __name__ == '__main__':
    setUp()
    web_thread = threading.Thread(target=run_web, daemon=True)
    web_thread.start()

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        GPIO.cleanup()
        print('Kiki Saludos :)')