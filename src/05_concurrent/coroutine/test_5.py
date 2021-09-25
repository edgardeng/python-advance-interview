'''
' asyncio 实现并发
'''

import asyncio
import time

now = lambda: time.time()


# 使用 await 等待耗时
async def do_work(x):
  print('do_work waiting: ', x)
  await asyncio.sleep(x)
  return 'Done after {} s'.format(x)


async def create():
  task_4 = asyncio.ensure_future(do_work(0.4))
  task_5 = asyncio.ensure_future(do_work(0.5))
  task_6 = asyncio.ensure_future(do_work(0.6))  # 多个任务
  tasks2 = [task_4, task_5, task_6]
  # 第1种
  # dones,pendings = await asyncio.wait(tasks2) #
  # for t in dones:
  #   print('Done Result:', t.result())

  # 第2种 返回结果的方式
  # results = await asyncio.gather(*tasks2)
  # for r in results:
  #   print('Done Result2:', r)

  # 第3种
  # return await asyncio.gather(*tasks2)

  # 第4种
  # return await asyncio.wait(tasks2)

  # 第5种 配合loop.run_until_complete(create())
  for task in asyncio.as_completed(tasks2):
    r = await task
    print('Done Result5:', r)


def basic_usage():
  task_1 = asyncio.ensure_future(do_work(0.1))
  task_2 = asyncio.ensure_future(do_work(0.2))
  task_3 = asyncio.ensure_future(do_work(0.3))  # 多个任务
  tasks = [task_1, task_2, task_3]
  start = now()
  loop = asyncio.get_event_loop()  # 创建事件循环
  loop.run_until_complete(asyncio.wait(tasks))  # 将协程对象加入事件循环
  print('using time:   ', now() - start)
  for task in tasks:
    print('result: ', task.result())


# 协程的嵌套
def basic_usage2():
  start = now()
  loop = asyncio.get_event_loop()  # 创建事件循环
  loop.run_until_complete(create())  # 将协程对象加入事件循环
  print('using time:   ', now() - start)

  # 第3种获取结果 配合 return await asyncio.gather(*tasks2)
  # results = loop.run_until_complete(create())
  # for r in results:
  #   print('Done Results:', r)

  # 第4种获取结果 配合 return await asyncio.wait(tasks2)
  # dones,pendings  = loop.run_until_complete(create())
  # for t in dones:
  #   print('Done Result4:', t.result())


if __name__ == '__main__':
  # basic_usage()
  basic_usage2()
