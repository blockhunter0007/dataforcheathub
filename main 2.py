import requests
import customtkinter as ctk
import os
import subprocess
import sys

# --- Konfiguration ---
CURRENT_VERSION = "1.0.00"
BASE_URL = "https://blockhunter0007.github.io/cheathubdumpingground/"
SERVER_JSON_URL = f"{BASE_URL}server.json"
UPDATE_URL = f"{BASE_URL}update" # Annahme: Dies ist die URL zur neuen .exe oder .py Datei

# --- Hauptanwendungsklasse ---
class CheatHubApp(ctk.CTk):
    def __init__(self, cheats_data):
        super().__init__()

        self.title("CheatHub")
        self.geometry("500x400")

        # --- UI Initialisierung ---
        self.label = ctk.CTkLabel(self, text="Willkommen bei CheatHub!", font=("Arial", 20))
        self.label.pack(pady=10)

        # Erstelle einen scrollbaren Frame, falls es viele Cheats gibt
        self.scrollable_frame = ctk.CTkScrollableFrame(self, label_text="Verfügbare Cheats")
        self.scrollable_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Erstelle für jeden Cheat die entsprechenden Widgets (Label, Button etc.)
        self.create_cheat_widgets(cheats_data)

    def create_cheat_widgets(self, cheats_data):
        """Erstellt dynamisch die UI-Elemente für jeden Cheat."""
        for cheat in cheats_data:
            # Container-Frame für jeden einzelnen Cheat
            cheat_frame = ctk.CTkFrame(self.scrollable_frame)
            cheat_frame.pack(pady=5, padx=5, fill="x", expand=True)

            # Name und Beschreibung des Cheats
            name_label = ctk.CTkLabel(cheat_frame, text=cheat.get("name", "N/A"), font=("Arial", 16, "bold"))
            name_label.pack(anchor="w", padx=10, pady=(5, 0))
            
            desc_label = ctk.CTkLabel(cheat_frame, text=cheat.get("description", "Keine Beschreibung."), wraplength=400, justify="left")
            desc_label.pack(anchor="w", padx=10, pady=(0, 5))

            # Überprüfen, ob die Datei bereits existiert
            folder_name = cheat.get("folder")
            file_name = cheat.get("location")
            local_path = os.path.join(folder_name, file_name) if folder_name and file_name else None
            
            button_text = "Starten" if local_path and os.path.exists(local_path) else "Herunterladen"
            
            # Button zum Herunterladen/Starten
            button = ctk.CTkButton(cheat_frame, text=button_text)
            # WICHTIG: lambda wird hier verwendet, um sicherzustellen, dass jeder Button
            # die korrekten Cheat-Daten und den richtigen Button-Verweis erhält.
            button.configure(command=lambda c=cheat, b=button: self.handle_cheat_click(c, b))
            button.pack(anchor="e", padx=10, pady=5)

    def handle_cheat_click(self, cheat_info, button):
        """Verwaltet den Klick auf einen Cheat-Button."""
        if button.cget("text") == "Herunterladen":
            self.download_cheat(cheat_info, button)
        else:
            self.start_cheat(cheat_info)

    def download_cheat(self, cheat_info, button):
        """Lädt die Cheat-Datei herunter."""
        folder_name = cheat_info.get("folder")
        file_name = cheat_info.get("location")

        if not folder_name or not file_name:
            print(f"Fehler: 'folder' oder 'location' fehlt in den JSON-Daten für {cheat_info.get('name')}")
            return

        # Erstelle den Ordner, falls er nicht existiert
        try:
            os.makedirs(folder_name, exist_ok=True)
        except OSError as e:
            print(f"Fehler beim Erstellen des Ordners {folder_name}: {e}")
            return

        download_url = f"{BASE_URL}{file_name}"
        local_path = os.path.join(folder_name, file_name)

        print(f"Starte Download für '{cheat_info['name']}' von {download_url}...")
        button.configure(text="Lädt herunter...", state="disabled")
        
        try:
            with requests.get(download_url, stream=True) as r:
                r.raise_for_status()
                with open(local_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            print(f"Download erfolgreich! Gespeichert unter: {local_path}")
            button.configure(text="Starten", state="normal")
        except requests.exceptions.RequestException as e:
            print(f"Fehler beim Download: {e}")
            button.configure(text="Fehler", state="normal")


    def start_cheat(self, cheat_info):
        """Startet die heruntergeladene Cheat-Datei."""
        folder_name = cheat_info.get("folder")
        file_name = cheat_info.get("location")
        local_path = os.path.join(folder_name, file_name)

        print(f"Versuche, '{local_path}' zu starten...")
        try:
            # subprocess.Popen startet den Prozess, ohne auf ihn zu warten
            subprocess.Popen([local_path])
            print(f"'{local_path}' wurde gestartet.")
        except FileNotFoundError:
            print(f"Fehler: Die Datei '{local_path}' wurde nicht gefunden.")
        except Exception as e:
            print(f"Ein Fehler ist beim Starten der Datei aufgetreten: {e}")

# --- Update-Funktion ---
def update_application():
    """Lädt die neue Version der Anwendung herunter."""
    print("Veraltete Version erkannt. Starte das Update...")
    try:
        response = requests.get(UPDATE_URL)
        response.raise_for_status()
        
        # Speichert die neue Version. Der Benutzer muss sie manuell ersetzen.
        new_filename = "CheatHub_new.exe" # oder .py
        with open(new_filename, 'wb') as f:
            f.write(response.content)
            
        print(f"Update erfolgreich heruntergeladen als '{new_filename}'.")
        print("Bitte schließe die alte Anwendung und ersetze sie durch die neue.")
        # Hier könnte man ein Batch-Skript starten, das die alte Datei nach Beendigung ersetzt.
        # Das ist aber komplexer und plattformabhängig.
        
    except requests.exceptions.RequestException as e:
        print(f"Fehler beim Herunterladen des Updates: {e}")

# --- Startlogik ---
def main():
    """Hauptfunktion, die die Version prüft und die App startet."""
    try:
        response = requests.get(SERVER_JSON_URL)
        # Wirft einen Fehler bei Statuscodes wie 404 oder 500
        response.raise_for_status()
        
        data = response.json()
        
        # 1. Versionsprüfung
        server_version = data.get('version')
        if server_version and server_version != CURRENT_VERSION:
            update_application()
            # Beende das Skript nach der Update-Anweisung, damit nicht die alte GUI startet.
            return
        
        # 2. GUI starten, wenn Version aktuell ist
        if 'cheats' in data:
            app = CheatHubApp(data['cheats'])
            app.mainloop()
        else:
            print("Keine 'cheats' in den Server-Daten gefunden.")

    except requests.exceptions.RequestException as e:
        print(f"Netzwerkfehler: Konnte keine Verbindung zum Server herstellen. {e}")
    except ValueError:
        print("Fehler: Die Antwort vom Server ist kein gültiges JSON-Format.")


if __name__ == "__main__":
    main()