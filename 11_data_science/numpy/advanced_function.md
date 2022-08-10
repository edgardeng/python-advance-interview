# Numpy

## Advanced Function 高级函数

常用的十二个高级函数

1. where    查找/筛选
2. cumsum   累加和
3. cumprod  累乘积
4. argmin   最小值（元素下标）
5. argmax   最大值（元素下标）
6. sort     排序
7. unique   唯一值
8. in1d     是否包含于
9. intersect1d  公共元素
10. union1d     并集
11. setdiff1d   差集（在X，不在Y的元素）
12. setxor1d    异或集（在一个数组，但不同时存在2个数组中）


### np.where(condition,x,y) 查找 

 > 用法一：满足条件(condition)，输出x，不满足输出y。
 
 > 用法二：筛选出满足条件(condition)的元素。

```python
import numpy as np
x = np.arange(0, 10)
y = np.where(x > 5)      # 返回位置 元组
y = np.where(x > 5,x,5)   # 查找数组中大于5的值，并返回。对于小于等于5的部分，直接用5代替
# [0 0 0 0 0 0 6 7 8 9]
y = np.where(x > 5, x, x*10) # 对于小于等于5的部分，直接用 某个数组中的值 代替

```

### np.cumsum()和np.cumprod()

np.cumsum()：按照不同轴，计算元素的累加和。
np.cumprod()：按照不同轴，计算元素的累乘积。

```python
    x = np.array([[1, 2], [4, 5], [7, 8]])
    # 若不设置axis，则会自动将数组拉成一条直线，然后进行累加或累乘
    y = np.cumsum(x)
    y = np.cumprod(x)

    y = np.cumsum(x, 0) # 0表示【按列方向操作】 1表示【按行方向操作】
    y = np.cumprod(x, 0)

```

### np.argmin()和np.argmax()

* np.argmin()：按照不同轴，返回最小值元素的下标。
* np.argmax()：按照不同轴，返回最大值元素的下标
> 若不设置axis，则会自动将数组拉成一条直线，返回最大值、最小值元素的下标。

```python
import numpy as np
x = np.array([[2,1,7],[6,0,3],[5,4,8]])
np.argmin(x) # 4
np.argmax(x) # 8
np.argmin(x,axis=0)
np.argmin(x,axis=1)
```

> axis=0表示【按列方向操作】；  axis=1表示【按行方向操作】；

### np.sort()
> 按照不同轴，进行元素排序,  默认是按照行操作，相当于axis=1。
 
```python
x = np.array([[2,1,7],[6,0,3],[5,4,8]])
np.sort(x)
np.sort(x,axis=1)
```

### np.unique()
> 计算x中的唯一元素，并返回结果

```python
x = np.array([1,1,2,3,4,3,4,5,6])
np.unique(x)  # 1,2,3,4,5,6
```

### np.intersect1d()
> 交集：计算x和y的公共元素, 并返回有序结果

```python
import numpy as np
x = np.array(([8,1,5,2,7,3,6,4]))
y = [1,5,8]
np.intersect1d(x,y) # [1,5,8]
```

### np.union1d()
> 计算x和y的并集，返回有序结果

```python
import numpy as np
x = np.array(([8,1,5,2,7,3,6,4]))
z = [10,11,8]
np.union1d(x,z) # [1,2,3,4,5,6,7,8,11]
```

### np.in1d()
> 返回 “x的元素是否包含于y”的布尔型数组

```python
import numpy as np
x = np.array(([8,1,5,2,7,3,6,4]))
y = [1,5,8]
np.in1d(x,y) # [True,True,True,False, False, False, False, False]
```

### np.setdiff1d()
> 集合的差，即元素在x中且不在y中

```python
import numpy as np
x = np.array(([8,1,5,2,7,3,6,4]))
y = [1,5,8]
np.setdiff1d(x,y) # [2,7,3,6,4]
```

### np.setxor1d()
> 集合的对称差，存在于一个数组中但不同时存在于两个数组中

```python
import numpy as np
x = np.array(([8,1,5,2,7,3,6,4]))
y = [1,5,8]
np.setxor1d(x,y) # [2,3,4,6,7]
```