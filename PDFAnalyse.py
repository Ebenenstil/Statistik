import pandas as pd
import pdfplumber

# Datei einlesen
pdf_path = 'Ida.pdf'

# Listen für die gesammelten Daten
data = []

# PDF öffnen und Seiten durchlaufen
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        if text:
            lines = text.split('\n')
            klasse = None
            jahr = None
            gesamt = None
            weiblich = None
            wohnort = None
            schuelerzahl = None
            
            for line in lines:
                # Debugging: Ausgabe der aktuellen Zeile
                print(f"Processing line: {line}")
                
                # Klasse und relevante Daten erkennen
                if 'Adr Jg P TKM Schul Kl.-' in line:
                    klasse = line.split()[-1]
                    print(f"Found Klasse: {klasse}")
                elif 'Altersstruktur aller Schüler/Schülerinnen' in line:
                    # Sammeln der Altersstruktur
                    age_line = lines[lines.index(line) + 1].strip().split()
                    if len(age_line) >= 3:
                        jahr = age_line[0]
                        gesamt = age_line[1]
                        weiblich = age_line[2]
                        print(f"Found Altersstruktur - Jahr: {jahr}, Gesamt: {gesamt}, Weiblich: {weiblich}")
                elif 'Wohnort der Schüler/Schülerinnen' in line:
                    # Sammeln der Wohnortdaten
                    wohnort = lines[lines.index(line) + 1].strip()
                    schuelerzahl_line = lines[lines.index(line) + 2].strip().split()
                    schuelerzahl = schuelerzahl_line[-1] if len(schuelerzahl_line) > 0 else None
                    print(f"Found Wohnort: {wohnort}, Schülerzahl: {schuelerzahl}")
                    
                    # Hinzufügen der Daten zur Liste nur, wenn alle Informationen vorhanden sind
                    if klasse and jahr and gesamt and weiblich and wohnort and schuelerzahl:
                        data.append([klasse, jahr, gesamt, weiblich, wohnort, schuelerzahl])
                        print(f"Added data: {klasse}, {jahr}, {gesamt}, {weiblich}, {wohnort}, {schuelerzahl}")

# DataFrame erstellen
df = pd.DataFrame(data, columns=['Klasse', 'Geburtsjahr', 'Schüler gesamt', 'Schüler weiblich', 'Wohnort', 'Schüleranzahl am Wohnort'])

# DataFrame in eine Excel-Datei exportieren
output_file = 'Schuelerdaten_analyse.xlsx'
df.to_excel(output_file, index=False)

print(f'Daten erfolgreich in {output_file} exportiert.')
