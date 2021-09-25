import time
from tasks_demo.celery import cel


@cel.task
def send_email(res):
  time.sleep(5)
  return "完成向%s发送邮件任务" % res
