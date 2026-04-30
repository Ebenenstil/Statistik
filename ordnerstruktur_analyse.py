import os
import subprocess

def process_pdf_in_subfolders(base_folder):
    # Durchlaufe alle Unterordner im Basisordner
    for dirpath, _, files in os.walk(base_folder):
        for file in files:
            # Überprüfe, ob die Datei eine PDF-Datei ist
            if file.lower().endswith('.pdf'):
                pdf_path = os.path.join(dirpath, file)
                print(f"Verarbeite PDF: {pdf_path}")
                
                # Aufruf des Gesamtskripts mit der PDF-Datei als Argument
                subprocess.run(['python', 'Schuelerzahlenanalyse.py', pdf_path, dirpath])

if __name__ == "__main__":
    # Ersetze 'dein_basisordner' durch den Pfad zu deinem Basisordner
    base_folder = 'Schulen'
    process_pdf_in_subfolders(base_folder)
