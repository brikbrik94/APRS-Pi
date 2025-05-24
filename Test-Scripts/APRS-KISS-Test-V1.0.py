
import socket
import time

KISS_FEND = b'\xC0'

HOST = "127.0.0.1"
PORT = 8001

def decode_ax25(frame):
    try:
        frame = frame[:-2]
        dest = ''.join([chr(b >> 1) for b in frame[0:6]]).strip()
        src = ''.join([chr(b >> 1) for b in frame[7:13]]).strip()
        info = frame[16:].decode(errors='ignore')
        return f"{src} > {dest} | {info}"
    except Exception as e:
        return f"Fehler beim Dekodieren: {e}"

def read_kiss_frames(sock):
    buffer = b''
    sock.settimeout(1.0)
    last_keepalive = time.time()

    while True:
        try:
            data = sock.recv(1024)
            if not data:
                print("Verbindung geschlossen.")
                break
            buffer += data

            # Keep-alive alle 5 Sekunden
            if time.time() - last_keepalive > 5:
                try:
                    sock.sendall(b'\xC0\x00\xC0')
                except:
                    break
                last_keepalive = time.time()

            while KISS_FEND in buffer:
                parts = buffer.split(KISS_FEND)
                for i in range(len(parts) - 1):
                    frame = parts[i + 1]
                    if frame and frame[0] == 0x00:
                        ax25 = frame[1:]
                        print(decode_ax25(ax25))
                buffer = parts[-1]

        except socket.timeout:
            continue
        except Exception as e:
            print(f"Fehler beim Lesen: {e}")
            break

def main():
    while True:
        print("🔌 Verbinde zu KISS TCP auf 127.0.0.1:8001 ...")
        try:
            with socket.create_connection((HOST, PORT), timeout=5) as sock:
                print("✅ Verbindung hergestellt. Warte auf APRS Frames...
")
                read_kiss_frames(sock)
        except Exception as e:
            print(f"❌ Verbindung fehlgeschlagen: {e}")
        print("⏳ Neuer Versuch in 5 Sekunden...
")
        time.sleep(5)

if __name__ == "__main__":
    main()
