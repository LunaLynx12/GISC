# -*- coding: utf-8 -*-

from ipaddress import ip_address

class Safeguards:
    @staticmethod
    def validate_target(target_ip: str):
        """Ensure target is within allowed private ranges"""
        private_ranges = [
            ("10.0.0.0", "10.255.255.255"),
            ("192.168.0.0", "192.168.255.255"),
            ("172.16.0.0", "172.31.255.255")
        ]
        
        ip = ip_address(target_ip)
        for start, end in private_ranges:
            if ip_address(start) <= ip <= ip_address(end):
                return True
        
        raise ValueError(f"Target {target_ip} not in private IP range")

    @staticmethod
    def enforce_limits(packet_count: int):
        """Limit attack scale"""
        max_packets = 5000  # Ethical ceiling
        if packet_count > max_packets:
            raise ValueError(f"Exceeded max packets ({max_packets})")