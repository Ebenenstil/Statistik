import os
import PyPDF2
import re
import datetime


input_folder = "/Users/davidknospe/Documents/Statistik/SCHULEN"
ergebnis_folder = "/Users/davidknospe/Documents/Statistik"


def pdf_to_matrix(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        all_text = ''
        for page_num in range(len(reader.pages)):
            all_text += reader.pages[page_num].extract_text() + '\n'

    word_pattern = re.compile(r'\w+')
    return [words for line in all_text.splitlines() if (words := word_pattern.findall(line))]


def extract_schueler_analyse(matrix):
    schueler_analyse = []

    for row_index, row in enumerate(matrix):
        if row[0] == "Adr" and row_index + 2 < len(matrix):
            target_row = matrix[row_index + 2]
            next_row = matrix[row_index + 3] if row_index + 3 < len(matrix) else []

            z_index = next((i for i, v in enumerate(target_row) if v == 'z'), None)
            z_value = target_row[z_index + 1] if z_index is not None and z_index + 1 < len(target_row) else None

            w_index = next((i for i, v in enumerate(next_row) if v == 'w'), None)
            w_value = next_row[w_index + 1] if w_index is not None and w_index + 1 < len(next_row) else None

            schueler_analyse.append([target_row[1], target_row[2], z_value, w_value])

    return schueler_analyse


def aggregate_schueler_data(schueler_analyse):
    aggregated = {}

    for row in schueler_analyse:
        key = (row[0], row[1])
        if len(row) >= 4:
            try:
                v2 = int(row[2]) if row[2] and row[2].isdigit() else 0
                v3 = int(row[3]) if row[3] and row[3].isdigit() else 0
                if key not in aggregated:
                    aggregated[key] = [0, 0]
                aggregated[key][0] += v2
                aggregated[key][1] += v3
            except (ValueError, AttributeError) as e:
                log(f"Aggregierungsfehler in Zeile {row}: {e}")
        else:
            log(f"Nicht genügend Werte in Zeile: {row}")

    return [[k0, k1, v[0], v[1]] for (k0, k1), v in aggregated.items()]


def append_to_ergebnis(name, aggregated_data, txt_path):
    with open(txt_path, 'a', encoding='utf-8') as f:
        f.write(f"--- {name} ---\n")
        for row in aggregated_data:
            f.write(f"  Jahrgang: {row[0]}  |  Klasse: {row[1]}  |  Gesamt: {row[2]}  |  Weiblich: {row[3]}\n")
        f.write("\n")


def log(message):
    with open("prozess_log.txt", 'a', encoding='utf-8') as log_file:
        log_file.write(message + '\n')


def process_pdfs_in_folder(folder_path):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    txt_path = os.path.join(ergebnis_folder, f"Ergebnis_{timestamp}.txt")
    count = 0
    fehler = []

    for dirpath, _, filenames in os.walk(folder_path):
        for filename in filenames:
            if filename.endswith('.pdf'):
                pdf_path = os.path.join(dirpath, filename)
                print(f"Verarbeite PDF: {pdf_path}")
                name = os.path.splitext(filename)[0]
                try:
                    matrix = pdf_to_matrix(pdf_path)
                    schueler_analyse = extract_schueler_analyse(matrix)
                    aggregated_data = aggregate_schueler_data(schueler_analyse)
                    if not aggregated_data:
                        fehler.append(name)
                        log(f"{filename}: keine Schülerzahlen gefunden.")
                        continue
                    append_to_ergebnis(name, aggregated_data, txt_path)
                    log(f"{filename} erfolgreich verarbeitet.")
                    count += 1
                except Exception as e:
                    fehler.append(name)
                    log(f"Fehler beim Verarbeiten von {filename}: {e}")

    with open(txt_path, 'a', encoding='utf-8') as f:
        if fehler:
            f.write(f"Fehler bei Schule: {', '.join(fehler)}\n")
        f.write(f"Eingelesene Schulen: {count}\n")


if __name__ == "__main__":
    process_pdfs_in_folder(input_folder)
