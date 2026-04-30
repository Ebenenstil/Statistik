# Statistik - Setup-Anleitung (macOS / zsh)

Diese Anleitung hilft Ihnen, den Arbeitsbereich lokal auf einem macOS-System mit zsh einzurichten. Sie basiert auf den in den Skripten verwendeten Bibliotheken (`PyPDF2`, `PyMuPDF` (fitz), `pdfplumber`, `pandas`).

## 1) Python-Version
Verwenden Sie Python 3.10 oder neuer. Prüfen Sie die Version mit:

```bash
python3 --version
```

## 2) Virtuelle Umgebung (empfohlen)
Empfohlen ist eine isolierte virtuelle Umgebung:

```bash
cd /Users/davidknospe/Documents/Statistik
python3 -m venv .venv
source .venv/bin/activate
```

Um die venv wieder zu verlassen, verwenden Sie `deactivate`.

## 3) Abhängigkeiten installieren
Installieren Sie die Abhängigkeiten aus `requirements.txt`:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Hinweis: `PyMuPDF` wird als `fitz` importiert (z. B. `import fitz`). Falls Probleme beim Kompilieren auftreten, stellen Sie sicher, dass Xcode-Command-Line-Tools installiert sind:

```bash
xcode-select --install
```

## 4) Beispielskript ausführen
Die Skripte erwarten PDF-Dateien im Dateisystem. Ein einfaches Ausführen eines Skripts:

```bash
python3 Schuelerzahlenanalyse.py
```

Weitere Skripte im Projekt:
- `PDFSearch.py` (zeigt, wie man mit PyMuPDF PDFs zeilenweise liest)
- `PDFAnalyse.py` (pdfplumber + pandas Verarbeitung)
- `PDFMatrix.py` / `PDFMatrixSUCHE` (PyPDF2-basierte Matrix-Extraktion)

## 5) Häufige Probleme
- Falls `pdfplumber` keine Texte extrahiert: PDF kann gescannte Bilder enthalten. In diesem Fall ist OCR (z. B. Tesseract) erforderlich.
- Bei Import- oder Versionkonflikten: venv neu erstellen und `pip install -r requirements.txt` erneut ausführen.

## 6) Nächste Schritte (optional)
- `tasks.json` für VS Code anlegen (Setup/Run-Tasks)
- Kleine Tests hinzufügen, um die Extraktionsfunktionen zu verifizieren
- CI (GitHub Actions) zum Laufen bringen, um Linting/Tests zu automatisieren

---
Wenn Sie möchten, erstelle ich die VS Code-Tasks und einfache Unit-Tests für zentrale Funktionen (z. B. `pdf_to_matrix`).
