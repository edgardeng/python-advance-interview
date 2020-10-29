# Python中的集合类型
> Python中的集合类型数据包括: List（列表）,Tuple（元组）, Set（集合）,Dictionary（字典）

### 集合 Set

> set集合，是一个无序且不重复的元素集合。
>集合对象是一组无序排列的可哈希的值，集合成员可以做字典中的键。
 用in和not in操作符检查成员，由len()内建函数得到集合的基数(大小)， 用 for 循环迭代集合的成员。

#### 创建

```python
s = set()
s = {11,22,33,44}

s = {} # 此创建的实际上是一个空字典

a=set('boy')
b=set(['y', 'b', 'o','o'])
c=set({"k1":'v1','k2':'v2'})
d={'k1','k2','k2'}
e={('k1', 'k2','k2')}
print(a,type(a))
```
#### 功能
__增加__

```python
a=set('python')
a.add('tina') # {'tina', 'o', 'p', 'n', 't', 'y', 'h'}
print(a)
b=set('python')
b.update('tina') # {'o', 'i', 'p', 'a', 'n', 't', 'y', 'h'}
print(b)
```
add是单个元素的添加，而update是批量的添加。输出结果是无序的，并非添加到尾部。

__删除__（remove，discard，pop）
```python
c.remove('p')
c.discard('p')
c.pop()
c.clear()
```
discard删除指定元素，当指定元素不存在时，不报错；
remove删除指定元素，但当指定元素不存在时，报错：KeyError。
pop删除任意元素，并可将移除的元素赋值给一个变量，不能指定元素移除。
clear 清空

set的特有功能：
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

__转换__
```python
se = set(range(4))
li = list(se)
tu = tuple(se)
st = str(se)
```


###  列表 List

> 序列中的每个元素都分配一个数字 - 它的位置，或索引，第一个索引是0，第二个索引是1，依此类推。

Python有6个序列的内置类型，但最常见的是列表和元组。序列都可以进行的操作包括索引，切片，加，乘，检查成员。

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
* list.remove(obj) 移除列表中某个值的第一个匹配项
* list.reverse() 反向列表中元素
* list.sort(cmp=None, key=None, reverse=False) 对原列表进行排序
* list.clear() 清空列表
* list.copy() 复制列表

### 元组 Tuple

>元组与列表类似，不同之处在于元组的元素不能修改。  元组使用小括号，列表使用方括号。

__创建__
```python
tup1 = ('Google', 'Runoob', 1997, 2000)
tup2 = (1, 2, 3, 4, 5 )
tup3 = "a", "b", "c", "d"   #  不需要括号也可以

tup1 = (50)
type(tup1)     # 只包含一个元素时 不加逗号，类型为整型
tup1 = (50,)   # 加上逗号，类型为元组
```   
组与字符串类似，下标索引从0开始，可以进行截取，组合等.可使用 + , * 和 []  

重要函数: len(tuple), max(tuple), min(tuple), tuple(seq) 将列表转换为元组。

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


## 面试题 interview problem

### list, set, dict 使用 in 判断一个元算是否存在的时间复杂度

* list 查找时间复杂度 O(n)
* set 查找时间复杂度 O(1)
* dict 查找时间复杂度 O(1)
