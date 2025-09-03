''' 
02/09/2025
Chiara Catalini
Voice control using Rhasspy
'''
import asyncio
import websockets
import json
from motor import forward, backward, left, right, stopped

rhasspy_ws = 'ws://localhost:12101/api/events/intent'

async def voice_loop():
    while True:
        try:
            async with websockets.connect(rhasspy_ws) as websocket:
                async for message in websocket:
                    data = json.loads(message)
                    intent_name = data['intent']['name']
                    text = data['text']

                    if intent_name == 'Forwards':
                        forward()
                    
                    elif intent_name == 'Backward':
                        backward()
                    
                    elif intent_name == 'Left':
                        left()
                    
                    elif intent_name == 'Right':
                        right()
                    
                    elif intent_name == 'Stopped':
                        stopped()

        except Exception as e:
            print(e)
            await asyncio.sleep(3)