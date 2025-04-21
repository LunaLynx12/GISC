import socket
from utils import RISKY_PORTS

def grab_banner(ip, port):
    try:
        with socket.socket() as s:
            s.settimeout(2)
            s.connect((ip, port))
            if port == 80:
                s.sendall(b"GET / HTTP/1.0\r\nHost: localhost\r\n\r\n")
            return s.recv(1024).decode(errors="ignore").strip()
    except:
        return "N/A"

def scan_target(ip):
    findings = []
    for port, service in RISKY_PORTS.items():
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(2)
                result = s.connect_ex((ip, port))
                if result == 0:
                    banner = grab_banner(ip, port)
                    findings.append({
                        "port": port,
                        "service": service,
                        "banner": banner
                    })
        except Exception:
            continue
    return findings
