import time
from tasks_demo.celery import cel


@cel.task
def send_msg(name):
  time.sleep(5)
  return "完成向%s发送短信任务" % name
