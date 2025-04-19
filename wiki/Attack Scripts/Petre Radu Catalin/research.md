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
# TO FILL
```

Ransomware Rqport

~~image here~~

Fig 1.2: Simulation report showing encrypted test files and recovery key

### Intelligent Port Scanner
Purpose: Enhanced DVWA service discovery

Code Structure:

```python
#!/bin/python3
# TO FILL
```

Port Scan Report

~~image here~~

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

- ransomware_template.html [link]

- portscan_template.html [link]

