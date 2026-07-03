variable "aws_region" {
  description = "Região da AWS (Learner Lab normalmente us-east-1)"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Prefixo usado nos nomes/tags dos recursos"
  type        = string
  default     = "cllone"
}

variable "instance_type" {
  description = "Tipo das instâncias EC2 (t3.medium: 2 vCPU / 4 GB, suficiente para k3s)"
  type        = string
  default     = "t3.medium"
}

variable "worker_count" {
  description = "Quantidade de nós worker (>= 3 para atender ao requisito da avaliação)"
  type        = number
  default     = 3
}

variable "disk_size_gb" {
  description = "Tamanho do disco raiz de cada instância (GB)"
  type        = number
  default     = 20
}

variable "key_name" {
  description = "Nome da key pair criada na AWS"
  type        = string
  default     = "cllone-key"
}

variable "ssh_public_key_path" {
  description = "Caminho da chave pública SSH (ex.: ~/.ssh/cllone.pub)"
  type        = string
}

variable "ssh_private_key_path" {
  description = "Caminho da chave privada SSH usada pelo Ansible (ex.: ~/.ssh/cllone)"
  type        = string
}

variable "ssh_ingress_cidr" {
  description = "CIDR autorizado a acessar via SSH (use seu IP/32 para maior segurança; 0.0.0.0/0 para liberar)"
  type        = string
  default     = "0.0.0.0/0"
}
