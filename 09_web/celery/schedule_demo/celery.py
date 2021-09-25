from datetime import timedelta
from celery import Celery
from celery.schedules import crontab
'''
- 使用Beat自动启动定时任务

1. 启动 Beat 程序 $ celery beat -A proj (`celery beat -A schedule_demo `) # Celery Beat进程会读取配置文件的内容，周期性的将配置中到期需要执行的任务发送给任务队列 (不执行)
2. 启动 worker 进程 $ celery -A proj worker -l info 或者$ celery -B -A proj worker -l info (有任务就会执行)
'''


cel = Celery('tasks',
             broker='redis://127.0.0.1:6379/1',
             backend='redis://127.0.0.1:6379/2',
             include=[
               'schedule_demo.task1',
               'schedule_demo.task2',
              ])
cel.conf.timezone = 'Asia/Shanghai'
cel.conf.enable_utc = False


@cel.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
  from schedule_demo.task1 import send_a_email
  # Calls test('hello') every 10 seconds.
  sender.add_periodic_task(10.0, send_a_email.s('hello'), name='add every 10')

  # Calls test('world') every 30 seconds
  sender.add_periodic_task(30.0, send_a_email.s('world'), expires=10)

  # Executes every Monday morning at 7:30 a.m.
  sender.add_periodic_task(
    crontab(hour=10, minute=51, day_of_week=1),
    send_a_email.s('Happy Mondays!'),
  )

cel.conf.beat_schedule = {
  # 名字随意命名
  'task_name_schedule_at': {
    'task': 'schedule_demo.task1.send_a_email', # 执行tasks1下的send_a_email函数
    # 每隔2秒执行一次
    # 'schedule': 1.0,
    'schedule': crontab(minute="*/2"),  # '*/1': 每分钟， '*/2': 每2分钟
    # 'schedule': timedelta(seconds=6), # 每隔6s发一次
    # 传递参数
    'args': (' 张三A ',)
  },
  # 'add-every-12-seconds': {
  #     'task': 'celery_tasks.task01.send_email',
  #     每年4月11号，8点42分执行
  #     'schedule': crontab(minute=42, hour=8, day_of_month=11, month_of_year=4),
  #     'args': ('张三',)
  # },
}
