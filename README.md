# ☁️ Cloud Attack Framework

Welcome to the **Cloud Attack Framework** project! This repository simulates a multi-stage cyber attack targeting both on-system backdoors and AWS cloud misuse.

---

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
  - Memory analysis with Volatility3  

---

## 🖥️ Lab Setup Overview

| VM Name         | Role                     | OS         | Tools Installed                 |
|-----------------|--------------------------|------------|--------------------------------|
| Attacker VM     | Attack launch & control  | Kali Linux | Python, Rust, Tor              |
| Victim VM 1     | Windows target           | Windows 10 | Persistence scripts            |
| Victim VM 2     | Linux target             | Ubuntu     | Persistence scripts            |
| Detection VM    | Monitoring & analysis    | Ubuntu     | Falco, Suricata, Volatility3  |
| AWS Environment | Cloud resources          | AWS EC2    | Boto3, Terraform               |

---

## 🖼️ Architecture Diagram

![Architecture Diagram](diagrams/architecture-diagram.png)

---
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
## 🎯 Project Overview & Tasks

### 1. PDF Malware Delivery  
Using Python, we generate a malicious PDF file that, when opened on the victim machine, drops malware to establish initial access.

**Screenshot:**  
![PDF Delivery](screenshots/pdf_delivery.png)

---

### 2. Command & Control (C2)  
The C2 server and client communicate using encrypted messages over covert channels (DNS or Tor), allowing stealthy remote control.

**Screenshot:**  
![C2 Channel Running](screenshots/c2_channel_running.png)

---

### 3. Persistence on Target Systems  
Scripts are implemented to ensure the malware starts on every reboot for both Linux and Windows machines, leveraging system services and startup files.

---

### 4. AWS Abuse & Cloud Exploitation  
Once AWS credentials are stolen, boto3 scripts list AWS services, upload malware payloads to S3, and launch fake ECS containers to maintain cloud presence. Terraform tracks AWS resource changes.

**Screenshot:**  
![AWS Abuse Output](screenshots/aws_abuse_output.png)

---

### 5. Detection & Monitoring  
Falco and Suricata monitor system behaviors and network traffic for suspicious activity, while AWS CloudTrail logs are reviewed for anomalous API calls.

**Screenshot:**  
![Falco Alert](screenshots/falco_alerts.png)

---

### 6. Memory Forensics  
Volatility3, integrated with Jupyter notebooks, inspects memory dumps inside Docker containers to uncover hidden malicious processes or artifacts.

---


---

## 🚀 How to Use

1. **Deploy VM Setup:** Prepare attacker and victim VMs as per architecture.  
2. **Run PDF Malware Generator:** Create malicious PDF and deliver it to victims.  
3. **Start C2 Server:** Launch the encrypted covert communication channel.  
4. **Establish Persistence:** Run OS-specific persistence scripts on target VMs.  
5. **Steal and Abuse AWS Credentials:** Use boto3 scripts to interact with AWS.  
6. **Monitor and Detect:** Deploy Falco and Suricata to catch suspicious activity.  
7. **Perform Memory Forensics:** Use Volatility3 to analyze memory dumps.  

---

## 📺 Demo Video

- [Watch Demo Video](https://youtu.be/your-demo-link)   

---

## 🤝 Contributions

Contributions, bug reports, and feature requests are welcome! Please open an issue or submit a pull request.

---

## 📜 License

MIT License © 2025 Harshita Bhati

---

## 📧 Contact

For questions or feedback, reach out at [harshubhati51@gmail.com]

