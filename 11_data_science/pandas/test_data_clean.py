'''
pandas demo -数据清洗 （ numpy-1.19.2  pandas-1.1.2  scikit-learn-0.23.2 ）
'''
import numpy as np
from pandas import Series, DataFrame
import pandas as pd
from sqlalchemy import create_engine


def is_null():
  df = pd.DataFrame(np.random.randn(10, 6))
  df.iloc[:4, 1] = None
  df.iloc[:2, 4:6] = None
  df.iloc[6, 3:5] = None
  df.iloc[8, 0:2] = None
  print('元数据:\r\n', df)
  result = df.isnull()
  print('判断缺失值:\r\n', result)
  result = df.isnull().any()  # 行是否全为空
  print('列级别的判断缺失值:\r\n', result, type(result))
  result = df[df.isnull().values == True].drop_duplicates()  # 只显示存在缺失值的行。使用drop_duplicates去掉重复的行
  print('列级别的判断缺失值:\r\n', result, type(result))
  result = df.columns[df.isnull().any() == True]
  print('为空或NA的列索引:\r\n', result, type(result))
  num = df.isnull().sum()
  print('每列为空的个数:\r\n', num)
  num = df.isnull().sum(axis=1)
  print('每行为空数据的个数:\r\n', num)


def clear_data():
  df = pd.DataFrame(np.random.randn(10, 6))
  df.iloc[:4, 1] = None
  df.iloc[:2, 4:6] = None
  df.iloc[6, 3:5] = None
  df.iloc[8, 0:2] = None
  print('元数据:\r\n', df)
  print('\r\ndropna 数据:\r\n', df.dropna())  # 不改变原数据
  print('\r\ndropna 删除列:\r\n', df.dropna(axis=1))
  print('\r\ndropna 全空才删除行:\r\n', df.dropna(how='all'))
  print('\r\ndropna 非空至少4个行:\r\n', df.dropna(thresh=4))
  print('\r\ndropna 检查2，4 列，删除相应的行:\r\n', df.dropna(subset=[2, 4]))
  print('\r\ndropna 检查2，4行，删除相应的列:\r\n', df.dropna(axis=1, subset=[2, 4]))
  print('\r\nfill 填充数据:\r\n', df.fillna(0))  # 全填充0
  print('\r\nfill 横向，向前填充:\r\n', df.fillna(axis=1, method='ffill'))
  print('\r\nfill 纵向，向上填充:\r\n', df.fillna(axis=0, method='ffill'))
  print('\r\nfill 不同的列用不同的数填充:\r\n', df.fillna(value={0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5}))  # 全填充0
  print('\r\nfill 只填充1次:\r\n', df.fillna(value={0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5}, limit=1))


def clear_duplicated_data():
  df = pd.DataFrame({'k1': ['one', 'two'] * 4, 'k2': [1, 2, 1, 2, 3, 4, 5, 6]})
  print('元数据:\r\n', df)
  print('duplicated 判断重复:\r\n', df.duplicated())
  print('duplicated 判断重复 全标记True:\r\n', df.duplicated(keep=False))
  print('duplicated 检查指定的列:\r\n', df.duplicated(subset='k1'))
  print('drop_duplicates 删除重复的行:\r\n', df.drop_duplicates())
  print('drop_duplicates 检查指定的列，删除重复的行:\r\n', df.drop_duplicates(subset='k1'))


def clear_except_data():
  df = pd.DataFrame(np.random.randn(1000, 4))  # 1000*4的正态分布
  print(df.describe())
  col = df[2]
  print('查找某列数据 绝对值>3的:\r\n', col[np.abs(col) > 3])
  print('查找全部含有 超过3，-3的值 取1行:\r\n', df[(np.abs(df) > 3).any(1)])
  df[np.abs(df) > 3] = np.sign(df) * 3
  print('修改数据后的统计描述:\r\n', df.describe())
  print('原数据的符号情况:\r\n', np.sign(df).head(10))

  print('-------3σ原则------')
  df = pd.read_csv('a.csv', encoding='bgk')
  print(df)

  # 定义拉依达原则 识别异常函数
  def outRange(ser: Series):
    boolInd = (ser.mean() - 3 * ser.std() > ser) | (ser.mean() + 3 * ser.std() > ser)  # bool 序列
    index = np.arange(len(ser))[boolInd]  # 布尔序列的下标
    out_range = ser.iloc[index]
    return out_range

  outlier = outRange(df['counts'])
  print(len(outlier), outlier.max(), outlier.min())

  print('-------箱型图------')

  def out_range(ser: Series):
    QL = ser.quantile(0.25)
    QU = ser.quantile(0.75)
    IQR = QU - QL
    # 超过上下界
    ser.loc[ser > QU + 1.5 * IQR] = QU + 1.5 * IQR
    ser.loc[ser < QL - 1.5 * IQR] = QL - 1.5 * IQR
    return ser

  df['counts'] = out_range(df['counts'])


# 数据转换
def data_convert():
  df = pd.DataFrame(
    {'food': ['bacon', 'pork', 'bacon', 'pastrami', 'beef', 'Bacon', 'Pastrami', 'honey ham', 'nova lox'],
     'ounce': [4, 3, 12, 2, 3, 4, 5, 12, 2]})
  print('元数据:\r\n', df)
  # 添加一列表示 该肉的动物涞源
  animals = {'bacon': 'pig', 'pork': 'pig', 'pastrami': 'cow', 'beef': 'cow', 'honey ham': 'pig', 'nova lox': 'salmon'}
  lower = df['food'].str.lower()
  # print(lower)
  df['animal'] = lower.map(animals)  # 映射
  print('map \r\n', df)
  df['animal_2'] = df['food'].map(lambda x: animals[x.lower()])
  print('map lambda \r\n', df)
  # replace
  data = pd.Series([1, -999, 2, -999, 1, -1000, 2, -999])
  print('Series 替换 \r\n', data.replace(-999, np.NAN))
  print('Series 替换多个值 \r\n', data.replace([-999, -1000], [np.NAN, 0]))

  # 重命名轴索引
  df = pd.DataFrame(np.arange(12).reshape(3, 4),
                    index=['A', 'B', 'C'], columns=['aa', 'bb', 'cc', 'dd'])
  df.index = df.index.map(lambda x: x.lower())
  print('index.map \r\n', df)
  df.rename(index=str.title, columns=str.upper,
            inplace=True)  # Python title() 方法返回"标题化"的字符串,就是说所有单词都是以大写开始，其余字母均为小写(见 istitle())。
  print('dataframe.rename \r\n', df)
  # 使用rename

  print('-' * 30, 'ya')
  df = pd.DataFrame(
    {'animal': ['pig', 'cow', 'hen', 'cat', 'dog', 'rat'],
     'count': [14, 13, 22, 56, 32, 29]})
  print('get_dummies: \r\n', pd.get_dummies(df))
  # 等宽离散
  counts = pd.cut(df['count'], 3)
  print('离散后的数量', counts.value_counts())

  # 等频率离散
  def samRateCut(data: DataFrame, k):
    w = data.quantile(np.arange(0, 1 + 1.0 / k, 1.0 / k))
    data = pd.cut(data, w)
    return data

  result = samRateCut(df['count'], 3)
  print('等频离散后的数量', result.value_counts())

  # 自定义离散
  def kmeanCunt(data: DataFrame, k):
    from sklearn.cluster import KMeans
    kmodel = KMeans(n_clusters=k)  # 建立模型
    kmodel.fit(data.values.reshape(len(data), 1))  # 训练模型
    c = pd.DataFrame(kmodel.cluster_centers_).sort_values(0)  # 输出聚类中心并排序
    w = c.rolling(2).mean().iloc[1:]  # 相邻2项求中点 作为边界点
    w = [0] + list(w[0]) + [data.max()]  # 把首末加上
    data = pd.cut(data, w)

  result2 = kmeanCunt(df['count'], 3)
  print('sklearn聚类离散后的数量', result2.value_counts())



if __name__ == '__main__':
  # clear_data()
  # clear_duplicated_data()
  # clear_except_data()
  data_convert()
