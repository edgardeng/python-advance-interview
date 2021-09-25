# -*- coding: utf-8 -*-
# @author: edgardeng
# @date:   2021-05-08
# @file:   


from threading import Thread
import time
import ctypes
import inspect


class AThread(Thread):
    def run(self) -> None:
        while True:
            time.sleep(2)
            print(time.time())


def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)


def close_sub_thread():
    p = AThread()
    # p.daemon = True  # 关闭子进程 方式2 使用 daemon
    p.start()

    for i in range(10):
        time.sleep(0.5)
        print(i)
    # 主进程结束，但子进程未结束

    # 关闭子进程 方式1 使用terminate
    _async_raise(p.ident, SystemExit)

if __name__ == '__main__':
    close_sub_thread()
