## Detaillierte Beschreibung des `setup_playbook.yml`

Das `setup_playbook.yml` ist ein Ansible-Playbook, das zur Automatisierung der Einrichtung der Entwicklungsumgebung für das GovTech-Netzwerkanalyse-Projekt verwendet wird. Es führt mehrere Aufgaben aus, um die PostgreSQL-Datenbank zu initialisieren und die Docker-Umgebung zu starten.

### Hauptaufgaben des Playbooks

1. **Erstellung der .env-Datei**

   - **Beschreibung**: Erstellt eine `.env`-Datei, die die Umgebungsvariablen für die Datenbankverbindung enthält.
   - **Vorgehensweise**: Nutzt das `copy` Modul, um eine Datei mit den Variablen `DB_PASSWORD`, `POSTGRES_DB` und `POSTGRES_USER` zu erstellen.

2. **Docker-Compose-Ausführung**

   - **Beschreibung**: Startet die Docker-Container, die für das Projekt erforderlich sind.
   - **Vorgehensweise**: Verwendet das `community.docker.docker_compose_v2` Modul, um `docker-compose up` auszuführen. Die Umgebungsvariablen werden aus der zuvor erstellten `.env`-Datei geladen.

3. **Warten auf PostgreSQL**

   - **Beschreibung**: Stellt sicher, dass der PostgreSQL-Dienst betriebsbereit ist, bevor fortgefahren wird.
   - **Vorgehensweise**: Nutzt das `wait_for` Modul, um auf den Port 5432 zu warten, der von PostgreSQL verwendet wird.

4. **Überprüfung des PostgreSQL-Zustands**

   - **Beschreibung**: Überprüft, ob der PostgreSQL-Container gesund ist.
   - **Vorgehensweise**: Verwendet das `community.docker.docker_container_info` Modul, um den Gesundheitszustand des Containers zu überprüfen und wartet, bis dieser als "healthy" markiert ist.

5. **Datenbankschema-Erstellung**

   - **Beschreibung**: Führt ein SQL-Skript aus, um das Datenbankschema zu erstellen.
   - **Vorgehensweise**: Liest den Inhalt des SQL-Skripts mit `ansible.builtin.slurp` und führt es mit dem `community.postgresql.postgresql_query` Modul aus.

6. **Initialdaten-Einfügung**
   - **Beschreibung**: Fügt initiale Daten in die Datenbank ein.
   - **Vorgehensweise**: Ein weiteres SQL-Skript wird gelesen und ausgeführt, um die Datenbank mit Startdaten zu befüllen.

### Ausführung des Playbooks

Um das Playbook auszuführen, stellen Sie sicher, dass Ansible installiert ist und führen Sie den folgenden Befehl im Terminal aus:

```bash
ansible-playbook setup_playbook.yml

```

### Einloggen in die Datenbank

```bash
docker exec -it linkedin_network-db-1 psql -U admin -d govtech_network
```

#### Postgres Befehle und Queries

- `\dt` - Zeigt alle Tabellen in der Datenbank an.
- `\d+ <table_name>` - Zeigt die Spalten und Constraints einer Tabelle an.
- `\q` - Beendet die Postgres-Sitzung.
