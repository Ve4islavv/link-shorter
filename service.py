from database.crud import add_slug_in_database, get_long_url

from exception import NoLongerUrlFoundError, SlugAlreadyExistError
from shortener import generate_random_slug



async def generate_short_url(
        long_url: str,
) -> str:
    async def _generate_slug_and_add_to_db(long_url):
            slug = generate_random_slug()
            await add_slug_in_database(slug, long_url)
            return slug
    for attempt in range(3):
        try:
            slug = await _generate_slug_and_add_to_db(long_url)
            return slug
        except SlugAlreadyExistError as ex:
            if attempt == 2:
                raise SlugAlreadyExistError from ex
    return await _generate_slug_and_add_to_db(long_url)


async def get_url_by_slug(slug: str) -> str | None:
    long_url = await get_long_url(slug)
    if not long_url:
        raise NoLongerUrlFoundError()
    return long_url





