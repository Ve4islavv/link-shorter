from contextlib import asynccontextmanager
from fastapi import FastAPI, Body, status, HTTPException
from fastapi.responses import RedirectResponse


from database.db import engine
from database.models import Base
from exception import SlugAlreadyExistError
from service import generate_short_url, get_url_by_slug


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield



app = FastAPI(lifespan=lifespan)


@app.post('/short_url')
async def generate_slug_url(long_url: str = Body(embed=True)):
    try:
        slug =  await generate_short_url(long_url)
    except SlugAlreadyExistError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='Не удалось сгенерировать slug')
    return {'data': slug}


@app.get('/{slug}')
async def redirect_to_url(slug: str):
    try:
        long_url = await get_url_by_slug(slug)
    except FileNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return RedirectResponse(url=long_url, status_code=status.HTTP_302_FOUND)