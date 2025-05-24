# APRS PI OLED V2.1

import os
import time
import datetime
import subprocess
import socket
import psutil
import gps
import smbus
import RPi.GPIO as GPIO
from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from luma.core.render import canvas
from PIL import ImageFont

# === KISS-TCP APRS-Funktion ===
def get_aprs_kiss_frame(mycall="OE5ITH", host="127.0.0.1", port=8001, timeout=2):
    try:
        with socket.create_connection((host, port), timeout=timeout) as sock:
            sock.settimeout(timeout)
            sock.sendall(b'\xC0\x00\xC0')
            data = sock.recv(1024)
            if not data:
                return "APRS: No Data"
            parts = data.split(b'\xC0')
            for part in parts:
                if part and part[0] == 0x00:
                    ax25 = part[1:-2]
                    dest = ''.join([chr(b >> 1) for b in ax25[0:6]]).strip()
                    src = ''.join([chr(b >> 1) for b in ax25[7:13]]).strip()
                    info = ax25[16:].decode(errors='ignore').strip()
                    return f"{src} > {dest} | {info}" if mycall in src else f"{src} RX"
    except Exception as e:
        return f"APRS Error: {e}"
    return "APRS: No Frame"

# === Setup ===
MYCALL = "OE5ITH"
BUTTON_GPIO = 17
OLED_PAGES = 4
AUTO_RESET_SECONDS = 30

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)

serial = i2c(port=1, address=0x3C)
device = sh1106(serial)
font = ImageFont.load_default()

page = 0
last_input_time = time.time()
session = gps.gps(mode=gps.WATCH_ENABLE)
bus = smbus.SMBus(1)
ina219_addr = 0x43

# === Button-Callback ===
def toggle_page(channel):
    global page, last_input_time
    page = (page + 1) % OLED_PAGES
    last_input_time = time.time()

GPIO.add_event_detect(BUTTON_GPIO, GPIO.FALLING, callback=toggle_page, bouncetime=300)

# === Hilfsfunktionen ===
def get_cpu_temp():
    try:
        output = os.popen("vcgencmd measure_temp").readline()
        return output.replace("temp=", "").strip()
    except:
        return "N/A"

def get_gps_status():
    try:
        report = session.next()
        if report['class'] == 'TPV':
            fix = hasattr(report, 'lat') and hasattr(report, 'lon')
            return "OK" if fix else "No Fix"
    except:
        pass
    return "No Fix"

def get_gps_coords():
    try:
        report = session.next()
        if report['class'] == 'TPV':
            lat = getattr(report, 'lat', 0.0)
            lon = getattr(report, 'lon', 0.0)
            alt = getattr(report, 'alt', 0.0)
            return lat, lon, alt
    except:
        pass
    return 0.0, 0.0, 0.0

def get_gps_sats():
    try:
        report = session.next()
        if report['class'] == 'SKY':
            return sum(1 for sat in report.satellites if sat.used)
    except:
        pass
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
            if line.startswith("*"):
                parts = line.split()
                return parts[0], parts[1], parts[8], parts[9]
    except:
        pass
    return "NTP", "?", "?", "?"

# === Display-Seiten ===
def draw_page1(draw):
    cpu = psutil.cpu_percent()
    temp = get_cpu_temp()
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    gps = get_gps_status()
    sats = get_gps_sats()
    bat_percent, bat_voltage, _, bat_state = get_battery_status()
    uptime = time.strftime("%H:%M:%S", time.gmtime(time.time() - psutil.boot_time()))

    draw.text((0, 0),  f"CPU: {cpu:.1f}% | Temp: {temp}", font=font, fill=255)
    draw.text((0, 10), f"RAM: {mem:.0f}%   | Disk: {disk:.0f}%", font=font, fill=255)
    draw.text((0, 20), f"GPS: {gps} | Sats: {sats}", font=font, fill=255)
    left = f"Bat: {bat_percent:.0f}%"
    right = f"{bat_voltage:.2f}V {bat_state}".rjust(15)
    draw.text((0, 30), f"{left} |{right}", font=font, fill=255)
    draw.text((0, 40), get_aprs_kiss_frame(MYCALL), font=font, fill=255)
    draw.text((0, 50), f"Uptime: {uptime}", font=font, fill=255)

def draw_page2(draw):
    lat, lon, alt = get_gps_coords()
    sats = get_gps_sats()
    bat_percent, voltage, current, _ = get_battery_status()
    draw.text((0, 0), f"Lat: {lat:.5f} Lon: {lon:.5f}", font=font, fill=255)
    draw.text((0, 10), f"Alt: {alt:.0f}m   Sats: {sats}", font=font, fill=255)
    draw.text((0, 20), f"Last: {get_aprs_kiss_frame(MYCALL).strip()}", font=font, fill=255)
    draw.text((0, 30), f"Bat: {voltage:.2f}V  {current:.0f}mA", font=font, fill=255)

def draw_page3(draw):
    percent, _, _, _ = get_battery_status()
    bar = int(percent // 5)
    draw.text((0, 0), "Akkuverlauf (Platzhalter)", font=font, fill=255)
    draw.text((0, 20), f"{percent:.0f}% [" + ("█" * bar) + ("." * (20 - bar)) + "]", font=font, fill=255)

def draw_page4(draw):
    src, refid, offset, jitter = get_ntpq_info()
    now = datetime.datetime.utcnow().strftime("%H:%M:%S")
    gps = get_gps_status()
    sats = get_gps_sats()
    draw.text((0, 0), f"Time src: {src} {refid}", font=font, fill=255)
    draw.text((0, 10), f"Offset:  {offset} ms", font=font, fill=255)
    draw.text((0, 20), f"Jitter:  {jitter} ms", font=font, fill=255)
    draw.text((0, 30), f"SysTime: {now} UTC", font=font, fill=255)
    draw.text((0, 40), f"GPS: {gps} | Sats: {sats}", font=font, fill=255)

# === Hauptloop ===
while True:
    with canvas(device) as draw:
        if time.time() - last_input_time > AUTO_RESET_SECONDS:
            page = 0
        if page == 0:
            draw_page1(draw)
        elif page == 1:
            draw_page2(draw)
        elif page == 2:
            draw_page3(draw)
        elif page == 3:
            draw_page4(draw)
    time.sleep(5)
