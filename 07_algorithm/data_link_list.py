from timeit import Timer

''' 链表的示例
'''


def append_test():
  li = []
  for i in range(10000):
    li.append(i)


def insert_test():
  li = []
  for i in range(10000):
    li.insert(0, i)


# 链表节点
class LinkNode(object):
  def __init__(self, ele):
    self.ele = ele
    self.next = None


# 单向链表
class SingleLinkList():
  def __init__(self, item=None):
    self._head = LinkNode(item) if item != None else None  # 私有化属性 _

  def add(self, item):
    node = LinkNode(item)
    node.next = self._head
    self._head = node

  def append(self, item):
    node = self._head
    if node == None:
      self._head = LinkNode(item)
      return
    while node.next != None:
      node = node.next
    node.next = LinkNode(item)

  def insert(self, index, item):
    # 如果传入的小于等于0 插入头部
    # 大于长度 插入尾部
    if index <= 0:
      self.add(item)
    count = 0
    node = self._head
    while count < index - 1 and node != None:
      count += 1
      node = node.next
    item.next = node.next
    node.next = LinkNode(item)

  def remove(self, v):
    node = self._head
    pre = None
    while node != None:
      if node.ele == v:
        # 找到了
        if pre == None:  # 头结点
          self._head = node.next
        else:
          pre.next = node.next
        break
      else:
        pre = node
        node = node.next

  def search(self, v):
    node = self._head
    while node != None:
      if node.ele == v:
        return True
      node = node.next
    return False

  def is_empty(self):
    return self._head == None

  def length(self):
    count = 0
    node = self._head
    while node != None:
      count += 1
      node = node.next
    return count

  def travel(self):
    node = self._head
    while node != None:
      print(node.ele)
      node = node.next
    print('')

  # append_time = Timer('append_test()', 'from __main__ import append_test')  # 使用timeit模块测试代码的 执行时间
  # print('append_test 1000 time = ', append_time.timeit(1000))
  # insert_time = Timer('insert_test()', 'from __main__ import insert_test')
  # print('insert_test 1000 time = ', insert_time.timeit(1000))

  singleLink = SingleLinkList()
  print('is_empty : ', singleLink.is_empty())
  print('length : ', singleLink.length())
  singleLink.travel()
  singleLink.append(3)
  singleLink.travel()
  singleLink.add(6)
  singleLink.travel()
