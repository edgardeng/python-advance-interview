## Coroutines

Coroutines use the Python await or yield keyword to suspend and resume execution instead of a chain of callbacks (cooperative lightweight threads as seen in frameworks like gevent are sometimes called coroutines as well, but in Tornado all coroutines use explicit context switches and are called as asynchronous functions).

协程使用Python await或yield关键字来挂起并恢复执行，而不是使用回调链(在gevent等框架中看到的协作轻量级线程有时也被称为协程，但在Tornado中，所有协程都使用显式上下文切换，并被称为异步函数)。

Coroutines make concurrency easier to reason about by reducing the number of places where a context switch can happen.
协程通过减少可能发生上下文切换的位置数量，使并发性更容易

Native coroutines are the recommended form whenever possible. Only use decorated coroutines when compatibility with older versions of Python is required.

```python
# Decorated:                    # Native:

# Normal function declaration
# with decorator                # "async def" keywords
@gen.coroutine
def a():                        async def a():
    # "yield" all async funcs       # "await" all async funcs
    b = yield c()                   b = await c()
    # "return" and "yield"
    # cannot be mixed in
    # Python 2, so raise a
    # special exception.            # Return normally
    raise gen.Return(b)             return b

```

Native coroutines: 原生协程
 * are generally faster. 生成更快
 * can use async for and async with statements which make some patterns much simpler. 语法简单
 * do not run at all unless you await or yield them. Decorated coroutines can start running “in the background” as soon as they are called. Note that for both kinds of coroutines it is important to use await or yield so that any exceptions have somewhere to go.
Decorated coroutines:
  * 额外的集成 additional integration with the concurrent.futures package, allowing the result of executor.submit to be yielded directly. For native coroutines, use IOLoop.run_in_executor instead.
  * support some shorthand for waiting on multiple objects by yielding a list or dict. Use tornado.gen.multi to do this in native coroutines.
  * can support integration with other packages including Twisted via a registry of conversion functions. To access this functionality in native coroutines, use tornado.gen.convert_yielded.
  * always return a Future object. Native coroutines return an awaitable object that is not a Future. In Tornado the two are mostly interchangeable.

### How it works 

A function containing yield is a generator.  含yield就是生成器
All generators are asynchronous; when called they return a generator object instead of running to completion. 

The @gen.coroutine decorator communicates with the generator via the yield expressions, and with the coroutine’s caller by returning a Future.

```python
# Simplified inner loop of tornado.gen.Runner
def run(self):
    # send(x) makes the current yield return x.
    # It returns when the next yield is reached
    future = self.gen.send(self.next)
    def callback(f):
        self.next = f.result()
        self.run()
    future.add_done_callback(callback)
```

The decorator receives a Future from the generator, waits (without blocking) for that Future to complete, then “unwraps” the Future and sends the result back into the generator as the result of the yield expression.

Most asynchronous code never touches the Future class directly except to immediately pass the Future returned by an asynchronous function to a yield expression.

### How to call a coroutine
Coroutines do not raise exceptions in the normal way: any exception they raise will be trapped in the awaitable object until it is yielded.
This means it is important to call coroutines in the right way, or you may have errors that go unnoticed:

```python
async def divide(x, y):
    return x / y

def bad_call():
    divide(1, 0) # should raise a ZeroDivisionError, but it won't 
```

In nearly all cases, any function that calls a coroutine must be a coroutine itself, and use the await or yield keyword in the call. When you are overriding a method defined in a superclass, consult the documentation to see if coroutines are allowed (the documentation should say that the method “may be a coroutine” or “may return a Future”):

```python
async def good_call():
    # await will unwrap the object returned by divide() and raise
    # the exception.
    await divide(1, 0)
```
Sometimes you may want to “fire and forget” a coroutine without waiting for its result. In this case it is recommended to use IOLoop.spawn_callback, which makes the IOLoop responsible for the call. If it fails, the IOLoop will log a stack trace:

```
# The IOLoop will catch the exception and print a stack trace in
# the logs. Note that this doesn't look like a normal call, since
# we pass the function object to be called by the IOLoop.
IOLoop.current().spawn_callback(divide, 1, 0)
```


Using IOLoop.spawn_callback in this way is recommended for functions using @gen.coroutine, but it is required for functions using async def (otherwise the coroutine runner will not start).

Finally, at the top level of a program, if the IOLoop is not yet running, you can start the IOLoop, run the coroutine, and then stop the IOLoop with the IOLoop.run_sync method. This is often used to start the main function of a batch-oriented program:

```
# run_sync() doesn't take arguments, so we must wrap the
# call in a lambda.
IOLoop.current().run_sync(lambda: divide(1, 0))
```

Coroutine patterns
Calling blocking functions
The simplest way to call a blocking function from a coroutine is to use IOLoop.run_in_executor, which returns Futures that are compatible with coroutines:

```
async def call_blocking():
await IOLoop.current().run_in_executor(None, blocking_func, args)
```

### Parallelism
The multi function accepts lists and dicts whose values are Futures, and waits for all of those Futures in parallel:

```
from tornado.gen import multi

async def parallel_fetch(url1, url2):
resp1, resp2 = await multi([http_client.fetch(url1),
http_client.fetch(url2)])

async def parallel_fetch_many(urls):
responses = await multi ([http_client.fetch(url) for url in urls])
# responses is a list of HTTPResponses in the same order

async def parallel_fetch_dict(urls):
responses = await multi({url: http_client.fetch(url)
for url in urls})
# responses is a dict {url: HTTPResponse}
In decorated coroutines, it is possible to yield the list or dict directly:

@gen.coroutine
def parallel_fetch_decorated(url1, url2):
resp1, resp2 = yield [http_client.fetch(url1),
http_client.fetch(url2)]
```
Interleaving
Sometimes it is useful to save a Future instead of yielding it immediately, so you can start another operation before waiting.

from tornado.gen import convert_yielded
```
async def get(self):
# convert_yielded() starts the native coroutine in the background.
# This is equivalent to asyncio.ensure_future() (both work in Tornado).
fetch_future = convert_yielded(self.fetch_next_chunk())
while True:
chunk = yield fetch_future
if chunk is None: break
self.write(chunk)
fetch_future = convert_yielded(self.fetch_next_chunk())
yield self.flush()
```

This is a little easier to do with decorated coroutines, because they start immediately when called:

```
@gen.coroutine
def get(self):
fetch_future = self.fetch_next_chunk()
while True:
chunk = yield fetch_future
if chunk is None: break
self.write(chunk)
fetch_future = self.fetch_next_chunk()
yield self.flush()
```
### Looping
In native coroutines, async for can be used. In older versions of Python, looping is tricky with coroutines since there is no way to yield on every iteration of a for or while loop and capture the result of the yield. Instead, you’ll need to separate the loop condition from accessing the results, as in this example from Motor:
```
import motor
db = motor.MotorClient().test

@gen.coroutine
def loop_example(collection):
cursor = db.collection.find()
while (yield cursor.fetch_next):
doc = cursor.next_object()
```
### Running in the background
PeriodicCallback is not normally used with coroutines. Instead, a coroutine can contain a while True: loop and use tornado.gen.sleep:

```python
async def minute_loop():
    while True:
        await do_something()
        await gen.sleep(60)

# Coroutines that loop forever are generally started with spawn_callback().        
IOLoop.current().spawn_callback(minute_loop)

```

Sometimes a more complicated loop may be desirable. For example, the previous loop runs every 60+N seconds, where N is the running time of do_something(). To run exactly every 60 seconds, use the interleaving pattern from above:

```python
async def minute_loop2():
    while True:
        nxt = gen.sleep(60)   # Start the clock.
        await do_something()  # Run while the clock is ticking.
        await nxt             # Wait for the timer to run out.
```
