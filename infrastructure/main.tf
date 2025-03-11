terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.38.0"
    }
  }
}

provider "aws" {
  region = "us-east-2"
}

# Configuración de la instancia EC2
resource "aws_instance" "deepseek_server" {
  ami                    = "ami-0884d2865dbe9de4b"  # Ubuntu 22.04 LTS
  instance_type          = "g4dn.xlarge"            # GPU NVIDIA T4
  key_name               = "R1"            # Nombre de tu clave SSH en AWS
  vpc_security_group_ids = [aws_security_group.deepseek_sg.id]

  tags = {
    Name = "deepseek-v3-server"
  }
}

# Grupo de seguridad para permitir tráfico HTTP y SSH
resource "aws_security_group" "deepseek_sg" {
  name        = "deepseek-sg"
  description = "Permitir trafico HTTP y SSH"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Restringe esto a tu IP en producción
  }

  ingress {
    from_port   = 80
    to_port     = 80
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
