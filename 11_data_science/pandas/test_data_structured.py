'''
pandas demo -数据规整 （ numpy-1.19.2  pandas-1.1.2  scikit-learn-0.23.2 ）
'''
import numpy as np
from pandas import Series, DataFrame
import pandas as pd
from sqlalchemy import create_engine


def test_index():
  data = pd.Series(np.random.randn(9), index=[['a', 'a', 'a', 'b', 'b', 'b', 'c', 'c', 'c'], [1, 2, 3] * 3])
  print(data.index)  # 会得到层次化索引MultiIndex
  print(data['a'])  # 利用层次化索引获取数据
  print(data['a':'c'])
  print(data[:, 1])
  print(data.loc['a':'c', 1:2])

  array = np.random.randn(20).reshape(4, 5)
  df = pd.DataFrame(array,
                    index=[['a', 'a', 'b', 'c'], [1, 2, 1, 2]],
                    columns=[['A', 'A', 'B', 'B', 'C'], [1, 2, 3, 1, 2]])
  print('使用列表创建层次索引\r\n', df)
  df2 = pd.DataFrame(np.random.randn(16).reshape(4, 4),
                     index=pd.MultiIndex.from_product([['a', 'b'], [1, 2]]),
                     columns=pd.MultiIndex.from_product([['A', 'B'], [1, 2]]))
  print('使用MultiIndex创建层次索引\r\n', df2)  # 注意行列匹配

  # 指定各层索引的名称
  df.index.names = ['k1', 'k2']  # 2层行索引
  df.columns.names = ['c1', 'c2']  # 2层列索引
  print(df)
  df.swaplevel('k1', 'k2')  # 返回数据的新副本
  print('使用 swaplevel 索引级别互换\r\n', df.swaplevel('k1', 'k2'))
  df.sort_index(level=0)  # 返回数据的新副本
  print('使用 sort_index 分类排序\r\n', df.swaplevel('k1', 'k2').sort_index(level=0))

  print('按层(行)汇总\r\n', df.sum(level='k1'))
  print('按层（列）汇总\r\n', df.sum(level='c1', axis=1))  # 其他是一样

  # 使用列作为行索引
  df = pd.DataFrame({
    'year': [2016, 2016, 2017, 2017, 2018, 2018],
    'fruit': ['apple', 'banana', 'apple', 'banana', 'apple', 'banana'],
    'production ': [10, 20, 20, 30, 30, 40],
    'profile': [50, 40, 40, 30, 30, 20]
  })
  new_df = df.set_index(['year', 'fruit'])
  print(new_df)
  print(new_df.reset_index())

  df3 = pd.DataFrame(np.random.randn(6).reshape(2, 3),
                     index=pd.Index(['A', 'B'], name='name'),
                     columns=pd.Index(['one', 'two', 'three'], name='no.'))
  print('stack 索引重塑\r\n', df3.stack())
  print('unstack 索引重塑\r\n', df3.stack().unstack())
  print('unstack 索引重塑\r\n', df3.stack().unstack(0))
  df = pd.DataFrame({'left': df3.stack(), 'right': df3.stack() + 3},
                    columns=pd.Index(['left', 'right'], name='side'))
  print('原数据\r\n', df)
  print('指定列 stack 索引重塑\r\n', df.unstack('name'))  #
  df = pd.DataFrame({'A': ['one', 'one', 'one', 'two', 'two', 'two'], 'B': list('abcdef'), 'C': range(1, 7)})
  print('原数据\r\n', df)
  print('pivot 旋转索引\r\n', df.pivot(index='A', columns='B', values='C'))


def test_concat():
  df1 = pd.DataFrame({'A': ['A1', 'A2', 'A3'], 'B': ['B1', 'B2', 'B3']})
  df2 = pd.DataFrame({'A': ['1', '2', '3'], 'B': ['1', '2', '3']})
  df3 = pd.DataFrame({'A': [0, 1, 2, 3], 'B': [10, 11, 12, 13], 'D': [20, 21, 22, 23]})

  print('索引相同的 横向叠加 \r\n', pd.concat([df1, df2], axis=1))
  print('索引不同的 横向叠加 \r\n', pd.concat([df1, df3], axis=1))
  print('索引不同的 横向叠加 inner \r\n', pd.concat([df1, df3], axis=1, join='inner'))
  print('索引相同的 纵向叠加 \r\n', pd.concat([df1, df2], axis=0))
  print('索引不同的 纵向叠加 \r\n', pd.concat([df1, df3], axis=0))
  print('索引不同的 纵向叠加 inner\r\n', pd.concat([df1, df3], axis=0, join='inner'))
  print('append 纵向叠加 \r\n', df1.append(df2))  # 返回新副本


# 主键合并数据
def test_merge():
  df1 = pd.DataFrame({'key': ['A', 'B', 'C', 'A'], 'data1': range(4)})
  df2 = pd.DataFrame({'key': ['A', 'B'], 'data2': range(2)})
  df3 = pd.DataFrame({'key2': ['A', 'A', 'B', 'B', 'C', 'C'], 'data3': range(11, 17)})

  print('merge 主键合并 \r\n', pd.merge(df1, df2))
  print('merge 主键合并 \r\n', pd.merge(df1, df2, on='key'))
  print('merge 主键合并 外连接 \r\n', pd.merge(df1, df2, how='outer'))
  print('列名不同 merge 主键合并 \r\n', pd.merge(df1, df3, left_on='key', right_on='key2'))
  print('join 主键合并 \r\n', df1.join(df2, lsuffix='_l', rsuffix='_r'))
  print('set_index join 主键合并 \r\n', df1.set_index('key').join(df2.set_index('key')))  # 通过指定的列连接
  print('set_index join 主键合并 \r\n', df1.join(df2.set_index('key'), on='key'))  # 通过指定的列连接


# 重叠合并数据
def test_combine():
  df1 = pd.DataFrame({'a': [1, np.NAN, 5, np.NAN], 'b': [np.NAN, 5, np.NAN, 4]})
  df2 = pd.DataFrame({'a': [5, 1, np.NAN, 8, 9], 'b': [np.NAN, 11, 12, 13, 14]})
  print(df1)
  print(df2)
  print('用后者给前者打补丁', df1.combine_first(df2))
  print('用后者给前者打补丁', df2.combine_first(df1))


if __name__ == '__main__':
  test_index()
  # test_concat()
  # test_merge()

  # test_combine()
