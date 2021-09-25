from multiprocessing import Queue, Process, Pool, Manager, Pipe
from time import sleep


def basic_usage():
  q = Queue(3) # 指定队列大小，如果不写默认无限
  q.put('消息1')
  q.put('消息2')
  q.put('消息3')
  # q.put('消息4') # 一直等待直到进入
  if not q.full():
    q.put('消息5', block=True, timeout=1) # 等待1s，如果还没有put成功，直接抛异常
  print('判断队列是否已满: %s' % q.full())
  print(q.get()) # 获取并删除
  print(q.get())
  print(q.get())
  # print(q.get()) # 一直等待获取
  if not q.empty():
    print(q.get(block=True,timeout=1)) # 等待获取，超时1s，则抛异常
  print('判断队列是否为空: %s' % q.empty())
  # print('队列大小 %d' % q.qsize()) # qsize error in mac osx

'''
' 队列中通信
' 如果使用Pool创建进程，需要使用 Manager中的Queue来完成进程间的通信
' 如果使用Process,则使用multiprocessing.Queue
'''
def write(q:Queue):
  a = ['a', 'b', 'c', 'd']
  for i in a:
      print('is writing %s' % i )
      q.put(i)
      sleep(1)

def read(q:Queue):
  for i in range(4):
    print('is redding %s' % q.get())
    sleep(1)

def queue_usage():
  # 进程的通信
  q = Queue()
  pw = Process(target=write, args=(q,))
  pr = Process(target=read, args=(q,))
  pw.start()
  pr.start()
  pw.join()
  pr.join()
  # 进程池
  q = Manager().Queue()
  pool = Pool(3)
  pool.apply(write, (q,))
  pool.apply(read, (q,))
  pool.close()


'''
'  pip u管道的使用
'''


def func_pipe(conn):
  conn.send('send by child')
  print('child recv:', conn.recv())
  conn.close()


def pipe_usage():
  parent_conn, child_conn = Pipe()	# 获得 Pipe 连接的两端
  p = Process(target=func_pipe, args=(child_conn, ))
  p.start()
  print('parent recv:', parent_conn.recv())
  parent_conn.send('send by parent')
  p.join()


if __name__ == '__main__':
  # basic_usage()

  pipe_usage()
