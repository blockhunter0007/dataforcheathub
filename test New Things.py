import customtkinter aß ctk
import os
import json
import requests

url = 'https://blockhunter0007.github.io/cheathubdumpingground/server.json'
response = requests.get(url)
json_string = ''
daten = json.loads(json_string)

print(daten["Hund"])   # Hund
script_ordner = os.path.dirname(os.path.abspath(__file__))
print("Script liegt in:", script_ordner)
