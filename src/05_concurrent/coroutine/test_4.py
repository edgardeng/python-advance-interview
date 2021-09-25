# 协程实现异步
import asyncio
import time

now = lambda: time.time()


# 使用 await 等待耗时
async def do_work(x):
  print('do_work waiting:  ', x)
  await asyncio.sleep(x)
  return 'Done after %d s' % x


def basic_usage():
  start = now()
  loop = asyncio.get_event_loop()  # 创建事件循环
  task = asyncio.ensure_future(do_work(3))
  loop.run_until_complete(task)  # 将协程对象加入事件循环
  print('using time:   ', now() - start)
  print('task result:   ', task.result())

if __name__ == '__main__':
  basic_usage()
