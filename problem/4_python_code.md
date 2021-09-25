## 三、Python 的代码使用


### 函数参数传递，下面程序运行的结果是？
> 考察可变类型
```python
def add(a, my_list=[]):
    my_list.append(a)
    return my_list

print(add('a')) # ['a']
print(add('b')) # ['a', 'b']
print(add('c')) # ['a', 'b', 'c']
```

### 代码简化

* 输出0-10的平方组成的列表 ` [x**2 for x in range(10)] `

* 实现1到100的和？    `sum(range(1,101)) `

* 输出一个[斐波那契数列](https://blog.csdn.net/chichu261/article/details/83589767)Fibonacci 
    `def fibo(n):
        if n <= 1:
            return n
        else:
            return (fibo(n - 1) + fibo(n - 2)) `

* 列表去重的方法 ` new_list = list(set(old_list))`

###  4G 内存怎么读取一个 5G 的数据？

**方法一**
可以通过生成器，分多次读取，每次读取数量相对少的数据（比如 500MB）进行处理，处理结束后在读取后面的 500MB 的数据。
```python
 def read_in_block(file_path = "/tmp/test.log"):
     BLOCK_SIZE = 1024
     with open(file_path, "r") as f:
         while True:
             block = f.read(BLOCK_SIZE)  # 每次读取固定长度到内存缓冲区
             if block:
                 yield block
             else:
                 return  # 如果读取到文件末尾，则退出

f = read_in_block()  # 迭代器对象
print(next(f))
print(next(f))
print(next(f))
# for block in read_in_block():
#  print block

def test4():
  with open("/tmp/test.log") as f:
    for line in f:
      print line 
#  for line in f 这种用法是把文件对象f当作迭代对象， 系统将自动处理IO缓冲和内存管理， 这种方法是更加pythonic的方法。 比较简洁。
```

**方法二** 通过 linux 命令 split 切割成小文件，然后再对数据进行处理，此方法效率比较高。可以按照行数切割，可以按照文件大小切割
 
### 列表[1,2,3,4,5],请使用map()函数输出[1,4,9,16,25]，并使用列表推导式提取出大于10的数，最终输出[16,25]。
> map是python高阶用法，字面意义是映射，它的作用就是把一个数据结构映射成另外一种数据结构。
> map的基本语法如下： map(函数, 序列1, 序列2, ...)
Python 2.x 返回列表。 Python 3.x 返回迭代器。

```python
list = [1,2,3,4,5]
def fn(x):
    return x ** 2

res = map(fn, list) 
res = [i for i in res if i > 10]
```

###  设计一个函数返回给定文件名的后缀?
> 考察字符串操作

1. rfind()  # 右侧字符出现的位置
2. 注意下面的0<pos<2 用法
3. if  ... else用法

```python
def get_suffix(filename, has_dot=False):
    """
    获取文件名的后缀名
    :param filename: 文件名
    :param has_dot: 返回的后缀名是否需要带点
    :return: 文件的后缀名
    """
    pos = filename.rfind('.')
    if 0 < pos < len(filename) - 1:
        index = pos if has_dot else pos + 1
        return filename[index:]
    else:
        return ''

```

### ：*args，**kwargs 这两个参数是什么意思？为什么要使用它们？

1. 如果我们不确定要往函数中传入多少个参数，或者我们想往函数中以列表和元组的形式传参数时，那就使要用*args；
2. 如果我们不知道要往函数中传入多少个关键词参数，或者想传入字典的值作为关键词参数时，那就要使用**kwargs。

> args和kwargs这两个标识符是约定俗成的用法，你当然还可以用*tom和**jarry，但是这样显的不专业。

```
def f(*args,**kwargs): 
	print(args, kwargs)

l = [1,2,3]
t = (4,5,6)
d = {'a':7,'b':8,'c':9}

f()
f(1,2,3)                    # (1, 2, 3) {}
f(1,2,3,"groovy")           # (1, 2, 3, 'groovy') {}
f(a=1,b=2,c=3)              # () {'a': 1, 'c': 3, 'b': 2}
f(a=1,b=2,c=3,zzz="hi")     # () {'a': 1, 'c': 3, 'b': 2, 'zzz': 'hi'}
f(1,2,3,a=1,b=2,c=3)        # (1, 2, 3) {'a': 1, 'c': 3, 'b': 2}

f(*l,**d)                   # (1, 2, 3) {'a': 7, 'c': 9, 'b': 8}
f(*t,**d)                   # (4, 5, 6) {'a': 7, 'c': 9, 'b': 8}
f(1,2,*t)                   # (1, 2, 4, 5, 6) {}
f(q="winning",**d)          # () {'a': 7, 'q': 'winning', 'c': 9, 'b': 8}
f(1,2,*t,q="winning",**d)   # (1, 2, 4, 5, 6) {'a': 7, 'q': 'winning', 'c': 9, 'b': 8}

def f2(arg1,arg2,*args,**kwargs): 
	print(arg1,arg2, args, kwargs)

f2(1,2,3)                       # 1 2 (3,) {}
f2(1,2,3,"groovy")              # 1 2 (3, 'groovy') {}
f2(arg1=1,arg2=2,c=3)           # 1 2 () {'c': 3}
f2(arg1=1,arg2=2,c=3,zzz="hi")  # 1 2 () {'c': 3, 'zzz': 'hi'}
f2(1,2,3,a=1,b=2,c=3)           # 1 2 (3,) {'a': 1, 'c': 3, 'b': 2}

f2(*l,**d)                   # 1 2 (3,) {'a': 7, 'c': 9, 'b': 8}
f2(*t,**d)                   # 4 5 (6,) {'a': 7, 'c': 9, 'b': 8}
f2(1,2,*t)                   # 1 2 (4, 5, 6) {}
f2(1,1,q="winning",**d)      # 1 1 () {'a': 7, 'q': 'winning', 'c': 9, 'b': 8}
f2(1,2,*t,q="winning",**d)   # 1 2 (4, 5, 6) {'a': 7, 'q': 'winning', 'c': 9, 'b': 8}
```

### 求出0~n的所有正整数中数字k（0~9）出现的次数。 

> 例如：k=1，n=12，那么 1 在 [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]一共出现5次[1,10,11,12]
输入：k=1，n=12
输出：5

方法一：

> 统计数字 1 在 [1,10,11,12]出现的次数这非常像Python中统计字符串a在字符串b中出现的次数：
b.count(a), 所以我们将把数字转为字符串来做统计。

```python
def digit_count(k,n):
    listn = []
    count = 0
    for i in range(0, n+1):
        count += str(i).count(str(k))
        if str(k) in str(i):
            listn.append(str(i))
    return count,listn
```

方法二 找规律


### 如何在python中使用三元运算符？

三元操作符语法如下，
[on_true] if [expression] else [on_false]

###  请尽可能列举python列表的成员方法，并给出以下列表操作的答案：
```python
a=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
a[::2]      # [1, 3, 5, 7, 9]
a[-2:]      # [9, 10]
```

 
一行代码实现对列表a中的偶数位置的元素进行加3后求和？

```
print(reduce(lambda x, y: x+y, [(x+3*((a.index(x)+1)%2)) for x in a])) # a中元素均不相同
# 或
print(reduce(lambda x, y: x+y, [a[x]+(x+1)%2*3 for x in range(0, 5)])) # 只适用于a中元素有5个情况
```

将列表a的元素顺序打乱，再对a进行排序得到列表b，然后把a和b按元素顺序构造一个字典d。

``` python
from random import shuffle
a = [1, 2, 3, 4, 5]
shuffle(a) # 打乱列表a的元素顺序
b = sorted(a, reverse=True) # 对a进行排序得到列表b
d = dict(zip(a, b)) # zip 并行迭代，将两个序列“压缩”到一起，然后返回一个元组列表，最后，转化为字典类型。
print(d)
``` 


### list = ['a','a','a',1,2,3,4,5,'A','B','C']提取出”12345”？
> 解压赋值的知识点

```python
list = ['a','a','a',1,2,3,4,5,'A','B','C']
a,b,c,*middle,d,e,f = list
print(middle)
print(type(middle))
```

### 如何实现tuple和list的转换？

函数tuple(seq)可以把所有可迭代的(iterable)序列转换成一个tuple, 元素不变，排序也不变 ` tuple([1,2,3,4,5]) `
 
函数list(seq)可以把所有的序列和可迭代的对象转换成一个list,元素不变，排序也不变  ` list((1,2,3,4,5)) `


### Python 中的 join() 和 split() 函数？

 * join() 函数可以将指定的字符添加到字符串中
 * split() 函数可以用指定的字符分割字符串
 
a=','.join('123456')
print(a) # 1,2,3,4,5,6
print(type(a)) # <class 'str'>

a='1,2,3,4,5,6'.split(',')
print(a) # ['1', '2', '3', '4', '5', '6']
print(type(a))# <class 'list'>


### 如何删除字符串中的前置空格？

* strip()：把头和尾的空格去掉
* lstrip()：把左边的空格去掉
* rstrip()：把右边的空格去掉
* replace('c1','c2')：把字符串里的c1替换成c2。故可以用replace(' ','')来去掉字符串里的所有空格
* split()：通过指定分隔符对字符串进行切片，如果参数num 有指定值，则仅分隔 num 个子字符串
* re.split(r'\s+', 'a b   c') # 使用正则表达式

### 解释 Python 中的成员运算符？

* **in 是判断是否包含**

` print('me' in 'disappointment') # True
  print('us' in 'disappointment') # False `
 
* **is 是判断内存地址**

is 是判断两个标识符是不是引用自一个对象

is not 是判断两个标识符是不是引用自不同对象

>  in 的 not 在前，is 的 not 在后

### 写一个函数, 输入一个字符串, 返回倒序排列的结果？

```python
# 1 使用字符串本身的翻转
def order_by(str):
    return str[::-1]

# 2 把字符串变为列表，用列表的reverse函数
def reverse2(text='abcdef'):
    new_text=list(text)
    new_text.reverse()
    return ''.join(new_text)
# 3 新建一个列表，从后往前取
def reverse3(text='abcdef'):
    new_text=[]
    for i in range(1,len(text)+1):
        new_text.append(text[-i])
    return ''.join(new_text)


# 4 利用双向列表deque中的extendleft函数
from collections import deque
def reverse4(text='abcdef'):
    d = deque()
    d.extendleft(text)
    return ''.join(d)
```

 
