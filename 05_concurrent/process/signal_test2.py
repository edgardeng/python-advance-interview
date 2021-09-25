# -*- coding: utf-8 -*-
# @author: edgardeng
# @date:   2021-03-18
# @file:   信号量

import signal
import time
from functools import partial
from multiprocessing import Process, Queue


class Counter(object):
    def __init__(self, val):
        self.current = val

    def next(self):
        self.current += 1
        return self.current

    def restart(self, val=0):
        self.current = val


def handler(counter, signalnum, queue):
    print("received signal:", signalnum)
    counter.restart(queue.get())


def start_count(q):
    counter = Counter(0)

    signal.signal(signal.SIGABRT, partial(handler, counter, q))

    while True:
        print('--', counter.next())
        time.sleep(0.2)


def interval_restart(q):
    """  定时重启"""
    while True:
        time.sleep(2)
        q.put(0)
        signal.alarm(2)


if __name__ == '__main__':
    queue = Queue()
    process1 = Process(target=start_count, args=(queue,))
    process2 = Process(target=interval_restart, args=(queue,))
    process1.start()
    process2.start()
