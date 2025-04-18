# -*- coding: utf-8 -*-
import argparse
import time
import sys
from syn_attack import SYNFlooder
from report_generator import AttackReporter

def main():
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
        
        # Execute attack
        attacker = SYNFlooder(args.target, args.port)
        attacker.send_flood(args.count)
        
        # Generate report if requested
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

if __name__ == "__main__":
    main()