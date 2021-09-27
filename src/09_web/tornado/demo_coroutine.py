import time

from tornado.ioloop import IOLoop
from tornado.gen import sleep


async def divide(x, y):
    return x / y


def bad_call():
    # This should raise a ZeroDivisionError, but it won't because
    # the coroutine is called incorrectly.
    divide(1, 0)


async def good_call():
    await divide(1, 0)

async def do_something():
    await sleep(5)

async def minute_loop():
    while True:
        print('minute_loop')
        t = time.time()
        nxt = sleep(10)   # Start the clock.
        await do_something()  # Run while the clock is ticking.
        await nxt
        print('loop end', time.time() -t)

# Coroutines that loop forever are generally started with
# spawn_callback().
# IOLoop.current().spawn_callback(minute_loop)


if __name__ == '__main__':
    # t = time.time()
    # IOLoop.current().run_in_executor(None, minute_loop)
    # print(time.time() -t)


    # # The IOLoop will catch the exception and print a stack trace in
    # # the logs. Note that this doesn't look like a normal call, since
    # # we pass the function object to be called by the IOLoop.
    # IOLoop.current().spawn_callback(divide, 1, 0)
    # # run_sync() doesn't take arguments, so we must wrap the
    # # call in a lambda.
    IOLoop.current().run_sync(minute_loop) # 或报错
