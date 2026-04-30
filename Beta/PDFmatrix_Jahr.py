import os
import json
import PyPDF2

def extract_matrix_from_pdf(pdf_path):
    matrix = []
    jahrgang_values = []

    # Öffnen der PDF-Datei
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        
        # Durchlaufen der Seiten und Extrahieren des Textes
        for page in reader.pages:
            text = page.extract_text()
            if text:
                # Zerlegen des Textes in Zeilen
                lines = text.split('\n')
                skip_to_next_adr = False
                adr_index = -1  # Index der "Adr"-Zeile
                
                for i, line in enumerate(lines):
                    # Zerlegen der Zeilen in Werte
                    values = line.split()  # Hier kannst du den Trennmechanismus anpassen
                    
                    # Speichern der Matrixwerte
                    matrix.append(values)

                    # Überprüfen, ob die Zeile mit "Adr" beginnt
                    if line.startswith("Adr"):
                        adr_index = i
                        # Speichern der Werte mit Index 1 und 2 von der nächsten Zeile +2
                        if adr_index + 2 < len(lines):
                            next_values = lines[adr_index + 2].split()
                            if len(next_values) > 2:
                                jahrgang_values.append({
                                    "Jahrgang": next_values[1],
                                    "P": next_values[2]
                                })
                        skip_to_next_adr = True
                        continue

                    # Werte ab der Zeile +16 nach "Adr" extrahieren
                    if skip_to_next_adr and adr_index + 16 <= i < len(lines):
                        if line.startswith("Adr"):
                            skip_to_next_adr = False  # Stoppe das Extrahieren, wenn eine neue "Adr"-Zeile gefunden wurde
                            continue
                        # Überprüfen, ob der erste Wert eine Zahl ist
                        first_value = values[0] if values else None
                        if first_value and first_value.isdigit():  # Prüfen, ob es sich um eine Zahl handelt
                            jahrgang_values.append({
                                "Wert": values  # Füge die gesamte Zeile als Wert hinzu (oder spezifische Indizes)
                            })

    return matrix, jahrgang_values

def save_matrix_to_json(matrix, json_path):
    with open(json_path, 'w') as json_file:
        json.dump(matrix, json_file, ensure_ascii=False, indent=4)

def save_jahrgang_to_json(jahrgang_values, json_path):
    with open(json_path, 'w') as json_file:
        json.dump(jahrgang_values, json_file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    pdf_file_path = 'Schulen/Wehberg/wehberg.pdf'  # Pfad zur PDF-Datei
    matrix_json_path = 'TestDatei.json'  # Pfad zur JSON-Ausgabedatei für die Matrix
    jahrgang_json_path = 'Jahrgang.json'  # Pfad zur JSON-Ausgabedatei für die Jahrgänge

    # Extrahiere die Matrix und Jahrgangswerte aus der PDF
    matrix, jahrgang_values = extract_matrix_from_pdf(pdf_file_path)

    # Speichere die Matrix in einer JSON-Datei
    save_matrix_to_json(matrix, matrix_json_path)

    # Speichere die Jahrgangswerte in einer JSON-Datei
    save_jahrgang_to_json(jahrgang_values, jahrgang_json_path)

    print(f"Matrix wurde erfolgreich in {matrix_json_path} gespeichert.")
    print(f"Jahrgangswerte wurden erfolgreich in {jahrgang_json_path} gespeichert.")
