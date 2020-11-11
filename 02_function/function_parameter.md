## Python 函数参数
> Python的函数定义非常简单，但灵活度却非常大。
> 除了正常定义的必选参数外，还可以使用默认参数、可变参数和关键字参数，使得函数定义出来的接口，不但能处理复杂的参数，还可以简化调用者的代码

### 位置参数

```python
def power(x):
    return x * x

def power(x, n):
    s = 1
    while n > 0:
        n = n - 1
        s = s * x
    return s
```
对于power(x)函数，参数x就是一个位置参数。必须传入有且仅有的一个参数x

power(x, n)函数有两个参数：x和n，这两个参数都是位置参数，调用函数时，传入的两个值按照位置顺序依次赋给参数x和n。

### 默认参数

```python
def power(x, n=2):
    pass
```

设置默认参数时，有几点要注意：

1. 必选参数在前，默认参数在后，否则Python的解释器会报错（思考一下为什么默认参数不能放在必选参数前面）；

2. 如何设置默认参数: 当函数有多个参数时，把变化大的参数放前面，变化小的参数放后面。变化小的参数就可以作为默认参数。

#### 默认参数有个最大的坑

```python 
def add_end(L=[]):
  L.append('END')
  return L
add_end([1, 2, 3]) #  [1, 2, 3, 'END'] 没问题

add_end() # ['END']
add_end() # ['END', 'END'] # 函数似乎每次都“记住了”上次添加了'END'后的list
```

因为默认参数L也是一个变量，它指向对象[]，每次调用该函数，如果改变了L的内容，则下次调用时，默认参数的内容就变了，不再是函数定义时的[]

>  定义默认参数要牢记一点：默认参数必须指向不变对象(str,None)！

### 可变参数
> 可变参数就是传入的参数个数是可变的，可以是1个、2个到任意个，还可以是0个。

```python
def calc(*numbers):
    sum = 0
    for n in numbers:
        sum = sum + n * n
    return sum
```

在参数前面加了一个*号。在函数内部，参数numbers接收到的是一个tuple，因此，函数代码完全不变

**如果已经有一个list或者tuple，要调用一个可变参数怎么办？**

```python
nums = [1, 2, 3]
calc(nums[0], nums[1], nums[2])
calc(*nums) # *nums表示把nums这个list的所有元素作为可变参数
```

### 关键字参数
> 关键字参数允许你传入0个或任意个含参数名的参数，这些关键字参数在函数内部自动组装为一个dict

```python
def person(name, age, **kw):
    print('name:', name, 'age:', age, 'other:', kw)
person('Bob', 35, city='Beijing')
extra = {'city': 'Beijing', 'job': 'Engineer'}
person('Jack', 24, **extra)
```

 把dict转换为关键字参数传进去 

### 命名关键字参数

对于关键字参数，函数的调用者可以传入任意不受限制的关键字参数。至于到底传入了哪些，就需要在函数内部通过kw检查。

和关键字参数**kw不同，命名关键字参数需要一个特殊分隔符*，*后面的参数被视为命名关键字参数

```python
def person(name, age, *, city, job):
    print(name, age, city, job)
person('Jack', 24, city='Beijing', job='Engineer')
```

如果函数定义中已经有了一个可变参数，后面跟着的命名关键字参数就不再需要一个特殊分隔符*了：

```python
def person(name, age, *args, city, job):
    print(name, age, args, city, job)
person('Jack', 24, 'Beijing', 'Engineer') # TypeError: person() takes 2 positional arguments but 4 were given
def person2(name, age, *, city='Beijing', job):
    print(name, age, city, job)
person2('Jack', 24, job='Engineer') 
```

1. 命名关键字参数必须传入参数名，这和位置参数不同。如果没有传入参数名，调用将报错
 
2. 命名关键字参数可以有缺省值 

### 参数组合
> 定义函数，可以用必选参数、默认参数、可变参数、关键字参数和命名关键字参数，这5种参数都可以组合使用。
> 但是请注意，参数定义的顺序必须是：必选参数、默认参数、可变参数、命名关键字参数和关键字参数。

参数组合示例

```python
def f1(a, b, c=0, *args, **kw):
    print('a =', a, 'b =', b, 'c =', c, 'args =', args, 'kw =', kw)

def f2(a, b, c=0, *, d, **kw):
    print('a =', a, 'b =', b, 'c =', c, 'd =', d, 'kw =', kw)

def f3(a, *args, b=2, **kwargs):
    print('a =', a, 'b =', b,  'args =', args, 'kw =', kw)

def f4(a=1, b=2, *args, **kwargs):
     print('a =', a, 'b =', b,  'args =', args, 'kw =', kw)
    # func_a(a=1,b=2, c=3) # 可用
    # func_a(0, 1, 2, 3)# 可用
    # func_a(0, k=4, j=5,b=2)# 可用
    # func_a(0, 1, 2, 3, 4, k=4, j=5)# 可用
#     func_a(1, 0,0,0,  k=4, j=5,b=3) 不可参数b重复了
#     func_a(a=1,2,c=3) 不可以
#     func_a(a=1,b=2,4,c=3)  # 不可以 位置参数不能在关键字参数后面

def f5(a, b, *args, c, **kwargs):  # 可定义 不可用 missing 1 required keyword-only argument: 'c'
    print('a =', a, 'b =', b,  'c =', c,'args =', args, 'kw =', kw)
# def f6(a, **kwargs, *args): # 不可定义

f1(1, 2) # a = 1 b = 2 c = 0 args = () kw = {}
f1(1, 2, c=3) # a = 1 b = 2 c = 3 args = () kw = {}
# f1(1, 2, c=3, 4) # 编译错误 SyntaxError 位置参数不能在关键字参数后面
f1(1, 2, 3, 'a', 'b') # a = 1 b = 2 c = 3 args = ('a', 'b') kw = {}
f1(1, 2, 3, 'a', 'b', x=99) # a = 1 b = 2 c = 3 args = ('a', 'b') kw = {'x': 99}
f2(1, 2, d=99, ext=None) # a = 1 b = 2 c = 0 d = 99 kw = {'ext': None}
f1(1, 2, x=4, y=5,c=99) # a = 1 b = 2 c = 99 args = () kw = {'x': 4, 'y': 5}
f1(1, 2, 3 , x=4, y=5,c=99) # 执行错误 TypeError: f1() got multiple values for argument 'c'

# f3(1, 0, 3, k=4, j=5) # 可以
# f3(1, 0,0,0,  k=4, j=5,b=3)# 可以 参数b重复了
# f3(1,b=2,3) # 不可以



# 通过一个tuple和dict， 调用
args = (1, 2, 3, 4)
kw = {'d': 99, 'x': '#'}
f1(*args, **kw) # a = 1 b = 2 c = 3 args = (4,) kw = {'d': 99, 'x': '#'}

```
 
