import asyncio
import logging

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings
from app.core.security import get_password_hash
from app.models.enums import ProfessionalCategory, Role
from app.models.professional import ProfessionalProfile, ProfileTag
from app.models.user import User

logger = logging.getLogger(__name__)


async def seed_database():
    engine = create_async_engine(str(settings.database_url), echo=False)
    async_session_local = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session_local() as session:
        try:
            result = await session.execute(select(func.count()).select_from(User))
            count = result.scalar()

            if not count:
                count = 0

            if count > 0:
                logger.info("Database already has data. Skipping seed.")
                return

            logger.info("Seeding database with sample data...")

            hashed_password = get_password_hash("senha123")

            patient1 = User(
                name="João Silva",
                email="joao@example.com",
                password=hashed_password,
                role=Role.PATIENT,
                cpf="52998224725",
                phone="11999999999",
                cep="01310-100",
                uf="SP",
                city="São Paulo",
                address="Av. Paulista, 1000",
            )
            session.add(patient1)

            patient2 = User(
                name="Maria Santos",
                email="maria@example.com",
                password=hashed_password,
                role=Role.PATIENT,
                cpf="71428793860",
                phone="11988888888",
                cep="01310-200",
                uf="SP",
                city="São Paulo",
                address="Av. Paulista, 2000",
            )
            session.add(patient2)

            prof1 = User(
                name="Dr. Carlos Mendes",
                email="carlos@example.com",
                password=hashed_password,
                role=Role.PROFESSIONAL,
                cpf="86378345120",
                phone="11977777777",
                cep="01310-300",
                uf="SP",
                city="São Paulo",
                address="Av. Paulista, 3000",
            )
            session.add(prof1)
            await session.flush()

            profile1 = ProfessionalProfile(
                user_id=prof1.id,
                bio="Médico clínico geral com 15 anos de experiência",
                category=ProfessionalCategory.PHYSICIAN,
                profissional_identification="CRM-SP-123456",
                services="Consultas gerais, check-ups, atestados",
                price=200.00,
                only_online=False,
                only_presential=False,
                rating=4.8,
                num_reviews=120,
                available_days_of_week="monday,tuesday,wednesday,thursday,friday",
                start_hour="08:00",
                end_hour="18:00",
            )
            session.add(profile1)
            await session.flush()

            session.add(ProfileTag(profile_id=profile1.id, name="Clínica Geral"))
            session.add(ProfileTag(profile_id=profile1.id, name="Check-up"))
            session.add(ProfileTag(profile_id=profile1.id, name="Atestados"))

            prof2 = User(
                name="Dra. Ana Paula",
                email="ana@example.com",
                password=hashed_password,
                role=Role.PROFESSIONAL,
                cpf="45842621650",
                phone="11966666666",
                cep="01310-400",
                uf="SP",
                city="São Paulo",
                address="Av. Paulista, 4000",
            )
            session.add(prof2)
            await session.flush()

            profile2 = ProfessionalProfile(
                user_id=prof2.id,
                bio="Nutricionista especializada em emagrecimento saudável",
                category=ProfessionalCategory.NUTRITIONIST,
                profissional_identification="CRN-SP-789012",
                services="Planos alimentares, acompanhamento nutricional",
                price=150.00,
                only_online=True,
                only_presential=False,
                rating=4.9,
                num_reviews=85,
                available_days_of_week="monday,wednesday,friday",
                start_hour="09:00",
                end_hour="17:00",
            )
            session.add(profile2)
            await session.flush()

            session.add(ProfileTag(profile_id=profile2.id, name="Emagrecimento"))
            session.add(ProfileTag(profile_id=profile2.id, name="Nutrição Esportiva"))
            session.add(ProfileTag(profile_id=profile2.id, name="Online"))

            prof3 = User(
                name="Dr. Roberto Lima",
                email="roberto@example.com",
                password=hashed_password,
                role=Role.PROFESSIONAL,
                cpf="29165873491",
                phone="11955555555",
                cep="01310-500",
                uf="SP",
                city="São Paulo",
                address="Av. Paulista, 5000",
            )
            session.add(prof3)
            await session.flush()

            profile3 = ProfessionalProfile(
                user_id=prof3.id,
                bio="Psicólogo clínico especializado em terapia cognitivo-comportamental",
                category=ProfessionalCategory.PSYCHOLOGIST,
                profissional_identification="CRP-SP-345678",
                services="Terapia individual, terapia de casal, ansiedade, depressão",
                price=180.00,
                only_online=False,
                only_presential=False,
                rating=5.0,
                num_reviews=200,
                available_days_of_week="monday,tuesday,wednesday,thursday,friday,saturday",
                start_hour="10:00",
                end_hour="20:00",
            )
            session.add(profile3)
            await session.flush()

            session.add(ProfileTag(profile_id=profile3.id, name="TCC"))
            session.add(ProfileTag(profile_id=profile3.id, name="Ansiedade"))
            session.add(ProfileTag(profile_id=profile3.id, name="Depressão"))
            session.add(ProfileTag(profile_id=profile3.id, name="Terapia de Casal"))

            await session.commit()
            logger.info("✅ Database seeded successfully!")
            logger.info("📊 Created:")
            logger.info("   - 2 patients")
            logger.info("   - 3 professionals")
            logger.info("   - 3 professional profiles")
            logger.info("   - 10 tags")
            logger.info("")
            logger.info("🔑 Login credentials (all users):")
            logger.info("   Password: senha123")
            logger.info("")
            logger.info("👥 Patients:")
            logger.info("   - joao@example.com (CPF: 529.982.247-25)")
            logger.info("   - maria@example.com (CPF: 714.287.938-60)")
            logger.info("")
            logger.info("👨‍⚕️ Professionals:")
            logger.info("   - carlos@example.com (Médico - CPF: 863.783.451-20)")
            logger.info("   - ana@example.com (Nutricionista - CPF: 458.426.216-50)")
            logger.info("   - roberto@example.com (Psicólogo - CPF: 291.658.734-91)")

        except Exception as e:
            await session.rollback()
            logger.error(f"Error seeding database: {e}")
            raise
        finally:
            await engine.dispose()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(seed_database())
