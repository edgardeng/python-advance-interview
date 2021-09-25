'''
pandas demo - Series的使用 （ pandas-1.1.2 ）
'''
import numpy as np
import pandas as pd
from pandas import DataFrame


def create_dataframe():
    df = DataFrame(np.random.randint(10, size=(2, 5)))
    print('自动行索引 :\r\n', df)
    df = DataFrame(np.random.randint(10, size=(2, 5)), columns=list('ABCDE'))
    print(df[['A']])
    print('-' * 10, )
    print(type(df[['A']]))
    print(df[['A']])
    print(dict(df[['A']]))
    print('-' * 10, )
    features = df[['A']]
    features = {key: np.array(value) for key, value in dict(features).items()}
    print(features)

    print('指定行列索引 :\n ', df)
    df = DataFrame([1, 2, 3, 5, 6])
    print('一维列表创建 :\n ', df)
    df = DataFrame([[1, 2, 3], [5, 6, 7]])
    print('二维列表创建 :\n ', df)
    df = DataFrame({'name': ['a', 'b', 'c'], 'age': [10, 11, 12]})  # 行数要相同
    print('字典创建 :\n ', df)
    df = DataFrame({'name': pd.Series(['a', 'b', 'c', 'd']), 'age': pd.Series([10, 11, 12])})
    print('series类型字典创建 :\n ', df)  # 如果行数对不上，会使用None填充
    df = DataFrame({'name': ['a', 'b', 'c'], 'age': [10, 11, 12]}, columns=['name', 'score'])
    print('字典创建,指定index，column :\n ', df)
    print('index:', df.index)
    print('columns:', df.columns)
    print('values:', df.values)
    print('dtypes:', df.dtypes)
    print('size:', df.size)
    print('ndim:', df.ndim)
    print('shape:', df.shape)

    df = DataFrame({'goods': ['cola', 'egg', 'cookie', 'apple', 'banana', 'milk', 'cola', 'egg', 'cookie'],
                    'quantity': [4, 5, 6, 10, 11, 12, 10, 11, 12],
                    'price': [13, 11, 14, 21, 20, 22, 21, 20, 22]})  # 行数要相同
    print('原始数据:\r\n', df)

    print('单列:\r\n', df['goods'])
    print('多列:\r\n', df[{'goods', 'price'}])
    print('单列多行:\r\n', df['goods'][:3])
    print('某个数据:\r\n', df['goods'][3])
    print('多列多行:\r\n', df[{'goods', 'price'}][:3])
    print('全列多行:\r\n', df[:][:3])
    print('前5行:\r\n', df.head())  # 默认 5
    print('前2行:\r\n', df.head(2))
    print('后5行:\r\n', df.tail())
    print('后2行:\r\n', df.tail(2))
    print('*************:\r\n', )
    print('行筛选:\r\n', df[df.goods == 'milk'])
    print('行筛选:\r\n', df[(df.goods == 'milk') & (df.price == 20)])
    print('行筛选:\r\n', df[df.price < 20])
    print('loc切片:\r\n', df.loc[:, 'goods'])
    print('loc切片:\r\n', df.loc[:, {'goods', 'price'}])
    print('loc切片:\r\n', df.loc[:3, {'goods', 'price'}])
    print('loc 索引切片:\r\n', df.loc[df.goods == 'milk', :])
    print('iloc 索引切片 单列:\r\n', df.iloc[:, 0])
    print('iloc 索引切片 多行多列:\r\n', df.iloc[0:3, 0:2])
    print('iloc 索引切片:\r\n', df.iloc[0:2, [0, 1]])


def update_dataframe():
    df = DataFrame({'goods': ['cola', 'egg', 'cookie', 'apple', 'banana', 'milk'],
                    'quantity': [4, 5, 6, 10, 11, 12],
                    'color': ['B', 'Y', 'Y', 'R', 'Y', 'W'],
                    'price': [13, 11, 14, 21, 20, 22]})
    df['total'] = df['quantity'] * df['price']
    print('添加列 :\r\n', df)
    df['isQualified'] = True
    print('添加列 固定值:\r\n', df)
    df.insert(2, 'allQuantity', [100, 50, 30, 100, 50, 30])
    print('插入列:\r\n', df)
    df.loc[6] = ['shampoo', 'B', 13, 100, 50, 650, True]
    print('插入行:\r\n', df)
    df.append({'goods': 'pear', 'quantity': 30, 'price': 12}, ignore_index=True)  # 字典不能是列表
    print('append添加行:\r\n', df)
    print('append 新值:\r\n', df.append({'goods': 'pear', 'quantity': 30, 'price': 12}, ignore_index=True))
    df.drop(labels='isQualified', axis=1, inplace=True)
    print('删除列:\r\n', df)
    df.drop(['allQuantity', 'total'], axis=1, inplace=True)
    print('删除多列:\r\n', df)
    df.drop(6, axis=0, inplace=True)
    print('删除一行:\r\n', df)
    df.drop([4, 5], axis=0, inplace=True)
    print('删除多行:\r\n', df)
    df.loc[3] = ['orange', 'O', 5, 12]  # 不存在则添加
    print('修改某行:\r\n', df)
    df.loc[:, 'quantity'] = 10
    print('修改某列:\r\n', df)
    df.loc[df.price > 15, 'price'] = 15
    print('修改某些:\r\n', df)
    print('-' * 30, '统计')
    print('np求和:', np.sum(df['quantity']))
    print('df求和:', df['quantity'].sum())
    print('df describe 描述性统计:\r\n', df[{'quantity', 'price'}].describe())
    print('频次统计：\r\n', df['color'].value_counts())
    # 数据类型转category类型
    df['color'] = df['color'].astype('category')
    print('category describe:\r\n', df['color'].describe())


def update_dataframe_column():
    print('*' * 20, '修改DataFrame的列')


if __name__ == '__main__':
    create_dataframe()
    # update_dataframe()
