import os

from tortoise import Tortoise, run_async


POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_DB_NAME = os.getenv('POSTGRES_DB_NAME')


async def connect_to_database():
    await Tortoise.init(
        db_url=f'postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:5432/${POSTGRES_DB_NAME}?schema'
               f'=public',
        modules={'models': ['app.features.telegraf.models']}
    )


async def database_creation():
    await connect_to_database()
    await Tortoise.generate_schemas()


if __name__ == '__main__':
    run_async(database_creation())
