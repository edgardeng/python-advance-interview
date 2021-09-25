# Python 并发编程

## 多进程

### 进程 (process)
进程是对各种资源管理的集合，包含对各种资源的调用、内存的管理、网络接口的调用
进程要操作 CPU 必须先启动一个线程，启动一个进程的时候会自动创建一个线程，进程里的第一个线程就是主线程
程序执行的实例
有唯一的进程标识符(pid)

> 在python中使用 multiprossing 模块
 
* Proccess

* Pool
    * apply 一个池工作进程中执行函数
    * apply_async 异步执行函数
    * close 关闭进程池，如果进程终止前完成有挂起的操作，将在工作
    * join 等待所有工作进程退出，（只能在close或terminate之后调用）
    * imap map函数版本，返回迭代器
    * imap_unordered 同上，结果顺序根据从工作进程接收到的时间任意确定
    * map 将可调用对象func应用给iterable中的所有项
       然后以列表的形式返回，通过将iterable划分为多块并将工作分派给工作进程，可以并行执行操作
    * map_async 返回结果是异步的
    * terminate 立即终止所有工作进程。如果p被垃圾回收，将自动调用该函数
    * get 返回结果，如果有必要则等到结果到达。timeout是可选的超时
    * ready 调用成功，返回True
    * successful 调用完成且没有引发异常，返回True
    * wait    等待结果变成可用，timeout是可选的超时   
       
所有进程都是由父进程启动的， 子进程的数据不共享

* Queue (multiprossing.Queue)多进程安全的队列， 先进先出
同步的、线程安全的队列类，包括FIFO（先入先出)队列Queue，LIFO（后入先出）队列LifoQueue，和优先级队列PriorityQueue。这些队列都实现了锁原语，能够在多线程中直接使用。可以使用队列来实现线程间的同步。

    * Queue.qsize() 返回队列的大小
    * Queue.empty() 如果队列为空，返回True,反之False
    * Queue.full() 如果队列满了，返回True,反之False，Queue.full 与 maxsize 大小对应
    * Queue.get([block[, timeout]])获取队列，timeout等待时间
    * Queue.get_nowait() 相当于Queue.get(False)，非阻塞方法
    * Queue.put(item) 写入队列，timeout等待时间
    * Queue.task_done() 在完成一项工作之后，Queue.task_done()函数向任务已经完成的队列发送一个信号。每个get()调用得到一个任务，接下来task_done()调用告诉队列该任务已经处理完毕。
    * Queue.join() 实际上意味着等到队列为空，再执行别的操作

> 线程间共享内存空间，进程间只能通过其他方法(Queue)进行通信

注意这个 multiprossing.Queue 不同于 queue.Queue
Queue type using a pipe, buffer and thread
两个进程的 Queue 并不是同一个，而是将数据 pickle 后传给另一个进程的 Queue
用于父进程与子进程之间的通信或同一父进程的子进程之间通信

* Pipe (管道) 是通过 socket 进行进程间通信的
    > 步骤与建立 socket 连接相似：建立连接、发送/接收数据（一端发送另一端不接受就会阻塞）、关闭连接

* Manager 实现的是进程间共享数据

  支持的可共享数据类型：
  list
  dict
  Value
  Array
  Namespace
  Queue 				queue.Queue
  JoinableQueue		queue.Queue
  Event 				threading.Event
  Lock 				threading.Lock
  RLock 				threading.RLock
  Semaphore 			threading.Semaphore
  BoundedSemaphore 	threading.BoundedSemaphore
  Condition 			threading.Condition
  Barrier 			threading.Barrier
  Pool 				pool.Pool
  
## 多线程 
(thread)
线程是实现多任务的一种方式。一个进程中，可以同时运行多个子任务/线程。
一个进程可以拥有多个并行的线程，其中每一个线程，共享当前进程的资源

区别

||进程|线程|
|:----|:----|:----|
|根本|资源分配的单位|调度和执行的单位|
|开销|每个进程有独立的代码和数据空间，进程间的切换有较大开销|线程可以看出轻量级的进程，多线程共享内存，切换开销小|
|环境|一个系统，多个进程/任务|在程序中，多个顺序流同时进行|
|内存|每个进程分配不同的内存区域|线程的资源是所属进程的资源|

在python2中使用 thread模块， 在python3使用threading

* Thread(group=None,target=None)

    * run
    * start
    * join
    * isAlive
    * getName
    * setName
 
* Lock
    acquire 上锁
    release 释放锁
 
* Queue
    
* Local
    本身是个全局变量。但每个线程可以利用它保存属于自己的属性，且其他线程不可见
        
__线程共享数据的安全问题__：

1. 多个线程同时修改一个变量是线程不安全的
2. 使用互斥锁，保证每次只有一个线程进行写入，保证多线程下的数据正确性


互斥锁
    如果多个线程共同对某个数据修改，可能出现不可预料的结果
锁的状态：锁定/未锁定

## 生产者 - 消费者 模式

生产者： 生产数据的线程

消费者： 消费数据的线程
生产者-消费者模式，通过一个容器来解决生产者和消费者的强耦合问题。
使用queue提供线程间通信
queeu.Queue 线程安全的


## 协程和异步
