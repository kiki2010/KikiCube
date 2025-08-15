''' 
15/08/2025
Chiara Catalini
'''
import requests

#URL where we send the intents
Rhasspy_URL = "http://localhost:12101/api/text-to-intent"

#The text of the intent
text = 'what time is it'

#Result
response = requests.post(Rhasspy_URL, data=text.encode("utf-8"))

print(response.json())