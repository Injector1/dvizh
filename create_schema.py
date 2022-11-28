import os

from tortoise import Tortoise, run_async


POSTGRES_USER = os.getenv("POSTGRES_USER", "user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_DB_NAME = os.getenv('POSTGRES_DB_NAME', "api")

print(POSTGRES_HOST, POSTGRES_USER)


async def connect_to_database():
    await Tortoise.init(
        db_url=f'postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:5432/{POSTGRES_DB_NAME}?schema=public',
        modules={'models': ['app.features.telegraf.models']},
    )


async def database_creation():
    await connect_to_database()
    await Tortoise.generate_schemas()


async def close_connection():
    await Tortoise.close_connections()

if __name__ == '__main__':
    try:
        run_async(database_creation())
        print('Scheme generated')
    except:
        print('error')

