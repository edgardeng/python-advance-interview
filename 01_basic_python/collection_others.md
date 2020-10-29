## collections 容器数据类型

 Python 内置核心数据类型包括list、tuple、dict、set外，
 
 Python 标准库 collections 模块提供的一系列容器数据类型，包括 ChainMap、Counter、deque、defaultdict、namedtuple()、OrderedDict 等

### ChainMap：组合多个映射对象
> ChainMap 是一种可以组合多个字典（或其他映射类型的对象）的容器类型，类似字典

```python

from collections import ChainMap
d_1 = {'name': 'bob', 'age': 27}
d_2 = {'age': 25, 'skill': 'coding', 'height': 175, 'weight': 120}
c = ChainMap(d_1, d_2) # ChainMap({'name': 'bob', 'age': 27}, {'})

d = {}
d.update(d_1)
d.update(d_2) # {{'name': 'bob', 'age': 25, 'address': ...}
```

ChainMap 类的构造函数 ，可以看到原始的映射对象被存放在一个列表中构成一个字典序列self.maps 
```python
def __init__(self, *maps):
    '''Initialize a ChainMap by setting *maps* to the given mappings.
    If no mappings are provided, a single empty dictionary is used.
    '''
    self.maps = list(maps) or [{}]          # always at least one map
```

* maps 属性
> maps 中组合的是映射对象的引用，所以 ChainMap 对象和我们之前提到的视图对象类似，可以反应原始映射的修改

在 ChainMap 中查询某个键时，会对原始的映射对象依次查询，直至找到这个键，若未找到，则默认引发 KeyError 异常。

```python
 c['age']  #  27 而不是 25
 c['address'] # KeyError: 'address'
```
> 如果一个类定义了 __getitem__ 方法，则当该类的实例对象 c 在进行索引操作时会调用 __getitem__ 方法，即 c[key] 会调用 c.__getitem__(key)

```python
def __missing__(self, key):
    raise KeyError(key)

def __getitem__(self, key):
    for mapping in self.maps:
        try:
            return mapping[key]
        except KeyError:
            pass
    return self.__missing__(key)   
```

在 ChainMap 中进行插入、更新、删除时，只会对原始映射中的第一个映射进行操作。

```python
c['address'] = 'XiErQi'
c['age'] = 30
c.pop('skill') #  KeyError: 
```

对应的 ChainMap 源码
```python
def __setitem__(self, key, value):
    self.maps[0][key] = value

def __delitem__(self, key):
    try:
        del self.maps[0][key]
    except KeyError:
        raise KeyError('Key not found in the first mapping: {!r}'.format(key))

def pop(self, key, *args):
    'Remove *key* from maps[0] and return its value. Raise KeyError if *key* not in maps[0].'
    try:
        return self.maps[0].pop(key, *args)
    except KeyError:
        raise KeyError('Key not found in the first mapping: {!r}'.format(key))
```

#### parents 属性

> 返回了一个不包含原始映射中的第一个映射的 ChainMap 对象，对应源码中 self.__class__(*self.maps[1:]) ，
> 其效果和 ChainMap(*d.maps[1:]) 

 在官方文档中，针对 parents 属性，提到了“使用的场景类似在 nested scopes 嵌套作用域中使用 nonlocal ，用例也可以类比内建函数 super() 

#### new_child(m=None) 方法

> 一个包含指定映射 m（未指定时，为空字典）及其他原有映射的 ChainMap 对象，其中指定映射位于底层 maps 列表首位，在其他原有映射之前
> new_child 方法可用于创建子上下文（ subcontexts ）

```python
>>> c.new_child()
ChainMap({}, {'name': 'jeff', 'age': 30, 'address': 'XiErQi'}, {'age': 25, 'skill': 'coding', 'height': 175, 'weight': 120})
>>> c.new_child({'gender': 'male'})
ChainMap({'gender': 'male'}, {'name': 'jeff', 'age': 30, 'address': 'XiErQi'}, {'age': 25, 'skill': 'coding', 'height': 175, 'weight': 120})

```

#### ChainMap 的应用场景

ChainMap 可以用于创建多个映射组成的查找链（在多个映射中搜索）、模拟嵌套上下文等，

1. 将用户指定的命令行参数优先于环境变量和默认值

2. 使用 ChainMap 对象作为嵌套上下文

### Counter：计数器
> Counter 类是 dict 的子类，可以简便、快速的进行可散列对象的计数
> 在一个 Counter 对象中，通常元素存储为字典的键，其计数值存储为字典的值，计数值是可以包括 0 和负值在内的整数值。

```python
>>> Counter([1, 2, 3, 2, 3, 2, 2, 2, 3])
Counter({2: 5, 3: 3, 1: 1})

```

**构造 Counter 对象**

```python
>>> Counter('bacbbc')
>>> Counter({'a': 1, 'b': 3, 'c': 2})
>>> Counter(a=1, b=3, c=2)
```

Counter 的 update 方法和 dict.update() 方法在效果上最明显的区别就是，前者是增加计数而后者是进行更新
```python
>>> c = Counter()
>>> c = Counter({'a':1, 'b':2})
>>> c.update({'a':2, 'b': 1})
>>> c # Counter({'a': 3, 'b': 3})
>>> c.update('aabb')
>>> c # Counter({'a': 5, 'b': 5})

```

获取元素计数

使用和字典相同的索引方法可以获取 Counter 对象中某个元素的计数。 `c['a']`
不同的是，对于在 Counter 对象中不存在的键，不会产生 KeyError ，而是会返回 0 作为其计数值 `c['c'] # 0`

数学运算
> Counter 对象支持多种数学运算，比如加、减、交集、并集、一元加、一元减

```python
>>> c_1 = Counter({'a': 3, 'b': 2})
>>> c_2 = Counter({'a': 4, 'b': 1, 'c': 2})
>>> c_3 = Counter({'a': 1, 'b': -5})
>>> c_1 + c_2 # Counter({'a': 7, 'b': 3, 'c': 2})
>>> c_1 - c_2 # Counter({'b': 1}) # 加减时，相同元素计数值便进行加减
>>> c_1 & c_2 # Counter({'a': 3, 'b': 1}) # 交集时，相同元素计数值取最小值
>>> c_1 | c_2 # Counter({'a': 4, 'b': 2, 'c': 2}) # 并集时，相同的元素计数值取最大值
>>> +c_3  # Counter({'a': 1})
>>> -c_3 # Counter({'b': 5})
```
> 注意两点：
>
> 第一，这些算术操作中只输出计数值大于 0 的元素及其计数值；
>
> 第二，对于在 Counter 对象中不存在的键，对应的计数值为 0。

#### most_common([n]) 方法

most_common([n]) 方法可以用于查询按照计数值由高到低排序的前 n 个元素及其计数值（ n 个最常见的元素和它们对应的计数值），计数值相同的元素按照首次出现的顺序进行排列

```python
from collections import Counter
Counter('casablanca').most_common(2) # [('a', 4), ('c', 2)]
Counter('casablanca').most_common()
[('a', 4), ('c', 2), ('s', 1), ('b', 1), ('l', 1), ('n', 1)]

# Counter('casablanca').most_common()[:-n-1:-1] 获取 n 个最不常见的元素
Counter('casablanca').most_common()[:-3:-1] # [('n', 1), ('l', 1)]
```

#### elements() 方法


