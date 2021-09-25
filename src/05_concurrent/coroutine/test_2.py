'''
' 在函数中使用了send ，该函数成为了一个 生成器(可以使用遍历，也可以使用遍历)

在函数中使用了send
'''
from time import sleep


# yield的使用
def foo():
  print('foo start.')
  while True:
    res = yield 4
    print('res:', res)


def basic_usage():
  g = foo()
  print(type(g))
  print(next(g))
  print('*' * 30)
  print(g.send(10))  # 使用send 发送一个数据


# 使用send + yield 实现生产/消费模式

def produce(c):
  for i in range(10):
    print('produce:    ', i)
    c.send(str(i))


def consume():
  while True:
    res = yield
    print('consume:    ', res)


if __name__ == '__main__':
  # basic_usage()
  c = consume()
  next(c)  # 先跑到 yield 那一步
  produce(c)
