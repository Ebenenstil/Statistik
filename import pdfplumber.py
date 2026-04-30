import pdfplumber
import pandas as pd

def extract_tables_from_pdf(pdf_path, output_csv_path=None, output_xls_path=None, output_json_path=None):
    # Öffne die PDF-Datei
    with pdfplumber.open(pdf_path) as pdf:
        all_tables = []
        # Iteriere über jede Seite der PDF
        for page in pdf.pages:
            # Extrahiere die Tabellen von der Seite
            tables = page.extract_tables()
            for table in tables:
                all_tables.append(table)
    
    # Konvertiere die Tabellen in DataFrames
    dataframes = [pd.DataFrame(table[1:], columns=table[0]) for table in all_tables]

    # Speichere die DataFrames in eine CSV-Datei
    if output_csv_path:
        combined_df = pd.concat(dataframes)
        combined_df.to_csv(output_csv_path, index=False)
        print(f"CSV-Datei erfolgreich unter {output_csv_path} gespeichert.")

    # Speichere die DataFrames in eine XLS-Datei
    if output_xls_path:
        with pd.ExcelWriter(output_xls_path) as writer:
            for i, df in enumerate(dataframes):
                df.to_excel(writer, sheet_name=f'Table_{i+1}', index=False)
        print(f"XLS-Datei erfolgreich unter {output_xls_path} gespeichert.")

    # Speichere die DataFrames in eine JSON-Datei
    if output_json_path:
        json_data = {f'Table_{i+1}': df.to_dict(orient='records') for i, df in enumerate(dataframes)}
        with open(output_json_path, 'w', encoding='utf-8') as json_file:
            json.dump(json_data, json_file, ensure_ascii=False, indent=4)
        print(f"JSON-Datei erfolgreich unter {output_json_path} gespeichert.")

# Beispielaufruf des Skripts
pdf_path = '/Users/davidknospe/Documents/Statistik/Test_Datei.pdf'
output_csv_path = '/Users/davidknospe/Documents/Statistik/output.csv'
output_xls_path = '/Users/davidknospe/Documents/Statistik/output.xlsx'
output_json_path = '/Users/davidknospe/Documents/Statistik/output.json'

extract_tables_from_pdf(pdf_path, output_csv_path, output_xls_path, output_json_path)
