import customtkinter as ctk
from customtkinter import CTkImage
import os
import json
import requests
from pathlib import Path
import time
import webbrowser
from PIL import Image, ImageTk
import keyring
import subprocess
import sys
import shutil


####################################################
version = "01.00.00"
####################################################
downloadjsonpath = Path(__file__).parent / "downloads" / "downloads.json"
if not downloadjsonpath.exists():
    with open(downloadjsonpath, "w", encoding="utf-8") as f:
        json.dump({}, f, ensure_ascii=False, indent=4)
downloadsfolder = Path(__file__).parent / "downloads"
login_infos = 0
assets_path = Path(__file__).parent / "assets"
bilder = [
    assets_path / "ad1.png",
    assets_path / "ad2.png",
    assets_path / "ad3.png"
]
downloadjson = {}
links = [
    "https://pinguinbrowser-660h.onrender.com",
    "https://pinguinbrowser-660h.onrender.com",
    "https://pinguinbrowser-660h.onrender.com"
]
aktuell = 0
response = None
daten = {}
json_load = False
dateipfad = Path(__file__).parent / "data" / "server.json"
script_ordner = Path(__file__).parent
url = 'https://blockhunter0007.github.io/cheathubdumpingground/server.json'
root = ctk.CTk()
root.title("Cheats")
root.geometry("600x400")
ctk.set_appearance_mode("dark")  # Dunkelmodus
ctk.set_default_color_theme("blue")  # Blaue Akzentfarbe
ads_visible = True  # True = Ads werden angezeigt, False = Ads werden ausgeblendet
current_exe = os.path.basename(sys.argv[0])  # Name der aktuell laufenden Datei
download_update_url = "https://example.com/deinprogramm.exe"


def update_button_click(download_update_url, old_exe):
    new_exe = "update.exe"
    response = requests.get(download_update_url, stream=True)
    with open(new_exe, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    print(f"Neue Datei {new_exe} wurde heruntergeladen.")

    updater_code = f"""
import os, time, shutil, subprocess

time.sleep(5)  # Warte, damit die alte Datei geschlossen ist

old_exe = r"{old_exe}"
new_exe = r"{new_exe}"

try:
    os.remove(old_exe)
except PermissionError:
    time.sleep(1)
    os.remove(old_exe)

shutil.move(new_exe, old_exe)
subprocess.Popen([old_exe], shell=True)
"""
    updater_file = "run_updater.py"
    with open(updater_file, "w", encoding="utf-8") as f:
        f.write(updater_code)

    subprocess.Popen([sys.executable, updater_file])
    sys.exit(0)


def update_message():
    update_window = ctk.CTkToplevel(root)
    update_window.title("Update verfügbar")
    update_window.geometry("400x200")
    update_window.grab_set()

    label = ctk.CTkLabel(update_window, text="Ein Update ist verfügbar!\nBitte lade die neueste Version herunter.")
    label.pack(pady=20, padx=20)

    download_button = ctk.CTkButton(
        update_window,
        text="Update jetzt installieren",
        command=lambda: update_button_click(download_update_url, current_exe)  # HIER richtig mit Parametern
    )
    download_button.pack(pady=10)

    close_button = ctk.CTkButton(
        update_window,
        text="Später",
        command=update_window.destroy
    )
    close_button.pack(pady=10)



def check_saved_login():
    saved_username = keyring.get_password("CheatAppUsername", "username")
    if saved_username:
        saved_password = keyring.get_password("CheatAppPassword", saved_username)
        if saved_password:
            # Automatischer Login
            print("Gefundene gespeicherte Login-Daten. Versuche automatischen Login...")
            login_with_credentials(saved_username, saved_password)

try:
    response = requests.get(url)
    print("HTTP Status:", response.status_code)
    print("Rohdaten (erste 500 Zeichen):", response.text[:1000])
    if response.status_code == 200:
        daten = response.json()  # JSON direkt parsen
        with open(dateipfad, "w", encoding="utf-8") as f:
            json.dump(daten, f, ensure_ascii=False, indent=4)
        json_load = True
    else:
        print("Fehler beim Abrufen:", response.status_code)
        json_load = False
        print(response)
except requests.exceptions.RequestException as e:
    print("Fehler beim Abrufen der URL:", e)
    json_load = False

#json_string = ''
#daten = json.loads(json_string)
#print(daten["Hund"])   # Hund

# Pfad zur server.json im Unterordner "data"
if json_load == False:
# Prüfen, ob die Datei existiert
    if not dateipfad.exists():
        print(f"Datei nicht gefunden: {dateipfad}")
        exit(1)
# JSON-Datei laden
    try:
        with open(dateipfad, "r", encoding="utf-8") as f:
            daten = json.load(f)
# Beispielzugriff auf die Daten
        print("Geladene Daten:")
        print(daten)
    except json.JSONDecodeError:
        print('failed finding jsnversion (initialisationcheck) please turn on your wifi to install our programm')
        print('we only need wifi to see what cheats we have and download them.')
        print('after turning on the wifi once you can use our product completly offline')
        time.sleep(10)
        exit(1)

if "version" in daten:
    if daten["version"] != version:
        update_message()
        print('update')
        print('your version', version, 'is not the newest its', daten["version"])
else:
    print('failed finding jsnversion (initialisationcheck) please turn on your wifi to install our programm')
    print('we only need wifi to see what cheats we have and download them.')
    print('after turning on the wifi once you can use our product completly offline')
    time.sleep(10)
    exit(1)

#################################
#              CTK              #
#################################

button_frame = ctk.CTkFrame(root)
button_frame.pack(padx=20, pady=20, fill="both", expand=True)
def button_click_start(name):
    print(f"Button {name} wurde geklickt! und gestartet")

def button_click_uninstall(name):
    if downloadjsonpath.exists():
        with open(downloadjsonpath, "r", encoding="utf-8") as f:
            data = json.load(f)

        if name in data:
            del data[name]

        with open(downloadjsonpath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    # UI nur für dieses Produkt aktualisieren
    btns = product_buttons[name]

    # Starten-Button zurück zu Download
    btns["start"].configure(text="Download", command=lambda n=name: button_click(n))

    # Deinstallieren-Button entfernen
    if btns.get("uninstall"):
        btns["uninstall"].destroy()
        btns["uninstall"] = None


# Funktion, die beim Klick ausgeführt wird
def button_click(name):
    # JSON aktualisieren
    if downloadjsonpath.exists():
        with open(downloadjsonpath, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {}

    data[name] = daten["products"][name]

    with open(downloadjsonpath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    # UI aktualisieren nur für dieses Produkt
    btns = product_buttons[name]

    # Download-Button zu Starten ändern
    btns["start"].configure(text="Starten", command=lambda n=name: button_click_start(n))

    # Deinstallieren-Button erstellen, falls noch nicht vorhanden
    if not btns.get("uninstall"):
        i = list(daten["products"]).index(name)
        uninstall_btn = ctk.CTkButton(button_frame, text="Deinstallieren", fg_color="red", hover_color="#ff4d4d",
                                      command=lambda n=name: button_click_uninstall(n))
        uninstall_btn.grid(row=i, column=2, padx=10, pady=5, sticky="ew")
        btns["uninstall"] = uninstall_btn

def open_login_window():
    global login_infos
    # 1. Neues Toplevel-Fenster erstellen
    login_window = ctk.CTkToplevel(root)
    login_window.title("Benutzer-Anmeldung")
    login_window.geometry("350x300")  # etwas mehr Platz für Fehlermeldung
    
    # Sorgt dafür, dass das Login-Fenster im Vordergrund bleibt
    login_window.grab_set()

    # 2. Widgets für das Login-Fenster erstellen
    
    # Benutzername Label und Eingabefeld
    username_label = ctk.CTkLabel(login_window, text="Benutzername")
    username_label.pack(pady=(20, 5), padx=30)

    username_entry = ctk.CTkEntry(login_window, width=200, placeholder_text="Benutzername eingeben")
    username_entry.pack(pady=5, padx=30)

    # Passwort Label und Eingabefeld
    password_label = ctk.CTkLabel(login_window, text="Passwort")
    password_label.pack(pady=(10, 5), padx=30)

    password_entry = ctk.CTkEntry(login_window, width=200, placeholder_text="Passwort eingeben", show="*")
    password_entry.pack(pady=5, padx=30)

    # Platz für Fehlermeldungen (initial leer, wird bei Fehler sichtbar gemacht)
    # Wir speichern das Label als Attribut des Fensters, damit login_api_call es updaten kann
    login_window.error_label = ctk.CTkLabel(login_window, text="", text_color="red")
    login_window.error_label.pack(pady=(5, 5), padx=30)

    # Anmelden-Button
    login_button = ctk.CTkButton(
        login_window,
        text="Anmelden",
        command=lambda: login_api_call(username_entry, password_entry, login_window)
    )
    login_button.pack(pady=10, padx=30)


def login_with_credentials(username, password):
    url = f"https://pinguinbrowser.pythonanywhere.com/accountapi/{username}/{password}"
    try:
        response = requests.get(url)
        result = response.json()
        if result.get("success"):
            # Benutzer automatisch anmelden
            anmelden_button.configure(text=username, command=lambda: show_logout_popup(username))
            if result.get("is_pro"):
                info_label.configure(text="(Pro)")
            else:
                info_label.configure(text="Pro kaufen")
            global ads_visible
            ads_visible = not result.get("is_pro")
        else:
            print("Gespeicherte Daten ungültig.")
    except:
        print("Fehler beim automatischen Login")


def login_api_call(username_entry, password_entry, login_window):
    global ads_visible
    global login_infos
    username = username_entry.get()
    password = password_entry.get()
    print(f"Anmelden mit Benutzername: {username} und Passwort: {password}")
    url = f"https://pinguinbrowser.pythonanywhere.com/accountapi/{username}/{password}"
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        # Netzwerkfehler → Meldung anzeigen
        msg = f"Netzwerkfehler: {e}"
        print(msg)
        login_window.error_label.configure(text=msg)
        return

    # Wenn wir hier sind, haben wir eine HTTP-Antwort
    if response.status_code == 200:
        try:
            result = response.json()
        except ValueError:
            login_window.error_label.configure(text="Ungültige Server-Antwort.")
            return

        if result.get('success') == True:
            print("Erfolgreich angemeldet!")
            keyring.set_password("CheatAppUsername", "username", username)
            keyring.set_password("CheatAppPassword", username, password)
            # Login-Fenster schließen
            login_window.destroy()

            # Button in Label mit Benutzernamen ändern
            anmelden_button.configure(text=username, command=lambda: show_logout_popup(username))

            # PRO-Status prüfen
            if result.get("is_pro") == True:
                info_label.configure(text=f"(Pro)")
                ads_visible = False
                bild_label.configure(image=None, text="")
                bild_label.update_idletasks()

                # Ads sofort ausblenden (UI aktualisieren)
                bild_label.configure(image=None, text="")
                bild_label.update_idletasks()
            else:
                info_label.configure(text="Pro kaufen")
                info_label.bind("<Button-1>", open_pro_website)
                ads_visible = True

            print("is pro:", result.get("is_pro"))

        elif result.get("success") == False:
            # Anmeldedaten falsch — Meldung im Login-Fenster anzeigen
            msg = result.get("message", "Anmeldung fehlgeschlagen. Benutzername/Passwort falsch.")
            print("Anmeldung fehlgeschlagen:", msg)
            login_window.error_label.configure(text=msg)
        else:
            # Unerwartete Antwortstruktur
            msg = "Unerwartete Server-Antwort."
            print(msg, result)
            login_window.error_label.configure(text=msg)
    elif response.status_code == 401:
        # HTTP 401 = Unauthorized (falsche Anmeldedaten)
        msg = "Ungültiger Benutzername oder Passwort."
        print(msg)
        login_window.error_label.configure(text=msg)
    else:
        # andere HTTP-Fehlercodes anzeigen
        msg = f"Fehler beim Abrufen: {response.status_code}"
        print(msg)
        login_infos = response.status_code
        login_window.error_label.configure(text=msg)


def show_logout_popup(username):
    logout_window = ctk.CTkToplevel(root)
    logout_window.title("Abmelden")
    logout_window.geometry("300x150")
    logout_window.grab_set()  # sorgt dafür, dass das Fenster im Vordergrund bleibt

    label = ctk.CTkLabel(logout_window, text=f"Angemeldet als {username}")
    label.pack(pady=20)

    logout_button = ctk.CTkButton(
        logout_window,
        text="Abmelden",
        fg_color="red",  # rote Farbe
        hover_color="#ff4d4d",
        command=lambda: logout(logout_window)
    )
    logout_button.pack(pady=10)

def open_pro_website(event=None):
    webbrowser.open("https://pinguinbrowser.pythonanywhere.com/")

def logout(logout_window):
    global ads_visible
    global anmelden_button
    # Popup schließen
    logout_window.destroy()
    # Button wieder auf "Anmelden" setzen
    anmelden_button.configure(text="Anmelden", command=open_login_window)
    info_label.configure(text="Anmelden")
    info_label.unbind("<Button-1>")
    ads_visible = True

    # Gespeicherte Login-Daten löschen
    saved_username = keyring.get_password("CheatAppUsername", "username")
    if saved_username:
        keyring.delete_password("CheatAppUsername", "username")
        keyring.delete_password("CheatAppPassword", saved_username)


def click_cheat_lable(product):
    def inner(event):
        # Neues Fenster erstellen
        info_window = ctk.CTkToplevel(root)
        info_window.title(product["name"])
        info_window.geometry("400x300")
        info_window.grab_set()

        # Produktinfos anzeigen
        name_label = ctk.CTkLabel(info_window, text=f"Name: {product['name']}")
        name_label.pack(pady=5, padx=10, anchor="w")

        id_label = ctk.CTkLabel(info_window, text=f"ID: {product['id']}")
        id_label.pack(pady=5, padx=10, anchor="w")

        version_label = ctk.CTkLabel(info_window, text=f"Version: {product['version']}")
        version_label.pack(pady=5, padx=10, anchor="w")

        cheat_version_label = ctk.CTkLabel(info_window, text=f"Cheat Version: {product['cheat_version']}")
        cheat_version_label.pack(pady=5, padx=10, anchor="w")

        updated_label = ctk.CTkLabel(info_window, text=f"Last Updated: {product['last_updated']}")
        updated_label.pack(pady=5, padx=10, anchor="w")

        keywords_label = ctk.CTkLabel(info_window, text=f"Keywords: {product['keywords']}", wraplength=380)
        keywords_label.pack(pady=5, padx=10, anchor="w")
    return inner



bilder_cache = []

def wechsel_bild():
    global aktuell
    if ads_visible:
        if not bild_label.winfo_ismapped():
            bild_label.pack(pady=10)

        # Bild laden
        img = Image.open(bilder[aktuell])
        ctk_img = CTkImage(img, size=(img.width, img.height))

        # Referenz speichern (nicht nur in Label!)
        bilder_cache.append(ctk_img)
        bild_label.configure(image=ctk_img, text="")
        bild_label.image = ctk_img

        aktuell = (aktuell + 1) % len(bilder)
    else:
        if hasattr(bild_label, "image"):
            del bild_label.image
        if bild_label.winfo_ismapped():
            bild_label.pack_forget()

    root.after(5000, wechsel_bild)


# Funktion zum Öffnen des Links
def open_link(event):
    link_index = (aktuell - 1) % len(links)  # vorheriges Bild
    webbrowser.open(links[link_index])

# Label erstellen
bild_label = ctk.CTkLabel(root, text="")
bild_label.pack(pady=20)
bild_label.bind("<Button-1>", open_link)

  # Start
anmelden_button = ctk.CTkButton(root, text="Anmelden", command=open_login_window)
anmelden_button.place(relx=1.0, rely=0, anchor="ne", x=-10, y=10)
info_label = ctk.CTkLabel(root, text="Not logged in")
info_label.place(relx=1.0, rely=0, anchor="ne", x=-10, y=50)
# Buttons dynamisch aus JSON erstellen




# globales Dictionary für Buttons
product_buttons = {}  # key = Produktname, value = {"start": Button, "uninstall": Button}

# Buttons dynamisch erstellen
for i, product_name in enumerate(daten["products"]):
    product = daten["products"][product_name]

    label = ctk.CTkLabel(button_frame, text=product_name)
    label.grid(row=i, column=0, padx=10, pady=5, sticky="w")
    label.bind("<Button-1>", click_cheat_lable(product))

    # Prüfen, ob Produkt bereits heruntergeladen
    with open(downloadjsonpath, "r", encoding="utf-8") as f:
        downloadjson = json.load(f)

    if product_name in downloadjson:
        # Starten-Button
        start_btn = ctk.CTkButton(button_frame, text="Starten", command=lambda n=product_name: button_click_start(n))
        start_btn.grid(row=i, column=1, padx=10, pady=5, sticky="ew")

        # Deinstallieren-Button
        uninstall_btn = ctk.CTkButton(button_frame, text="Deinstallieren", fg_color="red", hover_color="#ff4d4d",
                                      command=lambda n=product_name: button_click_uninstall(n))
        uninstall_btn.grid(row=i, column=2, padx=10, pady=5, sticky="ew")
    else:
        # Download-Button
        start_btn = ctk.CTkButton(button_frame, text="Download", command=lambda n=product_name: button_click(n))
        start_btn.grid(row=i, column=1, padx=10, pady=5, sticky="ew")

        uninstall_btn = None  # noch kein Deinstallieren-Button

    # Buttons speichern
    product_buttons[product_name] = {"start": start_btn, "uninstall": uninstall_btn}

check_saved_login()
wechsel_bild()
root.mainloop()
