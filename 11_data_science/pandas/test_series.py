'''
pandas demo - Series的使用 （ pandas-1.1.2 ）
'''
import numpy as np
from pandas import Series, DataFrame
import pandas as pd


def update_series():
  ser = Series([1, 2, 3, 4, 5], index=['a', 'b', 'c', 'd', 'e'])
  print('根据列表+索引创建:\n', ser)
  s = ser.drop('c') #
  print('删除后的结果:\n', s)
  s = ser.drop(['a', 'c']) #
  print('删除多个后的结果:\n', s)
  ser.pop('d')
  # ser.pop(0) # 索引删除 invalid key
  # ser.pop([0,1]) # 删除多个 invalid key
  print('pop删除，修改源数据:\n', ser)
  ser[0] = 1000
  ser['f'] = 2000
  ser2 = Series([100, 200], index=['x', 'y'])
  ser.append(ser2)
  print('修改Series:\n', ser)
  print(' Series append:\n', ser.append(ser2))


def create_series():
  # python 列表, 自动索引
  s = Series([1, 2, 3, 4, 5])
  print('根据列表创建:\n', s)
  s = Series([1, 2, 3, 4, 5], index=['a', 'b', 'c', 'd', 'e'])
  print('根据列表+索引创建:\n', s)
  # 标量值
  s = Series(100, index=['a', 'b', 'c', 'd', 'e'])
  print('标量值创建:\n', s)
  s = Series({'a': 100, 'b': 200, 'c': 300})
  print('python字典 创建:\n', s)
  s = Series({'a': 100, 'b': 200, 'c': 300}, index=['h', 'i', 'j'])
  print('python字典+索引 创建:\n', s)
  # python字典
  # ndarray
  s = Series(np.arange(1, 10, 2))
  print('ndarray 创建:\n', s)
  s = Series(np.arange(1, 10, 2), index=np.arange(10, 5, -1))
  print('ndarray + 索引创建:\n', s)

  # 其他函数：range
  print('-' * 30, '数据访问')
  # series的反问
  print(s.index, type(s.index))
  print(s.values, type(s.values))
  s.name = '序列的对象名称'
  s.index.name = '索引名称'
  print(s)
  print('位置访问:\n', s[6])
  print('标签索引:\n', s[10])
  print('多个数据:\n', s[{6, 7, 8}])
  print('切片:\n', s[:9], s[:-1])
  print('过滤：\n', s[s > 5])




if __name__ == '__main__':
  # create_series()
  update_series()
