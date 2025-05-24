# APRS PI OLED SPI V2.2 – für Waveshare 2.42" OLED (SSD1309, 128x64 SPI)

import os
import time
import datetime
import subprocess
import socket
import psutil
import gps
import smbus
import threading
from luma.core.interface.serial import spi
from luma.oled.device import ssd1309
from luma.core.render import canvas
from PIL import ImageFont

# === Display-Setup ===
serial = spi(device=0, port=0, gpio_DC=25, gpio_RST=24)
device = ssd1309(serial, width=128, height=64)
font = ImageFont.load_default()

# === GPS Listener ===
class GPSListener(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self.session = gps.gps(mode=gps.WATCH_ENABLE)
        self.last_tpv = None
        self.last_sky = None
        self.running = True

    def run(self):
        while self.running:
            try:
                report = self.session.next()
                if report['class'] == 'TPV':
                    self.last_tpv = report
                elif report['class'] == 'SKY':
                    self.last_sky = report
            except:
                continue

    def stop(self):
        self.running = False

# === APRS KISS Listener ===
class KISSListener(threading.Thread):
    def __init__(self, mycall="OE5ITH", host="127.0.0.1", port=8001):
        super().__init__(daemon=True)
        self.host = host
        self.port = port
        self.mycall = mycall
        self.latest_frame = "APRS: No Frame"
        self.running = True

    def run(self):
        while self.running:
            try:
                with socket.create_connection((self.host, self.port), timeout=10) as sock:
                    sock.settimeout(2.0)
                    buffer = b''
                    while self.running:
                        try:
                            data = sock.recv(1024)
                            if not data:
                                break
                            buffer += data
                            parts = buffer.split(b'\xC0')
                            for part in parts:
                                if part and part[0] == 0x00 and len(part) > 16:
                                    ax25 = part[1:-2]
                                    dest = ''.join([chr(b >> 1) for b in ax25[0:6]]).strip()
                                    src = ''.join([chr(b >> 1) for b in ax25[7:13]]).strip()
                                    info = ax25[16:].decode(errors='ignore').strip()
                                    if self.mycall in src:
                                        self.latest_frame = f"{src} > {dest} | {info}"
                                    else:
                                        self.latest_frame = f"{src} RX"
                            buffer = parts[-1]
                        except socket.timeout:
                            continue
                        except Exception:
                            break
            except Exception:
                self.latest_frame = "APRS: Verbindung fehlgeschlagen"
                time.sleep(5)

    def stop(self):
        self.running = False

# === Setup ===
MYCALL = "OE5ITH"
gps_listener = GPSListener()
gps_listener.start()
aprs = KISSListener(mycall=MYCALL)
aprs.start()
bus = smbus.SMBus(1)
ina219_addr = 0x43
page = 0

# === Funktionen ===
def get_cpu_temp():
    try:
        return os.popen("vcgencmd measure_temp").readline().replace("temp=", "").strip()
    except:
        return "N/A"

def get_gps_status():
    tpv = gps_listener.last_tpv
    return "OK" if tpv and hasattr(tpv, 'lat') else "No Fix"

def get_gps_coords():
    tpv = gps_listener.last_tpv
    if tpv:
        lat = getattr(tpv, 'lat', 0.0)
        lon = getattr(tpv, 'lon', 0.0)
        alt = getattr(tpv, 'alt', 0.0)
        return lat, lon, alt
    return 0.0, 0.0, 0.0

def get_gps_sats():
    sky = gps_listener.last_sky
    if sky and hasattr(sky, 'satellites'):
        return sum(1 for sat in sky.satellites if hasattr(sat, 'used') and sat.used)
    return 0

def get_battery_status():
    try:
        raw_voltage = bus.read_word_data(ina219_addr, 0x02)
        voltage = ((raw_voltage & 0xFF) << 8 | (raw_voltage >> 8)) * 0.004
        raw_current = bus.read_word_data(ina219_addr, 0x04)
        current = raw_current if raw_current < 32768 else raw_current - 65536
        current *= 0.1524
        percent = max(0, min(100, (voltage - 3.0) / 1.2 * 100))
        status = "CHG" if current > 10 else "DSCH" if current < -10 else "---"
        return percent, voltage, current, status
    except:
        return 0, 0.0, 0.0, "Err"

def get_ntpq_info():
    try:
        lines = subprocess.check_output(["ntpq", "-p"]).decode().splitlines()
        for line in lines:
            if line.startswith(('*', '+', '#', 'x', 'o')):
                parts = line.split()
                if len(parts) >= 10:
                    return parts[0], parts[1], parts[8], parts[9]
        return "NoSync", "-", "-", "-"
    except:
        return "NTP", "?", "?", "?"

# === Anzeige-Funktionen ===
def draw_page(draw, page):
    if page == 0:
        cpu = psutil.cpu_percent()
        temp = get_cpu_temp()
        mem = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        gps = get_gps_status()
        sats = get_gps_sats()
        bat_percent, bat_voltage, _, bat_state = get_battery_status()
        uptime = time.strftime("%H:%M:%S", time.gmtime(time.time() - psutil.boot_time()))

        draw.text((0, 0), f"CPU:{cpu:.0f}% T:{temp}", font=font, fill=255)
        draw.text((0, 10), f"RAM:{mem:.0f}% DSK:{disk:.0f}%", font=font, fill=255)
        draw.text((0, 20), f"GPS:{gps} Sats:{sats}", font=font, fill=255)
        draw.text((0, 30), f"BAT:{bat_percent:.0f}% {bat_voltage:.2f}V", font=font, fill=255)
        draw.text((0, 40), aprs.latest_frame[:24], font=font, fill=255)
        draw.text((0, 50), f"Uptime:{uptime}", font=font, fill=255)

    elif page == 1:
        lat, lon, alt = get_gps_coords()
        sats = get_gps_sats()
        draw.text((0, 0), f"Lat:{lat:.5f}", font=font, fill=255)
        draw.text((0, 10), f"Lon:{lon:.5f}", font=font, fill=255)
        draw.text((0, 20), f"Alt:{alt:.0f}m Sats:{sats}", font=font, fill=255)
        draw.text((0, 30), aprs.latest_frame[:24], font=font, fill=255)

    elif page == 2:
        percent, _, _, _ = get_battery_status()
        bar = int(percent // 5)
        draw.text((0, 0), "Akku:", font=font, fill=255)
        draw.text((0, 20), f"[{bar * '█'}{(20 - bar) * '.'}]", font=font, fill=255)

    elif page == 3:
        src, refid, offset, jitter = get_ntpq_info()
        now = datetime.datetime.utcnow().strftime("%H:%M:%S")
        draw.text((0, 0), f"SRC:{src} REF:{refid}", font=font, fill=255)
        draw.text((0, 10), f"Off:{offset} Jit:{jitter}", font=font, fill=255)
        draw.text((0, 20), f"UTC:{now}", font=font, fill=255)

# === Mainloop ===
try:
    while True:
        with canvas(device) as draw:
            draw_page(draw, page)
        page = (page + 1) % 4
        time.sleep(10)
except KeyboardInterrupt:
    aprs.stop()
    gps_listener.stop()
