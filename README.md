# APRS Pi – OLED Monitor Projekt

Ein multifunktionales Monitoring-Skript für den Raspberry Pi 4B mit Anzeige auf einem 2.42" OLED-Display.

## Hauptfunktionen

- GPS-Zeit- und Positionsanzeige (via gpsd)
- APRS-Rufzeichenanzeige (über Direwolf KISS TCP)
- Systemressourcenmonitor (CPU, RAM, Disk, Temperatur, Uptime)
- Ladezustand & Status eines UPS HAT (INA219)
- GPX-Logger (automatisch aktiv bei GPS-Fix)
- Steuerung per GPIO-Taster mit automatischem Rücksprung auf Hauptseite

## Hardware

- **Raspberry Pi 4B**
- **OLED 2.42" Waveshare (I2C)**
- **UPS HAT (D) mit INA219** (I2C Adresse: 0x43)
- **GNSS GPS HAT (MAX-M8Q)** (UART)
- **GPIO-Taster** an GPIO17 (Pin 11)

## Anschlüsse

Siehe `Wiring.txt` für Details zur Verkabelung.

## Projektstruktur

- `APRS-Pi-OLED-V2.3.py` – aktuelles Hauptskript für OLED-Betrieb
- `APRS-Pi-Console-V2.2.py` – Headless/Terminal-Version
- `OLD/` – Archiv früherer Versionen
- `Test-Scripts/` – Test- und Debug-Skripte
- `VERSION-HISTORY.txt` – Änderungsverlauf
- `README.md` – Diese Datei

## Voraussetzungen

- Python 3
- Empfohlene Pakete siehe `Test-Scripts/requirements-test-V1.0.py`

## Start

```bash
python3 APRS-Pi-OLED-V2.3.py
```

oder

```bash
python3 APRS-Pi-Console-V2.2.py
```

## Lizenz

Projektspezifisch, privat verwendet.
