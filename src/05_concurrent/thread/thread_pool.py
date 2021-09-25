# -*- coding: utf-8 -*-
# @author: dengxixi
# @date:   2021-07-08
# @file:

import time
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED

import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
}


list_time = []
def request_url(url):
    t = time.time()
    try:
        response = requests.get(url, headers=headers)
    except Exception as e:
        pass

    print(time.time() - t)
    list_time.append(time.time() -t)
    return response


def thread_pool_request():
    urls = [rf'https://www.ijq.tv/mingxing/{i}.html' for i in range(1841, 1850)]

    t_start = time.time()
    print('*' * 20, '线程池')
    with ThreadPoolExecutor(max_workers=10) as pool:
        all_task = [pool.submit(request_url, url) for url in urls]
        wait(all_task, timeout=0, return_when=ALL_COMPLETED)

    t_end = time.time()
    print('最大耗时', max(list_time))
    print('最小耗时', min(list_time))
    print('平均耗时', sum(list_time) / len(urls))
    print('总共耗时', t_end - t_start)


if __name__ == '__main__':
    thread_pool_request()

