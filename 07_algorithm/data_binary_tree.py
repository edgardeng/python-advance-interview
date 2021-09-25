'''二叉树
'''

class TreeNode(object):
  def __init__(self, ele):
    self.ele = ele
    self.left = None
    self.right = None


class Tree(object):
  def __init__(self, item=None):
    self.root = TreeNode(item) if item is not None else None

  # 添加 从左至右 从上到下添加
  def add(self, item):
    node = TreeNode(item)
    if self.root is None:
      self.root = node
    else:
      queue = []
      queue.append(self.root)
      while queue:
        current = queue.pop(0) # 取出第1个
        if current.left is None:
          current.left = node
          return
        queue.append(current.left)
        if current.right is None:
          current.right = node
          return
        queue.append(current.right)

  # 层析遍历
  def travel(self):
    queue = []
    if self.root is None:
      return
    else:
      queue.append(self.root)
    while queue: # 直到为空
      current = queue.pop(0)
      print(current.ele)
      if current.left is not None:
        queue.append(current.left)
      if current.right is not None:
        queue.append(current.right)

  # 先序遍历（根 左 右边）
  def pre_order_travel(self, node):
    if node is None:
      return
    else:
      # node = self.root
      print(node.ele)
      self.pre_order_travel(node.left)
      self.pre_order_travel(node.right)


  # 中序遍历（ 左 根 右）
  def in_order_travel(self, node):
    if node is None:
      return
    else:
      # node = self.root
      self.in_order_travel(node.left)
      print(node.ele)
      self.in_order_travel(node.right)

  # 后序遍历（ 左 右 根）
  def last_order_travel(self, node):
    if node is None:
      return
    else:
      self.last_order_travel(node.left)
      self.last_order_travel(node.right)
      print(node.ele)


if __name__ == '__main__':
  t = Tree()
  t.add(1)
  t.add(2)
  t.add(3)
  t.add(4)
  t.add(5)
  t.add(6)
  print('--------- ')
#     1
#  2    3
# 4 5  6

  t.travel()
  print('--------- ')
  t.pre_order_travel(t.root)
  print('--------- ')
  t.in_order_travel(t.root)
  print('--------- ')
  t.last_order_travel(t.root)
