import customtkinter as ctk
import os
import json
import requests
from pathlib import Path
import time


############
version = "01.00.00"
############



dateipfad = Path(__file__).parent / "data" / "server.json"
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

script_ordner2 = os.path.dirname(os.path.abspath(__file__))
script_ordner = Path(__file__).parent
if script_ordner != script_ordner2:
    print(script_ordner)
    print(script_ordner2)
    time.sleep(20)
else:
    print('pass test folder load')

if daten["version"] != version:
    print('update')
    print('your version', version, 'is not the newest its', daten["version"])
# Pfad zur server.json im Unterordner "data"
if json_load == False:
    offline_start()


def offline_start():
    json_datei = script_ordner / "data" / "server.json"
# Prüfen, ob die Datei existiert
    if not json_datei.exists():
        print(f"Datei nicht gefunden: {json_datei}")
        exit(1)
# JSON-Datei laden
    with open(json_datei, "r", encoding="utf-8") as f:
        daten = json.load(f)

# Beispielzugriff auf die Daten
    print("Geladene Daten:")
    print(daten)

# Beispiel: einzelne Werte auslesen (falls die Struktur bekannt ist)
# z.B. wenn die JSON so aussieht: {"user": {"name": "Blockhunter", "age": 20}}
# name = daten["user"]["name"]
# alter = daten["user"]["age"]
# print(name, alter)
