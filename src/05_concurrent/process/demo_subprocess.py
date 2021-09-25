# -*- coding: utf-8 -*-
# @author: edgardeng
# @date:   2021-03-18
# @file: subprocess 的示例

import subprocess
import sys


def out_readline():
    p = subprocess.Popen("python test.py", shell=True, stdout=subprocess.PIPE)
    # 设值subprocess.stdout=PIPE 即通过管道 p.stdout.read()取出
    while p.poll() is None:  # poll检查子进程是否终止，返回对象的returncode
        out = p.stdout.readline()
        if out:
            print(out)
    # out = p.stdout.read() # 一次性取出
    # print(out)


def test_communicate():
    print('*'*20)
    popen = subprocess.Popen('ping www.baidu.com', shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
    out, err = popen.communicate()

    print(out.decode('gbk'))
    print(err)
    print(str(popen.returncode))

    print('*'*20)
    popen = subprocess.Popen('python test.py', shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE )
    out, err = popen.communicate()
    print(out.decode('utf-8'))
    print(err)
    print(str(popen.returncode))


if __name__ == '__main__':
    # print('start')
    out_readline()
    # test_communicate()


