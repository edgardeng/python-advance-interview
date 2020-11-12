## 高阶函数 Higher-order function

### 1. 变量可以指向函数
以Python内置的求绝对值的函数abs()为例，调用该函数用以下代码：

```python
 abs(-10) # 10
 abs # <built-in function abs>
 f = abs
 f(-10) # 10
```

1. 函数本身也可以赋值给变量，即：变量可以指向函数。

2. 如果一个变量指向了一个函数，可以通过该变量来调用这个函数

### 函数名也是变量

对于abs()这个函数，完全可以把函数名abs看成变量，它指向一个可以计算绝对值的函数！

```
 abs = 10
 abs(-10) # Traceback (most recent call last): TypeError: 'int' object is not callable
 # 把abs指向10后，就无法通过abs(-10)调用该函数了！因为abs这个变量已经不指向求绝对值函数 
```
> 注：由于abs函数实际上是定义在__builtin__模块中的，所以要让修改abs变量的指向在其它模块也生效，要用__builtin__.abs = 10。

### 传入函数
既然变量可以指向函数，函数的参数能接收变量

一个函数就可以接收另一个函数作为参数，这种函数就称之为**高阶函数**。

```python
def add(x, y, f):
    return f(x) + f(y)
# add(-5, 6, abs) # f(x) + f(y) ==> abs(-5) + abs(6) ==> 11
```
 

### map

### reduce

### filter

### sorted

