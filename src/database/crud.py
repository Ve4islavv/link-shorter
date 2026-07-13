from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import ShortURL
from sqlalchemy import select

from src.exception import SlugAlreadyExistError


async def add_slug_in_database(
        slug: str,
        long_url: str,
        session: AsyncSession
):
        new_slug = ShortURL(
            slug=slug,
            long_url=long_url
        )
        session.add(new_slug)
        try:
            await session.commit()
        except IntegrityError:
            raise SlugAlreadyExistError


async def get_long_url(slug: str, session: AsyncSession) -> str | None:
        query = select(ShortURL).filter_by(slug=slug)
        result = await session.execute(query)
        res = result.scalar_one_or_none()
        if res:
            return  res.long_url
        else:
            return None

