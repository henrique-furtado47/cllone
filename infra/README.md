# Infraestrutura como Código — cllone

Provisionamento automatizado do cluster **k3s** (1 control plane + 3 workers) no
**AWS Learner Lab** com **Terraform**, configuração com **Ansible** e instalação
do **ArgoCD** para o deploy via GitOps.

```
infra/
├── terraform/          # Provisiona as instâncias EC2 + Security Group + key pair
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── terraform.tfvars.example
│   └── templates/inventory.tmpl   # gera o inventory do Ansible automaticamente
└── ansible/            # Instala k3s (server+agents) e ArgoCD
    ├── ansible.cfg
    ├── playbook.yml
    ├── group_vars/all.yml
    └── inventory.ini.example
```

## Pré-requisitos

- Terraform >= 1.3, Ansible, `curl`, um par de chaves SSH
- Sessão ativa do AWS Learner Lab

Gere as chaves SSH (uma vez):

```bash
ssh-keygen -t ed25519 -f ~/.ssh/cllone -N ""
```

## 1. Credenciais do Learner Lab

No painel do Learner Lab clique em **AWS Details → AWS CLI** e copie as
credenciais temporárias para o seu terminal:

```bash
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
export AWS_SESSION_TOKEN=...
export AWS_DEFAULT_REGION=us-east-1
```

> As credenciais expiram quando a sessão reinicia. Erro de autenticação no
> Terraform normalmente = token expirado (basta reexportar).

## 2. Provisionar (Terraform)

```bash
cd infra/terraform
cp terraform.tfvars.example terraform.tfvars   # ajuste os caminhos das chaves
terraform init
terraform plan
terraform apply -auto-approve
```

Ao final, o Terraform imprime os IPs e **gera `infra/ansible/inventory.ini`**
automaticamente a partir dos endereços das instâncias.

```bash
terraform output
```

## 3. Configurar o cluster (Ansible)

```bash
cd ../ansible
ansible all -m ping                 # valida a conectividade SSH
ansible-playbook playbook.yml
```

O playbook:

1. Instala o **k3s server** no control plane (Traefik já vem embutido);
2. Captura o `node-token` e junta os **3 workers** como agents;
3. Instala o **ArgoCD** e o expõe via NodePort;
4. Cria o namespace `cllone` e o `Secret` da aplicação (fora do Git);
5. Registra a **Application** do ArgoCD apontando para o repo `cllone-gitops`.

Ao final, ele imprime a URL/senha do ArgoCD e a URL da aplicação.

> Troque os segredos numa entrega real:
> `ansible-playbook playbook.yml -e postgres_password='...' -e cllone_secret_key='...'`

## 4. Acesso remoto com kubectl (opcional)

```bash
scp -i ~/.ssh/cllone ubuntu@<IP_PUBLICO_CONTROL_PLANE>:/etc/rancher/k3s/k3s.yaml ~/.kube/cllone.yaml
# troque 127.0.0.1 pelo IP público do control plane:
sed -i 's/127.0.0.1/<IP_PUBLICO_CONTROL_PLANE>/' ~/.kube/cllone.yaml
export KUBECONFIG=~/.kube/cllone.yaml
kubectl get nodes -o wide
```

## 5. Destruir tudo (economiza créditos)

```bash
cd infra/terraform
terraform destroy -auto-approve
```

## Endereços após o deploy

| Serviço            | URL                                              |
|--------------------|--------------------------------------------------|
| Frontend           | `http://<IP_CONTROL_PLANE>/`                     |
| Backend (API)      | `http://<IP_CONTROL_PLANE>/api/`                 |
| Swagger            | `http://<IP_CONTROL_PLANE>/api/docs/`            |
| Adminer (banco)    | `http://<IP_CONTROL_PLANE>:30800/`               |
| ArgoCD             | `https://<IP_CONTROL_PLANE>:<nodeport>` (admin)  |
