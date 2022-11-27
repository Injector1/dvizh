from tortoise import Tortoise, run_async


async def connect_to_database():
    await Tortoise.init(
        db_url='',
        modules={'models': ['app.features.telegraf.models']}
    )


async def database_creation():
    await connect_to_database()
    await Tortoise.generate_schemas()

if __name__ == '__main__':
    run_async(database_creation())
