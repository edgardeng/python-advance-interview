
## Queue 队列

Tornado’s tornado.queues module implements an asynchronous producer / consumer pattern for coroutines, 
analogous to the pattern implemented for threads by the Python standard library’s queue module.

Tornado的queues模块为协程实现了异步生产者/消费者模式，类似于Python标准库的queue模块为线程实现的模式。

A coroutine that yields `Queue.get` pauses until there is an item in the queue. 使用Queue.get时，直到有才返回

If the queue has a maximum size set, a coroutine that yields `Queue.put` pauses until there is room for another item. 使用Queue.put时，直到未满才返回

A Queue maintains a count of unfinished tasks, which begins at zero. put increments the count; task_done decrements it.
队列中存在一定的未完成任务，put+1，task_done-1

## Example

a concurrent web spider
