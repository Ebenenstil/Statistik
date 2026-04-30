import json

def load_schueler_analyse(json_file_path):
    # Laden der Schüleranalyse aus der JSON-Datei
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data["SchuelerAnzahl"]

def aggregate_schueler_data(schueler_analyse):
    aggregated_data = {}
    
    for row in schueler_analyse:
        key = (row[0], row[1])  # Verwende die ersten beiden Werte als Schlüssel
        # Stelle sicher, dass die Indizes 2 und 3 existieren
        if len(row) >= 4:
            value_2 = row[2]
            value_3 = row[3]
            
            # Überprüfen, ob Werte fehlen und ein Vermerk setzen
            if value_2 == "":
                value_2 = "!"  # Vermerk für fehlenden Wert
            else:
                value_2 = int(value_2)  # Umwandlung in int
            
            if value_3 == "":
                value_3 = "!"  # Vermerk für fehlenden Wert
            else:
                value_3 = int(value_3)  # Umwandlung in int
            
            # Aggregation der Werte
            if key not in aggregated_data:
                aggregated_data[key] = [0, 0]  # Initialisierung für Indizes 2 und 3
            
            if isinstance(value_2, int):
                aggregated_data[key][0] += value_2
            if isinstance(value_3, int):
                aggregated_data[key][1] += value_3
            
            # Bei fehlenden Werten die entsprechenden Vermerke hinzufügen
            if row[2] == "":
                aggregated_data[key][0] = "!"
            if row[3] == "":
                aggregated_data[key][1] = "!"
        else:
            print(f"Nicht genügend Werte in Zeile: {row}")  # Ausgabe, wenn nicht genügend Werte vorhanden sind

    # Formatierung der aggregierten Daten für die Ausgabe
    final_output = []
    for (key_0, key_1), values in aggregated_data.items():
        final_output.append([key_0, key_1, values[0], values[1]])
    
    return final_output

def save_aggregated_data_to_json(aggregated_data, json_file_path):
    # Speichern der aggregierten Daten in einer JSON-Datei
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(aggregated_data, json_file, indent=4, ensure_ascii=False)
    print(f"Aggregierte Daten in JSON-Datei gespeichert: {json_file_path}")

# Testaufruf
input_json_file_path = 'SchuelerAnzahl.json'
output_json_file_path = 'Gesamtzahl.json'

# Lade die Schüleranalyse
schueler_analyse = load_schueler_analyse(input_json_file_path)

# Aggregiere die Schülerdaten
aggregated_data = aggregate_schueler_data(schueler_analyse)

# Speichere die aggregierten Daten
save_aggregated_data_to_json(aggregated_data, output_json_file_path)
