# CLLone

A full-stack Kanban-style task management application built with **Python** (Django framework) on the backend and **JavaScript** with Vue 3 + Vite on the frontend.

---

## 🚀 Overview

This repository contains the backend and frontend components of the project:

- **backend/** – Django application (Python) providing a REST API and using SQLite for development.
- **frontend/** – Vue 3 single-page application (JavaScript/TypeScript) bundled with Vite.

---

## 📁 Repository Structure

```
backend/          # Django project (Python) — API REST
frontend/         # Vue 3 + Vite application (JavaScript)
infra/            # Infraestrutura como Código
  terraform/      #   provisiona EC2 no AWS Learner Lab (1 control plane + 3 workers)
  ansible/        #   instala k3s + ArgoCD e configura o cluster
docs/             # Documentação técnica (DOCUMENTACAO-TECNICA.md)
.github/workflows # CI/CD (GitHub Actions)
README.md         # This documentation
```

---

## 🚢 Infraestrutura, Kubernetes e Deploy contínuo (DevOps)

Este projeto vai além do código da aplicação: inclui provisionamento
automatizado em nuvem, cluster Kubernetes e deploy via GitOps.

- **Provisionamento (Terraform + Ansible):** veja [`infra/README.md`](infra/README.md).
  Cria um cluster **k3s** (1 control plane + 3 workers) na AWS e instala o **ArgoCD**.
- **Manifests / GitOps:** repositório separado
  [`cllone-gitops`](https://github.com/henrique-furtado47/cllone-gitops)
  (Kustomize + Traefik Ingress + Adminer).
- **CI/CD:** GitHub Actions em `.github/workflows/ci-cd.yml` — testa, builda e
  publica as imagens no Docker Hub e atualiza a tag no repo GitOps; o ArgoCD
  sincroniza o cluster.
- **Documentação técnica completa:** [`docs/DOCUMENTACAO-TECNICA.md`](docs/DOCUMENTACAO-TECNICA.md).

Fluxo resumido:

```
git push → GitHub Actions (testes → build → Docker Hub → bump tag no GitOps) → ArgoCD → k3s
                                                          Traefik: / → frontend, /api → backend
```

---

## 🛠 Requirements

- Python 3.12+ and pip (backend)
- Node.js 14+ and npm/yarn (frontend)
- Git (to clone the repo)

---

## 💻 Setup & Running

Instructions are provided for **Windows**, **macOS**, and **Linux**. Follow the appropriate section depending on your operating system.

### 🪟 Windows

1. **Clone the repository**
   ```powershell
   git clone https://github.com/henrique-furtado47/cllone.git
   cd cllone
   ```

2. **Backend (Python/Django)**
   ```powershell
   cd backend
   python -m venv venv
   venv\Scripts\Activate.ps1       # use `venv\Scripts\activate` if using cmd
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
   ```
   The API will be available at `http://127.0.0.1:8000`.

3. **Frontend (JavaScript/Vue 3)**
   ```powershell
   cd ..\frontend
   npm install                   # or `yarn`
   npm run dev                   # or `yarn dev`
   ```
   Access the app at `http://localhost:5173` (default Vite port).

### 🍎 macOS

1. **Clone the repository**
   ```bash
   git clone https://github.com/henrique-furtado47/cllone.git
   cd cllone
   ```

2. **Backend (Python/Django)**
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
   ```

3. **Frontend (JavaScript/Vue 3)**
   ```bash
   cd ../frontend
   npm install                   # or `yarn`
   npm run dev                   # or `yarn dev`
   ```

### 🐧 Linux

1. **Clone the repository**
   ```bash
   git clone https://github.com/henrique-furtado47/cllone.git
   cd cllone
   ```

2. **Backend (Python/Django)**
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
   ```

3. **Frontend (JavaScript/Vue 3)**
   ```bash
   cd ../frontend
   npm install                   # or `yarn`
   npm run dev                   # or `yarn dev`
   ```

---

## 🌐 API Documentation

The backend is a Django REST API. Visit the root URL to explore available endpoints. Authentication and other details are defined in code.

---

## 📚 License

This project is licensed under the [MIT License](LICENSE).

---

## 📘 Português / Portuguese

### 🚀 Visão Geral

Aplicação de gerenciamento de tarefas estilo Kanban desenvolvida com **Python** (framework Django) no backend e **JavaScript** com Vue 3 + Vite no frontend.

### 📁 Estrutura do Repositório

```
backend/          # Projeto Django (Python)
frontend/         # Aplicação Vue 3 + Vite (JavaScript)
README.md         # Esta documentação
```

### 🛠 Requisitos

- Python 3.12+ e pip (backend)
- Node.js 14+ e npm/yarn (frontend)
- Git (para clonar o repositório)

### 💻 Instalação & Execução

Siga as instruções conforme o seu sistema operacional.

#### 🪟 Windows

1. **Clone o repositório**
   ```powershell
   git clone https://github.com/henrique-furtado47/cllone.git
   cd cllone
   ```

2. **Backend (Python/Django)**
   ```powershell
   cd backend
   python -m venv venv
   venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
   ```

3. **Frontend (JavaScript/Vue 3)**
   ```powershell
   cd ..\frontend
   npm install
   npm run dev
   ```

#### 🍎 macOS

1. **Clone o repositório**
   ```bash
   git clone https://github.com/henrique-furtado47/cllone.git
   cd cllone
   ```

2. **Backend (Python/Django)**
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
   ```

3. **Frontend (JavaScript/Vue 3)**
   ```bash
   cd ../frontend
   npm install
   npm run dev
   ```

#### 🐧 Linux

1. **Clone o repositório**
   ```bash
   git clone https://github.com/henrique-furtado47/cllone.git
   cd cllone
   ```

2. **Backend (Python/Django)**
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
   ```

3. **Frontend (JavaScript/Vue 3)**
   ```bash
   cd ../frontend
   npm install
   npm run dev
   ```

---

### 📄 Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).
