# Data Statistic 数据统计

## pandas

> pandas是基于python的第三方库，提供高性能，易用数据类型和分析工具
> 基于numpy实现

|Numpy|pandas|
|:-----|:-----|
|作用：数据处理|数值计算|
|基础数据类型|扩展数据类型|
|关注数据的结构表达|关注数据的应用表达|
|维度：数据间的关系|数据与索引间的关系|

重要的2中数据结构: Sseries和Dataframe。 基本操作，关联操作。。

### Series
 > 一组数据及与之相关的数据索引组成，类似一个 带"标签"的数组

基本语法: `Series(data=None, index=None, dtype=None, name=None)`


创建方法：

* python 列表
* 标量值
* python字典
* ndarray
* 其他函数：range

数据的访问：

s.index 获取索引列表
s.values  获取数据列表
s.name

位置索引访问
标签索引访问
切片索引访问
布尔行访问（条件过滤访问）

删除数据
    drop函数： 删除后的副本，元数据不变
    pop函数： 删除数据，元数据改变
>  自动索引的，使用自动索引，自定义索引，使用自定义索引

修改数据
    通过索引修改数据
添加数据
 * 通过索引访问添加
 * append方法末尾添加，返回副本，源数据不变    
    

### DataFrame
 > 1. 由共用相同索引的一组列组成，主要用于表示二维数组
 > 2. 一个表格形数据类型，每列值的类型可以不同
 > 3. 二维数据/多维数据
 > 4. 行索引index 列索引column

DataFrame的创建

 pd.DataFrame(data=d, dtype=np.int8)

    
* 二维ndarray对象创建

* 列表创建

* 使用字典创建
    > 字典的key成为索引，行索引是字典中指定的index或自动索引 （也可以指定index，columns）

基本属性

* index 行索引列表
* columns 列索引列表
* values  元素
* dtypes 元素类型
* size  元素的个数
* ndim  维度
* shape 形状

数据查询

 * 访问单列数据
 * 访问多列数据
    > DataFrame中每一列都是一个Series对象
 * 访问单列多行数据
    > 类似Series
 * 访问某个数据
 * 访问多行多列数据
 * 访问多行数据
    > ds[:][:5]
    > head(rows=5) 访问前几行
    > tail(rows=5) 访问后几行
 * 访问任意数据
    * 按照条件筛选
        * and（&与）、or（｜或）、not（～非）、xor（^异或）
    * 使用loc切片
        * DataFrame.loc[行索引(名称或条件)，列索引]
        * 索引为区间时，前后都闭合
    * 使用iloc切片
        * DataFrame.iloc[行索引位置，列索引位置]
        * 行索引为区间时，前闭后开  
    > loc 更加灵活多变，可读性高，iloc代码简洁。建议多使用loc


添加数据
* 添加一列
    新建一个列索引，并赋固定值或非固定值，添加到最后一列
* 插入一列
    df.insert(int,column,value)
    * 插入值可以是 固定值 列表 series
* 添加一行
    * loc[rowindex] 方法添加行到末尾， 直接修改元数据
    * append 方法 在末尾添加行，返回副本，元数据不变
            
删除数据

* 删除列
    >  df.drop(label=,axis=0,inplace=False,)  // axis =1 表示列， inplace=True表示改变源数据
        
* 删除行
    >  df.drop(label=,axis=0,inplace=False,)  // axis =0 表示行， inplace=True表示改变源数据

修改数据
    * 使用loc方法获取数据并赋值修改
    

汇总/统计/计算

* 数值型数据统计 - 基于Numpy的统计函数
    > 例如： np.mean(df['colName'])

* 数值型数据统计 - 基于pandas的描述性统计方法
   > pandas提供便利的统计，如 df['colName'].mean()
   > min,max,mean,ptp 级差，median中位数，std标准差，var 方差， cov 协方差， sem 标准差，
     mode 众数， skew 样本偏度，kurt 样本峰值， quntile 四分位数 count 非空值数目，mad 平均绝对离差
   > describe 描述性统计（非空值数目/均值/四分位数/标准差） 

* 类别型数据统计
    * 描述类别型特征的分布状况，使用频次统计表
        > pd.value_counts
    * describe 能够支持category类型的数据进行描述性统计
        > 1. 返回四个统计量：非空元素的数目，类别数目，数目最多的类别，数目最多类别的数目
        > 2. category类型数据：使用astype方法转换类型

### 数据的加载与存储

#### 数据文件

pandas 提供了 将表格型数据读取为DataFrame对象的函数


|读取函数|说明|写入|
|:----|:----|:----|
|read_csv   |   从文件/url、文件类型对象中加载带分隔符的数据。默认分隔符为逗号|  to_csv |
|read_table  |   从文件/url、文件类型对象中加载带分隔符的数据。默认分隔符为制表符`\t`||
|read_fwf   |   读取定宽列格式的数据（无分隔符） ||
|read_clipboard| 读取剪贴板中的数据（read_table的剪贴板版，将网页转表格有用）   |
|read_excel     | 从excel读取表数据   |
|read_hdf       |读取pandas写的hdf5文件    |
|read_html      | 读取html中所有表格    |
|read_json      | 读取json字符串中的数据   |
|read_pickle    | 读取python pickle格式中存储的任意对象   |
|read_sas       | 读取存储在sas系统自定义存储格式的sas数据集   |
|read_stata     |  读取stata文件格式的数据集    |
|read_sql       |  使用 SQLAlchemy 读取sql查询结果   |
|read_feather   |  读取Feather二进制文件  |

> 文本文件：若干字符构成的计算机文件，典型的顺序文件
> csv 是逗号分隔的文件格式，分隔符不一定逗号，文件以纯文本形式存储表格数据

常用函数

##### read_csv
 
参数:
* filepath: 文件路径（string）
* sep：      分隔符（string）
* header    将某行数据作为列名（int/sequence） 默认自动识别
* names     列名（array）默认为None
* index_col 索引列的位置（int，sequence，False）
* dtype     写入数据类型（dict：列名为key，数据格式为values），默认为None
* nrows     读取前n行（int），默认为None，全读
* encoding 文本编码格式（string） 如：utf-8, gbk

```python
import pandas as pd
df = pd.read_csv('a.csv')
df = pd.read_table('a.csv',sep=',')
df = pd.read_table('a.csv', header=None) # 没有标题行
df = pd.read_table('a.csv', names=['A','B','C']) # 设置标题行
df = pd.read_table('a.csv', names=['A','B','C','info'], index_col='info')  # 设置行索引
df = pd.read_table('a.csv', index_col=['key1','key2'])  # 多个行索引，产生一个层次索引
df = pd.read_csv('a.csv'， sep='\s+') # 正则表达式 空白字符串为分隔符
df = pd.read_csv('a.csv'， skiprows=[0,2,3]) # 跳行读取
# 默认将NA， -1.#IND、NULL等当作缺失值. 默认使用NaN代理
sentienls = {'message':['foo','NA'], 'something':['two']}
df = pd.read_csv('a.csv', na_values=sentienls) # 将指定的值，读取为缺失值
```

##### to_csv 写入文件

参数:
* path_or_buf: 文件路径（string）
* sep：      分隔符（string）
* na_sep    缺失值 默认为''
* columns   写出的列名（list）
* header    是否写出列名（bool）
* index     是否将行名（索引）写出 
* index_lables     索引名（sequence）
* mode      写入模式（）默认w
* encoding 文本编码格式（string） 如：utf-8, gbk

##### read_excel

参数:
* io:           文件路径（string）
* sheet_name：   表内分表位置 （int，string）
* header        将某行数据作为列名 默认0（int,sequence）
* names         列名列表，默认为None（不包含标题行，传递header=None）
* index_col 索引列的位置（int，sequence，False）
* dtype     写入数据类型（dict：列名为key，数据格式为values），默认为None
 
```python
import pandas as pd
df = pd.read_excel('a.xlsx')
df = pd.read_table('a.xlsx', sheet_name=[0,1])
df = pd.read_table('a.xlsx', header=None)    # 没有标题行
```
##### to_excel
参数：
* excel_writer      文件路径（string）
* sheet_name        表内分表位置 ,默认0（int，string）
* na_sep             缺失值 默认为''
* columns           写出的列名（list）
* header            是否写出列名（bool）
* index             是否将行名（索引）写出 

#### read_json
> JavaScript Object Notation 轻量级数据交换格式

json.loads 函数将JSON字符串转成python dict 形式
 
#### to_json

```python
import pandas as pd
df = pd.read_json('a.json', encoding = 'utf-8')
df.to_json('a.json')
```

#### 数据库交互

ORM技术
 > 对象关系映射技术： 把关系数据库的表结构映射到对象上，通过使用描述对象和数据库之间映射的元数据，将程序中的对象持久化到关系数据库中
    
   
SQLALchemy
 > python语言的开源库，提供sql工具包及其orm工具
 > 使用 create_engine()来初始化数据库连接 
 > 连接字符串 （数据库类型+数据库驱动名称://用户名:口令@机器地址:端口号/数据库名）


数据库驱动
   * pymysql 
   * pymongo
   * pyredis    

读取数据库
  * read_sql_table 读取数据库的某个表格，不能实现查询
    > read_sql_table(table_name, con, schema=None, index_col=None 设定列为行名, coerce_float=True 是否将decimal类型转换成pandas中的float4)
  * read_sql_queue 实现查询操作，不能直接读取某个表
    > read_sql_query( sql语句, con, index_col=None, coerce_float=True, columns 读取数据的列名)
  * read_sql 既可以读取某个表，也能实现查询
    > read_sql(sql, con, index_col=None, coerce_float=True)

写入数据库
  * to_sql 
    name: 数据库名
    con 数据库连接
    if_exists   'fail':表名存在则不写入，replace：表存在则删除再重新创建，append：原表上追加数据。默认fail
    index 是否将行索引作为数据传入， 默认True
    index_label 是否引用索引名称
    dtype   写入的数据类型

```python
import pandas as pd
from sqlalchemy import create_engine
con = create_engine('mysql+pymysql://root:123456@localhost:3306/test')
info = pd.read_sql_table('order_detail', con=con)
result1 = pd.read_sql_query('select * from order_detail', con=con)
result2 = pd.read_sql('order_detail', con=con)
result3 = pd.read_sql('select id,name from order_detail', con=con)
df = pd.DataFrame({
    'id': [0,1,2],
    'name': ['alice', 'Mike', 'Tom'],
    'gender': ['F', 'M', 'M']
  })
df.to_sql('userInfo', con=con,index=False, if_exists='replace')
```


## 数据清洗

 预处理的过程：迁移 压缩 清洗 打散 分片 分块 以及多种转换处理
 
 清洗的目的：1 使数据可用 2 让数据更适合进行后续分析
 
 pandas和内置的python库提供了高级灵活快速的工具
 
###  处理缺省值
缺失值： 数据中的不完整的值/特征

padas对象所有描述性统计默认不包括缺失数据

对于数值数据，pandas使用浮点值 NaN 表示缺失数据 （哨兵值）对于时间数据，用NaT表示

padas处理缺省值的函数
    * dropna(self, axis=0, how="any", thresh=None, subset=None, inplace=False)    删除
        * axis - 维度 默认0行，1列
        * how - 'all' 全不缺失才删除行或列，'any'：只要存在缺失，就删除行或列
        * thresh - 一行或1列中出现规定数量的非NaN才保留
        * subset 在某些列的子集中选择出现缺失值的列删除，不在子集中的不删除
        * inplace 筛选过缺失值的新数据，存为副本，还是直接修改
    * fillna(self,value=None,method=None,axis=None,inplace=False,limit=None,downcast=None)    填充
        * value 填充值
        * axis  填充维度
        * method  'fill': 填充缺失值前面的值，'backfill'/'bfill': 填充缺失值后面的值
        * limit  确定填充个数。
    * isnull    判断
    * notnull   判断
    
###  处理重复数据

在处理重复数据之前，需要分析重复的原因 和 去除重复可能造成不良影响

重复数据2种：
    记录重复： 一个/多个特征记录的值完全相同 
    特征重复： 一个/多个特征名称不同，但数据完全相同

pandas 中DataFrame的处理函数

 * duplicated( self, subset: Optional[Union[Hashable, Sequence[Hashable]]] = None, keep: Union[str, bool] = "first") 判断重复数据
    * subset 指定判断重复的列
    * keep 标记重复的行 （Fisrt：除第一个，其他标记True。Last：除最后一个，其他标记True。False：全部标记True。默认first）
    * 返回布尔型的Series， 表示各行是否是重复


处理特征重复值

通过相关系数矩阵
  * 去除连续型特征重复，利用特征间的相似度，将相似度为1的特征去除1个
  * pandas中相似度的计算方法：corr
  * 通过相关系数矩阵去重存在一个弊端：只能对数值型重复特征去重，类别型特征不能

* DataFrame.corr(self, method="pearson", min_periods=1) -> "DataFrame":
  * method: ('person' : 皮尔森相关系数-用于连续呈正态分布的线性数据， 'kendall'：肯德尔相关性系数-分类变量，'spearman'： 斯皮尔曼相关系数-只要不满足皮尔森就选择)

* DataFrame.equels


###  处理异常数据

检测异常值的方法
  * 简单统计分析 （数组的相关运算）
    * 查找绝对值>3的数据  `df[np.abs(df) > 3]` 
    * 判断正负 `np.sign(df).head(10)`
    * any(1)复合条件的一行 `df[(np.abs(df) > 3).any(1)]` 
    * 大于3的赋值3，小于-3的赋值-3  `df[np.abs(df) > 3] = np.sign(df)*3` 
  * 3σ原则 (拉依达法则) 
     > 根据正态分布（σ标准差 u均值），距离平均值3σ的概率为 p(|x-u|>3σ)  <=0.003 
     > 当样本距离平均值大于 3σ 则认定该样本为异常值
  * 箱线图分析
    > 提供识别异常值的标准，即大于或小于箱型图设定的上下边界的为异常值
    > 上四分位数 U，下四分位数 L
    > 上下四分位的差值 LQR = U - L 上界 U+1.5LQR  下界：L-1.5LQR
    > 选取异常值比较客观， 有一定的优越性
       
![](./timg.jpeg)    
    
    
处理方法：
  * 删除
  * 视为缺失值
  * 平均值修正
  * 不处理
  
  
###  数据转换

3种转换方法：
 * 利用函数/映射进行数据转换
    * 1 根据数组、series、dataframe列中的值来实现转换
    * series的map方法可以接受一个函数或含有映射关系的字典型对象
    * series的replace方法实现替换
    * 轴标签，可以通过函数/映射进行转换，得到一个新标签的对象
 * 计算哑变量 处理类别数据转换
    > 常见的输入的特征为数值型。部分类别型，可以经过哑变量处理，在放入模型中
    > 原理：某个类别特征的取值有K个，经过哑变量处理变成K*K的稀疏矩阵 1是0非
 * 离散化连续性数据转换 
    > 某些模型（特别是分类算法如 ID3决策树和Apriori算法）要求数据是离散的。就需要将连续型特征（数值）变成离散型特征（类别） 
    > 连续特征的离散化：取值范围内，设定若干个离散的划分点，形成离散化的区间。不同的符号或整数值代表落在每个子区间的数据值
    > 离散化2个子任务： 确定分类数 + 如何映射
    > 1. 等宽法: pandas.cut
    > 2. 等频法: 将相同数量的记录放在每个区间，保证每个区间的数量基本一致 （使用cut）
    > 3. 聚类分析 ： 指定簇的个数，来决定产生的区间数
       > 一维聚类分方法: 1) 将连续型数据用聚类算法（k-means）进行聚类 2）处理聚类得倒的簇，将合并到一个簇的连续型数据做同一标记 
 
 * 对类别特征进行哑变量处理 get_dummies(data,prefix=None,prefix_sep="_",dummy_na=False,columns=None,sparse=False,drop_first=False,) -> "DataFrame":
  * data：待处理的数据（array/df,series）
  * prefix: 量化后列名的前缀
  * prefix_sep 前缀链接符号
  * dummy_na  是否为Nan值添加一行
  * columns df中需要编码的列名
  * sparse 虚拟列是否是稀疏的
  * drop_first 是否通过congk个分类级别中删除第一级来或得k-1个分类

 * 等宽离散 cut( x, bins, right: bool = True, labels=None, retbins: bool = False, precision: int = 3,include_lowest: bool = False,
   * x 数据
   * bins 若为int 代表离散化后的类别数目；若为序列，则表示切分的区间
   * right 右侧是否闭区间


###  数据规整

####  层次化索引
> 层次化索引 ： 在某一个方向拥有多个索引级别

作用：
* pandas 能够以较低维度形式处理高纬度的数据
* 可以按照层次统计数据
* 在数据重塑和基于分组的操作（如透视表生成）中扮演重要角色

##### Series 层次索引

一个有列表或数组组成的列表作为索引
``` python
  data = pd.Series(np.random.randn(9), index=[['a', 'a', 'a', 'b', 'b', 'b', 'c', 'c', 'c'], [1, 2, 3] * 3])
  print(data.index) # 会得到层次化索引MultiIndex 

  print(data['a']) # 利用层次化索引获取数据
  print(data['a':'c'])
  print(data[:,1])   # 通过切片获取数据
  print(data.loc['a':'c', 1:2])
```

##### DataFrame 层次索引

索引的建立:
    1. 一个有列表或数组组成的列表作为索引
    2. 使用MultiIndex创建索引
    3. 使用DataFrame的列作为层次索引: 
        * `set_index`函数,将多个列转换为行索引， 并创建新的DataFrame
        * `reset_index`函数，还原索引，重新变为默认的整型索引
    
索引的相关操作:

 * __重排__： 重新调整各条轴上各级别的顺序 swaplevel(self, i=-2, j=-1, axis=0)

 * __分级排序__： 根据指定级别傻姑娘的值对数据进行排序 sort_index(self,axis=0,level=None, ascending: bool = True, inplace: bool = False, sort_remaining: bool = True）
 
 * __根据级别汇总统计__：DataFrame 和 Serires的描述和汇总攻击都有一个level选项，用于指定某条轴上求和的级别


#### 数据合并

##### 堆叠合并数据

 pandas.concat(
        objs: Union[Iterable[FrameOrSeries], Mapping[Label, FrameOrSeries]], # 接受多个Series/DataFrame/Panel的组合
        axis=0,                                                              # 连接的轴向，默认0纵向、1横向
        join="outer",                                                        # 合并方式 （inner：交集合并，outer：并集合并）
        ignore_index: bool = False, 
        keys=None, # 与连接对象有关的值，用于形成连接轴向上的层次化索引
        levels=None,    # 接受包含多个sequence的list， 表示在指定keys参数后，指定用作层次化索引各级别上的索引
        names=None, # list，设置key和level后，用于分成级别的名称
        verify_integrity: bool = False, # 是否检查结果对象新轴上的重复情况， 如果发现会引发异常
        sort: bool = False,
        copy: bool = True,
    ) -> FrameOrSeriesUnion:

* 横向堆叠 axis=1， 将2个表在x轴向上拼接
    1. 如果2个表索引完全一样，不论join取什么值，都会直接拼接
    2. 如果索引不一样，若join=inner交集，返回索引重叠部分；join=outer并集，则显示并集部分数据，不足的使用空值
    
* 纵向堆叠 axis=0， 将2个表在y轴向上拼接
    1. 如果2个表索引完全一样，不论join取什么值，都会直接拼接
    2. 如果索引不一样，若join=inner交集，返回索引重叠部分；join=outer并集，则显示并集部分数据，不足的使用空值

* 使用append实现纵向叠加 （列名需要完一致）

    
##### 主键合并数据

主键合并： 通过多个键将2个数据集的行连接起来，类似SQL中的join

针对同一个主键存在2张包含不同字段的表，将其根据某个字段一一对应拼接起来，结果集列数为2个元数据的列数和减去连接键的数量

pandas.merge

|参数|说明|默认|
|:-----|:-----|:-----|
|left |要添加的新数据||
|right |要添加的新数据||
|how |连接方式（inner,outer,left,right）||
|on    |2个数据合并的主键（必须一样）||
|left_on   |表示left参数接收数据用于合并的主键||
|right_on    |表示right参数接收数据用于合并的主键||
|left_index  |是否将left参数的数据的index作为连接主键||
|right_index |是否将right参数的数据的index作为连接主键||
|sort    |是否根据连接键对合并后的数据进行排序||
|suffixes  |用于追加到left和right参数接收数据重叠列名的尾缀默认('_x','_y')||

DataFrame.join

|参数|说明|默认|
|:-----|:-----|:-----|
|other |dataframe,series参与连接的数据|无|
|how |连接方式（inner,outer,left,right）|left|
|on    |用于连接的列名|None|
|lsuffix   |用于追加到左侧重叠列名的末尾||
|rsuffix    |用于追加到右侧重叠列名的末尾||
|sort    |是否根据连接键对合并后的数据进行排序||


##### 重叠合并数据
如果2份数据的内容几乎一致，某些特征在其中一张表是完整的，而在另一张表上的数据则是缺失的，或者有索引全部或部分重叠的2个数据集，都可以用combine_first方法进行重叠数据合并

DataFrame.combine_other

##### 重塑层次化索引

DataFrame.stack 将原来的列索引转成最内层的行索引

DataFrame.unstack 逆操作： 将指定层的行索引还原成列索引

DataFrame.pivot 指定某列的值作为行索引， 指定某列的值作为列索引，然后在指定哪些列作为索引对应的值

