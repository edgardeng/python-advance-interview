'''堆栈的实现
'''
class Stack(object):
  def __init__(self):
    self.__list = []

  # 压栈
  def push(self, item):
    self.__list.append(item)

  def pop(self):
    self.__list.pop()

  # 返回栈顶元素
  def peek(self):
    return self.__list[len(self.__list)-1]

  def is_empty(self):
    return self.__list is None or len(self.__list) < 1

  def length(self):
    return len(self.__list)


class Queue(object):
  def __init__(self):
    self.__list = []

  # 进队
  def enqueue(self, item):
    # self.__list.append(item) # append 比 insert 快，时间复杂度低
    self.__list.insert(0, item) # 头部进来

  def dequeue(self):
    self.__list.pop()  # 尾部出去

  def is_empty(self):
    return self.__list is None or len(self.__list) < 1

  def length(self):
    return len(self.__list)

if __name__ == '__main__':
  s = Stack()
  s.push(1)
  s.push(2)
  s.push(3)
  print(s.is_empty())
  print(s.length())
  print(s.peek())
  s.pop()
  print(s.peek())

