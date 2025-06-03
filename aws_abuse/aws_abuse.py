import boto3
import os

# Use default AWS profile or environment credentials
session = boto3.Session(
    region_name='us-east-1'  # or your preferred region
)
ec2 = session.client("ec2")
s3 = session.client("s3")
ecs = session.client("ecs")

# Step 1: List EC2 Instances
print("[+] Listing EC2 Instances:")
ec2_response = ec2.describe_instances()
for reservation in ec2_response["Reservations"]:
    for instance in reservation["Instances"]:
        print(f"- Instance ID: {instance['InstanceId']} | State: {instance['State']['Name']}")

# Step 2: List S3 Buckets
print("\n[+] Listing S3 Buckets:")
s3_response = s3.list_buckets()
for bucket in s3_response["Buckets"]:
    print(f"- {bucket['Name']}")

# Step 3: Upload a File to S3 (Simulated Malware)
MALWARE_FILE = "fake_malware.txt"
BUCKET_NAME = input("\n[?] Enter target S3 bucket name to upload malware: ")

# Create a fake file
with open(MALWARE_FILE, "w") as f:
    f.write("This is a simulated malware payload.")

try:
    print(f"[+] Uploading {MALWARE_FILE} to S3 bucket {BUCKET_NAME}...")
    s3.upload_file(MALWARE_FILE, BUCKET_NAME, MALWARE_FILE)
    print("[+] Upload successful!")
except Exception as e:
    print(f"[!] Upload failed: {e}")

# Step 4: Launch a Fake ECS Task
print("\n[+] Listing ECS Clusters:")
clusters = ecs.list_clusters()["clusterArns"]

if not clusters:
    print("[!] No ECS clusters found. Skipping ECS launch.")
else:
    cluster_arn = clusters[0]
    print(f"[+] Using cluster: {cluster_arn}")
    print("[!] ECS task launch is a placeholder here. Manual task definition may be required.")
    # Add ECS task launch code here as needed.

# Cleanup
os.remove(MALWARE_FILE)
