import asyncio
from aiomq.core.clock import GLOBAL_CLOCK
from aiomq.api import aio_api, init_db

loop = asyncio.get_event_loop()

tasks = [
    asyncio.ensure_future(GLOBAL_CLOCK.runtime(loop)),
    asyncio.ensure_future(aio_api(host='127.0.0.1', port=8080, backlog=20000)),
    asyncio.ensure_future(init_db()),
]

loop.run_until_complete(asyncio.gather(*tasks))
