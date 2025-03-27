# This script is for educational purposes only. Use it responsibly and legally.
# Port scanning Script - by Posea Alina

import socket
from concurrent.futures import ThreadPoolExecutor

dmz_ip = "192.168.1.1"  # Replace with DMZ IP
private_network_ip = "10.0.0.1"  # Replace with private network IP
ports_to_scan = [22, 80, 443, 8080, 3306, 53, 21]
timeout = 1  # Timeout in seconds for socket connections
max_workers = 10  # Max workers for the thread pool

def scan_port(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((ip, port))

            if result == 0:
                print(f"Port {port} is open on {ip}")
    except socket.error as err:
        print(f"Error scanning {ip}:{port} - {err}")

def port_scan(ip, ports):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(lambda port: scan_port(ip, port), ports)

def main():
    print(f"Scanning ports on DMZ IP: {dmz_ip}")
    port_scan(dmz_ip, ports_to_scan)
    
    print(f"\nScanning ports on private network IP: {private_network_ip}")
    port_scan(private_network_ip, ports_to_scan)

if __name__ == "__main__":
    main()