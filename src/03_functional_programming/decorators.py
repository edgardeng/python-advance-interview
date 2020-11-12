import datetime
import functools
import types
import time


def log(func):
    def wrapper(*args, **kw):
        print('call %s():' % func.__name__)

        return func(*args, **kw)

    wrapper.__name__ = func.__name__  # 目的是把原始函数的__name__等属性复制到wrapper()函数
    return wrapper


@log
def now():
    print('now is running')


def log2(text):  # 三层嵌套的装饰器
    def decorator(func):
        @functools.wraps(func)  # 不需要编写wrapper.__name__ = func.__name__这样的代码，Python内置的functools.wraps就是干这个事
        def wrapper(*args, **kw):
            print('%s %s():' % (text, func.__name__))
            return func(*args, **kw)

        return wrapper

    return decorator


@log2('log.txt')
def now2():
    print('now is running')


def time_recorder(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        rt = f(*args, **kwargs)
        execution_time = time.perf_counter() - start
        print(f"The execution time of {f.__name__!r} is {execution_time:.3f} secs")
        return rt

    return wrapper


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

    @classmethod
    def func_2(cls):
        time.sleep(2)

    @staticmethod
    def func_3():
        time.sleep(3)


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


class CallRecord:
    """
    使用类做装饰器
    """

    CALLINFOS = {}

    # @functools.wraps # 不能使用 __init__  should return None, not 'function'
    def __init__(self,  func):
        functools.update_wrapper(self, func)
        self.func = func

    def __call__(self, *args, **kwargs):
        CallRecord.CALLINFOS[self.func.__name__] = str(datetime.datetime.now())
        print(CallRecord.CALLINFOS)
        return self.func(*args, **kwargs)


@CallRecord
def cls_foo():
    print(sum([1, 2, 3, 4, 5]))


@CallRecord
def cls_test():
    print('hello world')

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


if __name__ == '__main__':
    print('now name:', now.__name__)
    now()
    print('now2 name:', now2.__name__)
    now2()
    T().func_1()
    print(id( SingleT()),id( SingleT()))
    print(cls_foo, cls_foo.__name__)
    cls_test()
