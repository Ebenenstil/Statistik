import PyPDF2
import re
import json

def pdf_to_matrix(pdf_path):
    # PDF öffnen
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        all_text = ''
        
        # Text von allen Seiten extrahieren
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            all_text += page.extract_text() + '\n'
    
    # Text in Zeilen aufteilen und Wörter als Elemente speichern
    lines = all_text.splitlines()
    matrix = []
    
    # Regex zum Extrahieren von Wörtern und Zahlen
    word_pattern = re.compile(r'\w+')

    for line in lines:
        words = word_pattern.findall(line)
        if words:  # Nur nicht-leere Zeilen speichern
            matrix.append(words)
    
    return matrix

def save_matrix_to_json(matrix, json_file_path):
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(matrix, json_file, indent=4, ensure_ascii=False)
    print(f"Matrix in JSON-Datei gespeichert: {json_file_path}")

def save_matrix_to_txt(matrix, txt_file_path):
    with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
        for row in matrix:
            txt_file.write(' '.join(row) + '\n')
    print(f"Matrix in TXT-Datei gespeichert: {txt_file_path}")

# Testaufruf
pdf_path = 'wehberg.pdf'
matrix = pdf_to_matrix(pdf_path)

# Speichern der Matrix als JSON und TXT
json_file_path = 'matrix_output.json'
txt_file_path = 'matrix_output.txt'

save_matrix_to_json(matrix, json_file_path)
save_matrix_to_txt(matrix, txt_file_path)
