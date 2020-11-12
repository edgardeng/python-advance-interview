# Python 函数

> Python不但能非常灵活地定义函数，而且本身内置了很多有用的函数，可以直接调用

## 基础函数

### 函数的调用

```python
abs(100) 
abs(1, 2)  #  TypeError: abs() takes exactly one argument (2 given)
abs('a')   # TypeError: bad operand type for abs(): 'str'
a = abs
a(1)
```
1. 调用一个函数，需要知道函数的名称和参数
 >  如果传入的参数数量不对，会报TypeError的错误
 >  参数类型不能被函数所接受，也会报TypeError的错误

2. 函数名其实就是指向一个函数对象的引用，完全可以把函数名赋给一个变量，相当于给这个函数起了一个“别名”


### 函数的定义

```python
def my_abs(x):
    if not isinstance(x, (int, float)): # 适当地做参数检查是有必要的
        raise TypeError('bad operand type')
    if x >= 0:
        return x
    else:
        return -x
```

1. 定义一个函数要使用def语句，依次写出函数名、括号、括号中的参数和冒号:
2. 在缩进块中编写函数体，函数的返回值用return语句返回

#### 空函数

定义一个什么事也不做的空函数，可以用pass语句：

```python
def nop():
    pass
```
#### 返回多个值
> 返回值是一个tuple 而多个变量可以同时接收一个tuple，按位置赋给对应的值

```python
def move(x, y, step):
    nx = x + step
    ny = y - step 
    return nx, ny
x,y = move(1,1,2)
r = move(x,y,2)
```

### [函数参数](./02_function/function_parameter.md)

### 递归函数
> 如果一个函数在内部调用自身本身，这个函数就是递归函数。

举个例子，我们来计算阶乘
```python
def fact(n):
    if n==1:
        return 1
    return n * fact(n - 1)
fact(1)
fact(100)
```
递归函数的优点是定义简单，逻辑清晰

理论上，所有的递归函数都可以写成循环的方式，但循环的逻辑不如递归清晰。

#### 使用递归函数需要注意防止栈溢出。
在计算机中，函数调用是通过栈（stack）这种数据结构实现的，每当进入一个函数调用，栈就会加一层栈帧，每当函数返回，栈就会减一层栈帧。
由于栈的大小不是无限的，所以，递归调用的次数过多，会导致栈溢出。

```python
fact(1000)
# Traceback (most recent call last):
#  File "<stdin>", line 1, in <module>
#  File "<stdin>", line 4, in fact
#  ...
#  File "<stdin>", line 4, in fact
# RuntimeError: maximum recursion depth exceeded
```

> Python确实有递归次数限制，默认最大次数为1000. 但可以通过设置修改最大递归次数
 `import sys
  sys.setrecursionlimit(1500) `
 
解决递归调用栈溢出的方法是通过尾递归优化，事实上尾递归和循环的效果是一样的，所以，把循环看成是一种特殊的尾递归函数也是可以的。

尾递归是指，在函数返回的时候，调用自身本身，并且，return语句不能包含表达式

编译器或者解释器就可以把尾递归做优化，使递归本身无论调用多少次，都只占用一个栈帧，不会出现栈溢出的情况。

上面的fact(n)函数由于return n * fact(n - 1)引入了乘法表达式，所以就不是尾递归了。要改成尾递归方式，需要多一点代码，主要是要把每一步的乘积传入到递归函数中：

```python
def fact(n):
    return fact_iter(n, 1)

def fact_iter(num, product):
    if num == 1:
        return product
    return fact_iter(num - 1, num * product)
```

> 大多数编程语言没有针对尾递归做优化，Python解释器也没有做优化，所以，即使把上面的fact(n)函数改成尾递归方式，也会导致栈溢出。
