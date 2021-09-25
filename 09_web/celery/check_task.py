'''
- 查看celery调取结果
'''

from celery.result import AsyncResult


def check_result_with_id(id):
  from tasks_demo.celery import cel
  async_result = AsyncResult(id, app=cel)
  if async_result.successful():
    result = async_result.get()
    print(result)
    # result.forget() # 将结果删除,执行完成，结果不会自动删除
    # async.revoke(terminate=True)  # 无论现在是什么时候，都要终止
    # async.revoke(terminate=False) # 如果任务还没有开始执行呢，那么就可以终止。
  elif async_result.failed():
    print('执行失败')
  elif async_result.status == 'PENDING':
    print('任务等待中被执行')
  elif async_result.status == 'RETRY':
    print('任务异常后正在重试')
  elif async_result.status == 'STARTED':
    print('任务已经开始被执行')


if __name__ == '__main__':
  check_result_with_id('4470c1f7-7dcc-4c16-a106-774782c122d0')
