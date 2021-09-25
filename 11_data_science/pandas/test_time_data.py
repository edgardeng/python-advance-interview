'''
pandas demo -时间序列（ numpy-1.19.2  pandas-1.1.2  matplotlib-3.3.2 ）
'''

import numpy as np
import pandas as pd
from datetime import datetime
import pandas.tseries.offsets as offset


# datetime in pandas
def pandas_timestamp():
  dates = [datetime(2019, 1, 1), datetime(2019, 1, 3), datetime(2019, 1, 5),
           datetime(2019, 1, 7), datetime(2019, 1, 9), datetime(2019, 1, 11)]
  data = pd.Series(np.random.randn(6), index=dates)
  print('将datetime列表作为序列的索引 \r\n', data)
  print('时间索引 \r\n', data.index)
  print('时间索引 \r\n', )
  print('index[下标]访问索引和数据 \r\n', data[data.index[0]])
  print('日期访问数据：', data['20190101'])
  print('日期访问数据：', data['01/01/2019'])
  data = pd.Series(np.random.randn(100), index=pd.date_range('1/1/2019', periods=100))
  print('某年 \r\n', data['2019'])
  print('某月 \r\n', data['2019-02'])
  print('某日 \r\n', data[datetime(2019, 2, 1)])
  print('时间范围切片 \r\n', data['2019-02-01':'2019-03-01'])
  # 重复索引的时间序列

  dup_data = pd.Series(np.arange(4), index=pd.DatetimeIndex(['2019-01-01', '2019-01-01', '2019-01-02', '2019-01-02']))
  print('判断唯一性', dup_data.index.is_unique)
  print('根据索引聚合', dup_data.groupby(level=0).count())


def data_range_test():
  times = pd.date_range('2019-01-01', '2019-02-01', )
  print('指定开始、结束，默认频率为每天 \r\n', times)
  times = pd.date_range(start='2019-01-01', periods=10)
  print('指定日期数量的日期范围 \r\n', times)
  times = pd.date_range(start='2019-01-01', periods=10, freq='M')
  print('使用日期偏移量的日期范围 (每月) \r\n', times)
  times = pd.date_range(start='2019-01-01 10:00:00', periods=10)
  print('带时间信息的日期范围 \r\n', times)
  times = pd.date_range(start='2019-01-01 10:00:00', periods=10, normalize=True)
  print('规范化参数产生的日期范围 将时间变成00:00:00\r\n', times)
  times = pd.date_range(start='2019-01-01', periods=10, freq='4h')
  print('频率 每4小时\r\n', times)
  times = pd.date_range(start='2019-01-01', periods=10, freq='2h30min')
  print('频率 每2h30min小时\r\n', times)
  times = pd.date_range(start='2019-01-01', periods=10, freq='wom-3FRI')
  print('频率 每个月的第3个星期五\r\n', times)

  hour = offset.Hour()
  times = pd.date_range(start='2019-01-01', periods=10, freq=hour)
  print('使用日期偏移量类 每小时 \r\n', times)
  hour = offset.Hour(4)
  times = pd.date_range(start='2019-01-01', periods=10, freq=hour)
  print('使用日期偏移量类 每4小时 \r\n', times)
  mins = offset.Minute(30)
  times = pd.date_range(start='2019-01-01', periods=10, freq=hour + mins)
  print('使用日期偏移量类 每4小时30分 \r\n', times)


# 数据移动
def data_move_test():
  s = pd.Series(np.random.randn(6), index=pd.date_range('1/1/2019', periods=6, freq='M'))
  print('原数据 \r\n', s)
  # 单纯的前后移动（数据移动，产生缺失数据）
  print('数据往后移动 \r\n', s.shift(2))
  print('数据往前移动 \r\n', s.shift(-2))
  print('后移动  freg参数，根据频率移动，实际对时间戳进行位移而不是对数据进行位移 \r\n', s.shift(2, freq='M'))
  print('前移动 freg参数\r\n', s.shift(-2, freq='D'))

  now = datetime.today()
  print('datetim 今天：\r\n', now)
  print('datetim 偏移 3天\r\n', now + 3 * offset.Day())
  print('datetim 偏移 到本月底\r\n', now + offset.MonthEnd())
  print('datetim期偏移 第2月后的月底\r\n', now + offset.MonthEnd(2))

  print('rollforward 向前滚到当月底 \r\n', offset.MonthEnd().rollforward(now))
  print('rollforward 向后滚到上月底\r\n', offset.MonthEnd().rollback(now))
  print('Series的时间戳 向前滚到月底\r\n', s.groupby(offset.MonthEnd().rollforward).count())


def period_test():
  p = pd.Period(2019, freq='A-DEC')  # 创建日期 传入整数后字符串
  print('以12月结束的2019年每个月最后一天:', p)
  p = pd.Period('2019', freq='A-DEC')  # 创建日期 传入整数后字符串
  print('以12月结束的2019年每个月最后一天:', p)
  print('运算 p+2:', p + 2)
  print('运算 p-2:', p - 2)
  print('运算 差:', p - pd.Period('2021', freq='A-DEC'))
  rng = pd.period_range('2019-01-01', '2019-06-30', freq='M')
  print('日期范围:', rng)
  s = pd.Series(np.random.randn(6), index=rng)
  print('Series withd index 日期范围:', s)
  index = pd.PeriodIndex(['2018Q1', '2018Q2', '2018Q3'], freq='Q-DEC')
  print('字符串数组 创建日期范围索引', index)
  year = [2018, 2018, 2018, 2018, 2019, 2019, 2019, 2019]
  quarter = [1, 2, 3, 4, 1, 2, 3, 4]
  print('时间信息数组 创建PeriodIndex ', pd.PeriodIndex(year=year, quarter=quarter, freq='Q-DEC'))

  # 日期的频率转换
  print('转换成年初的一个月', p.asfreq('M', how='s'))
  print('转换成年末的一个月', p.asfreq('M'))
  p = pd.Period(2019, freq='A-JUN')  # 不以12月结束的年度 从2017-7 到 2018-6 为一个时期
  print('转换成年初的一个月', p.asfreq('M', how='s'))
  print('转换成年末的一个月', p.asfreq('M'))

  p = pd.Period('201903', 'M')
  print('高频到低频', p.asfreq('A-JUN'))
  rng = pd.period_range('2016', '2019', freq='A-DEC')
  s = pd.Series(np.random.randn(len(rng)), index=rng)
  print('series 原数据\r\n', s)
  print('series 的日期转换\r\n', s.asfreq('M', how='S'))
  print('series 的日期转换\r\n', s.asfreq('M', how='E'))


def quart_period_test():
  p = pd.Period('2018Q4', freq='Q-JAN')  # 2018年度：(2017-02 到 2018-01) 三个月为一个季度。 以1月结束的2018年度的每个季度最后一个月的最后公历日
  print('以1月结束的2018年度的每个季度最后一个月的最后公历日：', p)
  print('转换 为起始月：', p.asfreq('M', how='S'))
  print('转换 为结束月：', p.asfreq('M'))

  p2 = p.asfreq('B', 'e')  # 得到最后一个工作日
  print(p2)
  p4pm = (p.asfreq('B', 'e') - 1).asfreq('T', 'S') + 16 * 60  # .asfreq('T', 'S')  获得开始的分钟 00：00
  print(p4pm.to_timestamp())

  rng = pd.period_range('2017Q3', '2018Q4', freq='Q-JAN')
  s = pd.Series(np.random.randn(len(rng)), index=rng)
  print(s)
  new_rng = (rng.asfreq('B', 'e') - 1).asfreq('T', 'S') + 16 * 60
  s.index = new_rng.to_timestamp()
  print(s)

  rng = pd.date_range('2018-01-25', periods=10, freq='D')
  s = pd.Series(np.random.randn(len(rng)), index=rng)
  print('series 原数据\r\n', s)
  print('series 时间戳转时期\r\n', s.to_period())
  print('series 时间戳转时期\r\n', s.to_period('M'))
  print('series 时期转时间戳\r\n', s.to_period('M').to_timestamp(how='end'))


def resample_test():
  rng = pd.date_range('2018-01-25', periods=100, freq='D')
  s = pd.Series(np.random.randn(len(rng)), index=rng)
  print('series 原数据\r\n', s)
  print('series 月采样频率\r\n', s.resample('M').mean())
  print('series 月采样频率 时期范围\r\n', s.resample('M', kind='period').mean())
  rng = pd.date_range('2018-01-25', periods=20, freq='T')
  s = pd.Series(np.random.randn(len(rng)), index=rng)
  print('series 原数据\r\n', s)
  # 求和的方式，聚合在 5分钟块
  #
  print('降采样 \r\n', s.resample('5min', closed='right').count())
  print('降采样包含面元的左边界 \r\n', s.resample('5min', closed='left').sum())
  print('降采样 时间序列以面元右边界的时间戳为标记\r\n', s.resample('5min', closed='right', label='right').sum())
  # print('降采样 设置一个偏移量\r\n', s.resample('5min', closed='right', label='right', loffset='-1S').sum())
  print('ohlc采样 \r\n', s.resample('5min').ohlc())

  # 生采样
  df = pd.DataFrame(np.random.randn(2, 4),
                    index=pd.date_range('2018-01-25', periods=2, freq='W-WED'),
                    columns=list('ABCD'))
  print('df 原数据\r\n', df)
  print('resample +asfreq\r\n', df.resample('D').asfreq())
  print('resample +ffill\r\n', df.resample('D').ffill())
  print('resample +ffill + limit\r\n', df.resample('D').ffill(limit=2))  # 只填充2行

  df = pd.DataFrame(np.random.randn(24, 4),
                    index=pd.period_range('2018-01', '2019-12', freq='M'),
                    columns=list('ABCD'))
  print('时期索引的原数据\r\n', df)
  an_df = df.resample('A-DEC').mean()
  print('使用时期索引的数据进行重采用和时间戳类似\r\n', an_df)
  print('resample +ffill\r\n', an_df.resample('Q-DEC').ffill()) # 升序
  print('resample +ffill + convention\r\n', an_df.resample('Q-DEC', convention='end').ffill())
  print('resample +freq 不同\r\n', an_df.resample('Q-MAR').ffill())


if __name__ == '__main__':
  # pandas_timestamp()
  # data_range_test()
  # data_move_test()

  # period_test()
  # quart_period_test()
  resample_test()
