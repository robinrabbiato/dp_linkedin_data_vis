# GovTech Deutschland Netzwerkanalyse

## Projektübersicht

Dieses Projekt zielt darauf ab, die Strukturen der deutschen GovTech-Landschaft mittels einer Netzwerkanalyse zu untersuchen. Der Fokus liegt auf der Analyse sozialer Netzwerke deutscher GovTech-Unternehmen, um Verbindungen, Einflüsse und Cluster innerhalb dieses aufstrebenden Sektors zu identifizieren.

## Datenbasis

Die Grundlage unserer Analyse bildet ein Verzeichnis von GovTech-Profilen auf LinkedIn. Diese Daten umfassen:

- Unternehmensnamen
- Gründungsjahr
- LinkedIn-Profillink

Beispiel des Datenformats:

| Unternehmen                 | Typ     | Gründungsjahr | LinkedIn-Profil                                                           |
| --------------------------- | ------- | ------------- | ------------------------------------------------------------------------- |
| &effect data solutions GmbH | StartUp | 2019          | https://www.linkedin.com/company/and-effect/                              |
| 1000°DIGITAL GmbH           | StartUp | 2016          | https://www.linkedin.com/company/1000digital/                             |
| 1648 Factory                | StartUp | 2020          | https://www.linkedin.com/company/1648factory/about/                       |
| Abcalis GmbH                | StartUp | 2019          | https://www.linkedin.com/company/abcalis/                                 |
| academa.de                  | StartUp | 2020          | https://www.linkedin.com/company/academa-gmbh/                            |
| Accu:rate                   | StartUp | 2014          | https://www.linkedin.com/company/accu-rate/                               |
| admi                        | StartUp | 2022          | https://www.linkedin.com/company/admi-kommunal-gmbh/                      |
| AGVOLUTION                  | StartUp | 2020          | https://www.linkedin.com/company/agvolution/                              |
| aible solutions             | StartUp | 2017          | https://www.linkedin.com/company/aible-ai-and-machine-learning-solutions/ |

## Tech Stack

Für dieses Projekt verwenden wir folgenden Tech Stack:

- **Programmiersprache**: Python
- **Web Scraping**: inoffical [LinkedIn API](https://github.com/tomquirk/linkedin-api)
- **Datenbank**: PostgreSQL für die Datenspeicherung und -verarbeitung
- **Netzwerkanalyse**: NetworkX für die Erstellung und Analyse von Graphen
- **Containerisierung**: Docker für konsistente Entwicklungs- und Produktionsumgebungen
- **Orchestrierung**: Ansible für die Automatisierung von Deployment und Konfiguration

## Methodologie

Die Netzwerkanalyse wird wie folgt durchgeführt:

1. **Datenextraktion**:

   - Scraping der LinkedIn-Profile der gelisteten Unternehmen
   - Erfassung von Posts und Erwähnungen auf diesen Profilen
   - Sammlung von Informationen über Gründer und deren Aktivitäten

2. **Datenverarbeitung**:

   - Identifikation von Erwähnungen und Verlinkungen zwischen Unternehmen in den Posts
   - Erstellung einer gerichteten Kantenliste, wobei eine Erwähnung von Unternehmen A zu Unternehmen B als gerichtete Kante interpretiert wird
   - Bündelung der Aktivitäten von Unternehmen und deren Gründern

3. **Datenbankverarbeitung**:

   - Speicherung der extrahierten und verarbeiteten Daten in einer PostgreSQL-Datenbank
   - Nutzung von SQL-Abfragen für komplexe Datenanalysen und -aggregationen
   - Erstellung von Views und materialisierten Views für häufig benötigte Datenstrukturen

4. **Aktivitätsbündelung**:

   - Zusammenführung der Post-Aktivitäten von Unternehmen und ihren Gründern
   - Beispiel: Wenn Max Mustermann Firma X gegründet hat, werden die Post-Aktivitäten von Firma X und Max Mustermann gemeinsam betrachtet und analysiert

5. **Netzwerkanalyse**:

   - Konstruktion eines gerichteten Graphen basierend auf den extrahierten und gebündelten Kanten
   - Anwendung von Netzwerkanalyse-Metriken wie Zentralität, Clustering-Koeffizient und Community-Detektion

6. **Visualisierung**:
   - Erstellung von Netzwerkgraphen zur Darstellung der Verbindungen
   - Generierung von Heatmaps und anderen Visualisierungen zur Veranschaulichung der Netzwerkstruktur

## Erwartete Erkenntnisse

Durch diese Analyse erwarten wir Einblicke in:

- Schlüsselakteure im deutschen GovTech-Sektor
- Cluster von eng verbundenen Unternehmen und Gründern
- Informationsflüsse und Einflussstrukturen innerhalb der Branche
- Potenzielle Kooperationsmöglichkeiten und Synergien zwischen Unternehmen
- Die Rolle von Gründern als Verbindungsglieder zwischen verschiedenen Unternehmen und Initiativen

Diese Erkenntnisse können wertvoll sein für Entscheidungsträger, Investoren und die GovTech-Unternehmen selbst, um die Dynamik und Struktur des Sektors besser zu verstehen und strategische Entscheidungen zu treffen.
