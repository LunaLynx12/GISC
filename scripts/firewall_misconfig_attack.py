# This script is for educational purposes only. Use it responsibly and legally.
# Misconfigure Firewall Script - by Beatrice Kateule

import subprocess
import re
from termcolor import colored

# Config
TARGET_IP = "192.168.123.62"  # pfSense IP (LAN)
INTERNAL_NET = "18.9.8.0/24"   # LAN subnet to scan
HIGH_RISK_PORTS = [21, 22, 80, 443, 3389, 445, 8080]

def run_cmd(cmd):
    try:
        result = subprocess.check_output(cmd, shell=True, stderr=subprocess.PIPE).decode()
        return result.strip()
    except subprocess.CalledProcessError as e:
        return colored(f"[!] Error: {e.stderr.decode()}", "red")

def check_firewall_rules():
    print(colored("\n[+] Checking pfSense firewall rules...", "blue"))
    rules = run_cmd("ssh admin@{} 'pfctl -sr'".format(TARGET_IP))

# Check for dangerous rules
    if "LAN_NETWORK to any" in rules:
        print(colored("[!] RISK: Unrestricted LAN-to-ANY rule found!", "yellow"))
    if "OPT2_NETWORK" in rules and "LAN_NETWORK" in rules:
        print(colored("[!] RISK: Cross-zone traffic allowed (LAN→OPT2)!", "yellow"))
    
    print(colored("[*] Current rules:\n" + rules, "cyan"))

def scan_ports():
    print(colored("\n[+] Scanning high-risk ports on internal networks...", "blue"))
    for port in HIGH_RISK_PORTS:
        result = run_cmd(f"nmap -Pn -p {port} {INTERNAL_NET} | grep open")
        if result:
            print(colored(f"[!] OPEN PORT: {port} on {result.split()[1]}", "red"))

def test_port_forwarding():
    print(colored("\n[+] Testing HTTP port forwarding...", "blue"))
    http_rule = run_cmd("ssh admin@{} 'pfctl -sr | grep \"port = http\"'".format(TARGET_IP))
    if http_rule:
        internal_ip = re.search(r"to (\d+\.\d+\.\d+\.\d+)", http_rule).group(1) 
    print(colored(f"[!] Port 80 forwarded to {internal_ip}. Testing for vulnerabilities...", "yellow"))
        vuln_scan = run_cmd(f"nikto -h http://{TARGET_IP}")
        print(colored(vuln_scan, "cyan"))

def main():
    print(colored("\n=== pfSense Misconfiguration Auditor ===", "green", attrs=["bold"]))
    check_firewall_rules()
    scan_ports()
    test_port_forwarding()

if __name__ == "__main__":
    main()
