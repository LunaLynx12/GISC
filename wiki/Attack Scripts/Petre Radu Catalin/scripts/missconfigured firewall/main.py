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
