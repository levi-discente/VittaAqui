#!/bin/bash
set -e

echo "🚀 Starting VittaAqui application..."

# echo "⏳ Waiting for PostgreSQL..."
# until pg_isready -h postgres -p 5432 -U vitta_user; do
#   echo "PostgreSQL is unavailable - sleeping"
#   sleep 2
# done

echo "✅ PostgreSQL is ready!"

if [ "$DEBUG" = "True" ] || [ "$DEBUG" = "true" ]; then
    echo "🔧 DEBUG mode enabled - Running database initialization..."

    MIGRATION_COUNT=$(find alembic/versions -name "*.py" ! -name "__*" 2>/dev/null | wc -l)
    
    if [ "$MIGRATION_COUNT" -eq 0 ]; then
        echo "📝 No migrations found - Creating initial migration..."
        uv run alembic revision --autogenerate -m "Initial migration" || echo "⚠️  Failed to create migration"
    fi

    echo "📦 Running Alembic migrations..."
    uv run alembic upgrade head || echo "⚠️  Alembic migrations failed or no migrations to run"

    echo "🗄️  Initializing database tables..."
    uv run python scripts/init_db.py || echo "⚠️  Database already initialized"

    echo "🌱 Seeding database with sample data..."
    uv run python scripts/seed_db.py || echo "⚠️  Database already seeded"
else
    echo "🏭 Production mode - Only running Alembic migrations..."
    uv run alembic upgrade head
fi

echo "🎉 Database setup complete!"

echo "🚀 Starting FastAPI application..."
exec uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --reload-dir /app/app --reload-delay 0.5
