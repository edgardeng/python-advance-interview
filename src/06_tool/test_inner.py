'''
str 在内建模块中


内建属性
  常用内置类属性
    __dict__ 类的属性
    __name__ 类名
    __doc__   文档字符串 在init前
    __module__ 类所在的模块
    __base__ 类的所有父类构成的元组
  属性拦截器


内建函数
  range (start,end,step)
  map (func,iterable)    映射  func返回修改后的值
  filter(func,iterable)  过滤器: func返回True /False
  reduce (func,iterable)
  sorted(func,iterable)  排序: 返回排序后的副本
'''

from collections.abc import Iterator
# reduce 在 python3之后 引入toool
from functools import reduce




class Person():
  '''
    Person With Name Age
  '''

  def __init__(self, name, age):
    self.name = name
    self.age = age

  def __str__(self):
    return '(%s,%d)' % (self.name, self.age)

  # 属性拦截器
  # def __getattribute__(self, item):
  #   print('is get .' + item)
  #   if item == 'name':
  #     return 'Person-Name'  # 不能获取其他属性比如 self.age
  #   else:
  #     return 'OTHERS'


def double_list(x):
  return x * 2


if __name__ == '__main__':
  # p = Person('a', 1)
  # print(p.name)
  # print(p.age)
  # print(p.name)

  list = ['a', 'b', 'c']
  list2 = map(double_list, list)  # 返回一个迭代器
  list3 = map(lambda x: x * 3, list)  # 使用匿名函数
  print(type(list2))
  print(isinstance(list2, Iterator))
  print(list2)
  for i in list3:
    print(i)

  list4 = [x for x in range(0, 100)]
  list5 = filter(lambda x: x % 2 == 0, list4)  # 过滤出偶数 返回一个迭代器
  # for i in list5:
  #   print(i)
  sum_list = reduce(lambda x, y: x + y, list4) #
  print(sum_list)
  combine = reduce(lambda x, y: x + y, list)
  print(combine)
  list6 = [9,4,6,1,2]
  sort_list = sorted(list6) # 从小到大
  sort_list2 = sorted(list6, reverse=True) # 反向从大到小
  print(sort_list)
  print(sort_list2)

  list7 = [Person('a',1),Person('b',6),Person('c',3)]
  # sort_list = sorted(list7)  # 报错 TypeError: '<' not supported between instances of 'Person' and 'Person'
  sort_person = sorted(list7,key=lambda x:x.age)
  print(sort_person)
  for i in sort_person:
    print(i)
