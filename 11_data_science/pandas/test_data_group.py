'''
pandas demo -数据聚合（ numpy-1.19.2  pandas-1.1.2  scikit-learn-0.23.2 ）
'''

import numpy as np
import pandas as pd

df = pd.DataFrame({
  'key1': ['a', 'b', 'c'] * 2,
  'key2': ['one', 'two'] * 3,
  'data1': np.random.randn(6),
  'data2': np.random.randn(6)
})
print('原数据\r\n', df)


# groupby 的使用
def group_by_usage():
  # 单列分组
  grouped = df['data1'].groupby(df['key1'])
  print(grouped)
  print('\r\n goupby mean \r\n', grouped.mean())
  print('\r\n goupby sum \r\n', grouped.sum())
  print('\r\n 多列对单列 mean \r\n', df['data1'].groupby([df['key1'], df['key2']]).mean())
  print('\r\n 单列对多列 mean \r\n', df[['data1', 'data2']].groupby(df['key1']).mean())
  print('\r\n 多列对多列 sum \r\n', df.groupby([df['key1'], df['key2']]).mean())
  states = np.array(['A', 'B', 'C', 'D', 'E', 'F'])
  years = np.array([2015, 2016, 2017, 2018, 2019, 2020])
  print('\r\n 多列对多列 sum \r\n', df['data1'].groupby([states, years]).mean())
  print('\r\n 列名做分组 sum \r\n', df.groupby('key1').mean())
  print('\r\n 列名做分组 sum \r\n', df.groupby(['key1', 'key2']).mean())


# 聚合函数
def agg_usage():
  # 自定义聚合
  def get_ji_cha(arr):
    return arr.max() - arr.min()

  result = df.groupby('key1')
  print('\r\n 自定义聚合函数求极差 \r\n', result.agg(get_ji_cha))
  print('\r\n 对某一列使用聚合函数 \r\n', df.groupby(['key1'])['data1'].agg(np.mean))
  print('\r\n 对某一列使用 多个聚合函数 \r\n', df.groupby(['key1'])['data1'].agg([np.mean, np.sum]))
  print('\r\n 对某一列使用 自定义混合 \r\n', df.groupby(['key1'])['data1'].agg([np.mean, np.sum, get_ji_cha]))
  print('\r\n  使用  元组聚合函数 \r\n', df.groupby(['key1'])['data1'].agg([('mean_result', 'mean'), ('std_result', np.std)]))
  print('\r\n  使用  字典(字段名为key，函数为值)聚合函数 \r\n', df.groupby(['key1']).agg({'data1': 'max', 'data2': 'sum'}))
  print('\r\n  使用  字典(字段名为key，函数为值)聚合函数 \r\n', df.groupby(['key1']).agg({'data1': ['max', 'min'], 'data2': 'sum'}))
  print('\r\n  使用as_index 禁止分组作为索引 \r\n', df.groupby(['key1'], as_index=False).agg({'data1': ['max', 'min'], 'data2': 'sum'}))

# apply 聚合函数
def apply_usage():
  # 自定义聚合
  def top(df:pd.DataFrame, n=5, column='data1'):
    return df.sort_values(by=column)[-n:]
  df.sem
  print('\r\n 自定义聚合函数 apply \r\n',df.groupby('key1').apply(top) )
  print('\r\n 自定义聚合函数 apply传参数 \r\n',df.groupby('key1').apply(top, n=1, column='data2') )


# pivot_table透视表的使用
def pivot_table_usage():
  print('\r\n 透视表 默认使用聚合函数  \r\n', pd.pivot_table(df, index=['key1']) )
  print('\r\n 透视表  列  \r\n', pd.pivot_table(df, values=['data1','data2'], index=['key1'], columns='key2') )
  print('\r\n 透视表 添加分项小计  \r\n', pd.pivot_table(df, values=['data1','data2'], index=['key1'], columns='key2', margins=True) )
  print('\r\n 透视表 其他聚合函数  \r\n', pd.pivot_table(df, values=['data1','data2'], index=['key1'], columns='key2', margins=True, aggfunc='count') )
  print('\r\n 透视表 fill_value 填充空值  \r\n', pd.pivot_table(df, values=['data1','data2'], index=['key1'], columns='key2', fill_value=0) )
  print('\r\n  交叉表  \r\n', pd.crosstab(df.key1, df.key2 ) ) #
  print('\r\n  交叉表  \r\n', pd.crosstab(df.key1, df.key2, margins=True) )
  print('\r\n  交叉表  \r\n', pd.crosstab([df.key1, df.key2], df.data1, margins=True) )


if __name__ == '__main__':
  # group_by_usage()
  # agg_usage()
  # apply_usage()
  pivot_table_usage()
