import fitz  # PyMuPDF
import re    # Für die Suche nach Jahreszahlen

def read_pdf_line_by_line(pdf_path):
    # Öffne das PDF-Dokument
    document = fitz.open(pdf_path)
    
    # Regex für die Jahreszahlen zwischen 2010 und 2022
    year_pattern = re.compile(r'\b(201[0-9]|202[0-2])\b')
    
    # Variablen zum Speichern der Position von "Jg" und "P"
    jg_line = None
    p_line = None
    
    # Iteriere durch jede Seite im Dokument
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text = page.get_text("text")
        
        # Teile den Text der Seite in Zeilen auf
        lines = text.split('\n')
        
        # Iteriere durch die Zeilen und suche nach "Jg", "P" und Jahreszahlen
        for i, line in enumerate(lines):
            # Suche nach "Jg" und "P" in der aktuellen Zeile
            if "Jg" in line and "P" in line:
                jg_line = line  # Speichert die Zeile mit "Jg"
                p_line = line   # Speichert die Zeile mit "P"
            
            # Suche nach einer Jahreszahl in der aktuellen Zeile
            year_match = year_pattern.search(line)
            if year_match:
                year = year_match.group(0)
                print(f"Jahreszahl: {year}")
                
                # Wenn zuvor "Jg" und "P" gefunden wurden, extrahiere die Werte
                if jg_line and p_line:
                    # Positionen für die Werte nach "Jg" und "P" (+14 Zeichen)
                    jg_value_position = line.find("Jg") + 14
                    p_value_position = line.find("P") + 14

                    # Extrahiere die Werte an den Positionen (falls sie existieren)
                    jg_value = line[jg_value_position: jg_value_position + 5].strip()
                    p_value = line[p_value_position: p_value_position + 5].strip()
                    
                    print(f"Wert 14 Zeichen nach 'Jg': {jg_value}")
                    print(f"Wert 14 Zeichen nach 'P': {p_value}")
                
                # Gib die Folgezeilen aus (Gesamt und weiblich)
                if i + 1 < len(lines):
                    print(f"Gesamt: {lines[i + 1]}")
                if i + 2 < len(lines):
                    print(f"Davon weiblich: {lines[i + 2]}")

if __name__ == "__main__":
    pdf_path = "wehberg.pdf"  # Ersetze dies durch den Pfad zu deiner PDF-Datei
    read_pdf_line_by_line(pdf_path)
