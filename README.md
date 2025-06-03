# ☁️ Cloud Attack Framework

Welcome to the **Cloud Attack Framework** project! This repository simulates a multi-stage cyber attack targeting both on-system backdoors and AWS cloud misuse.


## 🎯 Project Goals

- Deliver malware embedded in a PDF file  
- Establish a covert Command & Control (C2) channel using DNS or Tor with encrypted messaging  
- Achieve persistence on both Linux and Windows systems  
- Abuse AWS services using stolen credentials:  
  - List AWS services  
  - Upload malware to S3  
  - Launch fake ECS containers  
  - Track changes via Terraform  
- Detect the attack using:  
  - Falco (system behavior monitoring)  
  - Suricata (network traffic inspection)  
  - AWS CloudTrail (AWS API activity logs)   



## 🖥️ Lab Setup Overview

| VM Name         | Role                     | OS         | Tools Installed                 |
|-----------------|--------------------------|------------|--------------------------------|
| Attacker VM     | Attack launch & control  | Kali Linux | Python, Rust, Tor, Falco, Suricata           |
| Victim VM 1     | Windows target           | Windows 10 | Persistence scripts            |
| Victim VM 2     | Linux target             | Ubuntu     | Persistence scripts            |
| AWS Environment | Cloud resources( S3, EC2, ECS)          |     |            |



## 🖼️ Architecture Diagram

![image](https://github.com/user-attachments/assets/8b7a28e7-731b-4edb-b71d-dc79b86e9cc5)

## 📂 Repository Structure

```
cloud-attack-framework/
├── README.md
├── pdf_dropper/ # Python scripts to generate malware PDFs
├── c2/ # Command & Control server & client code
├── aws_abuse/ # AWS abuse automation scripts using boto3 & Terraform
├── persistence/ # Windows & Linux persistence scripts
├── detection/ # Falco and Suricata configuration rules
├── memory_forensics/ # Volatility3 Jupyter notebooks and memory dumps
├── diagrams/ # Architecture diagrams and flowcharts
└── screenshots/ # Screenshots showing attack phases and detections
```

## 🚀 How to Use

1. **Deploy VM Setup:** Prepare attacker and victim VMs as per architecture.  
2. **Run PDF Malware Generator:** Create malicious PDF and deliver it to victims.  
3. **Start C2 Server:** Launch the encrypted covert communication channel.  
4. **Establish Persistence:** Run OS-specific persistence scripts on target VMs.  
5. **Steal and Abuse AWS Credentials:** Use boto3 scripts to interact with AWS.  
6. **Monitor and Detect:** Deploy Falco and Suricata to catch suspicious activity.  
7. **Perform Memory Forensics:** Use Volatility3 to analyze memory dumps.


## 🎯 Attack Steps

### 1. Malware Delivery via PDF

- Created fake PDF on Kali Linux
```
python3 generate_pdf.py
 ```

- Delivered to Windows 10 using USB/HTTP method
```
python3 -m http.server 8888
```

- User opens PDF triggering PowerShell script (persistent C2 setup)

**Screenshots:**

![WhatsApp Image 2025-06-03 at 01 58 32_ba3b842c](https://github.com/user-attachments/assets/33ae7939-5461-4273-b5e4-759308fdd4dd)

![WhatsApp Image 2025-06-03 at 01 58 30_47fcbd79](https://github.com/user-attachments/assets/5ef9ac87-8a1d-453d-9d37-468ff8d8ebfd)


### 2. Command & Control (C2) 
The C2 server and client communicate using encrypted messages over covert channels (DNS or Tor), allowing stealthy remote control.
- TCP Socket
  - C2 Server (attacker-controlled, listens for connections)
    - Listens on a port
    - Accepts encrypted messages from clients
    - Sends back encrypted responses
```
python3 c2_server.py
```
  - C2 Client (backdoor) on the victim, which:
    - Connects to attacker
    - Decrypts command
    - Executes (e.g., whoami, ipconfig, etc.)
    - Encrypts and sends back output
```
python3 c2_cleint.py
```
**Screenshot:**

![WhatsApp Image 2025-06-03 at 01 58 34_88cdea76](https://github.com/user-attachments/assets/46b2acb6-87ca-423d-93cd-a9b8cc5dc433)

- DNS C2 Channel
  - Custom DNS server on Kali
  - PowerShell script on Windows sends queries (TXT records)
  - Receives commands covertly from DNS responses
```
python3 dns_c2_server.py
```
```
python3 dns_c2_cleint.py
```


### 3. Persistence on Target Systems  
- Persistence was achieved via scheduled tasks and registry edits.
```
$action = New-ScheduledTaskAction -Execute "python.exe" -Argument "C:\Users\Public\dns_c2_client.py"
$trigger = New-ScheduledTaskTrigger -AtLogOn
Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "DNS_C2_Client" -Description "Runs DNS C2 Client at user logon"
```

![WhatsApp Image 2025-06-03 at 01 58 34_859ed960](https://github.com/user-attachments/assets/ce6fdaab-de82-4db8-a533-35d60a77d120)


### 4. Detection Tools

4.1 Suricata - Used to detect abnormal DNS queries or packet anomalies

  Installed and configured on Kali:
```
sudo apt install suricata
sudo suricata -i <your_interface> -c /etc/suricata/suricata.yaml -l /var/log/suricata
```
  or via [Youtube video](https://www.youtube.com/watch?v=uXNhwduQve8)
  

**Screenshot:** 
```
tail -f /var/log/suricata/
```

![WhatsApp Image 2025-06-03 at 01 58 28_6fe142e1](https://github.com/user-attachments/assets/0a63a5f0-2fc8-4e45-8b97-e513a4a1d22e)


4.2 Falco

  Installed natively on Kali (no Docker dependency) using [Falco Documentation](https://falco.org/docs/getting-started/falco-linux-quickstart).
  
  Detects container execution, abnormal file writes, shell access
  
  Logs runtime events on Kali

**Screenshot:** 
![WhatsApp Image 2025-06-03 at 01 58 33_3f9511d2](https://github.com/user-attachments/assets/396c1e03-e323-48ad-a06d-04639924c936)


4.3 AWS CloudTrail

  Captures all API activity (S3 list, EC2 launch, IAM policy creation),
  Accessed via AWS Console or CLI 
  
**Screenshot:** 

![WhatsApp Image 2025-06-03 at 01 58 30_f80035e1](https://github.com/user-attachments/assets/2f6c023b-d62a-483f-99f8-7560290d944b)


### 5. AWS Cloud Abuse

- Boto3: Custom scripts to access S3, create tokens, enumerate services
- Example Abuse

  - Created EC2 from Kali
  - Listed S3 buckets and IAM users
  - Enabled public access to bucket
 
**Screenshot:**

```
python3 aws_abuse.py
```

![WhatsApp Image 2025-06-03 at 01 58 34_464fd9f8](https://github.com/user-attachments/assets/8ff0827d-1738-49eb-80d8-db7564f01ed9)

```
python3 advance_aws_abuse.py
```

![WhatsApp Image 2025-06-03 at 01 58 34_aed6a79d](https://github.com/user-attachments/assets/612f068e-ef02-4e4e-8e8c-dc5b0346e294)

- Initialize and deploy with Terraform:
```
terraform init
terraform plan
terraform apply
```
**Screenshot:** 

![WhatsApp Image 2025-06-03 at 01 58 32_a992567a](https://github.com/user-attachments/assets/7d8ce24f-069b-4322-9604-ac3cd531ae9e) 

### 6. Container Forensics (Volatility3)

## Steps:

- Launched an Alpine Docker container:
```
docker run -dit --name suspect alpine sh
```

- docker run -dit --name suspect alpine sh
```
PID=$(docker inspect -f '{{.State.Pid}}' suspect)
sudo gcore -o /tmp/container_dump $PID
```
- Captured memory using gcore:

PID=$(docker inspect -f '{{.State.Pid}}' suspect)
sudo gcore -o /tmp/container_dump $PID

Analyzed dump using Volatility3:
```
vol -f /tmp/container_dump.$PID linux.pslist
```

## 📺 Demo Video

- [Watch Demo Video](https://youtu.be/your-demo-link)   

## 🤝 Contributions

Contributions, bug reports, and feature requests are welcome! Please open an issue or submit a pull request.


## 📜 License

MIT License © 2025 Harshita Bhati


## 📧 Contact

For questions or feedback, reach out at [harshubhati51@gmail.com]

