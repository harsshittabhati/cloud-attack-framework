import boto3
import os
import time
import json

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

# Step 5: EC2 instance management - launch or use existing
print("\n[+] EC2 instance management:")

choice = input("[?] Enter 'new' to launch a new EC2 instance or 'existing' to specify an instance ID: ").strip().lower()

if choice == "existing":
    instance_id = input("[?] Enter the existing EC2 Instance ID: ").strip()
    print(f"[+] Using existing EC2 instance: {instance_id}")

elif choice == "new":
    print("[+] Launching a new EC2 instance as post-compromise foothold...")
    try:
        response = ec2.run_instances(
            ImageId='ami-0c94855ba95c71c99',  # Amazon Linux 2 AMI (update if needed)
            MinCount=1,
            MaxCount=1,
            InstanceType='t2.micro',
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [{'Key': 'Name', 'Value': 'PostCompromiseInstance'}]
                }
            ]
        )
        instance_id = response['Instances'][0]['InstanceId']
        print(f"[+] EC2 instance launched successfully. Instance ID: {instance_id}")
        print("[*] Waiting 60 seconds for instance to initialize...")
        time.sleep(60)  # Wait for instance to initialize before actions
    except Exception as e:
        print(f"[!] Failed to launch EC2 instance: {e}")
        instance_id = None
else:
    print("[!] Invalid choice. Skipping EC2 instance management.")
    instance_id = None

# If we have a valid instance ID, allow further actions
if instance_id:
    while True:
        print("\n[+] Available EC2 actions:")
        print("1. Start instance")
        print("2. Stop instance")
        print("3. Terminate instance")
        print("4. Run command (via SSM)")
        print("5. Exit")

        action = input("[?] Choose an action (1-5): ").strip()

        if action == '1':
            try:
                ec2.start_instances(InstanceIds=[instance_id])
                print(f"[+] Start command sent to instance {instance_id}")
            except Exception as e:
                print(f"[!] Failed to start instance: {e}")

        elif action == '2':
            try:
                ec2.stop_instances(InstanceIds=[instance_id])
                print(f"[+] Stop command sent to instance {instance_id}")
            except Exception as e:
                print(f"[!] Failed to stop instance: {e}")

        elif action == '3':
            confirm = input(f"[!] Are you sure you want to TERMINATE instance {instance_id}? (yes/no): ").strip().lower()
            if confirm == 'yes':
                try:
                    ec2.terminate_instances(InstanceIds=[instance_id])
                    print(f"[+] Terminate command sent to instance {instance_id}")
                    break  # Exit after termination
                except Exception as e:
                    print(f"[!] Failed to terminate instance: {e}")
            else:
                print("[*] Termination cancelled.")

        elif action == '4':
            ssm = session.client('ssm')
            command = input("[?] Enter the shell command to run on the instance: ").strip()
            try:
                response = ssm.send_command(
                    InstanceIds=[instance_id],
                    DocumentName="AWS-RunShellScript",
                    Parameters={'commands': [command]}
                )
                command_id = response['Command']['CommandId']
                print(f"[+] Command sent with Command ID: {command_id}")
            except Exception as e:
                print(f"[!] Failed to run command via SSM: {e}")

        elif action == '5':
            print("[*] Exiting EC2 management.")
            break

        else:
            print("[!] Invalid choice. Please select a number between 1-5.")

# Step 6: Launch a Fake ECS Container
print("\n[+] Launching Fake Container in ECS...")

# Validate or create ECS cluster before proceeding
print("\n[+] Validating ECS Clusters:")
account_id = session.client("sts").get_caller_identity()["Account"]
available_clusters = ecs.list_clusters()["clusterArns"]
cluster_names = [arn.split('/')[-1] for arn in available_clusters]

print("[+] Existing ECS Clusters:")
for name in cluster_names:
    print(f"- {name}")

CLUSTER_NAME = input("[?] Enter ECS cluster name to launch container: ").strip()

if CLUSTER_NAME not in cluster_names:
    print(f"[!] Cluster '{CLUSTER_NAME}' not found. Creating new ECS cluster...")
    try:
        ecs.create_cluster(clusterName=CLUSTER_NAME)
        print(f"[+] Cluster '{CLUSTER_NAME}' created successfully.")
    except Exception as e:
        print(f"[!] Failed to create ECS cluster: {e}")
        exit(1)
else:
    print(f"[+] Using existing cluster: {CLUSTER_NAME}")

CONTAINER_NAME = "fake-container"
TASK_NAME = "fake-task"
FAKE_IMAGE = "public.ecr.aws/amazonlinux/amazonlinux:latest"

# Create Task Execution Role (if not exists)
iam = session.client("iam")
role_name = "ecsTaskExecutionRole"

try:
    iam.get_role(RoleName=role_name)
    print(f"[+] IAM role '{role_name}' already exists.")
except iam.exceptions.NoSuchEntityException:
    print("[+] Creating IAM Role for ECS Task Execution...")
    assume_role_policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {"Service": "ecs-tasks.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }]
    }
    iam.create_role(
        RoleName=role_name,
        AssumeRolePolicyDocument=json.dumps(assume_role_policy)
    )
    iam.attach_role_policy(
        RoleName=role_name,
        PolicyArn="arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
    )
    print("[+] IAM role created and policy attached.")

# Register Task Definition
try:
    print("[+] Registering task definition...")
    task_def = ecs.register_task_definition(
        family=TASK_NAME,
        networkMode="awsvpc",
        requiresCompatibilities=["FARGATE"],
        cpu="256",
        memory="512",
        executionRoleArn=f"arn:aws:iam::{session.client('sts').get_caller_identity()['Account']}:role/{role_name}",
        containerDefinitions=[{
            "name": CONTAINER_NAME,
            "image": FAKE_IMAGE,
            "essential": True,
            "command": ["sleep", "3600"]
        }]
    )
    print("[+] Task definition registered.")

    # Run Task
    print("[+] Running ECS task...")
    response = ecs.run_task(
        cluster=CLUSTER_NAME,
        launchType="FARGATE",
        taskDefinition=TASK_NAME,
        count=1,
        networkConfiguration={
            "awsvpcConfiguration": {
                "subnets": ["subnet-XXXXXXXXXXXX"],  # <-- Replace with actual subnet
                "assignPublicIp": "ENABLED"
            }
        }
    )
    print("[+] Fake container launched in ECS.")
except Exception as e:
    print(f"[!] Failed to launch ECS container: {e}")
