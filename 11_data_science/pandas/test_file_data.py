'''
pandas demo - Series的使用 （ pandas-1.1.2 ）
'''
import numpy as np
import pandas as pd
from sqlalchemy import create_engine


def excel_operate():
    df1 = pd.DataFrame([['99', '80'],
                        ['67', '98'],
                        ['69', '98'],
                        ['70', '97']],
                       index=['a', 'b', 'c', 'd'],
                       columns=['语文', '数学'])
    df1.to_excel("exams.xls")
    print(df1)
    print('*' * 30)

    df2 = pd.read_excel("exams.xls", header=0, index_col=0)
    # 求个人总分
    df2['总分'] = df2.sum(axis=1)  # 行求和
    # 求总分排名
    df2['排名'] = df2['总分'].rank(ascending=False)
    df2['排名'] = np.floor(df2['排名'])

    # 求科目平均分
    df2.loc['平均分'] = df2.mean()  # 列求平均
    df2.loc['平均分']['排名'] = None
    df2.to_excel("exams-new.xls")
    print(df2)


def database_dataframe():
    con = create_engine('mysql+pymysql://root:123456@localhost:3306/test')
    info = pd.read_sql_table('order_detail', con=con)
    print(info.head())
    result1 = pd.read_sql_query('select * from order_detail', con=con)
    result2 = pd.read_sql('order_detail', con=con)
    result3 = pd.read_sql('select id,name from order_detail', con=con)

    df = pd.DataFrame({
        'id': [0, 1, 2],
        'name': ['alice', 'Mike', 'Tom'],
        'gender': ['F', 'M', 'M']
    })
    df.to_sql('userInfo', con=con, index=False, if_exists='replace')
    result = pd.read_sql_query('select * from userInfo', con=con)
    df.fillna


if __name__ == '__main__':
    create_dataframe()
    database_dataframe()
