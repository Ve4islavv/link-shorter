from sqlalchemy.exc import IntegrityError

from database.db import new_session
from database.models import ShortURL
from sqlalchemy import select

from exception import SlugAlreadyExistError


async def add_slug_in_database(
        slug: str,
        long_url: str
):
    async with new_session() as session:
        new_slug = ShortURL(
            slug=slug,
            long_url=long_url
        )
        session.add(new_slug)
        try:
            await session.commit()
        except IntegrityError:
            raise SlugAlreadyExistError


async def get_long_url(slug: str) -> str | None:
    async with new_session() as session:
        query = select(ShortURL).filter_by(slug=slug)
        result = await session.execute(query)
        res = result.scalar_one_or_none()
        return res.long_url if res.long_url else None

