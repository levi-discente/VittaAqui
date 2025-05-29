# vittaAqui

**vittaAqui** é uma plataforma para agendamento e realização de consultas com profissionais de saúde, permitindo tanto atendimentos presenciais quanto online (telemedicina).  
O projeto contempla autenticação de usuários, controle de permissões, chat, cadastro de profissionais, e integrações com bancos de dados SQL/NoSQL e armazenamento de arquivos.

> **Este sistema é um trabalho da disciplina "Projeto e Prática I".**

---

## 🚀 Funcionalidades

- Cadastro e login de usuários e profissionais de saúde (clínico geral, nutricionista, psicólogo, fisioterapeuta, psiquiatra, personal trainer).
- Agendamento de consultas presenciais ou online.
- Chat com suporte a envio de anexos.
- Área do usuário para histórico, perfil, e documentos.
- API RESTful com autenticação JWT.
- Documentação automática via Swagger.

---

## 🧑‍💻 Como rodar localmente

### 1. **Pré-requisitos**

- [Go 1.21+](https://go.dev/doc/install)
- [Docker e Docker Compose](https://docs.docker.com/get-docker/)

### 2. **Clone o repositório**

```sh
git clone https://github.com/seu-usuario/vittaAqui.git
cd vittaAqui
```

### 3. **Configure as variáveis de ambiente**

Crie um arquivo `.env` baseado no `.env.example` fornecido:

```sh
cp .env.example .env
# Edite os valores conforme necessário (DB, JWT_SECRET, etc)
```

### 4. **Suba os bancos de dados**

```sh
docker compose up -d
```

Isso iniciará os serviços do PostgreSQL e MongoDB, usados pela aplicação.

### 5. **Instale as dependências Go**

```sh
go mod download
```

### 6. **(Opcional) Gere a documentação Swagger**

Se quiser atualizar a doc Swagger após mudanças nas rotas:

```sh
go install github.com/swaggo/swag/cmd/swag@latest
swag init
```

### 7. **Rode o servidor Go**

```sh
go run main.go
```

O servidor rodará por padrão em [http://localhost:8000](http://localhost:8000)

---

## 📑 Como acessar o Swagger (Documentação da API)

Com o servidor rodando, acesse:

```
http://localhost:8000/swagger/index.html
```

Aqui você pode testar os endpoints, autenticar com JWT e explorar toda a API REST da plataforma.

---

## 🗃️ Estrutura do Projeto

```
.
├── internal/
│   ├── config/
│   ├── handlers/
│   ├── middlewares/
│   ├── models/
│   ├── repositories/
│   ├── services/
│   └── utils/
├── main.go
├── docker-compose.yml
├── .env.example
├── go.mod
└── ...
```

---

## 👨‍🏫 Sobre

Este projeto foi desenvolvido como parte da disciplina **Projeto e Prática I** e tem fins acadêmicos, servindo de base para um sistema real de gestão e teleatendimento na área da saúde.

---

> **Atenção:** Não suba sua `.env` real no GitHub. Sempre use `.env.example` para o time.

---

**Sinta-se à vontade para sugerir melhorias ou contribuir!**
