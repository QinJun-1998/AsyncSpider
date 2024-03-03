# AsyncSpider

一个简单的aiohttp采集的封装

队列使用asyncio.Queue里的优先级队列（数值越小越优先），每次采集失败后，任务的优先级+1重新放回队列，达到一定值后不再重试；

设计：
1.失败后的任务重新抓取的优先级会降低
2.优先级既用来当作优先级，也用来作重试次数
3.封装了requests风格的response


## 调用方法
参考demo.py

调用基类，重写init_tasks和fetch方法即可


## 可扩展性
队列可改为redis队列，实现分布式 异步的redis库：aredis/aioredis

可在fetch方法里添加数据库存储：aiomysql
