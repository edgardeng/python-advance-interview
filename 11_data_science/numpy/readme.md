# Data Statistic 数据统计

## Numpy
> Numerical Python 的简称 科学计算的基础库，提供大量科学计算相关功能。 C语言编写
  
 * 快速的数组处理能力
 * 内存小
 * 在数据分析方面作为算法和库之间传递数据的容器
 * 对数组型数据，在存储和处理数据是比内置的python数据结构高效
 * 有低级语言（C/Fortran） 编写的库，直接操作Numpy数组中的数据，无需进行任何复制工作
 
### Numpy 支持的数据类型：

|类型|类型代码|说明｜
|:----|:----|:----|
| int8 , uint8 | i1, u1 | 有符号和无符号的8位整型｜
| int16 , uint16 | i2, u2 | 有符号和无符号的16位整型｜
| int32 , uint32 | i4, u4 | 有符号和无符号的32位整型｜
| int64 , uint64 | i8, u8 | 有符号和无符号的64位整型｜
| float16       | f2 | 半精度浮点数 ｜
| float32       | f4/f | 单精度浮点数，与C的浮点数兼容｜
| float64       | f8/d | 双精度浮点数， 与C的double和python的float兼容｜
| float128      | f16/q | 扩展精度浮点数｜
| Complex64     | c8| 2个32位浮点数表示的复数｜
| Complex128    | c16 | 2个64位浮点数表示的复数｜
| Complex256    | c32 | 2个128位浮点数表示的复数｜
| bool          | ? | 布尔类型｜
| object        | O | python对象类型｜
| string_       | S | 固定长度的字符串类型，每个字符1个字节 ｜
| unicode_      | U | 固定长度的unicode类型    ｜

### ndarray 对象
> N维数组对象ndarray。 一系列同类数据的集合，以0下标开始进行集合中元素的索引。

* 对象用于存储同一类型元素的多维数组
* 每个元素在内存中都有相同存储大小的区域
* 内部组成：
    * 一个指向数据（内存或内存映射文件中的一块数据）的指针
    * 数据类型/dtype，描述数组收纳柜的固定大小值的格子
    * 一个表示数组形状（shape）的元组，表示各维度大小的元组
    

#### 数据的创建

* array(p_object, dtype=None, *args, **kwargs)

* arange([start,] stop[, step,], dtype=None)

* random.randint(low, high=None, size=None, dtype=None):

* random.randn(*dn)

* random.normal(loc=0.0, scale=1.0, size=None)

* random.shuffle 随机排序

* random.choice 已存在的随机选择

#### ndarray 对象属性

* ndarray.ndim 秩 维度的数量
* shape     维度
* size  元素的个数
* dtype  对象的元素类型
* itemsize  每个元素的大小（字节为单位）
* flags     内存信息
* real      实部
* imag      虚部
* data    实际数组元素的缓存区


#### split 分隔
> numpy.split(ary, indices_or_sections, axis=0):

* indices_or_sections ：如果是个整数，平均切分，如果是个数组，沿轴切分的位置。
* axis 沿着哪个轴切分。 默认0 横向切分

hsplit

vsplit

### Dtype 数据类型
> 一个特殊的对象，含有ndarray将一块内存解释为特定数据类型所需的信息

Dtype 数值类型
> 一个类型名（float，int）

类型转换 
```
a.astype(np.float64)
```

np.astype 可以转换单个值的类型



直接排序
arr.sort(axis=0)
arr.sort(axis=1)

间接排序
* arr.argsort  返回值是重新排序值的下标
* np.lexsort(a, axis=-1,kind='quicksort', order=None):    返回值是按照最后一个传入数据排序

去重
    np.unique 找出数组中唯一值，并返回已排序的结果
重复
   np.tile(a,reps)
   np.repeate(a,reps, axios=)   
集合运算 
 np.intersect1d  返回交集，并排序
  np.union1d     返回并集，并排序   
  np.in1d       返回x包含鱼Y的布尔数组
  np.setdiff1d  差集 在x,不在y
  np.setxor1d   对称差  交集之外的部分


### [通用函数 ufunc](./universal_function.md)

> 一种对ndarray中的数据执行元素级运算的函数，返回值也是ndarray数组

* 数组运算函数
  
* 三角函数
  
* 位操作函数
  
* 逻辑运算函数
  
* 浮动运算函数

 * 四则运算 加（+） 减（-）乘（*） 除（/） 幂 （**）
   
 * 比较运算 > , < ,== , >= ,<= , != 
   
 * 布尔运算 any = 'or', all= 'and'

 * 统计函数

### [高级函数 ](./advanced_function.md)


###  文件输入输出

读写二进制文件

np.save(path, arr) 将数组的数据以二进制的格式保存

np.load(path)  从二进制的文件中读取数据到数组

np.savez(path, arr, ...)  将多个数组保存到一个文件中

  * load读取保存了多个数组的二进制文件时，得到的不是一个数组，而是一个NPZFile类型
  第一个数组的健 arr_0,以此类推。也可以为每个数组设置键： np.save(paht,a=arr1,.. )

    * 存储时 可以省略扩展名，默认为npy，但读取时不能省略扩展名。用savez保存，默认为.npz
    
读写文本文件 (csv)

np.savetxt(path, arr, fmt='%.18e', delimiter=' ') 
    数组写入某种分隔符隔开的文本文件中
np.loadtxt(path, arr, delimiter=' ')
