from gtts import gTTS
import os

# Der Text, den du umwandeln möchtest
text = """
Bitte analysiere das folgende Dokument mit Aktiennamen und eine aktuelle Einschätzung dazu. 
Bitte erstelle eine Tabelle mit vier Spalten und schreibe in die erste das Datum, das am Anfang des Dokumentes genannt wurde. 
In die Zweites Spalte den Namen der Aktien und in die dritte den Kommentar, der erfasst worden ist. 
In die vierte Spalte bitte die Kategorie, die oberhalb angegeben wurde, wie zum Beispiel Robotik oder Infrastruktur oder Quantencomputer.
"""

# Erstellen des text_to_speach_mp3-Objekts (Sprache: Deutsch)
tts = gTTS(text=text, lang='de')

# Speichern der Datei
dateiname = "aktien_analyse_prompt_1.mp3"
tts.save(dateiname)

print(f"Die Datei '{dateiname}' wurde erfolgreich erstellt.")