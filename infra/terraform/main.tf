###############################################################################
# cllone - Provisionamento do cluster k3s no AWS Learner Lab
#
# Cria: 1 control-plane + N workers (default 3), um Security Group compartilhado
# e uma key pair. Ao final, gera automaticamente o inventory do Ansible.
#
# IMPORTANTE (AWS Learner Lab):
#   As credenciais são temporárias. Antes de rodar o Terraform exporte:
#     export AWS_ACCESS_KEY_ID=...
#     export AWS_SECRET_ACCESS_KEY=...
#     export AWS_SESSION_TOKEN=...
#     export AWS_DEFAULT_REGION=us-east-1
#   (copie de "AWS Details" no Learner Lab). Erro de auth = token expirado.
###############################################################################

terraform {
  required_version = ">= 1.3.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    local = {
      source  = "hashicorp/local"
      version = "~> 2.4"
    }
  }
}

provider "aws" {
  region = var.aws_region
  # As credenciais vêm das variáveis de ambiente do Learner Lab.
}

# ---------------------------------------------------------------------------
# AMI Ubuntu 22.04 LTS (Canonical) - mais recente
# ---------------------------------------------------------------------------
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# ---------------------------------------------------------------------------
# Key pair - usa a chave pública informada pelo aluno
# ---------------------------------------------------------------------------
resource "aws_key_pair" "cllone" {
  key_name   = var.key_name
  public_key = file(var.ssh_public_key_path)
}

# ---------------------------------------------------------------------------
# Security Group: SSH + Traefik (80/443) + API do k3s (6443) + NodePorts
# + todo o tráfego interno entre os nós (self)
# ---------------------------------------------------------------------------
resource "aws_security_group" "cluster" {
  name        = "${var.project_name}-sg"
  description = "cllone k3s cluster security group"

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.ssh_ingress_cidr]
  }

  ingress {
    description = "Traefik HTTP (frontend / e backend /api)"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Traefik HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "API do k3s (kubectl remoto)"
    from_port   = 6443
    to_port     = 6443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "NodePorts (ArgoCD, Adminer, etc.)"
    from_port   = 30000
    to_port     = 32767
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Tráfego irrestrito ENTRE os nós do cluster (flannel/VXLAN 8472, kubelet, etc.)
  ingress {
    description = "Trafego interno do cluster"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    self        = true
  }

  egress {
    description = "Saida irrestrita"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name    = "${var.project_name}-sg"
    Project = var.project_name
  }
}

# ---------------------------------------------------------------------------
# Control plane (1 instância)
# ---------------------------------------------------------------------------
resource "aws_instance" "control_plane" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = var.instance_type
  key_name               = aws_key_pair.cllone.key_name
  vpc_security_group_ids = [aws_security_group.cluster.id]

  root_block_device {
    volume_size = var.disk_size_gb
    volume_type = "gp3"
  }

  tags = {
    Name    = "${var.project_name}-control-plane"
    Role    = "server"
    Project = var.project_name
  }
}

# ---------------------------------------------------------------------------
# Workers (N instâncias - default 3, atende o requisito "3 ou mais")
# ---------------------------------------------------------------------------
resource "aws_instance" "worker" {
  count                  = var.worker_count
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = var.instance_type
  key_name               = aws_key_pair.cllone.key_name
  vpc_security_group_ids = [aws_security_group.cluster.id]

  root_block_device {
    volume_size = var.disk_size_gb
    volume_type = "gp3"
  }

  tags = {
    Name    = "${var.project_name}-worker-${count.index + 1}"
    Role    = "agent"
    Project = var.project_name
  }
}

# ---------------------------------------------------------------------------
# Geração automática do inventory do Ansible a partir dos IPs criados
# ---------------------------------------------------------------------------
resource "local_file" "ansible_inventory" {
  filename = "${path.module}/../ansible/inventory.ini"
  content = templatefile("${path.module}/templates/inventory.tmpl", {
    control_plane_public_ip  = aws_instance.control_plane.public_ip
    control_plane_private_ip = aws_instance.control_plane.private_ip
    worker_public_ips        = aws_instance.worker[*].public_ip
    ssh_private_key_file     = var.ssh_private_key_path
  })
}
