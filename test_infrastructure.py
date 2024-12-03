import boto3
import pytest
import time

# Configure your AWS resources for testing (these would be the names or IDs of the resources created by Terraform)
EC2_INSTANCE_ID = "i-xxxxxxxxxxxxxxxxx"
APPDYNAMICS_AGENT_HOST = "your-appdynamics-agent-host"

# Initialize the boto3 EC2 client
ec2 = boto3.client('ec2', region_name='us-east-1')

# Test if EC2 instance is running
def test_ec2_instance_running():
    response = ec2.describe_instances(InstanceIds=[EC2_INSTANCE_ID])
    assert len(response['Reservations']) > 0
    instance = response['Reservations'][0]['Instances'][0]
    assert instance['State']['Name'] == 'running', f"EC2 instance {EC2_INSTANCE_ID} is not running."

# Optionally, add a delay for the AppDynamics agent setup to allow time for the agent to start
def test_appdynamics_agent_installed():
    # Make sure the EC2 instance is up and running first
    time.sleep(60)  # Wait for the agent to initialize on the EC2 instance (if needed)
    
    # This could be an HTTP check to ensure that the AppDynamics agent is serving data
    # For example, using requests to make sure the agent is responding on a specific port or endpoint
    import requests
    url = f'http://{APPDYNAMICS_AGENT_HOST}:8090/agent'
    response = requests.get(url)
    
    assert response.status_code == 200, f"AppDynamics agent is not reachable at {url}."

# Example test to check if S3 bucket exists
def test_s3_bucket_exists():
    s3 = boto3.client('s3', region_name='us-east-1')
    bucket_name = "your-deployment-bucket"
    try:
        response = s3.head_bucket(Bucket=bucket_name)
        assert response['ResponseMetadata']['HTTPStatusCode'] == 200, f"S3 bucket {bucket_name} does not exist or is not accessible."
    except s3.exceptions.ClientError as e:
        assert False, f"S3 bucket {bucket_name} does not exist or is not accessible. Error: {e}"

# You could add more tests for other resources depending on your infrastructure
