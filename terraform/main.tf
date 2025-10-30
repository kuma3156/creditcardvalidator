provider "aws" {
  region = var.aws_region
}

# Security Group to allow HTTP and SSH
resource "aws_security_group" "fastapi_sg" {
  name        = "fastapi_sg"
  description = "Allow SSH and HTTP"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# EC2 instance
resource "aws_instance" "fastapi_app" {
  ami           = var.ami_id       # Update with Linux AMI ID
  instance_type = var.instance_type
  key_name      = var.key_name
  security_groups = [aws_security_group.fastapi_sg.name]

  # Install Docker & run container
  user_data = <<-EOF
              #!/bin/bash
              sudo yum update -y
              sudo yum install docker -y
              sudo docker pull ghcr.io/kuma3156/creditcardvalidator/creditcardvalidatorapi:latest
              docker run -d -p 8000:8000 ghcr.io/kuma3156/creditcardvalidator/creditcardvalidatorapi:latest
              EOF

  tags = {
    Name = "fastapi-validator"
  }
}
