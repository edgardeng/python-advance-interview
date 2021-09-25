from threading import Thread, current_thread, Lock, local
from time import sleep
from queue import Queue


def thread1(name, delay):
  print('thread (%s) is running ' % current_thread().getName())
  print('thread1 is running with %s' % name)
  sleep(delay)
  print('thread1 is ending with %s' % name)


def thread2(name, delay):
  print('thread2 is running %s' % name)
  sleep(delay)
  print('thread2 is ending %s' % name)


def basic_usage():
  t1 = Thread(target=thread1, args=('one', 2,))
  t1.start()
  t2 = Thread(target=thread2, args=('two', 1,))
  t2.start()
  t1.join()
  t2.join()
  print('main thread is ending')


'''
' 自定义线程
'''


class ClockThead(Thread):
  def __init__(self, func, name, args):
    super().__init__(target=func, name=name, args=args)

  def run(self) -> None:
    print('ClockThead is running %s' % self._name)
    self._target(*self._args)


'''
' 线程共享全局变量
'''
num = 0
lock = Lock()


def test1():
  global num
  lock.acquire()  # 上锁
  for i in range(1000000):
    num += 1
  lock.release()
  print('test1 after num= %d ' % num)


def test2():
  global num
  lock.acquire()
  for i in range(1000000):
    num += 1
  lock.release()
  print('test2 after num= %d ' % num)


def global_usage():
  global num
  t1 = Thread(target=test1)
  t2 = Thread(target=test2)
  t1.start()
  t2.start()
  t1.join()
  t2.join()
  print('main thread is ending num= %d' % num)


'''
' 线程同步
' 
'''

# 3 把锁
lock1 = Lock()
lock2 = Lock()
lock3 = Lock()
lock2.acquire()
lock3.acquire()


class Task1(Thread):
  def run(self):
    while True:
      if lock1.acquire():
        print('-- task 1')
        sleep(1)
        lock2.release()


class Task2(Thread):
  def run(self):
    while True:
      if lock2.acquire():
        print('-- task 2')
        sleep(1)
        lock3.release()


class Task3(Thread):
  def run(self):
    while True:
      if lock3.acquire():
        print('-- task 3')
        sleep(1)
        lock1.release()


def sync_usage():
  t1 = Task1()
  t2 = Task2()
  t3 = Task3()
  t1.start()
  t2.start()
  t3.start()


'''
' 生产者-消费模式
'''
# 全局的队列
queue2 = Queue()


class Producter(Thread):
  def run(self):
    global queue2
    count = 0
    while True:
      if queue2.qsize() < 1000:
        for i in range(100):
          count += 1
          msg = 'is creating No.%d' % count
          queue2.put(msg)
          print(msg)
        sleep(0.5)


class Consumer(Thread):
  def run(self):
    while True:
      if queue2.qsize() > 100:
        for i in range(10):
          msg = 'is getting %s' % queue2.get()
          print(msg)
      sleep(1)


def product_consumer():
  p = Producter()
  c = Consumer()
  p.start()
  sleep(1)
  c.start()

'''
' TheadLocal的使用
'''
local_val = local()


def get_student_name():
  name = local_val.name
  print('Thread(%s), name = %s ' % (current_thread().getName(), name))


def process_thread(name):
  local_val.name = name
  get_student_name()


def thread_local_usage():
  t1 = Thread(target=process_thread, args=('张三',))
  t2 = Thread(target=process_thread, args=('李四',))
  t1.start()
  t2.start()


if __name__ == '__main__':
  # basic_usage()
  # ClockThead(thread1, 'ClockTheadName', ('clock', 0.5,)).start()
  # global_usage()
  # sync_usage()
  # product_consumer()
  thread_local_usage()
