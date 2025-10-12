# VittaAqui

<!--toc:start-->

- [VittaAqui](#vittaaqui)
  - [🚀 Stack Tecnológica](#🚀-stack-tecnológica)
  - [📋 Pré-requisitos](#📋-pré-requisitos)
  - [🔧 Instalação](#🔧-instalação)
    - [Opção 1: Docker (Recomendado)](#opção-1-docker-recomendado)
    - [Opção 2: Local com uv](#opção-2-local-com-uv)
  - [🐳 Docker](#🐳-docker)
    - [Comandos Úteis](#comandos-úteis)
    - [Modo Desenvolvimento (Automático)](#modo-desenvolvimento-automático)
    - [Dados de Exemplo (Seed)](#dados-de-exemplo-seed)
  - [✨ Funcionalidades Principais](#funcionalidades-principais)
    - [🏥 Sistema de Agendamentos](#🏥-sistema-de-agendamentos)
    - [🔐 Autenticação e Autorização](#🔐-autenticação-e-autorização)
    - [📊 Compatibilidade Frontend](#📊-compatibilidade-frontend)
  - [📦 Estrutura do Projeto](#📦-estrutura-do-projeto)
  - [🔐 Autenticação](#🔐-autenticação)
  - [📝 Migrations](#📝-migrations)
  - [🌐 API Endpoints](#🌐-api-endpoints)
    - [🔐 Autenticação (`/api/auth`)](#🔐-autenticação-apiauth)
      - [**POST /api/auth/register**](#post-apiauthregister)
      - [**POST /api/auth/login**](#post-apiauthlogin)
    - [👤 Usuários (`/api/users` ou `/api/user`)](#👤-usuários-apiusers-ou-apiuser)
    - [👨‍⚕️ Profissionais (`/api/professionals` ou `/api/professional`)](#👨‍️-profissionais-apiprofessionals-ou-apiprofessional)
      - [**GET /api/professionals/** ou **GET /api/professional/list**](#get-apiprofessionals-ou-get-apiprofessionallist)
      - [**GET /api/professionals/{profile_id}**](#get-apiprofessionalsprofileid)
      - [**GET /api/professional/profile/user/{user_id}**](#get-apiprofessionalprofileuseruserid)
      - [**GET /api/professionals/me**](#get-apiprofessionalsme)
      - [**POST /api/professionals/**](#post-apiprofessionals)
      - [**PUT /api/professionals/{profile_id}** ou **PUT /api/professionals/me**](#put-apiprofessionalsprofileid-ou-put-apiprofessionalsme)
      - [**GET /api/professionals/{profile_id}/appointments**](#get-apiprofessionalsprofileidappointments)
      - [**GET /api/professionals/{profile_id}/available-slots**](#get-apiprofessionalsprofileidavailable-slots)
    - [📅 Agendamentos (`/api/appointments`)](#📅-agendamentos-apiappointments)
      - [**POST /api/appointments/**](#post-apiappointments)
      - [**GET /api/appointments/my** ou **GET /api/appointments/my-appointments**](#get-apiappointmentsmy-ou-get-apiappointmentsmy-appointments)
      - [**GET /api/appointments/{appointment_id}**](#get-apiappointmentsappointmentid)
      - [**PUT /api/appointments/{appointment_id}**](#put-apiappointmentsappointmentid)
      - [**DELETE /api/appointments/{appointment_id}**](#delete-apiappointmentsappointmentid)
    - [🔑 Autenticação em Rotas Protegidas](#🔑-autenticação-em-rotas-protegidas)
  - [🧪 Testes](#🧪-testes)
  - [🔍 Qualidade de Código](#🔍-qualidade-de-código)
  - [📚 Documentação](#📚-documentação)
  - [📝 Notas Importantes](#📝-notas-importantes)
    - [Validações](#validações)
    - [Comportamentos](#comportamentos)
    - [Categorias Profissionais](#categorias-profissionais)
    - [Status de Agendamento](#status-de-agendamento)
  - [🤝 Contribuindo](#🤝-contribuindo)
  - [📄 Licença](#📄-licença)
  <!--toc:end-->

Plataforma de telemedicina e agendamento de consultas desenvolvida com **FastAPI**, **SQLAlchemy 2.0**, **Alembic** e **uv**.

> Este sistema é um trabalho da disciplina "Projeto e Prática I".

## 🚀 Stack Tecnológica

- **FastAPI** - Framework web moderno e rápido
- **SQLAlchemy 2.0** - ORM com suporte async
- **Alembic** - Migrations de banco de dados
- **Pydantic v2** - Validação de dados
- **PostgreSQL** - Banco de dados relacional
- **uv** - Gerenciador de pacotes ultra-rápido
- **Ruff** - Linter e formatter
- **Docker** - Containerização

## 📋 Pré-requisitos

- Python 3.12+
- PostgreSQL 15+
- Docker e Docker Compose
- uv (opcional, mas recomendado)

## 🔧 Instalação

### Opção 1: Docker (Recomendado)

```bash
cp .env.example .env

docker compose up --build
```

Acesse: <http://localhost:8000/docs>

### Opção 2: Local com uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh

cd VittaAqui
uv venv
source .venv/bin/activate

uv sync

cp .env.example .env

docker compose up -d postgres

alembic upgrade head

uvicorn app.main:app --reload
```

## 🐳 Docker

### Comandos Úteis

```bash
docker compose up --build

docker compose up -d

docker compose logs -f app

docker compose down

docker compose down -v
```

### Modo Desenvolvimento (Automático)

O Docker Compose verifica a variável `DEBUG` no `.env`:

**DEBUG=True** (Modo Dev):

1. ✅ Aguarda PostgreSQL estar pronto
2. ✅ Verifica se existem migrations
3. ✅ Se não existir, cria automaticamente com `alembic revision --autogenerate`
4. ✅ Aplica migrations com `alembic upgrade head`
5. ✅ Executa `init_db.py` (fallback)
6. ✅ **Popula banco com dados de exemplo** (`seed_db.py`)
7. ✅ Inicia aplicação

**DEBUG=False** (Produção):

- Executa apenas migrations existentes
- Não popula dados de exemplo

**Tudo funciona com um único comando:** `docker compose up`

### Dados de Exemplo (Seed)

O banco é automaticamente populado com:

- **2 pacientes** (João, Maria)
- **3 profissionais** (Dr. Carlos - Médico, Dra. Ana - Nutricionista, Dr. Roberto - Psicólogo)
- **Senha padrão**: `senha123`
- **CPFs válidos** e únicos

**Logins disponíveis:**

- `joao@example.com` (Paciente - CPF: 529.982.247-25)
- `maria@example.com` (Paciente - CPF: 714.287.938-60)
- `carlos@example.com` (Médico - CPF: 863.783.451-20)
- `ana@example.com` (Nutricionista - CPF: 458.426.216-50)
- `roberto@example.com` (Psicólogo - CPF: 291.658.734-91)

## ✨ Funcionalidades Principais

### 🏥 Sistema de Agendamentos

- **Criação automática de perfil profissional** ao registrar com `role=professional`
- **Cálculo de horários disponíveis** baseado em:
  - Horários de atendimento configurados
  - Dias da semana disponíveis
  - Datas bloqueadas
  - Agendamentos existentes
- **Filtros avançados** para buscar profissionais (nome, categoria, tags, tipo de atendimento)
- **Validação de conflitos** de horários
- **Gerenciamento de status** (pending, confirmed, completed, cancelled)

### 🔐 Autenticação e Autorização

- **JWT tokens** com expiração configurável
- **Validação de CPF** no registro
- **Senha mínima de 8 caracteres**
- **Rotas protegidas** por role (patient/professional)

### 📊 Compatibilidade Frontend

- **Rotas com aliases** para compatibilidade (`/api/user` e `/api/users`)
- **Form-urlencoded** para registro e login
- **Timezone automático** (remove timezone de datetime)
- **Strings vazias tratadas** como `null` em filtros

## 📦 Estrutura do Projeto

```
app/
├── main.py                 # Aplicação FastAPI
├── core/
│   ├── config.py          # Configurações (env vars)
│   ├── database.py        # Setup do banco de dados
│   └── security.py        # JWT e hashing de senhas
├── models/                # Modelos SQLAlchemy
│   ├── user.py
│   ├── professional.py
│   └── appointment.py
├── schemas/               # Schemas Pydantic
│   ├── user.py
│   ├── professional.py
│   └── appointment.py
├── api/
│   ├── deps.py           # Dependências (auth, db)
│   └── v1/               # Rotas da API v1
│       ├── auth.py
│       ├── users.py
│       ├── professionals.py
│       └── appointments.py
├── crud/                 # Operações de banco de dados
├── services/             # Lógica de negócio
└── utils/                # Utilitários e exceções
```

## 🔐 Autenticação

A API usa **JWT (JSON Web Tokens)**.

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "email=user@example.com&password=senha123"

curl http://localhost:8000/api/users/me \
  -H "Authorization: Bearer SEU_TOKEN"
```

## 📝 Migrations

```bash
alembic revision --autogenerate -m "Descrição"

alembic upgrade head

alembic downgrade -1

alembic history
```

## 🌐 API Endpoints

### 🔐 Autenticação (`/api/auth`)

#### **POST /api/auth/register**

Criar nova conta de usuário.

**Entrada (form-urlencoded):**

- `name`, `email`, `password` (min 8 chars), `cpf` (11 dígitos)
- `role`: `"patient"` ou `"professional"`
- `phone`, `cep`, `uf`, `city`, `address` (opcionais)
- `profissional_identification`, `category` (obrigatórios se `role=professional`)

**Categorias:** `physician`, `nutritionist`, `psychologist`, `personal_trainer`, `other`

**Nota:** Profissionais têm perfil criado automaticamente com valores padrão.

#### **POST /api/auth/login**

Fazer login e obter token JWT.

**Entrada (form-urlencoded):**

- `email`, `password`

**Saída:**

```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "name": "João",
    "email": "joao@example.com",
    "role": "patient"
  }
}
```

---

### 👤 Usuários (`/api/users` ou `/api/user`)

- **GET /api/user/me** - Buscar perfil do usuário logado
- **PUT /api/users/me** - Atualizar perfil
- **DELETE /api/users/me** - Deletar conta
- **GET /api/users/{user_id}** - Buscar usuário por ID
- **GET /api/users/** - Listar todos os usuários (com paginação)

---

### 👨‍⚕️ Profissionais (`/api/professionals` ou `/api/professional`)

#### **GET /api/professionals/** ou **GET /api/professional/list**

Listar profissionais com filtros.

**Query Params:**

- `name` - Buscar por nome
- `category` - Filtrar por categoria
- `tags` - Filtrar por tags (array)
- `only_online`, `only_presential` - Filtrar por tipo de atendimento
- `skip`, `limit` - Paginação

**Exemplo:**

```bash
GET /api/professionals/?category=physician&name=Carlos&skip=0&limit=10
```

#### **GET /api/professionals/{profile_id}**

Buscar perfil profissional por ID do perfil.

#### **GET /api/professional/profile/user/{user_id}**

Buscar perfil profissional por ID do usuário.

#### **GET /api/professionals/me**

Buscar meu perfil profissional (usuário logado).

#### **POST /api/professionals/**

Criar perfil profissional.

**Entrada (JSON):**

```json
{
  "bio": "Médico especialista em cardiologia",
  "category": "physician",
  "profissional_identification": "CRM-123456",
  "services": "Consultas, Exames",
  "price": 200.0,
  "only_online": true,
  "only_presential": false,
  "available_days_of_week": "monday,wednesday,friday",
  "start_hour": "08:00",
  "end_hour": "18:00",
  "tags": ["Cardiologia", "Clínica Geral"],
  "unavailable_dates": [{ "date": "2025-12-25", "reason": "Feriado" }]
}
```

#### **PUT /api/professionals/{profile_id}** ou **PUT /api/professionals/me**

Atualizar perfil profissional.

#### **GET /api/professionals/{profile_id}/appointments**

Listar agendamentos de um profissional específico.

**Query Params:**

- `start_date`, `end_date` - Filtrar por período (formato: YYYY-MM-DD)
- `skip`, `limit` - Paginação

**Exemplo:**

```bash
GET /api/professionals/1/appointments?start_date=2025-10-01&end_date=2025-10-31
```

#### **GET /api/professionals/{profile_id}/available-slots**

Calcular horários disponíveis para agendamento.

**Query Params:**

- `target_date` - Data desejada (obrigatório, formato: YYYY-MM-DD)
- `duration_minutes` - Duração do slot (default: 60, min: 15, max: 480)

**Exemplo:**

```bash
GET /api/professionals/1/available-slots?target_date=2025-10-13&duration_minutes=60
```

**Saída:**

```json
{
  "date": "2025-10-13",
  "available_slots": [
    { "start_time": "08:00", "end_time": "09:00" },
    { "start_time": "09:00", "end_time": "10:00" }
  ],
  "unavailable_reason": null
}
```

---

### 📅 Agendamentos (`/api/appointments`)

#### **POST /api/appointments/**

Criar agendamento (apenas pacientes).

**Entrada (JSON):**

```json
{
  "professional_id": 1,
  "start_time": "2025-10-13T20:00:00",
  "end_time": "2025-10-13T21:00:00"
}
```

**Nota:** Timezone é removido automaticamente.

#### **GET /api/appointments/my** ou **GET /api/appointments/my-appointments**

Buscar meus agendamentos (paciente ou profissional).

**Query Params:** `skip`, `limit`

#### **GET /api/appointments/{appointment_id}**

Buscar agendamento por ID.

#### **PUT /api/appointments/{appointment_id}**

Atualizar agendamento.

**Entrada (JSON - todos opcionais):**

```json
{
  "start_time": "2025-10-13T21:00:00",
  "end_time": "2025-10-13T22:00:00",
  "status": "confirmed"
}
```

**Status:** `pending`, `confirmed`, `completed`, `cancelled`

#### **DELETE /api/appointments/{appointment_id}**

Cancelar agendamento.

---

### 🔑 Autenticação em Rotas Protegidas

Todas as rotas exceto `/api/auth/register` e `/api/auth/login` requerem:

```bash
Authorization: Bearer {token}
```

**Exemplo:**

```bash
curl http://localhost:8000/api/user/me \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

## 🧪 Testes

```bash
pytest

pytest --cov=app --cov-report=html

pytest tests/test_auth.py -v
```

## 🔍 Qualidade de Código

```bash
ruff check .
ruff format .

pre-commit install
pre-commit run --all-files
```

## 📚 Documentação

- **Swagger UI**: <http://localhost:8000/docs>
- **ReDoc**: <http://localhost:8000/redoc>
- **OpenAPI JSON**: <http://localhost:8000/openapi.json>

## 📝 Notas Importantes

### Validações

- **CPF**: Deve ter 11 dígitos e ser válido (algoritmo de validação)
- **Senha**: Mínimo 8 caracteres
- **Email**: Formato válido e único
- **Horários**: Formato `HH:MM` (ex: `08:00`, `18:30`) ou vazio/null
- **Datas**: Formato ISO `YYYY-MM-DD` ou `YYYY-MM-DDTHH:MM:SS`

### Comportamentos

- **Timezone**: Automaticamente removido de datetime (banco usa timestamp sem timezone)
- **Strings vazias**: Convertidas para `null` em query params
- **Perfil profissional**: Criado automaticamente ao registrar com `role=professional`
- **Conflitos de horário**: Validados automaticamente ao criar/atualizar agendamentos
- **SQLAlchemy unique()**: Necessário em queries com `joinedload` de coleções

### Categorias Profissionais

- `physician` - Médico
- `nutritionist` - Nutricionista
- `psychologist` - Psicólogo
- `personal_trainer` - Personal Trainer
- `other` - Outros

### Status de Agendamento

- `pending` - Aguardando confirmação
- `confirmed` - Confirmado
- `completed` - Concluído
- `cancelled` - Cancelado

## 🤝 Contribuindo

1. `pre-commit install`
2. `git checkout -b feature/nova-feature`
3. `git commit -m "feat: adiciona nova feature"`
4. `git push origin feature/nova-feature`
5. Abra um Pull Request

## 📄 Licença

Trabalho acadêmico da disciplina "Projeto e Prática I".
