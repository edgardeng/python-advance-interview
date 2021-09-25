# 协程实现异步
import asyncio
import time

now = lambda: time.time()


# 使用 async关键字 使函数编程 协程队形
async def do_work(x):
  print('do_work waiting:  ', x)


# 有返回结果的协程对象
async def do_work2(x):
  print('do_work waiting:  ', x)
  return 'Done with {}'.format(x)


def basic_usage():
  start = now()
  loop = asyncio.get_event_loop()  # 创建事件循环
  loop.run_until_complete(do_work(3))  # 将协程对象加入事件循环
  print('using time:   ', now() - start)


# task的使用

def task_usage():
  coroutine = do_work(3)
  loop = asyncio.get_event_loop()
  task = loop.create_task(coroutine)  # 创建任务
  print(task)  # Task 是asyncio.Future的子类
  loop.run_until_complete(task)  # 状态 pending -> finished
  print(task)


def callback(future: asyncio.Future):
  print('callback: ', future.result())


def task_callback_usage():
  coroutine = do_work2(3)
  loop = asyncio.get_event_loop()
  task = loop.create_task(coroutine)  # 创建任务
  task.add_done_callback(callback)  # 给任务添加绑定函数
  loop.run_until_complete(task)  # 状态 pending -> finished

  # ---- 如果不绑定回调 直接使用 task的result获取返回结果
  print('直接返回，', task.result())


if __name__ == '__main__':
  # basic_usage()
  # task_usage()
  task_callback_usage()
