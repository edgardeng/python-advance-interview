## 魔法函数
　　
> Python内置的以双下划线开头并以双下划线结尾的函数（不能自己定义，没有用），如__init__(),等很多，用于实现并定制很多特性，非常灵活，且是隐式调用的。

### Python的数据模型以及数据模型对Python的影响
　　
  * 魔法函数会直接影响到Python语法本身，如让类变成可迭代的对象，
  * 也会影响Python的一些内置函数的调用，如实现__len__()能对对象调用len()方法。

### 说明魔法函数的重要性（举例len()）
　　　
  如果len()方法调用的对象是Python内置的类型，如list，set，dict（cpython）等，会直接获取（有一个数据表示长度），而不用去遍历。

### 魔法函数一览

 1. 非数学运算：
 
    * 字符串表示：\__repr__，\__str__ 定制字符串格式化 \__repr__类似，但是是开发模式下
    * 集合序列相关：__len__，__getitem__，__setitem__，__delitem__，__contains__
    * 迭代相关：__iter__,__next__
    * 可调用：__call__
    * with上下文管理器：__enter__,__exit__
    * 数值转换：__abs__,__bool__,__int__,__float__,__hash__,__index__
    * 元类相关：__new__,__init__
    * 属性相关：__getattr__、 __setattr__,__getattribute__、setattribute__,__dir__
    * 属性描述符：__get__、__set__、 __delete__
    * 协程：__await__、__aiter__、__anext__、__aenter__、__aexit__
    
 2. 数学运算：
    *  一元运算符：__neg__（-）、__pos__（+）、__abs__ 
    *  二元运算符：__lt__(<)、 __le__ <= 、 __eq__ == 、 __ne__ != 、 __gt__ > 、 __ge__ >=
    *  算术运算符：__add__ + 、 __sub__ - 、 __mul__ * 、 __truediv__ / 、 __floordiv__ // 、 __mod__ % 、 __divmod__ divmod() 、 __pow__ ** 或 pow() 、 __round__ round()
    *  反向算术运算符：__radd__ 、 __rsub__ 、 __rmul__ 、 __rtruediv__ 、 __rfloordiv__ 、 __rmod__ 、__rdivmod__ 、 __rpow__
    *  增量赋值算术运算符：__iadd__ 、 __isub__ 、 __imul__ 、 __itruediv__ 、 __ifloordiv__ 、 __imod__ 、__ipow__
    *  位运算符：__invert__ ~ 、 __lshift__ << 、 __rshift__ >> 、 __and__ & 、 __or__ | 、 __xor__ ^
    *  反向位运算符：__rlshift__ 、 __rrshift__ 、 __rand__ 、 __rxor__ 、 __ror__
    *  增量赋值位运算符：__ilshift__ 、 __irshift__ 、 __iand__ 、 __ixor__ 、 __ior__

### 常用的魔法函数

* __getitem__ 把类变成一个可迭代的对象（一次一次取数据，直到抛异常）：

```python

```

