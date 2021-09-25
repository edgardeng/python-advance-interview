'''
pandas demo - DataFrame的创建 （ pandas-1.1.2 ）
'''

import numpy as np
import pandas as pd
from pandas import DataFrame


def create_from_file():
    data = pd.DataFrame([['99', '80'],
                         ['67', '98'],
                         ['69', '98'],
                         ['70', '97']],
                        index=['a', 'b', 'c', 'd'],
                        columns=['语文', '数学'])
    data.index.names = ['姓名']
    print(data.index.names)
    data2 = data.reset_index()
    data2.columns = ['姓名', '语文', '数学']

    data.to_excel("exams.xls", index_label='姓名')
    print('*' * 30, 'create from xls')
    df = pd.read_excel("exams.xls", header=0, index_col=0)
    print(df)

    data.to_excel("exams.xlsx", index_label='姓名')
    print('*' * 30, 'create from xlsx')
    df = pd.read_excel("exams.xlsx", header=0, index_col=0, engine='openpyxl')
    print(df)
    # 1、io，Excel的存储路径
    # 2、sheet_name，要读取的工作表名称
    # 3、header， 用哪一行作列名
    # 4、names， 自定义最终的列名
    # 5、index_col， 用作索引的列
    # 6、usecols，需要读取哪些列
    # 7、squeeze，当数据仅包含一列
    # 8、converters ，强制规定列数据类型
    # 9、skiprows，跳过特定行
    # 10、nrows ，需要读取的行数
    # 11、skipfooter ， 跳过末尾n行

    data.to_csv('exams.csv', index_label='姓名')
    print('*' * 30, 'create from csv')
    df = pd.read_csv("exams.csv", header=0, index_col=0)
    print(df)

    data.to_json("exams.json", force_ascii=False)
    print('*' * 30, 'create from json 1')
    df = pd.read_json("exams.json", encoding='GBK')
    print(df)

    data2.to_json("exams2.json", force_ascii=False, orient="records", index=True)
    print('*' * 30, 'create from json 2')
    df = pd.read_json("exams2.json", encoding='GBK')
    print(df)

    dict_data = data.to_dict()
    print('*' * 30, 'create from dict')
    df = pd.DataFrame.from_dict(dict_data)
    print(dict_data)
    print(df)

    dict_data2 = data2.to_dict(orient='records')
    print('*' * 30, 'create from dict records')
    df = pd.DataFrame.from_records(dict_data2)
    print(dict_data2)
    print(df)

    print(data.index)
    print(data.to_html(index_names=['姓名']))


def create_from_random():
    data = np.random.randint(20, size=(4, 5))
    df = DataFrame(data)
    print(type(data), data.shape)

    print('*' * 30, 'create from random 2*5')
    print(df)  # 无索引自建数字索引

    df = DataFrame(data, index=list('abcd'), columns=list('ABCDE'))
    df.index.names = ['name']

    print('*' * 30, 'create from random<2*5> and index, columns')
    print(df)

    df = DataFrame({'A': np.random.randint(20, size=4), 'B': np.random.randint(20, size=4)})
    print('*' * 30, 'create from dict(random<2*5>)')
    print(df)


if __name__ == '__main__':
    create_from_file()
    create_from_random()
