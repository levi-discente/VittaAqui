from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import appointments, auth, professionals, reviews, users
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Plataforma de telemedicina e agendamento de consultas",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["health"])
async def health_check():
    return {
        "status": "www",
        "app": settings.app_name,
        "version": settings.app_version,
    }


app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(
    professionals.router, prefix="/api/professionals", tags=["professionals"]
)
app.include_router(
    appointments.router, prefix="/api/appointments", tags=["appointments"]
)
app.include_router(reviews.router, prefix="/api/reviews", tags=["reviews"])

# Rotas compatíveis com frontend antigo
app.include_router(users.router, prefix="/api/user", tags=["user-legacy"])
app.include_router(
    professionals.router, prefix="/api/professional", tags=["professional-legacy"]
)
