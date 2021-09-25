# -*- coding: utf-8 -*-
# @Date     : 2021/1/4 10:46
# @Author   : edgardeng
# @File     : 多进程,多线程 写一个文件

import asyncio
import time
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
from multiprocessing import Process
from threading import Thread, Lock


def write_log(t, lock=None):
    time.sleep(t)
    if lock:
        with lock:
            with open('test-log.txt', "a+") as f:
                now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                f.write(f'{now} create {t} \n')
    else:
        with open('test-log.txt', "a+") as f:
            now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            f.write(f'{now} create {t} \n')


async def async_write_log(t):
    await asyncio.sleep(t)
    with open('test-log.txt', "a+") as f:
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        f.write(f'{now} create {t} \n')


def process_write():
    # 多进程写程序，会部分写不进去
    times = [i for i in range(4)] * 5
    ps = [Process(target=write_log, args=(t,)) for t in times]
    for p in ps:
        p.start()


def thread_pool_write():
    # 线程池 写文件，先后顺序会乱
    # 线程少数据全， 线程多的时候，会掉数据。需要加锁保证数据
    times = [i for i in range(4)] * 50
    print(times)
    lock = None # Lock()
    with ThreadPoolExecutor(max_workers=50) as pool:
        all_task = [pool.submit(write_log, t, lock) for t in times]
        wait(all_task, timeout=0, return_when=ALL_COMPLETED)


def thread_write():
    # 线程写文件，会顺序写入。
    # 线程少数据全， 线程多的时候，会掉数据 需要加锁保证数据
    times = [i for i in range(4)] * 50
    print(times)
    lock = Lock()
    ts = [Thread(target=write_log, args=(t, lock)) for t in times]
    for t in ts:
        t.start()
    # 耗时0

def asyncio_write():
    # 协程写文件 会顺序写入。数据全
    loop = asyncio.get_event_loop()
    times = [i for i in range(4)] * 50
    tasks = [asyncio.ensure_future(async_write_log(t)) for t in times]
    loop.run_until_complete(asyncio.wait(tasks))


if __name__ == '__main__':
    print('start', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    # process_write()    # 耗时0
    thread_pool_write()  # 耗时 ALL_COMPLETE 8s (200个线程，线程池最大50)
    # thread_write()     # 耗时0
    # asyncio_write()    # 耗时为最长的那个协程
    print('end', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
