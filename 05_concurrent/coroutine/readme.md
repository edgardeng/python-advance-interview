# Coroutine 协程

## 协程概念
线程是系统级别的，由操作系统调度
协程是程序级别的，由程序根据自己需要调度

子程序的顺序执行在栈中

一个线程会有多个函数，这些函数称为子程序。在子程序执行过程中，可以中断去执行别的子程序，而别的子程序也可以中断回来继续执行之前的子程，这个过程称为 协程

```
def A()
def B()
```

由协程执行，在执行A的过程可以中断去执行B，在回来执行A

协程拥有自己的寄存器上下文和栈

协程调度切换时，将寄存器上下文

协程优点：
    * 无需线程上下文切换的开销，避免无意义的调度，提高性能
    * 无需原子操作锁定及同步的开销
    * 方便切换控制流
    * 高并发+高扩展+低成本
    
协程的缺点：
   * 无法利用多核资源 （本质是单线程）
   * 进行阻塞操作是会阻塞整个程序
   
### python的实现

在python中，通过generator实现。
在generator中，不但可以通过for迭代，可不断抵用next()函数，获取由yield语句返回的下一个值

* yield  
    > 看作return
* send
    > 给 generator 发送数据


## 同步 & 异步

同步： 先执行一个事务，如果遇到阻塞，会一直等待，直到第一个事务完毕，才能执行第二个
异步： 执行第一个事务，如果遇到阻塞，会直接执行第二个，不会等待。通过状态、同志、回调来处理结果

并发的方式有多种：多线程，多进程，异步IO

多线程，多进程场景： CPU密集型（科学计算）
异步IO： IO密集型（网络爬虫/web服务）


### asyncio
> 在python中使用asyncio（python3.4引入）
asyncio的编程模型就是一个消息循环。从asyncio模块直接获取一个EventLoop的引用，然后把需要执行的协程扔到EventLoop中

  * event_loop 事件循环
  * coroutine 协程
  * task 任务
  * future 待执行
  * aysnc / wait （python3.5定义 协程的关键字）

Don’t directly create Task instances: use the ensure_future() function or the BaseEventLoop.create_task() method.

翻译：不要直接创建 Task 实例，应该使用 ensure_future() 函数或 BaseEventLoop.create_task() 方法。

为什么呢？看 create_task 的文档：

Third-party event loops can use their own subclass of Task for interoperability. In this case, the result type is a subclass of Task.

翻译：为了 interoperability，第三方的事件循环可以使用自己的 Task 子类。这种情况下，返回结果的类型是 Task 的子类。

那么用 ensure_future 还是 create_task 呢？先对比一下函数声明：

asyncio.ensure_future(coro_or_future, *, loop=None)
BaseEventLoop.create_task(coro)

显然，ensure_future 除了接受 coroutine 作为参数，还接受 future 作为参数。

看 ensure_future 的代码，会发现 ensure_future 内部在某些条件下会调用 create_task，综上所述：

ensure_future: 最高层的函数，推荐使用！
create_task: 在确定参数是 coroutine 的情况下可以使用。
Task: 可能很多时候也可以工作，但真的没有使用的理由！

#### await

使用await 可以针对耗时的操作进行挂起，如生成器的yield。
协程遇到await，事件循环会挂起该协程，执行别的协程，直到其他的协程也挂起或执行完毕，再进行下一个协程


### 并发和并行

并发： 多个任务需要同时执行
并行：同一个时刻有多个任务执行

状态：

* Pending
* Running
* Done
* Cancelled











   
