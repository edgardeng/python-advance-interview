# -*- coding: utf-8 -*-
# @author: edgardeng
# @date:   2021-05-08
# @file:   

from multiprocessing import Process, Queue
import time


class AProcess(Process):
    def run(self) -> None:
        while True:
            time.sleep(2)
            print(time.time())


def close_sub_process():
    p = AProcess()
    p.daemon = True  # 关闭子进程 方式2 使用 daemon
    p.start()

    for i in range(10):
        time.sleep(0.5)
        print(i)
    # 主进程结束，但子进程未结束

    # 关闭子进程 方式1 使用terminate
    # p.terminate()

if __name__ == '__main__':
    close_sub_process()
