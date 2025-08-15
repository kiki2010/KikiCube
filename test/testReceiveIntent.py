''' 
15/08/2025
Chiara Catalini
'''
import asyncio
import websockets
import json
from datetime import datetime

rhasspy_ws = "ws://localhost:12101/api/events/intent"

async def listen_intent():
    while True:
        try:
            async with websockets.connect(rhasspy_ws) as websocket:
                print("Connecting")
                async for message in websocket:
                    data = json.loads(message)
                    intent_name = data["intent"]["name"]
                    text = data["text"]
                    print(f"intent: {intent_name} | text: {text}")

                    if intent_name == 'GetName':
                        now = datetime.now().strftime("%H:%M:%S")
                        print(f"The time is {now}")

        except (websockets.ConnectionClosedError, OSError) as e:
            print(f"Error: {e}")
            await asyncio.sleep(3)

asyncio.run(listen_intent())