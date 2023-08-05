import asyncio


class Clock:
    def __init__(self):
        self.cron_job = asyncio.Queue()
        self.loop = None

    async def next(self):
        if self.cron_job.qsize():
            return await self.cron_job.get()
        return None

    async def runtime(self, loop):
        self.loop = loop
        while True:
            if job := await self.next():
                print(job)
            await asyncio.sleep(1)


GLOBAL_CLOCK = Clock()
