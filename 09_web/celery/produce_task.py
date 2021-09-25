'''
- 执行celery 任务
'''
from datetime import datetime,timedelta


def produce_task_from_single():
  from celery_task import send_email
  result = send_email.delay("yuan")
  print(result.id)


def produce_task_from_module():
  from tasks_demo.task1 import send_email
  from tasks_demo.task2 import send_msg

  # 立即告知celery去执行test_celery任务，并传入一个参数
  result = send_email.delay('yuan')
  print(result.id)
  result = send_msg.delay('yuan')
  print(result.id)


def produce_task_from_async():
  from tasks_demo.task1 import send_email

  # 方式一 定时（某个时间）
  v1 = datetime(2020, 9, 1, 10, 9, 5) #
  v2 = datetime.utcfromtimestamp(v1.timestamp()) # 转成标准时间
  result = send_email.apply_async(args=["One Timestamp",], eta=v2)
  print(result.id)

  # 方式二 定时（当前时间+时间值）
  ctime = datetime.now() # 当前时间
  utc_ctime = datetime.utcfromtimestamp(ctime.timestamp()) # 默认用utc时间
  task_time = utc_ctime + timedelta(seconds=10) # 当前时间 往后推一定的时间
  result2 = send_email.apply_async(args=["Current + timedelta"], eta=task_time)
  print(result2.id)



if __name__ == '__main__':
  # 1. 开启work：celery worker -A tasks_demo -l info -P eventlet
  # 2. 添加任务（执行produce_task.py)
  # 3. 检查任务执行结果（执行check_result.py）
  # produce_task_from_module()
  produce_task_from_async()
