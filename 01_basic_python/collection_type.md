# Python中的集合类型
> Python中的集合类型数据包括: List（列表）,Tuple（元组）, Set（集合）,Dictionary（字典）

### 集合 Set

> set集合，是一个无序且不重复、不可变对象的元素集合。
> 集合对象是一组无序排列的可哈希的值，集合成员可以做字典中的键。
 用in和not in操作符检查成员，由len()内建函数得到集合的基数(大小)， 用 for 循环迭代集合的成员。

#### 创建

```python
s = set()
s = {11,22,33,44}
# s[0] TypeError 集合不能进行索引、切片

s = {} # 此创建的实际上是一个空字典
for i in s:
  print(i, end=' ') # 集合也是可迭代、可变的

a=set('boy')
b=set(['y', 'b', 'o','o'])
c=set({"k1":'v1','k2':'v2'})
d={'k1','k2','k2'}
e={('k1', 'k2','k2')}
print(a,type(a))
```

集合中的元素和字典的键在表现上具有一定的相似性，比如相等的数值（ 1 和 1.0 ）在集合中只包含一个，对比在字典中，对于值相等的数值来说，也会被当作同一键处理；字典的 keys() 方法生成的视图对象也支持集合的相关操作。
```python
>>> {1, 1.0}
{1}
>>> {1: 'Kate', 1.0: 'nina'}
{1: 'nina'}
```

#### 功能
__增加__

```python
a=set('python') # 向 set() 传递一个可迭代对象或者使用集合字面量的方式
a.add('tina') # {'tina', 'o', 'p', 'n', 't', 'y', 'h'}
print(a)
b=set('python')
b.update('tina') # {'o', 'i', 'p', 'a', 'n', 't', 'y', 'h'}
print(b)

{i // 3 for i in range(10)}  # 集合推导

```
add是单个元素的添加，而update是批量的添加。输出结果是无序的，并非添加到尾部。

__删除__（remove，discard，pop）
```python
c.remove('p')
c.discard('p')
c.pop()
c.clear()
```
discard 删除指定元素，当指定元素不存在时，不报错；
remove  删除指定元素，但当指定元素不存在时，报错：KeyError。
pop     删除任意元素，并可将移除的元素赋值给一个变量，不能指定元素移除。
clear   清空

set的集合运算：

```python
s1 = {0}
s2 = {i % 2 for i in range(10)}
s = set('hi')
t = set(['h', 'e', 'l', 'l', 'o'])
print(s.intersection(t), s & t)  # 交集
print(s.union(t), s | t)   # 并集
print(s.difference(t), s - t)  # 差集
print(s.symmetric_difference(t), s ^ t) # 对称差集
print(s1.issubset(s2), s1 <= s2) # 子集（被包含） True True
print(s1.issuperset(s2), s1 >= s2)   # 父集（包含）False False

print(s.isdisjoint(t))  #（disjoint脱节的，）即如果没有交集，返回True，否则返回False
s.difference_update(t)  # 将差集覆盖到源集合，即从当前集合中删除和B中相同的元素
s.intersection_update(t)  # 将交集覆盖到源集合
s.symmetric_difference_update(t)#将对称差集覆盖到源集合
```

|运算符	|对应的方法|	作用|
|:----|:----|:----|
|set & other & ...	|intersection(*others)	|返回所有集合的交集|
|set &= other & ...	|intersection_update(*others)	|将原集合更新为所有集合的交集|
|set ｜ other ｜ ...	|union(*others)	|返回所有集合的并集|
|set ｜= other ｜ ...	|update(*others)	|将原集合更新为所有集合的并集|
|set - other - ...	|difference(*others)	|返回原集合和其他集合的差集|
|set -= other ｜ ...	|difference_update(*others)	|将原集合更新为原集合和其他集合的差集|
|set ^ other	|symmetric_difference(other)	|返回这两个集合的对称差集|
|set ^= other	|symmetric_difference_update(other)|	将原集合更新为这两个集合的对称差集|

集合的比较
 
|运算符|	对应的方法|	作用|
|:----|:----|:----|
|set < other|		|判断前者是否为后者的真子集|
|set <= other|	issubset(other)	|判断前者是否为后者的子集|
|set > other|	|	判断前者是否为后者的真超集|
|set >= other|	issuperset(other)|	判断前者是否为后者的超集|
| |isdisjoint(other)|	判断两个集合是否相交|

```python
 {1, 2, 3} < {2, 3, 4} # False
>>> [1, 2, 3] < [2, 3, 4] # True
>>> {1, 2, 3} == {3, 2, 1} # True
>>> [1, 2, 3] == [3, 2, 1] # False
>>> {2, 3} < {2, 3, 4} # True

>>> {3, 4, 5, 6} > {3, 4} # True
```

当 set 和 frozenset 在集合运算时，其返回的结果类型和第一个操作数一致

```python
>>> set('bc') & frozenset('abc')
{'b', 'c'}
>>> frozenset('abc') & set('bc')
frozenset({'b', 'c'})
```


__转换__
```python
se = set(range(4))
li = list(se)
tu = tuple(se)
st = str(se)
```


**集合运算的常用场景**

1. 集合运算中的交集、差集、并集、是否相交，是否为子集等操作常应用于现实的场景中，比如计算两个数据集中相同数据的个数 len(set(iterable) & set(iterable))。

2. 利用集合运算来解决实际问题，简化代码逻辑，避免手动的循环以及成员关系判断，提高代码运行效率。

    ```python
    l_1 = [1, 2, 3]
    l_2 = [2, 1, 3]
    l_1 == l_2 # False
    l_1.sort() == l_2.sort() # True
    set(l_1) == set(l_2) # True
    ```

3. 集合相等性比较可以应用在比较两个列表中的元素是否一致，从而降低性能开销：

4.  使用 `set(dir(set)) - set(dir(frozenset))` 来获得 set 对象和 frozenset 对象在属性列表上的差别
    其他同类型的场景下，比如对比字符串、列表等之间的差别： `set('hello!') - set('Hello')`



#### 不可变集合 frozenset([iterable])
> 不可变集合是可散列的（本身不可改变，且只能包含可散列对象），可以被集合包含或作为字典的键存在

```python
>>> {{1, 2, 3}: 6} # TypeError: unhashable type: 'set'
>>> f = frozenset([1, 2, 3])
>>> f.add() # AttributeError: 'frozenset' object has no attribute 'add'
>>> {f: 6} # {frozenset({1, 2, 3}): 6}
```

###  列表 List

> 序列中的每个元素都分配一个数字 - 它的位置，或索引，第一个索引是0，第二个索引是1，依此类推。

Python有6个序列的内置类型，但最常见的是列表和元组。
序列都可以进行的操作包括索引，切片，加，乘，检查成员。

__创建__ 只要把逗号分隔的不同的数据项使用方括号括起来即可。

```python
list1 = ['Google', 'Runoob', 1997, 2000]
list2 = [1, 2, 3, 4, 5 ]
list3 = ["a", "b", "c", "d"]
```
与字符串的索引一样，列表索引从0开始。列表可以进行截取、组合等。
访问列表中的值使用下标索引来访问列表中的值，同样你也可以使用方括号的形式截取字符``list[1]; list2[1:5]`

__Python列表脚本操作符__

列表对+ 和 * 的操作符与字符串相似。+ 号用于组合列表，* 号用于重复列表。

|Python表达式|	结果|	描述|
|:----|:----|:----|
|len([1, 2, 3])	|3	|长度|
|[1, 2, 3] + [4, 5, 6]	|[1, 2, 3, 4, 5, 6]	|组合,拼接|
|['Hi!'] * 4	|['Hi!', 'Hi!', 'Hi!', 'Hi!']	|重复|
|3 in [1, 2, 3]	|True	|元素是否存在于列表中|
|for x in [1, 2, 3]: print(x, end=" ")	|1 2 3|	迭代|


__列表截取__

`L=['Google', 'Runoob', 'Taobao']`

|Python表达式|	结果|	描述|
|:----|:----|:----|
|L[2]	|'Taobao'	|读取第三个元素|
|L[-2]	|'Runoob'	|从右侧开始读取倒数第二个元素: count from the right|
|L[1:]	|['Runoob', 'Taobao']	|输出从第二个元素开始后的所有元素|


__嵌套列表__

使用嵌套列表即在列表里创建其它列表，例如：
```python
a = ['a', 'b', 'c']
n = [1, 2, 3]
x = [a, n]
x[0] # ['a', 'b', 'c']
x[0][1] #  'b'
```

__重要函数__

* len(list) 列表元素个数
* max(list) 返回列表元素最大值
* min(list) 返回列表元素最小值
* list(seq) 将元组转换为列表

__重要方法__

* list.append(obj) 在列表末尾添加新的对象
* list.count(obj) 统计某个元素在列表中出现的次数
* list.extend(seq) 在列表末尾一次性追加另一个序列中的多个值（用新列表扩展原来的列表）
* list.index(obj) 从列表中找出某个值第一个匹配项的索引位置
* list.insert(index, obj) 将对象插入列表
* list.pop([index=-1]) 移除列表中的一个元素（默认最后一个元素），并且返回该元素的值
* list.remove(obj) 移除列表中某个值的第一个匹配项 当要移除的元素不存在时，会引发 ValueError
* list.reverse() 反向列表中元素
* list.sort(cmp=None, key=None, reverse=False) 对原列表进行排序
* list.clear() 清空列表
* list.copy() 深复制列表 等同`a[:]`, `list[a]`

__列表排序__
> 可使用 list.sort(key=None, reverse=False) 或者内置函数 sorted(iterable, *, key=None, reverse=False)
>
>（形参中的 * 代表 * 之后的 key 和 reverse 为仅限关键字参数，即在调用该函数时，若传递 key 或 reverse 参数，则必须按照关键字参数的形式

* `a.sort()` ` # 默认按照升序进行排列

* `a.sort(key=str.upper)`  # 使用一个单参数函数作为 key，使用它的返回结果进行排序 

* `a.sort(key=str.upper, reverse=True)` # 使用 reverse 参数按照降序

* `a.sort(key=lambda x: x['price'])`  使用 key 参数来基于一个键进行排序

*  `import operator a.sort(key=operator.itemgetter('price'), reverse=True)` 使用 operator 标准库提供的访问器来代替 lambda

> 注意一点，有些方法是没有返回值的（返回值为 None ）

#### 列表推导式

*  `[i * 2 for i in a]` 使用 for 循环

*  `[i for i in range(10) if i % 2 == 0]` 使用 if 分句

*  `[i if i % 2 == 0 else None for i in range(10)]`

* `[(i, j) for i in name for j in price]  # [('apple', 10),('apple', 5),..]`  嵌套循环

* `[(i, j) for i in name for j in price if j > 5]`

* `[(i, j) for i in name if i[0] != 'a' for j in price if j > 5]`

__列表乘法__

```python
a = [1, 2, 3]
b = a * 3   # [1, 2, 3, 1, 2, 3, 1, 2, 3]
c = [a] * 3 # [[1, 2, 3], [1, 2, 3], [1, 2, 3]]

```


### 元组 Tuple

> 元组与列表类似，不同之处在于元组的元素不能修改。  元组使用小括号，列表使用方括号。
> 元组可以包含任意的 Python 对象，包括它们组成的嵌套结构等

__创建__
```python
tup1 = ('Google', 'Runoob', 1997, 2000)
tup2 = (1, 2, 3, 4, 5 )
tup3 = "a", "b", "c", "d"   #  不需要括号也可以

tup1 = (50)
type(tup1)     # 只包含一个元素时 不加逗号，类型为整型
tup1 = (50,)   # 加上逗号，类型为元组
```   
> 包含单一元素的元组，需要在元素后面添加逗号

组与字符串类似，下标索引从0开始，可以进行截取，组合等.可使用 + , * 和 []  

重要函数: len(tuple), max(tuple), min(tuple), tuple(seq) 将列表转换为元组。

#### 命名元组 namedtuple
> 期望访问元组中的元素时通过类似键名访问的方式，可以使用标准库 collections 中的 namedtuple() 函数

```python
from collections import namedtuple
Date = namedtuple('Date', ['year', 'month', 'day'])
d = Date(2019, 12, 9)
d.year, d.month, d.day # (2019, 12, 9)
d[0], d[1], d[2] # (2019, 12, 9)
```

存在列表的情况下为什么还需要元组？

* 元组具有不可变性，元组的不可变性提供了数据的一致性
* 元组常用于表示固定意义的、具有一定相关性的数据 (大部分情况下元组可以作为字典的键,(包含的元素均为可散列时))
* 一般情况下，创建常量元组的效率高于列表
* 元组无需像列表那样进行空间超额分配，其占用空间大小固定，相对于列表具有一定的空间占用优势
* 元组在索引等操作上具有一定效率优势



### 字典 Dict

> 字典是另一种可变容器模型，且可存储任意类型对象。字典的每个键值(key=>value)对用冒号(:)分割，每个对之间用逗号(,)分割，整个字典包括在花括号({})

__创建__
```python
dict = {'Alice': '2341', 'Beth': '9102', 'Cecil': '3258'}
dict2 = { 'abc': 123, 98.6: 37 };
dict3 = {'Name': 'Runoob', 'Age': 7, 'Class': 'First'}
print ("dict3['Name']: ", dict3['Name'])

```

键必须是唯一的，但值则不必。值可以取任何数据类型，但键必须是不可变的，如字符串，数字或元组。

如果用字典里没有的键访问数据，会输出错误：KeyError

修改字典
向字典添加新内容的方法是增加新的键/值对，修改或删除已有键/值对如下实例:
```python
dict['Age'] = 8;               # 更新 Age
dict['School'] = "High scholl"  # 添加信息
del dict['Name'] # 删除键 'Name'
dict.clear()     # 清空字典
del dict         # 删除字典
```

字典键的特性

字典值可以是任何的 python 对象，既可以是标准的对象，也可以是用户定义的，但键不行。

1. 不允许同一个键出现两次。创建时如果同一个键被赋值两次，后一个值会被记住，如下实例：

2. 键必须不可变，所以可以用数字，字符串或元组充当，而用列表就不行，如下实例：

__内置函数__：

len(dict), str(dict), type(variable)

__内置方法__：

* dict.clear() 删除字典内所有元素
* dict.copy() 返回一个字典的浅复制
* dict.fromkeys() 创建一个新字典，以序列seq中元素做字典的键，val为字典所有键对应的初始值
* dict.get(key, default=None) 返回指定键的值，如果值不在字典中返回default值
* key in dict 如果键在字典dict里返回true，否则返回false
* dict.items() 以列表返回可遍历的(键, 值) 元组数组
* dict.keys() 返回一个迭代器，可以使用 list() 来转换为列表
* dict.setdefault(key, default=None) 和get()类似, 但如果键不存在于字典中，将会添加键并将值设为default
* dict.update(dict2) 把字典dict2的键/值对更新到dict里
* dict.values() 返回一个迭代器，可以使用 list() 来转换为列表
* pop(key[,default]) 删除字典给定键 key 所对应的值，返回值为被删除的值。key值必须给出。 否则，返回default值。
* popitem() 随机返回并删除字典中的一对键和值(一般删除末尾对)。

**字典的比较**

在 Python 2.X 中，字典之间是支持大小比较的，它通过比较排序之后的键值对列表来完成

在 Python 3.X 中，字典间的大小比较不再被支持

#### 字典背后的散列表
> 什么是散列、为什么字典的键需要可散列、为什么字典的搜索效率非常高等等。

字典是一种具有关联性质的容器，它采用了散列表（ hash table ）来实现（ hash 常被音译为哈希，被翻译为散列）。字典也常被称为散列表，映射（ map ），或者关联数组（ associative array ）
 
散列表的基本思路是通过散列函数将键映射为一个索引值，继而通过该索引值来进行内存中的数据访问。

一个好的散列函数不仅仅是快速和便于计算的，并且它也是可以减少散列冲突的

散列函数的常用构造方法包括直接定址法、数字分析法、平方取中法、折叠法、除留余数法、随机数法

**散列冲突**

> 在映射的过程中，可能会出现不同的键得到的散列值是相同的，即 k1 != k2，但 f(k1) = f(k2)

散列冲突是需要在散列表的实现中解决的，常用的处理冲突的方法包括开放定址法、再哈希法、链地址法等
Python 中解决散列冲突问题采用的方法为开放定址法。

**字典的内存开销**

负载因子是指散列表中的已占用的空间和总空间的比值，当负载因子小于某个阈值时，发生散列冲突的概率将会随之上升。

当负载因子小于 2/3 时，Python 会在插入新值时会散列表进行扩容，以减少散列冲突发生的概率。


**可散列的: 在 Python 中 hashable 的含义什么？**

* 一个对象的哈希值如果在其生命周期内不改变，则称为可哈希。（具有 \__hash__() 方法），并可以同其他对象进行比较（具有 \__eq__() 方法）
* 只有可哈希的对象才能作为字典的键或者集合中的成员。
* 并非所有的不可变类型都是可哈希的，比如包含不可哈希元素的不可变容器。

大多数 Python 中的不可变内置对象都是可哈希的；
可变容器（例如列表或字典）都不可哈希；
不可变容器（例如元组或 frozenset）仅当它们的元素均为可哈希时才是可哈希的。 
用户定义类的实例对象默认是可哈希的。 
它们在比较时一定不相同（除非是与自己比较），它们的哈希值的生成是基于它们的 id()

在 Python 中 hash() 可用于返回某个对象的散列值（前提是这个对象可散列），其值为整数。 `hash('python') # 9026591364990531778`


## 面试题 interview problem

### list, set, dict 使用 in 判断一个元算是否存在的时间复杂度

* list 查找时间复杂度 O(n)
* set 查找时间复杂度 O(1)
* dict 查找时间复杂度 O(1)
