# VittaAqui - Python/FastAPI

Plataforma de telemedicina e agendamento de consultas desenvolvida com **FastAPI**, **SQLAlchemy 2.0** e **Alembic**.

## 🚀 Stack Tecnológica

- **FastAPI** - Framework web moderno e rápido
- **SQLAlchemy 2.0** - ORM com suporte async
- **Alembic** - Migrations de banco de dados
- **Pydantic v2** - Validação de dados
- **PostgreSQL** - Banco de dados relacional
- **uv** - Gerenciador de pacotes ultra-rápido
- **Ruff** - Linter e formatter

## 📋 Pré-requisitos

- Python 3.12+
- PostgreSQL 15+
- uv (recomendado) ou pip

## 🔧 Instalação

### 1. Instalar uv (recomendado)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Clonar e configurar o projeto

```bash
cd VittaAqui

# Criar ambiente virtual
uv venv

# Ativar ambiente virtual
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate  # Windows

# Instalar dependências
uv pip install -e ".[dev]"
```

### 3. Configurar variáveis de ambiente

```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

### 4. Inicializar banco de dados

```bash
# Subir PostgreSQL (via Docker)
docker compose up -d postgres

# Criar tabelas
python scripts/init_db.py

# Ou usar Alembic (quando configurado)
alembic upgrade head
```

## 🏃 Executar o servidor

```bash
# Modo desenvolvimento (com reload)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Modo produção
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

Acesse:
- **API**: http://localhost:8000
- **Documentação Swagger**: http://localhost:8000/docs
- **Documentação ReDoc**: http://localhost:8000/redoc

## 🧪 Testes

```bash
# Executar todos os testes
pytest

# Com cobertura
pytest --cov=app --cov-report=html

# Testes específicos
pytest tests/test_auth.py -v
```

## 🔍 Qualidade de Código

```bash
# Linting e formatting com Ruff
ruff check .
ruff format .

# Pre-commit hooks
pre-commit install
pre-commit run --all-files
```

## 📦 Estrutura do Projeto

```
app/
├── main.py              # Entry point FastAPI
├── core/                # Configurações centrais
│   ├── config.py        # Settings
│   ├── database.py      # Database session
│   └── security.py      # JWT, password hashing
├── models/              # SQLAlchemy models
├── schemas/             # Pydantic schemas
├── api/                 # Routers
│   ├── deps.py          # Dependencies
│   └── v1/              # API v1
├── crud/                # CRUD operations
├── services/            # Business logic
└── utils/               # Utilities
```

## 🔐 Autenticação

A API usa **JWT (JSON Web Tokens)** para autenticação.

### Fazer login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "email=user@example.com&password=senha123"
```

### Usar token

```bash
curl http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

## 📝 Migrations (Alembic)

```bash
# Criar nova migration
alembic revision --autogenerate -m "Descrição da mudança"

# Aplicar migrations
alembic upgrade head

# Reverter migration
alembic downgrade -1

# Ver histórico
alembic history
```

## 🐳 Docker

```bash
# Build e run
docker compose up -d

# Logs
docker compose logs -f app

# Parar
docker compose down
```

## 📚 Documentação da API

A documentação interativa está disponível em:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🤝 Contribuindo

1. Instale pre-commit hooks: `pre-commit install`
2. Crie uma branch: `git checkout -b feature/nova-feature`
3. Faça commit: `git commit -m "feat: adiciona nova feature"`
4. Push: `git push origin feature/nova-feature`
5. Abra um Pull Request

## 📄 Licença

Este projeto é um trabalho acadêmico da disciplina "Projeto e Prática I".
