variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "ami_id" {
  description = "AMI ID for the EC2 instance (e.g., Ubuntu 22.04)"
  type        = string
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"
}

variable "key_name" {
  description = "Name of the AWS key pair for SSH access"
  type        = string
}

variable "docker_image" {
  description = "Full Docker image name including tag (e.g., ghcr.io/user/repo:latest)"
  type        = string
}
