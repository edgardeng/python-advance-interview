import asyncio
import functools

"""
事件循环
"""
from datetime import datetime


async def task(i):
    print(f'I will sleep {i}s at {datetime.now()}')
    await asyncio.sleep(i)


async def task2(loop, i):
    print(f'I will sleep {i}s at {datetime.now()}')
    await asyncio.sleep(i)
    loop.stop()  # 第二种运行方式


def done_callback(l, future):
    l.stop()
    print(f'Done at {datetime.now()}')
    # print(future)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    print(f'loop create at {datetime.now()}')

    # 第一种运行方式 顺序执行
    # loop.run_until_complete(task(1))
    # loop.run_until_complete(task(3))

    # 第二种运行方式( 第二个协程没结束，loop 就停止了——被先结束的那个协程给停掉的。)
    # asyncio.ensure_future(task2(loop, 1))
    # asyncio.ensure_future(task2(loop, 3))
    # loop.run_forever() # stop 后，就结束了

    # 解决第二种运行方式的最佳方法
    futures = asyncio.gather(task(1), task(3))
    futures.add_done_callback(functools.partial(done_callback, loop))
    loop.run_forever()

    loop.close()
    print(f'loop close at {datetime.now()}')
