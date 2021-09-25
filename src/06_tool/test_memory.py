'''
' 内存管理机制
1 小整数池 [-2,256]
2 大整数池
3 字符串
  intern机制 （相同的字符串（不包含空格/特殊字符），默认只有一个份）
  id() 查地址
  is  判断两个对象是不是同一个

垃圾回收机制 gc - garbage collection
  1. 引用计数机制
    获取引用计数 sys.getrefcount()
    添加引用计数 (加入列表，复制给新对象，将对象作为形参)
    减少引用计数 （移除）
  2. 隔代回收机制
'''

import sys, gc, time


class Person(object):
  def __init__(self):
    print('create.. :', hex(id(self)))  # 内存地址 转16进制

  def __new__(cls, *args, **kwargs):
    print('new..')
    return super(Person, cls).__new__(cls)
    # return super().__new__(cls)

  def __del__(self):
    print('del..')


def start():
  while True:
    a = Person()
    b = Person()
    a.child = b
    b.child = a
    del a  # 无法删除，只是减少引用计数
    del b
    print(gc.get_count())
    print(gc.get_threshold())
    time.sleep(0.1)


if __name__ == '__main__':
  # a = '122'
  # b = '123'
  # c = '122'
  # print(id(a), id(b), id(c))
  # print(a is c, a is b)
  #
  # p = Person()
  # print(sys.getrefcount(p))
  # print('-' * 50)
  #
  # list = []
  # list.append(p)
  # print(sys.getrefcount(p))
  # list.remove(p)
  # print(sys.getrefcount(p))
  # del p
  # print('-' * 50)
  # gc.set_threshold(100,5,5)
  # start()
  #
  a = 10
  b = 10
  print(id(a)==id(b))


