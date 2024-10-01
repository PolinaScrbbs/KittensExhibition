from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Kitten


async def kitten_exists(session: AsyncSession, name: str) -> bool:
    query = select(exists().where(Kitten.name == name))
    result = await session.execute(query)
    return result.scalar()
