# programmieruebung_Auf_2-5
# 🧠 EKG-Auswertungs-App

Diese interaktive App dient der Visualisierung und Analyse von EKG- und Leistungsdaten in sportwissenschaftlichen Kontexten. Entwickelt mit Streamlit, ermöglicht sie die Auswahl von Versuchspersonen, die Anzeige individueller Messdaten sowie die Auswertung von Herzfrequenzzonen.

---

## 🔧 Voraussetzungen

### 📦 Installation mit PDM

1. 📥 Projekt-Repository klonen:
    1. Kopiere die https-Adresse des Codes 
    2. Öffne den entsprechenden Ordner und kopiere den Code in die git bash 
    3. öffne den Ordner in Visual Studio Code 

2. 📦 Abhängigkeiten installieren:
    1. Gib in der powershell den Befehl `pdm install´ ein, um das erstellte pdm und alles wichtigen Pakete zu installieren 

Wichtig: Stelle sicher, dass PDM bereits auf dem PC installiert ist. Falls nicht:  

---

## 🚀 Anwendung starten
Dazu in der powershell den Befehl streamlit run main.py eingeben
> Die App öffnet sich im Browser unter `http://localhost:8501`

---

## 🧭 Projektstruktur

```
├── data/
│   ├── activities/
│   │   └── activity.csv            # Messdaten (Herzfrequenz, Leistung)
│   ├── pictures/
│   │   └── <personenbilder>.jpg    # Fotos der Versuchspersonen
│   └── personen.csv                # Metadaten (Name, Bildpfad etc.)
├── read_data.py                    # Datenzugriff: Personenliste, Bildpfade
├── read_pandas.py                  # Datenanalyse, Zonenberechnung, Plots
├── main.py                         # Streamlit-GUI der App
└── README.md                       # Diese Datei
```

---

## ⚙️ Funktionen der App

- Auswahl einer Versuchsperson inkl. Bildanzeige
- Anzeige von Herzfrequenz & Leistung über die Zeit
- Automatische Einteilung der Herzfrequenz in Zonen
- Eingabe oder automatische Erkennung der maximalen Herzfrequenz
- Auswertung:
  - maximale und durchschnittliche Leistung
  - durchschnittliche Leistung in jeder Herzfrequenzzone
- Interaktive Diagramme mit Plotly

---

## 🧪 Beispielnutzung

1. Starte die App mit `streamlit run main.py`
2. Wähle eine Versuchsperson aus
3. Überprüfe oder passe die maximale Herzfrequenz an
4. Analysiere:
   - Herzfrequenz-/Leistungskurven
   - farbige Zonenmarkierung im Diagramm
   - statistische Kennzahlen pro Zone

---

## 📸 Hinweis zu den Daten

- `personen.csv` enthält die Versuchspersonen (Name, Bildpfad, evtl. weitere Daten)
- Die Messdaten müssen unter `data/activities/activity.csv` im richtigen Format vorliegen
- Bilder liegen unter `data/pictures/` und sollten korrekt mit den Namen verknüpft sein

---

## 👩‍🔬 Zielgruppe

Diese Anwendung richtet sich an:
- Sportwissenschaftler:innen
- Trainer:innen
- Studierende in Projekten zur Leistungsdiagnostik
