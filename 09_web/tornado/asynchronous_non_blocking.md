# Tornado

## Asynchronous and non-Blocking I/O

Real-time web features require a long-lived mostly-idle connection per user. 
In a traditional synchronous web server, this implies devoting one thread to each user, which can be very expensive.
实时网络功能要求每个用户都有一个长期的、几乎是空闲的连接。
在传统的同步web服务器中，这意味着为每个用户分配一个线程，这可能非常昂贵。

To minimize the cost of concurrent connections, Tornado uses a single-threaded event loop. 
This means that all application code should aim to be asynchronous and non-blocking because only one operation can be active at a time.
为了最小化并发连接的开销，Tornado使用单线程事件循环。
所有应用程序代码都应该以异步和非阻塞为目标，因为一次只能有一个操作是活动的。

### Blocking
A function blocks when it waits for something to happen before returning.
A function may block for many reasons: network I/O, disk I/O, mutexes, etc. 
In fact, every function blocks, at least a little bit, while it is running and using the CPU (for an extreme example that demonstrates why CPU blocking must be taken as seriously as other kinds of blocking, consider password hashing functions like bcrypt, which by design use hundreds of milliseconds of CPU time, far more than a typical network or disk access).

A function can be blocking in some respects and non-blocking in others. 
In the context of Tornado we generally talk about blocking in the context of network I/O, although all kinds of blocking are to be minimized.
在Tornado的上下文中，我们通常讨论网络I/O中的阻塞，尽管所有类型的阻塞都要被最小化。

### Asynchronous 异步

An asynchronous function returns before it is finished, and generally causes some work to happen in the background before triggering some future action in the application (as opposed to normal synchronous functions, which do everything they are going to do before returning). 
There are many styles of asynchronous interfaces:

 * Callback argument 回调参数
 * Return a placeholder (Future, Promise, Deferred) 返回一个占位符(
 * Deliver to a queue 发送到队列
 * Callback registry (e.g. POSIX signals) 回调注册表(例如POSIX信号)
 
Regardless of which type of interface is used, asynchronous functions by definition interact differently with their callers; 
there is no free way to make a synchronous function asynchronous in a way that is transparent to its callers (systems like gevent use lightweight threads to offer performance comparable to asynchronous systems, but they do not actually make things asynchronous).
无论使用哪种类型的接口，从定义上讲，异步函数与调用者的交互是不同的;
没有一种方法可以让同步函数以对其调用者透明的方式实现异步(像gevent这样的系统使用轻量级线程来提供与异步系统相当的性能，但它们实际上并没有实现异步)。

Asynchronous operations in Tornado generally return placeholder objects (Futures), with the exception of some low-level components like the IOLoop that use callbacks. Futures are usually transformed into their result with the await or yield keywords.

### Examples

Here is a sample synchronous function:

```python
from tornado.httpclient import HTTPClient
def synchronous_fetch(url):
    http_client = HTTPClient()
    response = http_client.fetch(url)
    return response.body

```

same function rewritten asynchronously as a native coroutine:

```python
from tornado.httpclient import AsyncHTTPClient
async def asynchronous_fetch(url):
    http_client = AsyncHTTPClient()
    response = await http_client.fetch(url)
    return response.body
```

早期版本，tornado.gen实现
Or for compatibility with older versions of Python, using the tornado.gen module:

```python
from tornado.httpclient import AsyncHTTPClient
from tornado import gen

@gen.coroutine
def async_fetch_gen(url):
    http_client = AsyncHTTPClient()
    response = yield http_client.fetch(url)
    raise gen.Return(response.body)
```

Coroutines are a little magical, but what they do internally is something like this:

```python
from tornado.concurrent import Future
from tornado.httpclient import AsyncHTTPClient

def async_fetch_manual(url):
    http_client = AsyncHTTPClient()
    my_future = Future()
    fetch_future = http_client.fetch(url)
    def on_fetch(f):
        my_future.set_result(f.result().body)
    fetch_future.add_done_callback(on_fetch)
    return my_future
```

Notice that the coroutine returns its Future before the fetch is done.
注意，协程在获取完成之前返回Future。
This is what makes coroutines asynchronous.

Anything you can do with coroutines you can also do by passing callback objects around, but coroutines provide an important simplification by letting you organize your code in the same way you would if it were synchronous.
任何你能用协程做的事，你也可以通过传递回调对象来做，但是协程提供了一个重要的简化，让你以相同的方式组织你的代码如果它是同步的。

This is especially important for error handling, since `try/except` blocks work as you would expect in coroutines while this is difficult to achieve with callbacks.
