import aiohttp
import asyncio
import sys

from loguru import logger
from AsyncSpider.response import Response


class BaseSpider:
    def __init__(self, retry_times=10, concurrency=3):
        self.task_queue = asyncio.PriorityQueue()
        self.session = None
        self.concurrency = concurrency
        self.retry_times = retry_times

        if sys.platform == 'win32':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    def init_tasks(self) -> list:
        pass

    @staticmethod
    async def extract_response(r) -> Response:
        return Response({
            'text': await r.text(),
            'content': await r.read(),
            'status': r.status,
            'headers': r.headers
        })

    async def get(self, url=None, **kwargs) -> Response:
        async with self.session.get(url=url, **kwargs) as r:
            return await self.extract_response(r)

    async def post(self, url=None, **kwargs) -> Response:
        async with self.session.post(url=url, **kwargs) as r:
            return await self.extract_response(r)

    async def worker(self, queue):
        while True:
            task = await queue.get()
            priority, url = task[0], task[1]
            try:
                if priority <= self.retry_times:
                    logger.info('第%s次采集: %s' % (priority, url))
                    await self.fetch(url)
                else:
                    logger.warning('达到重试次数上限: %s' % url)
            except Exception as e:
                logger.error(e)
                priority += 1
                queue.put_nowait((priority, url))
                pass
            queue.task_done()

    async def fetch(self, url):
        pass

    def finish(self):
        pass

    async def run(self):
        tasks = self.init_tasks()

        [self.task_queue.put_nowait((1, url)) for url in tasks]

        conn = aiohttp.TCPConnector(force_close=True, enable_cleanup_closed=True)
        self.session = aiohttp.ClientSession(connector=conn)

        workers = [asyncio.create_task(self.worker(queue=self.task_queue)) for _ in range(self.concurrency)]
        await self.task_queue.join()
        [w.cancel() for w in workers]

        await self.session.close()

        self.finish()

