variable "aws_region" {
  description = "The AWS region to deploy into"
  default     = "us-east-1"
}

variable "instance_type" {
  description = "EC2 instance type"
  default     = "t2.micro"
}

variable "appd_license_key" {
  description = "AppDynamics license key"
  type        = string
}

variable "appd_controller_host" {
  description = "AppDynamics controller host"
  type        = string
}

