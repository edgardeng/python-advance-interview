import time
from schedule_demo.celery import cel


@cel.task
def send_a_msg(name):
  time.sleep(5)
  return "完成向%s发送短信任务" % name
