import shutil
import importlib.util
import socket

def check_module(name):
    result = importlib.util.find_spec(name) is not None
    print(f"Modul '{name}': {'OK' if result else 'FEHLT'}")
    return result

def check_program(cmd):
    result = shutil.which(cmd) is not None
    print(f"Programm '{cmd}': {'OK' if result else 'FEHLT'}")
    return result

def check_port(host, port, label):
    try:
        s = socket.create_connection((host, port), timeout=2)
        s.close()
        print(f"{label} ({host}:{port}): OK")
        return True
    except Exception as e:
        print(f"{label} ({host}:{port}): FEHLT ({e})")
        return False

def check_i2c_device(addr):
    try:
        import smbus
        bus = smbus.SMBus(1)
        bus.read_byte(addr)
        print(f"I2C-Gerät bei 0x{addr:02X}: OK")
        return True
    except Exception as e:
        print(f"I2C-Gerät bei 0x{addr:02X}: FEHLT ({e})")
        return False

def main():
    print("=== Systemvoraussetzungen für OLED-Monitor prüfen ===\n")

    modules = ['gps', 'smbus', 'psutil', 'PIL', 'luma.core', 'luma.oled']
    for mod in modules:
        check_module(mod)

    print()
    programmes = ['gpxlogger', 'ntpq']
    for prog in programmes:
        check_program(prog)

    print()
    check_port("127.0.0.1", 2947, "gpsd")
    check_port("127.0.0.1", 8000, "AGWPE-Port (Direwolf)")
    check_i2c_device(0x43)

    print("\n=== Prüfung abgeschlossen ===")

if __name__ == "__main__":
    main()
