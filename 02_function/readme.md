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

### [函数的参数](f)

