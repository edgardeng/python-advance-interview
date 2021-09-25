''' 双向链表的案例
'''

# 双向链表节点
class LinkNode(object):
  def __init__(self, ele):
    self.ele = ele
    self.next = None
    self.prev = None


# 双向链表
class DoubleLinkNodeList(object):

  def __init__(self, item = None):
    self.__head = LinkNode(item) if item is not None else None  # 私有化属性 _

  def add(self, item):
    node = LinkNode(item)
    if self.__head is not None:
      self.__head.prev = node
    node.next = self.__head
    self.__head = node

  def append(self, item):
    node = self.__head
    if node is None:
      self.__head = LinkNode(item)
      return
    while node.next != None:
      node = node.next
    last = LinkNode(item)
    last.prev = node
    node.next = last

  # 指定位置的插入
  def insert(self, index, item):
    # 如果传入的小于等于0 插入头部
    # 大于长度 插入尾部
    if index <= 0:
      self.add(item)
      return
    count = 0
    node = self.__head
    while count < index - 1 and node.next is not None:
      count += 1
      node = node.next
    new_node = LinkNode(item)
    new_node.next = node.next
    new_node.prev = node
    node.next = new_node

  # 删除 结点（某个值）
  def remove(self, item):
    node = self.__head
    while node != None:
      if node.ele == item: # 找到了
        if node.prev is None:
          node.prev = None
          self.__head = node.next # 头结点
        else:
          if node.next is not None:
            node.next.prev = node.prev
          node.prev.next = node.next
        break
      else:
        node = node.next


  def search(self, v):
    node = self.__head
    while node != None:
      if node.ele == v:
        return True
      node = node.next
    return False

  def is_empty(self):
    return self.__head == None

  def length(self):
    count = 0
    node = self.__head
    while node != None:
      count += 1
      node = node.next
    return count

  def travel(self):
    node = self.__head
    while node != None:
      print(node.ele)
      node = node.next
    print('')


if __name__ == '__main__':
  double_link = DoubleLinkNodeList()
  double_link.add(1)
  double_link.add(2)
  double_link.add(3)
  double_link.append(4)
  double_link.append(5)
  double_link.append(6)
  double_link.insert(-1, 0)
  double_link.insert(300, 200)
  double_link.insert(4, 400)
  double_link.remove(200)
  double_link.travel()
  print(double_link.search(3))
