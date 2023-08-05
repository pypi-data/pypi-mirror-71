from aiohttp import web


async def index(request):
    return web.Response(body='hello world!', content_type='text/plain',)


urlpatterns = [
    web.get('/', index),
]
