# 📡 APRS Pi – OLED Monitor for Raspberry Pi

A compact, Python-based APRS monitoring system for Raspberry Pi. It displays real-time GPS, APRS, and system data on a 2.42" I2C OLED screen.

---

## 🧭 Project Overview

APRS Pi uses:
- **Direwolf** to decode APRS packets (via KISS TCP)
- **gpsd** to retrieve GPS data
- **Pillow + Adafruit SSD1306** for OLED display rendering
- Optionally: **INA219 UPS HAT** for voltage monitoring

It is designed to run headless and includes support for systemd startup and GPX logging.

---

## 🧱 Hardware Requirements

| Component                    | Link                                                                 |
|-----------------------------|----------------------------------------------------------------------|
| Raspberry Pi 4B             | https://www.raspberrypi.com/products/raspberry-pi-4-model-b/         |
| 2.42" OLED (SH1106, I2C)    | https://www.waveshare.com/wiki/2.42inch_OLED_Module                  |
| GNSS HAT (MAX-M8Q, UART)    | https://www.waveshare.com/wiki/GNSS_HAT_(B)                          |
| UPS HAT (D) with INA219     | https://www.waveshare.com/wiki/UPS_HAT_(D)                           |
| Push button (GPIO17)        | https://www.reichelt.at/taster-smd-omron-b3f-1000-p16802.html        |

👉 Wiring schematic: [`docs/wiring.svg`](docs/wiring.svg)

---

## 📦 Software Requirements (Summary)

This project depends on the following software tools:

| Component         | Purpose                            |
|------------------|------------------------------------|
| **gpsd**          | GPS interface and SHM time source  |
| **pps-tools**     | PPS synchronization (optional)     |
| **ntp**           | Accurate system time (via PPS)     |
| **hamlib-utils**  | rig control testing via `rigctl`   |
| **Direwolf**      | APRS decoding (KISS TCP mode)      |
| **Python 3**      | Runtime environment                |
| **Adafruit SSD1306** + Pillow | OLED rendering         |

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

- [OLED Setup](https://github.com/brikbrik94/APRS-Pi/wiki/OLED-Pages)
- [Hardware Details](https://github.com/brikbrik94/APRS-Pi/wiki/Hardware-Setup)
- [Troubleshooting](https://github.com/brikbrik94/APRS-Pi/wiki/Troubleshooting)
- [Changelog](https://github.com/brikbrik94/APRS-Pi/wiki/Changelog)

---

## 📜 License

This project is licensed under the MIT License.

---

## 🤝 Contributing

Pull requests and suggestions are always welcome!
