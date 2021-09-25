from multiprocessing import Process, Pool, Manager
import time
import os

'''
' 使用多进程
'
'''
from time import sleep


def single_process(name, age, **kwargs):
  print('a process is running, name:%s, age:%d' % (name, age))
  print('kwargs', kwargs)
  sleep(2)
  print('a process is done')


'''
' 继承Procees，使用进程子类
'''


class ClockProcess(Process):
  def __init__(self, interval):
    Process.__init__(self)
    self.interval = interval

  def run(self):
    print('ClockProcess start at {}'.format(time.ctime()))
    sleep(self.interval)
    print('ClockProcess end at {}'.format(time.ctime()))


'''
' 进程池的使用 Pool([num_process []])
' 提供指定数量的进程，供用户调用，当有新的请求提交到pool时，
  如果进程池没有满，会创建新进程来执行请求。如果已满，请求会等待，直到有进程结束，池不满时再执行
'''

'''
' 全局变量在多进程中 不 共享
'''
num = 1


def global_work1():
  global num
  num += 5
  print('global_work1 end at %d' % num)


def global_work2():
  global num
  num += 10
  print('global_work2 end at %d' % num)


def test_multi_process():
  # p = Process(target=single_process, args=('a', 1 ))
  # p.start()
  # p2 = Process(target=single_process, args=('b', 10), kwargs ={'b':1} )
  # p2.start()
  # print('p.is_alive()', p2.is_alive())
  # p2.join() # 主进程调用join的子进程结束后，才结束
  # # p.join(1) # 只等待1s
  # # 使用进程的属性
  # print('p2.pid', p2.pid)
  # print('p.name', p2.name)
  # print('p.is_alive()', p2.is_alive())
  # p = ClockProcess(2)
  # p.start()
  ##### 进程池的使用 #####
  # pool = Pool(processes=3)
  # for i in range(5):
  #   name = 'hello %d ' % i
  #   pool.apply_async(func=single_process, args=(name, i)) # apply 同步执行，apply_async异步执行
  # pool.close() # 如果不接受请求了，就关闭， 如果不使用join，且使用apply_async直接关闭
  # pool.join()
  Process(target=global_work1).start()
  Process(target=global_work2).start()
  print('globe num = %d' % num)  #
  print('test_multi_process done')

# pool.apply_async(func=foo, args=(i, ), callback=bar) 进程反馈
def bar(*args):
  print('>>done: ', args, os.getpid())


manager = Manager()
m_dict = manager.dict()
m_list = manager.list()


def func():
  m_dict['key'] = 'value'
  m_list.append(os.getpid())


def manager_usage():
  p_list = []
  for i in range(10):
    p = Process(target=func)
    p.start()
    p_list.append(p)
  for p in p_list:
    p.join()
  print(m_list)
  print(m_dict)


if __name__ == '__main__':
  # test_multi_process()
  manager_usage()
