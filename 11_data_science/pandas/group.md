## 数据的分组与聚合

分组组合的机制：  拆分 --- 应用 --- 合并

* pandas对象中的数据根据一个或多个键 被拆分split为多组 （拆分操作是在对象的特定轴上进行的）

* 将一个函数应用apply到各个分组并产生新的值

* 所有这些函数的执行结果 会 被合并combine到最终结果中

### 方法

 * DataFrame.grougby 分组 （根据索引或字段对数据进行分组）
    > * by          分组的依据， 接收 list，string，mapping，generator
    > * axis        操作的轴向 默认 0
    > * level       标签级别 （int，索引名）
    > * as_index    是否以索引形式输出 默认 True                                    
    > * sort        是否对分组依据标签排序 默认 True
    > * group_keys  是否显示分组标签名称
    > * squeeze     是否在允许的情况下返回数据进行降维 默认False

> ! 使用groupby分组后的结果是GroupBy对象，不能直接查看，存在内存中，输出的是内存地址
 
    
分组键 可以有多种形式，且类型不必相同：
    * 列表或数组，长度和带分组的轴一样
    * 表示DataFrame某个列名的值
    * 字典 Series， 给出 轴上的值与分组名之间的对应关系
    * 函数 ，处理轴索引或索引中标签， 对索引进行计算后再分组
    
    
GroupBy对象 常用的描述性统计方法 (聚合运算)
    * count
    * cumcount
    * head
    * size
    * max
    * min std
    * mean median sum 

### groupby方法的使用
  
 * 单列对单列进行分组
```python
 group = df['data1'].groupby(df['key1'])
 group.mean()
 group.sum()
```

* 多列对单列进行分组 `group = df['data1'].groupby([df['key1'] ,df['key2'] ])`

* 单列对多列进行分组 `group = df[['data1','data2']].groupby(df['key1'])`

* 多列对多列进行分组 `group = df.groupby([df['key1'] ,df['key2'] ])`

* 数组作为分组键
```python
states = np.array(['a','b','c'])
years = np.array([2018,2019,2020])
group = df.groupby([states,years])
```

* 列名字符串 作为分组键 `group = df.groupby('key1') group = df.groupby(['key1','key2'])`

* 麻烦列
    * 非数值列，在数值运算时会忽略掉



## 数据聚合

1. 使用Groupby对象的统计函数 聚合
2. 自定义聚合函数  agg / aggregate
    > agg / aggregate 都支持对每个分组应用某个函数

* DataFrame.agg(func=None, axis=0, *args, **kwargs):

* DataFrame.aggregate(func=None, axis=0, *args, **kwargs):
    > func 应用于每行/每列的函数 list，dict，fuction
    > axis 操作轴向，默认0

聚合函数：（内置/自定义函数）
 * 传入的聚合函数，由（name,function）元组组成的列表， 第一个元素会被用作聚合后的DataFrame的列名 
 * 对一个列或不同的列应用不同的函数，具体是向agg传入一个从列名映射到函数的字典，将字段名作为key，函数名作为值
 * 对某一列可以应用多个聚合函数
                                                          
                                                             
### apply 方法聚合数据

apply 将待处理的对象拆分成多个片段，然后对各片段调用传入的函数，最后尝试将各片段组合在一起

apply 将函数应用到每一列

apply 传入的函数只能作用域整个DataFrame或者Series， 不能像agg方法一样，对不同字段应用不同函数来获取不同结果


DataFrame.apply
    > * func         应用的函数
    > * axis        操作的轴向 默认 0
    > * broadcast     是否进行广播，默认false
    > * raw            是否将ndarray对象传递给函数，默认False                               
    > * reduce        返回值的格式
    

### transform 方法聚合数据

 * 对整个DataFrame的所有元素进行操作
 * 只有一个参数func ，表示操作函数
 * 能够对DataFrame分组后的GroupBy对象进行操作， 可以实现组内离差标准化等操作
 * 在计算离差标准化的时候结果中有NaN， 由于根据离差标准化公式，最大值和最小值相同时的情况下分母是0。
    而分母为0的数在python中为NaN
    

## 透视表
> pivot table 透视表是各种电子表格程序和其他数据分析软件中一种常见的数据汇总工具

* 根据一个或多个键对数据进行聚合，并根据行和列的分组键将数据分配到各个矩形区域

* 在Python和Pandas中，通过groupby以及重塑运算制作透视表

* DataFrame.pivot_table 实现透视表

* pandas.pivot_table
    > * data        表的数据
    > * values      想要聚合的数据字段名 默认全部数据
    > * index       行分组键
    > * columns     列分组键
    > * aggfunc     聚合函数，默认是mean
    > * margins     汇总的开关。默认True， 结果集中出现名为ALL的行和列
    > * dropna      是否删掉全为NaN的列 默认False
    > * fill_value    存在缺失值，以指定值进行填充，默认NaN

 
## 交叉表

cross-tabulation 交叉表是一种计算分组频率的特殊透视表

* pandas.crosstab() 制作交叉表
   > 基本和pivot_table参数一致。 不同：crosstab的index，columns，values填入的都是对应的从DataFrame中取出的某一列
 
 
 
 
 
 
