from tortoise import Tortoise


async def init_db():
    # Here we connect to a SQLite DB file.
    # also specify the app name of "models"
    # which contain models from "app.models"
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        # db_url='mysql://root:sun851010@localhost:3306/czqb',
        modules={'models': ['czqb_api.models.users']}
    )
    # global rdb
    # rdb = await aioredis.create_redis_pool('redis://:123456@localhost/0?encoding=utf-8', maxsize=100)
    # Generate the schema
    # await Tortoise.generate_schemas()
