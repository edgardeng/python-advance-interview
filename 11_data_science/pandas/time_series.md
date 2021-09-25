## 时间序列

### 时间相关的类
> 字符串转标准时间类型

|类名称|说明|转换函数|
|:----|:----|:----|
|Timestamp| 基础的时间类，表示某个时间点|`pd.to_datetime('2018-1-1')`|
|Period     |单个时间跨度，比如某一天，某一个小时||
|Timedelta  |不同单位的时间，如： 1天，1.5小时..||
|DatetimeIndex  |一组Timestamp组成的Index， 用于Series和DataFrame的索引|`pd.to_datetime(['2018-1-1')]`||
|PeriodIndex    |一组Period组成的Index， 用于Series和DataFrame的索引||
|TimedeltaIndex |一组Timedelta组成的Index， 用于Series和DataFrame的索引||

日期索引的数据
  * .index[下标] 访问某个索引
  * [日期字符串]， 如df['2018-01-01']
  * 对较长的时间序列，传入'年' 或'年月' 可返回对应的数据切片
  * 通过时间范围进行切片索引
  
带有重复索引的时间序列
  * 。index.is_unique 检查索引日期是否唯一
  * 对非唯一时间戳的数据进行聚合，通过groupby 并传入 level
  
  
#### 生成日期范围

pandas.data_range
 > * start 开始时间
 > * end 结束日期
 > * periods 固定日期，整数'
 > * freq 日期偏移量 string/DateOffset
 > * normalize 若为True，将start，end正则化到午夜时间戳
 > * name 生成索引对象的名称

data_range函数的用法：
* 指定开始、结束，默认频率为每天
* 指定日期数量的日期范围
* 使用日期偏移量的日期范围
* 带时间信息的日期范围
* 规范化参数产生的日期范围

##### 日期偏移量
* 和基础频率对应
* 包括均匀偏移量/喵点偏移量
* 导入模块 pandas.tseries.offsets
* 偏移量对照表：

|别名|偏移量类型|说明|
|:----|:----|:----|
|D      |Day            | 每日（历日）  |
|B      |BusinessDay    | 每工作日  |
|H      |Hour            | 每日（历日）  |
|T/M      |Minute    | 每日（历日）  |
|S      |Second    | 每日（历日）  |
|L/ms      |Milli    | 毫秒  |
|U      |Micro    | 微秒  |
|M      |MonthEnd    | 每月最后一天  |
|BM      |BusinessMonthEnd    | 每月最后一个工作日  |
|MS      |MonthBegin     | 每月第一天  |
|BMS      |BusinessMonthBegin    | 每月第一个工作日  |
|W-MON，W-TUE ..      |Week    | 每周（MON TUE ..）  |
|WOM_1MON,WOM_2MON,..      |WeekOfMonth    | 每日（历日）  |
|Q-JAN,Q-FEB,..   |QuarterEnd    | 季度最后一个月的最后一天  |
|BQ-JAN,BQ-FEB,..      |BusinessQuarterEnd     |季度最后一个月的最后一工作日   |
|QS-JAN,QS-FEB,..       |QuarterBegin    | 季度最后一个月的第一天  |
|BQS-JAN,BQS-FEB,..      |BusinessQuarterBegin      | 季度最后一个月的第一一工作日  |


#### 日期的移动

* 沿着时间轴移动数据 (使用shift方法 实现前移或后移)
   > shift（periods=1,freq=None,axis=0） 索引不变            
   > * 例: Series.shift(2) 单纯后移，数据往后移动，产生会缺失值
   > * 例: Series.shift(-2, freq='D') 带freq前移，数据不动，时间戳的值往前移动
  
* 通过偏移量对日期进行移动

  在datetime，Timestamp对象中使用
  
  锚点偏移量： 频率所描述的时间点并不是均匀分割的偏移量
  > 例如 MonthEnd对象的rollforward方法、rollback方法
       
 
 
### 时期 Period

时期表示时间区间，如数日..

* 创建时期对象    `pd.Period(2019, freq='A-DEC') `
* 时期的算术运算   ` pd.Period(2019, freq='A-DEC') + 1`
 
#### 时期范围 PeriodIndex

* 时期范围作为轴索引    ` pd.period_range('2019-01-01', '2019-06-30', freq='M')`
* 字符串数组创建        `pd.PeriodIndex(['2018Q1', '2018Q2', '2018Q3'], freq='Q-DEC')`
* 时间信息数组创建     ` pd.PeriodIndex(year=year, quarter=quarter, freq='Q-DEC')`
> 固定频率的数据集通常将时间信息分开存放在多个列中，选取时间信息的列作为参数创建 Periodindex

#### 日期的频率转换

* 通过 period.asfreq(freq, how='end')   // how : {'E', 'S', 'end', 'start'}, default 'end'
* 高频率到底频率时， 较大的时期是由较小的时期的位置决定的
* PeriodIndex 或 TimeSeries 的频率转换方式相同

#### 按季度计算的时期频率
 
 许多季度型数据会设计财年末的概念。通常是一年12隔越中某月的最后一个工作日/日历日
 
 pandas 支持的季度频率  Q-JAN 到 Q-DEC
 
 
示例额：
 * 财政年度 / 季度
 * 季度倒数第二个工作日的下午4点时间戳
 * 相同运算应用到TimeSeries
 
 
#### Timestamp 和 Period 相互转换

* to_period 将时间戳索引的Series/DataFrame 转换成日期索引 （会出现重复时期）
* to_timestamp 

### 重采样

重采样（resampling）： 将时间序列从一个频率转换到另一个频率的处理过程

分类
 * 降采样
   > 待聚合的数据不必拥有固定频率，期望的频率会自动定义聚合的面元边界，这些面元将时间序列拆分多个片段
   > 考虑： 1 区间哪边是闭合的？ 2 如何标记聚合面元，用区间的开头还是末尾
   * OHLC 重采用
     > how='ohlc' 得到一个含有4中聚合值的DataFrame
     > 金融领域的时间序列聚合方式：OHLC  open 开盘 close 收盘，high 最大值 ，low 最小值       
 
 * 升采样
    > 低频到高频 不需要聚合
    > 使用asfreq 方法转换
    > 使用 resampling 实现填充和插值
    >
   
 * 其他 （每周三 -> 每周五）


 
使用 Series / DataFrame 的 resample 方法， 参数如下


|参数|说明|默认|
|:----|:----|:----|
|rule           | 重采样频率 字符串/DataOffset| |
|how            | 聚合函数： mean，ohlc。。|mean|
|axis           |轴|0|
|fill_method    |升采样如何插值 ffill/bfill||
|closed         |降采样时，时间段哪一端闭合 rihgt，left|left|
|label          |降采样 如何设置标签  rihgt，left|left|
|loffset        |面元标签的校正值||
|limit          |允许填充的最大时期数||
|kind           |聚合到period，timestamp，默认时间序列的索引类型||
|convention     |低频到高频的用法 start，end|start|




### 频率转换
