
import asyncio
import logging

from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config import settings
from app.core.database import Base

logger = logging.getLogger(__name__)


async def init_db():
    engine = create_async_engine(str(settings.database_url), echo=True)

    async with engine.begin() as conn:

        await conn.run_sync(Base.metadata.create_all)

    await engine.dispose()
    logger.info("✅ Database initialized successfully!")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(init_db())
