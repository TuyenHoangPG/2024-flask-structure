import logging
import os

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from dotenv import find_dotenv, load_dotenv

env_file = find_dotenv(filename=f'.env.{os.getenv("FLASK_ENV")}')
load_dotenv(env_file)


class Config:
    """Base configuration."""

    SQLALCHEMY_DATABASE_URI = f'postgresql://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@{os.getenv("POSTGRES_HOST") if os.getenv("POSTGRES_HOST") else "postgres"}:{os.getenv("POSTGRES_PORT")}/{os.getenv("POSTGRES_DB")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    REDISTOGO_URL = f'redis://{os.getenv("REDIS_HOST")}:{os.getenv("REDIS_PORT")}'

    BCRYPT_LOG_ROUNDS = 10

    CORS_ORIGIN_WHITELIST = os.getenv("CORS_ORIGIN_WHITELIST").split(sep=",")

    SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    REFRESH_TOKEN_EXPIRED_TIME = int(os.getenv("REFRESH_TOKEN_EXPIRED_TIME"))
    TOKEN_EXPIRE_HOURS = 0
    TOKEN_EXPIRE_MINUTES = 0

    CACHE_TYPE = "redis"
    CACHE_REDIS_HOST = os.environ["REDIS_HOST"] if os.environ["REDIS_HOST"] else "redis"
    CACHE_REDIS_PORT = os.environ["REDIS_PORT"]
    CACHE_REDIS_DB = os.environ["REDIS_DB"]
    CACHE_REDIS_PASSWORD = os.environ["REDIS_PASSWORD"]
    CACHE_DEFAULT_TIMEOUT = os.environ["REDIS_DEFAULT_TIMEOUT"]
    CACHE_KEY_PREFIX = f'{os.environ["APP_NAME"]}_{os.environ["FLASK_ENV"]}_'

    MAIL_SERVER = os.getenv("EMAIL_HOST")
    MAIL_PORT = os.getenv("EMAIL_PORT")
    MAIL_USERNAME = os.getenv("EMAIL_USER")
    MAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_FROM = os.getenv("EMAIL_FROM")

    BASE_URL = os.getenv("BASE_URL")

    S3_REGION = os.getenv("S3_REGION")
    S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
    S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
    S3_SECRET_KEY = os.getenv("S3_SECRET_KEY")
    S3_MEDIA_PREFIX = os.getenv("S3_MEDIA_PREFIX")

    CELERY_BROKER_URL = f"redis://:{CACHE_REDIS_PASSWORD}@{CACHE_REDIS_HOST}:{CACHE_REDIS_PORT}/{CACHE_REDIS_DB}"
    CELERY_RESULT_BACKEND = f"redis://:{CACHE_REDIS_PASSWORD}@{CACHE_REDIS_HOST}:{CACHE_REDIS_PORT}/{CACHE_REDIS_DB}"

    LOG_LEVEL = logging.DEBUG
    LOG_FORMAT = "%(asctime)s [%(levelname)s] %(message)s"
    LOG_DIR = "logs"


class ProdConfig(Config):
    """Production configuration."""

    ENV = "prod"
    DEBUG = False
    TOKEN_EXPIRE_HOURS = 1


class UatConfig(Config):
    """UAT configuration."""

    ENV = "uat"
    DEBUG = False
    TOKEN_EXPIRE_HOURS = 1


class QaConfig(Config):
    """QA configuration."""

    ENV = "qa"
    DEBUG = True
    TOKEN_EXPIRE_HOURS = 12

    APISPEC_SPEC = APISpec(
        title="Demo API spec",
        version="v1",
        info={"description": "This is Demo Api docs"},
        plugins=[MarshmallowPlugin()],
        produces=["application/json"],
        openapi_version="2.0.0",
    )


class DevConfig(Config):
    """Development configuration."""

    ENV = "dev"
    DEBUG = True
    TOKEN_EXPIRE_MINUTES = 0
    TOKEN_EXPIRE_HOURS = 12

    APISPEC_SPEC = APISpec(
        title="Demo API spec",
        version="v1",
        info={"description": "This is Demo Api docs"},
        plugins=[MarshmallowPlugin()],
        produces=["application/json"],
        openapi_version="2.0.0",
    )


ENV_CONFIG_DICT = {
    "dev": DevConfig,
    "qa": QaConfig,
    "uat": UatConfig,
    "prod": ProdConfig,
}


def get_config(config_name):
    """Retrieve environment configuration settings."""
    return ENV_CONFIG_DICT.get(config_name, DevConfig)
