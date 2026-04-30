import os
import PyPDF2
import re
import json


input_folder = "/Users/davidknospe/Documents/SCHULEN"   # Pfad zu deinen PDFs
output_folder = "/Users/davidknospe/Documents/SCHULEN/output"  # Pfad für JSON-Ausgaben
fertig =  "/Users/davidknospe/Documents/SCHULEN/output/Fertig" 

def pdf_to_matrix(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        all_text = ''
        
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            all_text += page.extract_text() + '\n'
    
    lines = all_text.splitlines()
    matrix = []
    word_pattern = re.compile(r'\w+')

    for line in lines:
        words = word_pattern.findall(line)
        if words:
            matrix.append(words)
    
    return matrix

def save_matrix_to_json(matrix, json_file_path):
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(matrix, json_file, indent=4, ensure_ascii=False)
    print(f"Matrix in JSON-Datei gespeichert: {json_file_path}")

def load_matrix_from_json(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        matrix = json.load(json_file)
    return matrix

def extract_schueler_analyse(matrix):
    schueler_analyse = []
    target_rows = []

    for row_index, row in enumerate(matrix):
        if row[0] == "Adr":
            if row_index + 2 < len(matrix):
                target_row = matrix[row_index + 2]
                if row_index + 3 < len(matrix):
                    next_row = matrix[row_index + 3]
                
                z_index = next((i for i, v in enumerate(target_row) if v == 'z'), None)
                z_value = target_row[z_index + 1] if z_index is not None and z_index + 1 < len(target_row) else None

                w_index = next((i for i, v in enumerate(next_row) if v == 'w'), None)
                w_value = next_row[w_index + 1] if w_index is not None and w_index + 1 < len(next_row) else None

                schueler_analyse.append([target_row[1], target_row[2], z_value, w_value])
                target_rows.append((z_value, w_value))

    return schueler_analyse, target_rows

def save_schueler_analyse_to_json(schueler_analyse, target_rows, json_file_path):
    output_data = {
        "SchuelerAnzahl": schueler_analyse,
        "TargetRows": [{"ZValue": row[0], "WValue": row[1]} for row in target_rows]
    }
    
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(output_data, json_file, indent=4, ensure_ascii=False)
    print(f"SchuelerAnzahl in JSON-Datei gespeichert: {json_file_path}")

def load_schueler_analyse(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data["SchuelerAnzahl"]

def aggregate_schueler_data(schueler_analyse):
    aggregated_data = {}
    
    for row in schueler_analyse:
        key = (row[0], row[1])
        if len(row) >= 4:
            try:
                value_2 = int(row[2]) if row[2].isdigit() else 0
                value_3 = int(row[3]) if row[3].isdigit() else 0
                
                if key not in aggregated_data:
                    aggregated_data[key] = [0, 0]
                
                aggregated_data[key][0] += value_2
                aggregated_data[key][1] += value_3

            except (ValueError, AttributeError) as e:
                log_error(f"Fehler bei der Verarbeitung von Zeile: {row}, Fehler: {str(e)}")
                continue
        else:
            log_error(f"Nicht genügend Werte in Zeile: {row}")

    final_output = []
    for (key_0, key_1), values in aggregated_data.items():
        final_output.append([key_0, key_1, values[0], values[1]])
    
    return final_output

def save_aggregated_data_to_json(aggregated_data, json_file_path):
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(aggregated_data, json_file, indent=4, ensure_ascii=False)
    print(f"Aggregierte Daten in JSON-Datei gespeichert: {json_file_path}")

def log_error(message):
    with open("prozess_log.txt", 'a', encoding='utf-8') as log_file:
        log_file.write(message + '\n')

def process_pdfs_in_folder(folder_path):
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            if filename.endswith('.pdf'):
                pdf_path = os.path.join(dirpath, filename)
                print(f"Verarbeite PDF: {pdf_path}")
                try:
                    matrix = pdf_to_matrix(pdf_path)
                    matrix_json_file = os.path.join(output_folder, f"{filename.split('.')[0]}_matrix_output.json")
                    save_matrix_to_json(matrix, matrix_json_file)

                    schueler_analyse, target_rows = extract_schueler_analyse(matrix)
                    schueler_json_file = os.path.join(output_folder, f"{filename.split('.')[0]}_SchuelerAnzahl.json")
                    save_schueler_analyse_to_json(schueler_analyse, target_rows, schueler_json_file)

                    aggregated_data = aggregate_schueler_data(schueler_analyse)
                    gesamt_json_file = os.path.join(fertig, f"{filename.split('.')[0]}_Gesamtzahl.json")
                    save_aggregated_data_to_json(aggregated_data, gesamt_json_file)

                    log_error(f"{filename} erfolgreich verarbeitet.")
                except Exception as e:
                    log_error(f"Fehler beim Verarbeiten von {filename}: {str(e)}")

if __name__ == "__main__":
    process_pdfs_in_folder(input_folder)
