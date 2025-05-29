# 📚  API School System

Uma API RESTful desenvolvida com Flask para gerenciamento de **alunos**, **professores** e **turmas**, cada um com seu respectivo CRUD (Create, Read, Update e Delete). O projeto está estruturado utilizando **Blueprints**, seguindo uma arquitetura inspirada no padrão MVC. A persistência de dados é feita com **SQLite**, com planos para futura migração para **MySQL**.

⚙️ Operações Disponíveis nas Entidades

Vocês podem realizar as seguintes operações com as entidades Aluno, Professor e Turma:

- Criar novos registros

- Deletar registros existentes

- Atualizar registros existentes

- Listar todos os registros

- Listar por ID registros específicos

Essas operações estão disponíveis através dos respectivos endpoints da API 😉 .
---

## 🛠 Tecnologias Utilizadas
- 🐍 Python + Flask

- 🛢️ SQLite (com futura migração para MySQL)

- 📘 Swagger com flask-restx

- 🧪 TDD com unittest e pytest

- 🐳 Docker

- ☁️ Render (Deploy automático)

- 🔧 Postman para testar os endpoints e o CRUD da API School System

## 🚀 Deploy

A API está hospedada no Render e pode ser acessada aqui:  
🔗 [https://api-school-system.onrender.com/](https://api-school-system.onrender.com/)


## 📑 Documentação Swagger

A documentação interativa da API está disponível via Swagger:  
🔗 [https://api-school-system.onrender.com/docs](https://api-school-system.onrender.com/docs)

---
### Exemplos de uso

- Listar todos os alunos:  
  `GET https://api-school-system.onrender.com/alunos`

- Buscar um professor por ID (exemplo com ID 2):  
  `GET https://api-school-system.onrender.com/professores/2`

- Listar todas as turmas:  
  `GET https://api-school-system.onrender.com/turmas`

---

## 🐳 Rodando com Docker

Caso prefiram rodar localmente com Docker:

### 1. Clone o repositório
```
git clone https://github.com/LarissaPiresDev/API---School-System.git
cd API---School-System
```
### 2. Build uma imagem do repositório
```
docker build -t school-api .
```
### 3. Execute o container
```
docker run --rm -d -p 5003:5003 --name school-api-container school-api
```
---

## 🛠🛠 Microsservissos que rodam com a Api School System
### - Criar atividades de acordo com o ID de professor [Clique Aqui para Acessar](https://github.com/LarissaPiresDev/Atividade)
### - Criar reservas de salas de acordo com o ID de turma [Clique aqui para Acessar](https://github.com/LarissaPiresDev/Reserva-salas)

## 📁 Estrutura do Projeto
```
API---School-System/
│
├── 📁 api/
│   ├── 📁 aluno/
│   │   ├── 🐍 aluno_routes.py
│   │   └── 🐍 aluno_models.py
│   ├── 📁 professor/
│   │   ├── 🐍 professor_routes.py
│   │   └── 🐍 professor_models.py
│   ├── 📁 turma/
│   │   ├── 🐍 turma_routes.py
│   │   └── 🐍 turma_models.py
│   ├── 📁 swagger/
│   │   ├── 🐍 __init__.py
│   │   ├── 🐍 swagger_config.py
│   │   └── 📁 namespace/
│   │       ├── 🐍 aluno_namespace.py
│   │       ├── 🐍 professor_namespace.py
│   │       └── 🐍 turma_namespace.py
│   ├── 📁 instance/
│   │   └── 🛢️ app.db
│   ├── 🐍 app.py
│   └── 🐍 config.py
│
├── 🐳 Dockerfile
├── 📄 requirements.txt
└── 📄 README.md
```
