'''
' asyncio 协程的状态 和停止
'''
import asyncio
import time

now = lambda: time.time()


# 使用 await 等待耗时
async def do_work(x):
  print('do_work waiting: ', x)
  await asyncio.sleep(x)
  print('end do work')
  return 'Done after {} s'.format(x)


def basic_usage():
  task_1 = asyncio.ensure_future(do_work(4))
  task_2 = asyncio.ensure_future(do_work(5))
  task_3 = asyncio.ensure_future(do_work(6))  # 多个任务
  tasks = [task_1, task_2, task_3]
  start = now()
  try:
    loop = asyncio.get_event_loop()  # 创建事件循环
    loop.run_until_complete(asyncio.wait(tasks))  # 将协程对象加入事件循环
  except KeyboardInterrupt as e:
    # 获取时间循环所有的任务列表
    print(asyncio.Task.all_tasks())
    for task in asyncio.Task.all_tasks():
      print(task.cancel()) # 取消成功 返回True
    loop.stop()
    loop.run_forever()
  finally:
    loop.close()
  print('using time:   ', now() - start)



async def create():
  task_4 = asyncio.ensure_future(do_work(3))
  task_5 = asyncio.ensure_future(do_work(4))
  task_6 = asyncio.ensure_future(do_work(5))  # 多个任务
  tasks2 = [task_4, task_5, task_6]
  dones,pendings = await asyncio.wait(tasks2) #
  for t in dones:
    print('Done Result:', t.result())


def basic_usage_stop():
  start = now()
  loop = asyncio.get_event_loop()  # 创建事件循环
  try:
    task_create = asyncio.ensure_future(create())
    loop.run_until_complete(task_create)  # 将协程对象加入事件循环
  except KeyboardInterrupt as e:
    # 获取时间循环所有的任务列表
    print(asyncio.all_tasks())

    print(asyncio.gather(*asyncio.Task.all_tasks()).cancel())
    # for task in asyncio.Task.all_tasks():
    #   print(task.cancel()) # 取消成功 返回True
    loop.stop()
    loop.run_forever()
  finally:
    loop.close()
  print('using time:   ', now() - start)




if __name__ == '__main__':
  # basic_usage()
  # basic_usage_stop()
  asyncio.run(do_work(3))
  print('end')