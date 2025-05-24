# APRS PI Console V2.1

import os
import time
import datetime
import subprocess
import socket
import psutil
import gps
import smbus

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
session = gps.gps(mode=gps.WATCH_ENABLE)
bus = smbus.SMBus(1)
ina219_addr = 0x43

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

# === Anzeige aller Seiten in Konsole ===
def show_page1():
    print("=== Seite 1: System & Status ===")
    print(f"CPU: {psutil.cpu_percent():.1f}% | Temp: {get_cpu_temp()}")
    print(f"RAM: {psutil.virtual_memory().percent:.0f}% | Disk: {psutil.disk_usage('/').percent:.0f}%")
    print(f"GPS: {get_gps_status()} | Sats: {get_gps_sats()}")
    bat_percent, bat_voltage, _, bat_state = get_battery_status()
    print(f"Bat: {bat_percent:.0f}% | {bat_voltage:.2f}V {bat_state}")
    print(get_aprs_kiss_frame(MYCALL))
    uptime = time.strftime("%H:%M:%S", time.gmtime(time.time() - psutil.boot_time()))
    print(f"Uptime: {uptime}")
    print("-" * 50)

def show_page2():
    print("=== Seite 2: GPS & Akku ===")
    lat, lon, alt = get_gps_coords()
    print(f"Lat: {lat:.5f} Lon: {lon:.5f}")
    print(f"Alt: {alt:.0f}m | Sats: {get_gps_sats()}")
    print(f"Last: {get_aprs_kiss_frame(MYCALL).strip()}")
    _, voltage, current, _ = get_battery_status()
    print(f"Bat: {voltage:.2f}V  {current:.0f}mA")
    print("-" * 50)

def show_page3():
    print("=== Seite 3: Akkuverlauf ===")
    percent, _, _, _ = get_battery_status()
    bar = int(percent // 5)
    print(f"Akkuladung: {percent:.0f}% [{'█' * bar}{'.' * (20 - bar)}]")
    print("-" * 50)

def show_page4():
    print("=== Seite 4: Zeit & Quelle ===")
    src, refid, offset, jitter = get_ntpq_info()
    now = datetime.datetime.utcnow().strftime("%H:%M:%S")
    print(f"Time src: {src} {refid}")
    print(f"Offset: {offset} ms | Jitter: {jitter} ms")
    print(f"SysTime: {now} UTC")
    print(f"GPS: {get_gps_status()} | Sats: {get_gps_sats()}")
    print("-" * 50)

# === Hauptloop ===
def main():
    while True:
        os.system("clear")
        show_page1()
        show_page2()
        show_page3()
        show_page4()
        time.sleep(10)

if __name__ == "__main__":
    main()
