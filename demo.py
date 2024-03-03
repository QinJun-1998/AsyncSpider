import asyncio

from AsyncSpider import BaseSpider


class TestSpider(BaseSpider):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.results = []

    def init_tasks(self) -> list:
        return ['url' for _ in range(10)]

    async def fetch(self, url):
        response = await self.get(url=url)
        print(response.json()['origin'])
        self.results.append(response.json()['origin'])

    def finish(self):
        print('采集完成，采集结果是: %s' % self.results)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(TestSpider(retry_times=10, concurrency=3).run())
