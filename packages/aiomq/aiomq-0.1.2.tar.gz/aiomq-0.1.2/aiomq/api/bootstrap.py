from aiohttp import web
from aiomq.api import urls

app = web.Application()
app.add_routes(urls.urlpatterns)


