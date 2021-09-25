"""
协程案例
"""

# 1. 创建10个协程，访问100次百度
import asyncio
import time

import urllib3

num = 0
http = urllib3.PoolManager()

import aiohttp


async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


async def visit_baidu():
    global num
    while num < 100:
        # await 后面只能跟异步程序或有__await__属性的对象，因为异步程序与一般程序不同
        num += 1
        await asyncio.sleep(0)  #
        # http.request('GET', 'http://www.baidu.com')
        await fetch('http://www.baidu.com')  # await后面必须是异步函数（带async的函数）

    # await http.request('GET', 'http://www.baidu.com') # object HTTPResponse can't be used in 'await' expression
    # RuntimeWarning: coroutine 'visit_baidu' was never awaited


def create_tasks_visit_baidu():
    loop = asyncio.get_event_loop()
    tasks = []
    start = time.time()
    for _ in range(10):
        # tasks.append(loop.create_task(visit_baidu()))
        tasks.append(asyncio.ensure_future(visit_baidu()))
    loop.run_until_complete(asyncio.wait(tasks))
    print('using time:   ', time.time() - start)
    print(num)


if __name__ == '__main__':
    create_tasks_visit_baidu()
