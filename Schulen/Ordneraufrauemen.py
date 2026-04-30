import os
import shutil

def distribute_json_files(base_folder):
    # Durchlaufe alle Dateien im Basisordner
    for filename in os.listdir(base_folder):
        # Überprüfen, ob die Datei eine JSON-Datei ist
        if filename.endswith('.json'):
            # Extrahiere den Schulnamen aus dem Dateinamen (Präfix)
            school_name = filename.split('_')[0]  # z.B. "Ida" aus "Ida_SchuelerAnzahl.json"
            target_folder = os.path.join(base_folder, school_name)
            
            # Überprüfen, ob der Zielordner existiert
            if os.path.exists(target_folder):
                # Kopiere die JSON-Datei in den entsprechenden Unterordner
                source_file = os.path.join(base_folder, filename)
                target_file = os.path.join(target_folder, filename)
                
                try:
                    shutil.move(source_file, target_file)  # Datei verschieben
                    print(f"Datei {filename} wurde nach {target_folder} verschoben.")
                except Exception as e:
                    print(f"Fehler beim Verschieben von {filename}: {str(e)}")
            else:
                print(f"Zielordner {target_folder} existiert nicht. Datei {filename} wurde nicht verschoben.")

if __name__ == "__main__":
    distribute_json_files('Schulen')
