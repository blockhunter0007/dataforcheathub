import requests
import customtkinter as ctk

# URL der JSON-Datei
app = ctk.CTk()

url = "https://blockhunter0007.github.io/cheathubdumpingground/server.json"

# Anfrage senden, um die JSON-Daten abzurufen
response = requests.get(url)
def update_version():
    print("Outdated version detected, please update to the latest version.")



def onclick():
    print("Button clicked!")

    
def app_start():
    app = ctk.CTk()
    app.title("CheatHub")
    app.geometry("400x300")
    label = ctk.CTkLabel(app, text="Welcome to CheatHub!")
    label.pack(pady=20)
    button = ctk.CTkButton(app, text="Klick mich!", command=onclick)
    button.pack(pady=20)
    print("App started successfully.")
    app.mainloop()
# Überprüfen, ob die Anfrage erfolgreich war (Statuscode 200 bedeutet OK)
if response.status_code == 200:
    # JSON-Daten parsen
    data = response.json()
    # Version aus den Daten herausfiltern
    if 'version' in data:
        version = data['version']
        print(f"Die Version ist: {version}")
        if version != "1.0.00":
            update_version()
        else:
            app_start()
    else:
        print("Kein 'version'-Feld in den Daten gefunden.")
else:
    print(f"Fehler: {response.status_code}")

