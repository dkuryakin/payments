import logging

from app import app
from routes.v1 import router as router_v1
from settings import settings

logging.basicConfig(level=settings.loglevel)

logging.debug(settings.dict())

app.include_router(router_v1, prefix='/v1')
