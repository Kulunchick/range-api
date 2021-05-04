from fastapi import FastAPI
from pydantic import BaseSettings
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi_mail import ConnectionConfig
import aioredis
from fastapi_limiter import FastAPILimiter

class Settings(BaseSettings):
    MONGO_URL: str
    MONGO_DB: str
    REDIS_PASS: str
    ADMIN_MAIL: str
    MAIL_PASS: str
    MAIL_PORT: int

    class Config:
        env_file = '.env'


app = FastAPI()

@app.on_event('startup')
async def startup_db_client():
    settings = Settings()
    app.settings = settings
    app.smtp = ConnectionConfig(
        MAIL_USERNAME=settings.ADMIN_MAIL,
        MAIL_FROM=settings.ADMIN_MAIL,
        MAIL_PASSWORD=settings.MAIL_PASS,
        MAIL_PORT=settings.MAIL_PORT,
        MAIL_SERVER="smtp.rangesoft.tech",
        MAIL_TLS=False,
        MAIL_SSL=False
    )
    redis = await aioredis.create_redis_pool("redis://redis-14764.c135.eu-central-1-1.ec2.cloud.redislabs.com:14764", password="gv6vXDIAJNTLL2fJ1QtPr8CVVWCQedFH")
    FastAPILimiter.init(redis)
    app.mongodb_client = AsyncIOMotorClient(settings.MONGO_URL)
    app.mongodb = app.mongodb_client[settings.MONGO_DB]

from app.routes.auth import routes as auth_routes

app.include_router(
    auth_routes,
    prefix='/api/auth'
)

async def root():
    return {"message": "Hello World"}

app.add_api_route('/', root)

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()