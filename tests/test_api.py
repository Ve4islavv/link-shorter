from tests.conftest import ac
from httpx import AsyncClient


async def test_generate_slug(ac: AsyncClient):
    result = await ac.post('/short_url', json={'long_url': 'https://www.google.com'})
    assert result.status_code == 200