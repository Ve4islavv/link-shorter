from contextlib import asynccontextmanager
from typing import AsyncGenerator, Annotated
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Body, status, HTTPException
from fastapi.params import Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import engine, new_session
from src.database.models import Base
from src.exception import SlugAlreadyExistError, NoLongerUrlFoundError
from src.service import generate_short_url, get_url_by_slug


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield



app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=["*"],
    allow_headers=["*"],
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with new_session() as session:
        yield session


@app.post('/short_url')
async def generate_slug_url(
        session: Annotated[AsyncSession, Depends(get_session)],
        long_url: str = Body(embed=True)):
    try:
        slug =  await generate_short_url(long_url, session)
    except SlugAlreadyExistError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='Не удалось сгенерировать slug')
    return {'data': slug}


@app.get('/{slug}')
async def redirect_to_url(slug: str, session: Annotated[AsyncSession, Depends(get_session)]):
    try:
        long_url = await get_url_by_slug(slug, session)
    except NoLongerUrlFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return RedirectResponse(url=long_url, status_code=status.HTTP_302_FOUND)

