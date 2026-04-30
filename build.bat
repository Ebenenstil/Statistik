@echo off
echo Installiere Abhaengigkeiten...
pip install -r requirements.txt
pip install pyinstaller

echo.
echo Erstelle Executable...
pyinstaller --onefile --console --name Schuelerzahlenanalyse Schuelerzahlenanalyse.py

echo.
echo Fertig! Die Datei liegt in: dist\Schuelerzahlenanalyse.exe
echo Kopiere dist\Schuelerzahlenanalyse.exe zusammen mit dem SCHULEN-Ordner auf den Ziel-PC.
pause
