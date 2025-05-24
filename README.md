# 📡 APRS Pi – OLED Monitor for Raspberry Pi

&#x20;

A compact, Python-based APRS monitoring system for Raspberry Pi. It displays real-time GPS, APRS, and system data on a 2.42" I2C OLED screen.

---

## 🧭 Project Overview

APRS Pi uses:

* [**Direwolf**](https://github.com/wb2osz/direwolf) to decode APRS packets (via KISS TCP)
* [**gpsd**](https://gpsd.io/) to retrieve GPS data
* [**luma.oled**](https://github.com/rm-hull/luma.oled) for OLED display rendering
* Optionally: [**INA219 UPS HAT**](https://www.waveshare.com/wiki/UPS_HAT_%28D%29) for voltage monitoring

It is designed to run headless and includes support for systemd startup and GPX logging.

---

## 🧱 Hardware Requirements

| Component                                                                             | Description                 |
| ------------------------------------------------------------------------------------- | --------------------------- |
| [Raspberry Pi 4B](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/)       | Raspberry Pi mainboard      |
| [2.42" OLED (SH1106, I2C)](https://www.waveshare.com/wiki/2.42inch_OLED_Module)       | OLED display for output     |
| [GNSS HAT (MAX-M8Q, UART)](https://www.waveshare.com/wiki/GNSS_HAT_%28B%29)           | GPS module                  |
| [UPS HAT (D) with INA219](https://www.waveshare.com/wiki/UPS_HAT_%28D%29)             | Power backup and monitoring |
| [Push button (GPIO17)](https://www.reichelt.at/taster-smd-omron-b3f-1000-p16802.html) | Manual page switching       |

👉 Wiring schematic: [`docs/wiring.svg`](docs/wiring.svg)

---

## 📦 Software Requirements (Summary)

This project depends on the following software tools:

| Component                                                                                    | Purpose                           |
| -------------------------------------------------------------------------------------------- | --------------------------------- |
| [**gpsd**](https://gpsd.io/)                                                                 | GPS interface and SHM time source |
| [**pps-tools**](https://github.com/redlab-i/pps-tools)                                       | PPS synchronization (optional)    |
| [**ntp**](https://www.ntp.org/)                                                              | Accurate system time (via PPS)    |
| [**hamlib-utils**](https://sourceforge.net/projects/hamlib/)                                 | rig control testing via `rigctl`  |
| [**Direwolf**](https://github.com/wb2osz/direwolf)                                           | APRS decoding (KISS TCP mode)     |
| [**Python 3**](https://www.python.org/)                                                      | Runtime environment               |
| [**luma.oled**](https://github.com/rm-hull/luma.oled) + [Pillow](https://python-pillow.org/) | OLED rendering                    |

📖 For step-by-step installation instructions, visit:
👉 [Installation Guide (Wiki)](https://github.com/brikbrik94/APRS-Pi/wiki/Installation)

---

## 🚀 Getting Started

Run Direwolf:

```bash
direwolf -t 0 -n 1 -c ~/direwolf.conf
```

Launch OLED script:

```bash
python3 APRS-Pi-OLED-V2.3.py
```

Enable automatic startup using `systemd`:
👉 [Systemd Service Setup](https://github.com/brikbrik94/APRS-Pi/wiki/Systemd-Service)

---

## 📖 Documentation

Full project documentation is available in the GitHub Wiki:
👉 [APRS Pi Wiki](https://github.com/brikbrik94/APRS-Pi/wiki)

* [OLED Setup](https://github.com/brikbrik94/APRS-Pi/wiki/OLED-Pages)
* [Hardware Details](https://github.com/brikbrik94/APRS-Pi/wiki/Hardware-Setup)
* [Troubleshooting](https://github.com/brikbrik94/APRS-Pi/wiki/Troubleshooting)
* [Changelog](https://github.com/brikbrik94/APRS-Pi/wiki/Changelog)

---

## 📜 License

This project is licensed under the MIT License.

---

## 🤝 Contributing

Pull requests and suggestions are always welcome!
