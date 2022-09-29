from aiohttp import web
from models import question, choice


async def index(request):
    async with request.app['db'].acquire() as conn:
        cursor = await conn.execute(choice.select())
        records = await cursor.fetchall()
        data = [dict(q) for q in records]
        debug = [print(dict(q)) for q in records]
        return web.Response(text=str(data))
