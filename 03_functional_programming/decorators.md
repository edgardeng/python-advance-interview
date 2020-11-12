## 装饰器

要增强函数的功能，又不希望修改函数的定义，在代码运行期间动态增加功能的方式，称之为“装饰器”（Decorator）

装饰器的案例：
  * 日志记录
  * 调用跟踪管理
  * 参数验证、
  *  在 Web 应用中进行登录验证或路由注册
  * 在事件驱动系统中进行回调注册
  * 线程锁的获取和释放
  * 性能优化中记录任务执行时间等

### 函数装饰器

本质上，decorator就是一个返回函数的高阶函数

```python
def log(func):
    def wrapper(*args, **kw):
        print('call %s():' % func.__name__)
        return func(*args, **kw)
    return wrapper

@log
def now():
    print('now is running')
 now.__name__
'wrapper'

```
调用now()函数，不仅会运行now()函数本身，还会在运行now()函数前打印一行日志
> 把@log放到now()函数的定义处，相当于执行了语句： `now = log(now)`

如果decorator本身需要传入参数，那就需要编写一个返回decorator的高阶函数，写出来会更复杂。比如，要自定义log的文本：

```python
def log(text):
    def decorator(func):
        def wrapper(*args, **kw):
            print('%s %s():' % (text, func.__name__))
            return func(*args, **kw)
        return wrapper
    return decorator
```

和两层嵌套的decorator相比，3层嵌套的效果是这样的： `now = log('execute')(now)`

### 类装饰器
> 类装饰器通常用于拦截实例的创建，在实例创建的过程中插入额外的逻辑，从而扩展实例的功能

例子，类装饰器给每个方法加上装饰器
```python
def time_recorder_for_kls(cls):
    class Wrapper(object):
        def __init__(self, *args, **kwargs):
            self.instance = cls(*args, **kwargs)

        def __getattribute__(self, attr):
            try:
                ar = super().__getattribute__(attr)
            except AttributeError:
                pass
            else:
                return ar
            f = self.instance.__getattribute__(attr)
            if isinstance(f, (types.MethodType, types.FunctionType)):
                return time_recorder(f)
            else:
                return f
    return Wrapper

@time_recorder_for_kls
class T:
    def func_1(self):
        time.sleep(1)
```

在 Python 3.7 中，标准库提供了 dataclasses 数据类，作为一种常用的类装饰器，它主要用于自动添加一些特殊方法，比如 __init__() 等

一个常见的示例，使用类装饰器编写单例类
```python
def singleton(cls):
    @functools.wraps(cls)
    def wrapper(*args, **kwargs):
        if not wrapper.obj:
            wrapper.obj = cls(*args, **kwargs)
        return wrapper.obj
    wrapper.obj = None
    return wrapper


@singleton
class SingleT:
    pass
```


    
### 装饰器的发展

1. 在 Python 2.4 中，添加了针对函数及方法的装饰器语法（ PEP 318 – Decorators for Functions and Methods ）
```python
@classmethod
@output_serialization
def foo(self):
    pass
```

2. 在 Python 2.6 和 3.0 中，又进一步添加了针对类的装饰器语法（ PEP 3129 – Class Decorators ）

```python
class A:
  pass
A = foo(bar(A))

@foo
@bar
class A:
  pass
```

3. 目前Python内置多种装饰器: @classmethod、@staticmethod、@property 等，
   在基础库，如 functools 模块中的 @cached_property、@lru_cache、@singledispatch、@wraps

### 类编写装饰器
使用类或者函数和类的组合等方式来编写。使用类编写装饰器的典型模式是实现 __init__() 和 __call__() 方法

```python
class CallRecord:
    """
    使用类做装饰器
    """

    CALLINFOS = {}

    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func

    def __call__(self, *args, **kwargs):
        CallRecord.CALLINFOS[self.func.__name__] = str(datetime.datetime.now())
        print(CallRecord.CALLINFOS)
        return self.func(*args, **kwargs)


@CallRecord
def foo():
    print(sum([1, 2, 3, 4, 5]))


@CallRecord
def test():
    print('hello world')
```
    
使用类编写装饰器的缺点

```python
class T:
    @CallRecord
    def m(self, a, b):
        pass
T().m(1, 2) # TypeError: m() missing 1 required positional argument: 'b'
```
self 参数接收的是 CallRecord 实例，并不会像 m(self, a, b) 方法那样接收 T 实例，并且 T 实例也不会被包含在 __call__() 方法的 args 变长参数中，这就导致了我们在装饰器生成的 CallRecord 实例中，无法将 T 实例传递给 m 方法


### 装饰器嵌套

```python
@time_recorder
@register
def test():
    time.sleep(1)
    print('hello world!')
```
在嵌套的装饰器结构中，前一个装饰器所返回的可调用对象会成为后一个装饰器所装饰的对象，最后一个装饰器所返回的可调用对象会和被装饰对象的名称进行重新绑定

### 装饰器参数

```python
permissions = []
def permission_verification(permission_type):
    def decorator(view):
        @functools.wraps(view)
        def wrapped_view(*args, **kwargs):
            if permission_type in permissions:
                return view(*args, **kwargs)
            raise Exception("Permission not allowed!")
            return wrapped_view
    return decorator

@permission_verification('is_superuser')
def foo():
    pass
```
装饰器参数的示例中，可包含了三个层次，分别称为装饰器参数接收层、装饰器层、可调用对象返回层


### functools.wraps

被装饰函数的原有名称可能会被绑定至另外的可调用对象上，从而使得原有名称所引用对象的类型、帮助信息等重要信息发生变化

如何解决这个问题呢？最方便的方式便是通过 `@functools.wraps` ，它会将一个函数中的关键帮助信息赋值到另外一个函数上

### functools.update_wrapper

functools.update_wrapper() 的具体形式是functools.update_wrapper(wrapper, wrapped, assigned=WRAPPER_ASSIGNMENTS, updated=WRAPPER_UPDATES)

它的作用, 会更新 wrapper 函数使其类似于 wrapped 函数，位于参数列表中的可选参数用于指定原函数的哪些属性要直接赋值至 wrapper 函数中的相关属性，这些属性包括 __module__、__name__、 __qualname__、__annotations__ 以及文档字符串 __doc__ 等。

对于 functools.update_wrapper() 来说，使用的频率会相对较少一些，常用于使用类编写装饰器
