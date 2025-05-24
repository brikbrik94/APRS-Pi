# 🔧 Installation Guide – APRS Pi (Raspberry Pi 4B)

This guide walks you through installing the required packages and tools to run the APRS Pi OLED monitoring setup on Raspberry Pi OS (Debian-based).

---

## 📦 System Requirements

- Raspberry Pi OS (Lite or Full)
- Python 3.x
- Internet access (apt, git)
- UART & I2C enabled in `raspi-config`

---

## 1. 🛰 GPSD & PPS Setup

### Install gpsd and tools

```bash
sudo apt update
sudo apt install gpsd gpsd-clients gpsd-tools libgps-dev
```

### Configure gpsd

```bash
sudo nano /etc/default/gpsd
```

Update the file:

```
USBAUTO="false"
DEVICES="/dev/ttyS0 /dev/pps0"
GPSD_OPTIONS="-n"
```

Restart service:

```bash
sudo systemctl restart gpsd
```

Test GPS:

```bash
cgps
```

---

## 2. 🕒 PPS & NTP Configuration (Optional, but recommended)

```bash
sudo apt install pps-tools
sudo nano /boot/config.txt
```

Append:

```
dtoverlay=pps-gpio
```

Enable PPS on every boot:

```bash
sudo nano /etc/modules
```

Add:

```
pps-gpio
```

Test with:

```bash
sudo ppstest /dev/pps0
```

### Install and configure NTP

```bash
sudo apt install ntp
sudo nano /etc/ntp.conf
```

Add to the end:

```
# PPS
server 127.127.22.0 minpoll 4 maxpoll 4
fudge 127.127.22.0 refid PPS
fudge 127.127.22.0 flag3 1

# GPS via gpsd
server 127.127.28.0 minpoll 4 maxpoll 4 prefer
fudge 127.127.28.0 refid GPS
fudge 127.127.28.0 time1 +0.130
```

Restart and check:

```bash
sudo systemctl restart ntp
ntpq -p
```

---

## 3. 📶 Hamlib (for rigctl)

```bash
sudo apt install hamlib-utils
```

Test:

```bash
rigctl -l
```

---

## 4. 📡 Direwolf – APRS Decoder

> ⚠️ **Important:** gpsd and hamlib must be installed before building Direwolf.

### Install build tools and clone repo

```bash
sudo apt install git cmake libasound2-dev
git clone https://github.com/wb2osz/direwolf.git
cd direwolf
mkdir build && cd build
cmake ..
make -j4
sudo make install
```

Optional: install man pages and icons

```bash
sudo make install-man
sudo make install-conf
```

Run Direwolf:

```bash
direwolf -t 0 -n 1 -c ~/direwolf.conf
```

---

## 5. 🧪 Optional Tools

- `gpxlogger` – GPS track logging:  
  https://gpsd.gitlab.io/gpsd/gpxlogger.html
- `ppstest`, `ntpq` – PPS & time diagnostics

---

## ✅ Final Notes

- Test `rigctl` for device listing
- Test `cgps` and `gpxlogger` for GPS data
- Check `ntpq -p` for GPS/PPS synchronization
- Confirm Direwolf KISS TCP mode with your APRS script
