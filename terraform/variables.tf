variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "ami_id" {
  description = "AMI ID for the EC2 instance (e.g., Ubuntu 22.04)"
  type        = string
  default     = "ami-0bdd88bd06d16ba03"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"
}

variable "key_name" {
  description = "Name of the AWS key pair for SSH access"
  type        = string
  default     = "kuma"
}
