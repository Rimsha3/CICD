import boto3
import paramiko
import time
import requests
import os

# AWS EC2 client
ec2_client = boto3.client('ec2', region_name='us-east-1')  # Replace with your AWS region

# EC2 instance IDs (replace with your actual EC2 instance IDs or fetch dynamically)
instance_ids = ["i-xxxxxxxxxxxxxxxxx", "i-yyyyyyyyyyyyyyyy"]  # Replace with actual instance IDs

# The user to SSH into EC2 (change this depending on your AMI's user)
ssh_user = "ec2-user"  # For Amazon Linux, change if you're using a different AMI

# AppDynamics agent check endpoint (use an appropriate endpoint for your AppDynamics configuration)
appdynamics_check_url = "http://localhost:8080"  # Example check URL, adjust for your agent configuration

# Function to check if EC2 instance is running
def check_instance_running(instance_id):
    """
    Check if the EC2 instance is running.
    """
    response = ec2_client.describe_instances(InstanceIds=[instance_id])
    state = response['Reservations'][0]['Instances'][0]['State']['Name']
    valid_states = ['running', 'pending']  # Handle states like pending if necessary
    return state in valid_states

# Function to get the public IP address of the instance
def get_instance_ip(instance_id):
    """
    Get the public IP address of an EC2 instance.
    """
    response = ec2_client.describe_instances(InstanceIds=[instance_id])
    return response['Reservations'][0]['Instances'][0]['PublicIpAddress']

# Function to check if the AppDynamics agent is installed and running on the EC2 instance
def check_appdynamics_agent(ip):
    """
    Check if the AppDynamics agent is installed and running by accessing the agent's health check or status page.
    (This assumes AppDynamics exposes an HTTP status endpoint or service)
    """
    try:
        response = requests.get(f"http://{ip}:8080", timeout=10)  # Adjust timeout if needed
        if response.status_code == 200:
            print(f"AppDynamics agent is running on {ip}.")
            return True
        else:
            print(f"AppDynamics agent is not running on {ip}, status code: {response.status_code}.")
            return False
    except requests.RequestException as e:
        print(f"Error accessing AppDynamics agent on {ip}: {str(e)}")
        return False

# Function to SSH into EC2 instance and check if AppDynamics agent is installed
def check_appdynamics_agent_via_ssh(ip):
    """
    SSH into the EC2 instance and check if the AppDynamics agent is installed.
    """
    try:
        # SSH into EC2 instance
        key_path = os.environ.get("EC2_KEY_PATH", "/path/to/your/keypair.pem")  # Use environment variable for security
        key = paramiko.RSAKey.from_private_key_file(key_path)
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh_client.connect(ip, username=ssh_user, pkey=key)

        # Check if AppDynamics agent exists
        stdin, stdout, stderr = ssh_client.exec_command('ls /opt/AppDynamicsJavaAgent')
        output = stdout.read().decode('utf-8').strip()

        if output:
            print(f"AppDynamics agent is installed at /opt/AppDynamicsJavaAgent on {ip}.")
        else:
            print(f"AppDynamics agent is NOT installed on {ip}.")

        ssh_client.close()
    except Exception as e:
        print(f"Error SSH-ing into {ip}: {str(e)}")

# Main function to check all instances and the AppDynamics agent
def test_instances():
    """
    Run all tests for the infrastructure (EC2 instances and AppDynamics agent).
    """
    for instance_id in instance_ids:
        print(f"Checking EC2 instance {instance_id}...")

        # 1. Check EC2 instance status
        if check_instance_running(instance_id):
            print(f"EC2 instance {instance_id} is running.")
        else:
            print(f"EC2 instance {instance_id} is NOT running!")

        # 2. Get public IP for the instance
        ip = get_instance_ip(instance_id)
        print(f"Instance {instance_id} public IP: {ip}")

        # 3. Check if AppDynamics agent is running (via HTTP or SSH)
        print(f"Checking if AppDynamics agent is installed on {ip}...")
        if not check_appd
