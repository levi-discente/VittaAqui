# VittaAqui

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

Acesse: http://localhost:8000/docs

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

## 📦 Estrutura do Projeto

```
app/
├── main.py
├── core/
│   ├── config.py
│   ├── database.py
│   └── security.py
├── models/
├── schemas/
├── api/
│   ├── deps.py
│   └── v1/
├── crud/
├── services/
└── utils/
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

## 🌐 Endpoints

### Auth
- `POST /api/auth/register`
- `POST /api/auth/login`

### Users
- `GET /api/users/me`
- `PUT /api/users/me`
- `DELETE /api/users/me`
- `GET /api/users/{id}`
- `GET /api/users/`

### Professionals
- `POST /api/professionals/`
- `GET /api/professionals/me`
- `PUT /api/professionals/me`
- `GET /api/professionals/`
- `GET /api/professionals/{id}`

### Appointments
- `POST /api/appointments/`
- `GET /api/appointments/my-appointments`
- `GET /api/appointments/{id}`
- `PUT /api/appointments/{id}`
- `DELETE /api/appointments/{id}`

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

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🤝 Contribuindo

1. `pre-commit install`
2. `git checkout -b feature/nova-feature`
3. `git commit -m "feat: adiciona nova feature"`
4. `git push origin feature/nova-feature`
5. Abra um Pull Request

## 📄 Licença

Trabalho acadêmico da disciplina "Projeto e Prática I".
