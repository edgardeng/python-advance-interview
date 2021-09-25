from celery import Celery

'''
' 配置文件
'''
cel = Celery('celery_demo',  # 名称
             broker='redis://localhost:6379/1',  # 中间件
             backend='redis://localhost:6379/2',  # 结果存储
             # 包含以下两个任务文件，去相应的py文件中找任务，对多个任务做分类
             include=['tasks_demo.task1',
                      'tasks_demo.task2']
             )

# 时区
cel.conf.timezone = 'Asia/Shanghai'
# 是否使用UTC
cel.conf.enable_utc = False
