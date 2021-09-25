'''
' 在函数中使用了yield ，该函数成为了一个 生成器
' 可以使用遍历，也可以使用遍历
'''
from time import sleep

# yield的使用
def foo():
  print('foo start.')
  while True:
    res = yield 4
    print('res:', res)


def A():
  while True:
    print('----- A -----')
    yield
    sleep(0.5)


def B(c):
  while True:
    print('----- B -----')
    c.__next__()
    sleep(0.5)

def basic_usage():
  g = foo()
  print(type(g))
  print(next(g))
  print('*' * 30)
  print(next(g))
  print('*' * 30)
  print(next(g))
  print('*' * 30)
  a = A() # 生成一个生成器对象
  B(a)




if __name__ == '__main__':
  basic_usage()
