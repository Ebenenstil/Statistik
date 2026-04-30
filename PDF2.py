import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import pandas as pd

# Setze den korrekten Pfad zu Tesseract
pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'

def ocr_image_to_text(image):
    return pytesseract.image_to_string(image)

def extract_and_summarize_data(pdf_path):
    # Konvertiere PDF-Seiten zu Bildern
    images = convert_from_path(pdf_path)
    all_text = []

    for image in images:
        text = ocr_image_to_text(image)
        all_text.append(text)

    all_tables = []
    for text in all_text:
        lines = text.split('\n')
        table = [line.split() for line in lines if line.strip() != '']
        all_tables.append(table)

    all_tables = [table for table in all_tables if table]

    if not all_tables:
        print("Keine Tabellen in der PDF-Datei gefunden.")
        return

    # Initialisiere Zähler für Mädchen und Jungen
    total_girls = 0
    total_boys = 0

    # Funktion zur Summierung der Schülerzahlen
    def sum_schuelerzahlen(table):
        nonlocal total_girls, total_boys
        for row in table:
            try:
                # Prüfe, ob die Zeile relevante Daten enthält
                if len(row) > 3 and "Adr" in row[0] and "Jg" in row[1]:
                    # Extrahiere die Schülerzahl (Zeile 1 für Mädchen, Zeile 2 für Jungen)
                    maedchen = int(row[3])
                    jungen = int(row[4])
                    total_girls += maedchen
                    total_boys += jungen
            except ValueError:
                continue

    # Überprüfe alle Tabellen
    for table in all_tables:
        sum_schuelerzahlen(table)

    print(f"Gesamtanzahl der Mädchen: {total_girls}")
    print(f"Gesamtanzahl der Jungen: {total_boys}")

# Beispielaufruf des Skripts
pdf_path = '/Users/davidknospe/Documents/Statistik/ida.pdf'
extract_and_summarize_data(pdf_path)
