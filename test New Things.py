import customtkinter as ctk
import os
import json
import requests
from pathlib import Path
import time


############
version = "01.00.00"
############


daten = {}
json_load = False
dateipfad = Path(__file__).parent / "data" / "server.json"
script_ordner = Path(__file__).parent
url = 'https://blockhunter0007.github.io/cheathubdumpingground/server.json'
response = requests.get(url)
if response.status_code == 200:
    daten = response.json()  # JSON direkt parsen
    with open(dateipfad, "w", encoding="utf-8") as f:
        json.dump(daten, f, ensure_ascii=False, indent=4)
    json_load = True
else:
    print("Fehler beim Abrufen:", response.status_code)
    json_load = False

#json_string = ''
#daten = json.loads(json_string)
#print(daten["Hund"])   # Hund

if daten["version"] != version:
    print('update')
    print('your version', version, 'is not the newest its', daten["version"])
# Pfad zur server.json im Unterordner "data"
if json_load == False:
# Prüfen, ob die Datei existiert
    if not dateipfad.exists():
        print(f"Datei nicht gefunden: {dateipfad}")
        exit(1)
# JSON-Datei laden
    with open(dateipfad, "r", encoding="utf-8") as f:
        daten = json.load(f)
# Beispielzugriff auf die Daten
    print("Geladene Daten:")
    print(daten)

# Beispiel: einzelne Werte auslesen (falls die Struktur bekannt ist)
# z.B. wenn die JSON so aussieht: {"user": {"name": "Blockhunter", "age": 20}}
# name = daten["user"]["name"]
# alter = daten["user"]["age"]
# print(name, alter)
