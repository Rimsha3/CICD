provider "aws" {
  region = "us-east-1"
  access_key = "your_access_key"
  secret_key = "your_secret_key"
}

resource "aws_instance" "appd_ec2" {
  count         = 2  # Create two instances
  ami           = "AppD-image"  # Replace with the appropriate AMI ID
  instance_type = var.instance_type
  key_name      = "AppD-keypair"  # Replace with your key pair

  user_data = <<-EOF
              #!/bin/bash
              # Install AppDynamics agent
              wget -qO- https://download.appdynamics.com/download/prod/appdynamics-agents/AppDynamicsJavaAgent.zip -O /tmp/AppDynamicsJavaAgent.zip
              unzip /tmp/AppDynamicsJavaAgent.zip -d /opt
              # Configure and start the agent (using placeholders here, adapt as necessary)
              echo "controller.host=${var.appd_controller_host}" >> /opt/AppDynamicsJavaAgent/conf/controller-info.xml
              echo "controller.licenseKey=${var.appd_license_key}" >> /opt/AppDynamicsJavaAgent/conf/controller-info.xml
              EOF

  tags = {
    Name = "AppD EC2 Instance ${count.index + 1}"
  }
}

output "instance_public_ips" {
  value = aws_instance.appd_ec2[*].public_ip
}
