'''
' 基本使用
' 启动celery： celery worker -A celery_app_task -l info
'''

import celery
import time
backend='redis://127.0.0.1:6379/1' #
broker='redis://127.0.0.1:6379/2' # 消息中间件

cel=celery.Celery('test',backend=backend,broker=broker)
@cel.task # 使用装饰器
def send_email(name):
  print("向%s发送邮件..."%name)
  time.sleep(5)
  print("向%s发送邮件完成"%name)
  return "ok"




