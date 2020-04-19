import re

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fixtures import fixtures
from migrations import migrations
from models.base import db
from settings import settings

app = FastAPI(
    title=settings.title,
    version=settings.version,
)

origins = re.split(r'\s+', settings.origins.strip())
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await db.set_bind(settings.postgres_dsn)

    # For real production we need better migrations/fixtures subsystem.
    # Also, in production we have initiate these processes manually or inside ci/cd pipeline.
    await migrations()
    await fixtures()


@app.on_event("shutdown")
async def shutdown():
    await db.pop_bind().close()
