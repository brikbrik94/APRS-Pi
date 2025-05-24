# APRS Pi – OLED Monitor Projekt

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Ein multifunktionales APRS- und Systemmonitoring-Projekt auf Basis eines Raspberry Pi 4B mit OLED-Display-Anzeige.

## 🔧 Funktionen

- Anzeige von GPS-Zeit & Positionsdaten (über `gpsd`)
- APRS "Last heard"-Callsign via Direwolf (KISS TCP)
- Systemressourcen-Monitor (CPU, RAM, Disk, Temperatur, Uptime)
- Akkuüberwachung (Spannung, Strom, Ladezustand) über UPS HAT (INA219)
- GPX-Logging bei GPS-Fix
- Seitenumschaltung per GPIO-Taster, Rücksprung nach 30 s zur Hauptseite

## 🖥️ Screenshot

*(Ein Screenshot der OLED-Anzeige kann hier ergänzt werden)*

## 🧰 Voraussetzungen

### 🐍 Python 3 + Bibliotheken

Installiere notwendige Pakete:

```bash
pip install -r Test-Scripts/requirements-test-V1.0.py
```

### 📦 Installierte Software

- **gpsd** – GPS-Daemon zur Kommunikation mit GNSS-Modulen  
  👉 https://gpsd.io/

- **Direwolf** – APRS-Encoder/Decoder, verwendet KISS TCP  
  👉 https://github.com/wb2osz/direwolf

- **rigctl** (aus `hamlib`) – optional zur Steuerung von Funkgeräten  
  👉 https://sourceforge.net/projects/hamlib/

Optional: `gpxlogger` für kontinuierliches Tracking (läuft über gpsd)

## ⚙️ Hardware

| Komponente                | Beschreibung / Link |
|--------------------------|---------------------|
| Raspberry Pi 4B          | https://www.raspberrypi.com/products/raspberry-pi-4-model-b/ |
| OLED 2.42" (I2C, SH1106) | https://www.waveshare.com/2.42inch-oled-module.htm |
| UPS HAT (D) mit INA219   | https://www.waveshare.com/ups-hat-d.htm |
| GNSS MAX-M8Q GPS HAT     | https://www.waveshare.com/max-m8q-gnss-hat.htm|
| Taster (GPIO17)          | Standard-Taster, z. B. https://www.reichelt.at/taster |

Details zu den Anschlüssen: siehe `Wiring.txt`

## 📁 Projektstruktur

```
APRS-Pi/
├── APRS-Pi-OLED-V2.3.py             # OLED-Version (aktuell)
├── APRS-Pi-Console-V2.2.py          # Terminal-Version
├── OLD/                             # Vorherige Releases
├── Test-Scripts/                    # Testtools & Anforderungen
├── Wiring.txt                       # Hardware-Anschlussübersicht
├── VERSION-HISTORY.txt              # Änderungsverlauf
├── LICENSE                          # MIT-Lizenz
└── README.md                        # Diese Datei
```

## ▶️ Start

```bash
python3 APRS-Pi-OLED-V2.3.py
# oder
python3 APRS-Pi-Console-V2.2.py
```

## 📄 Lizenz

Dieses Projekt steht unter der MIT-Lizenz – siehe [LICENSE](LICENSE) für Details.

## 🙋 Mitwirken

Vorschläge, Fehlerberichte oder Erweiterungen sind willkommen!
