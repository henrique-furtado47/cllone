output "control_plane_public_ip" {
  description = "IP público do control plane (SSH, kubectl remoto, Traefik, ArgoCD)"
  value       = aws_instance.control_plane.public_ip
}

output "control_plane_private_ip" {
  description = "IP privado do control plane (usado pelos workers para join no k3s)"
  value       = aws_instance.control_plane.private_ip
}

output "worker_public_ips" {
  description = "IPs públicos dos workers"
  value       = aws_instance.worker[*].public_ip
}

output "worker_private_ips" {
  description = "IPs privados dos workers"
  value       = aws_instance.worker[*].private_ip
}

output "app_url" {
  description = "URL da aplicação (Traefik na porta 80 do control plane)"
  value       = "http://${aws_instance.control_plane.public_ip}/"
}

output "ansible_inventory_path" {
  description = "Arquivo de inventory gerado para o Ansible"
  value       = local_file.ansible_inventory.filename
}
