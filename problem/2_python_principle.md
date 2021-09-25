## 一、Python 原理

### 1. Python中的GIL是什么？

 python多线程有个全局解释器锁（global interpreter lock），简称GIL，这个GIL并不是python的特性，他是只在Cpython解释器里引入的一个概念，而在其他的语言编写的解释器里就没有这个GIL例如：Jython。

 因为Python的执行依赖于解释器。Python最初的设计理念在于，为了解决多线程之间数据完整性和状态同步的问题，设计为在任意时刻只有一个线程在解释器中运行。而当执行多线程程序时，由GIL来控制同一时刻只有一个线程能够运行。即Python中的多线程是表面多线程，也可以理解为fake多线程，不是真正的多线程。


 任一时间只能有一个线程运用解释器，跟单cpu跑多个程序一个意思，我们都是轮着用的，这叫“并发”，不是“并行”。
 
 为什么会有GIL？
 多核CPU的出现，充分利用多核，采用多线程编程慢慢普及，难点就是线程之间数据的一致性和状态同步
 
 如何避免受到GIL的影响
 
 说了那么多，如果不说解决方案就仅仅是个科普帖，然并卵。GIL这么烂，有没有办法绕过呢？我们来看看有哪些现成的方案。
 
 用multiprocess替代Thread
 
 multiprocess库的出现很大程度上是为了弥补thread库因为GIL而低效的缺陷。它完整的复制了一套thread所提供的接口方便迁移。唯一的不同就是它使用了多进程而不是多线程。每个进程有自己的独立的GIL，因此也不会出现进程之间的GIL争抢。
 
 
 Python GIL其实是功能和性能之间权衡后的产物，它尤其存在的合理性，也有较难改变的客观因素：

* 因为GIL的存在，只有IO Bound场景下得多线程会得到较好的性能
* 如果对并行计算性能较高的程序可以考虑把核心部分也成C模块，或者索性用其他语言实现
* 在Python编程中，如果想利用计算机的多核提高程序执行效率，用多进程代替多线程
* 对于非原子操作，在Python进行多线程编程时也需要使用互斥锁（如thread中的lock）保证线程安全。
* GIL在较长一段时间内将会继续存在，但是会不断对其进行改进


### 2. Python中的多进程和多线程使用场景

**线程**
线程是操作系统能够进行运算调度的 最小单位 。它被包含在进程之中，是进程中的实际运作单位。

一条线程指的是进程中一个单一顺序的控制流，一个进程中可以并发多个线程，每条线程并行执行不同的任务。

一个线程是一个execution context（执行上下文），即一个cpu执行时所需要的一串指令。

**进程**

一个程序的 执行实例 就是一个进程。每一个进程提供执行程序所需的所有资源。（进程本质上是资源的集合）

一个进程有一个虚拟的地址空间、可执行的代码、操作系统的接口、安全的上下文（记录启动该进程的用户和权限等等）、唯一的进程ID、环境变量、优先级类、最小和最大的工作空间（内存空间），还要有 至少一个线程 。

每一个进程启动时都会最先产生一个线程，即主线程 然后主线程会再创建其他的子线程。

**进程与线程区别**

1. 同一个进程中的线程共享同一内存空间，但是进程之间是独立的。
2. 同一个进程中的所有线程的数据是共享的（进程通讯），进程之间的数据是独立的。
3. 对主线程的修改可能会影响其他线程的行为，但是父进程的修改（除了删除以外）不会影响其他子进程。
4. 线程是一个上下文的执行指令，而进程则是与运算相关的一簇资源。
5. 同一个进程的线程之间可以直接通信，但是进程之间的交流需要借助中间代理来实现。
6. 创建新的线程很容易，但是创建新的进程需要对父进程做一次复制。
7. 一个线程可以操作同一进程的其他线程，但是进程只能操作其子进程。
8. 线程启动速度快，进程启动速度慢（但是两者运行速度没有可比性）。 

**哪些情况适合用多线程呢：**
 
 只要在进行耗时的IO操作的时候，能释放GIL，所以只要在IO密集型的代码里，用多线程就很合适
 
 哪些情况适合用多进程呢：
 
 用于计算密集型，比如计算某一个文件夹的大小
 
### 是否了解线程的同步和异步？

线程同步：多个线程同时访问同一资源，等待资源访问结束，浪费时间，效率低

例子:你说完，我再说。

线程异步：在访问资源时在空闲等待时同时访问其他资源，实现多线程机制

你喊朋友吃饭，朋友说知道了，待会忙完去找你 ，你就去做别的了。

### 3. 简单介绍一下python函数式编程？

在函数式编程中，函数是基本单位，变量只是一个名称，而不是一个存储单元。

除了匿名函数外，Python还使用fliter(),map(),reduce(),apply()函数来支持函数式编程。

围绕 fliter(), map(), reduce() .apply() 来介绍


### 4.  python中函数装饰器有什么作用？
> 装饰器本质上是一个Python函数，可以让其他函数在不需要做任何代码变动的前提下增加额外功能，装饰器的返回值也是一个函数对象。

经常用于有切面需求的场景，比如：插入日志、性能测试、事务处理、缓存、权限校验等场景。

有了装饰器，就可以抽离出大量与函数功能本身无关的雷同代码并继续重用。
 
### 5. python下多线程的限制以及多进程中传递参数的方式？

 python多线程有个全局解释器锁（global interpreter lock），简称GIL，这个GIL并不是python的特性，他是只在Cpython解释器里引入的一个概念，而在其他的语言编写的解释器里就没有这个GIL例如：Jython。

 这个锁的意思是任一时间只能有一个线程运用解释器，跟单cpu跑多个程序一个意思，我们都是轮着用的，这叫“并发”，不是“并行”。
 
 为什么会有GIL？
 多核CPU的出现，充分利用多核，采用多线程编程慢慢普及，难点就是线程之间数据的一致性和状态同步
 说到GIL解释器锁，我们容易想到在多线程中共享全局变量的时候会有线程对全局变量进行的资源竞争，会对全局变量的修改产生不是我们想要的结果，而那个时候我们用到的是python中线程模块里面的互斥锁，哪样的话每次对全局变量进行操作的时候，只有一个线程能够拿到这个全局变量；看下面的代码：
```python
import threading
 global_num = 0
 
 def test1():
     global global_num
     for i in range(1000000):
         global_num += 1
 
     print("test1", global_num)
 
 
 def test2():
     global global_num
     for i in range(1000000):
         global_num += 1
 
     print("test2", global_num)
 
 t1 = threading.Thread(target=test1)
 t2 = threading.Thread(target=test2)
 t1.start()
 t2.start()
```
 
 加入互斥锁
 ```python
 import threading
 import time
 global_num = 0
 
 lock = threading.Lock()
 
 def test1():
     global global_num
     lock.acquire()
     for i in range(1000000):
         global_num += 1
     lock.release()
     print("test1", global_num)
 
 
 def test2():
     global global_num
     lock.acquire()
     for i in range(1000000):
         global_num += 1
     lock.release()
     print("test2", global_num)
 
 t1 = threading.Thread(target=test1)
 t2 = threading.Thread(target=test2)
 start_time = time.time()
 
 t1.start()
 t2.start()
  ```



### 请描述 方法重载与方法重写？
* 方法重载
 > 是在一个类里面，方法名字相同，而参数不同。返回类型可以相同也可以不同。
重载是让类以统一的方式处理不同类型数据的一种手段。

* 方法重写
 > 子类不想原封不动地继承父类的方法，而是想作一定的修改，这就需要采用方法的重写。方法重写又称方法覆盖。


### 如何提高Python 程序的运行性能？

* 使用多进程，充分利用机器的多核性能
* 对于性能影响较大的部分代码，可以使用 C 或 C++编写
* 对于 IO 阻塞造成的性能影响，可以使用 IO 多路复用来解决
* 尽量使用 Python 的内建函数
* 尽量使用局部变量

### 如何提高python的运行效率？

1. 数据结构一定要选对,能用字典就不用列表：字典在索引查找和排序方面远远高于列表。
2. 多用python中封装好的模块库,关键代码使用外部功能包（Cython，pylnlne，pypy，pyrex）
3. 使用生成器
4. 针对循环的优化, 尽量避免在循环中访问变量的属性
5. 使用较新的Python版本
 
###   Python 中的作用域？
简记为 LEGB

* 本地作用域(Local)
* 当前作用域被嵌入的本地作用域(Enclosing locals)
* 全局/模块作用域(Global)
* 内置作用域(Built-in)。

### 如何理解 Python 中字符串中的\字符？

* 转义字符 \n \t
* 路径名中用来连接路径名  c:\abc\def
* 编写太长代码手动软换行

###  为什么函数名字可以当做参数用?
Python 中一切皆对象，函数名是函数在内存中的空间，也是一个对象。

###   Python字典有什么特点，从字典中取值，时间复杂度是多少？
> dict（字典）是另一种可变容器模型，且可存储任意类型对象。
 
字典的特性

1. 查找速度快
    无论dict有10个元素还是10万个元素，查找速度都一样。而list的查找速度随着元素增加而逐渐下降。
    不过dict的查找速度快不是没有代价的，dict的缺点是占用内存大，还会浪费很多内容，list正好相反，占用内存小，但是查找速度慢。
2. 字典值可以没有限制地取任何python对象，既可以是标准的对象，也可以是用户定义的，但键不行。
    不允许同一个键出现两次。键必须不可变，所以可以用数字，字符串或元组充当，所以用列表就不行。
3. dict的第二个特点就是存储的key-value序对是没有顺序的！

从字典中取值，时间复杂度是 O(1)，字典是hash table实现

### 说一说Python自省？
**自省** 就是面向对象的语言所写的程序在运行时，能够知道对象的类型。(运行时能够获知对象的类型)

例如python, buby, object-C, c++都有自省的能力，这里面的c++的自省的能力最弱，只能够知道是什么类型，而像python可以知道是什么类型，还有什么属性。

Python中比较常见的自省（introspection）机制(函数用法)有： dir()，type(), hasattr(), isinstance()，通过这些函数，我们能够在程序运行时得知对象的类型，判断对象是否存在某个属性，访问对象的属性。

 * dir() 函数 返回传递给它的任何对象的属性名称经过排序的列表。如果不指定对象，则 dir() 返回当前作用域中的名称。
 * type() 函数有助于我们确定对象是字符串还是整数，或是其它类型的对象。
 * 对象拥有属性，并且 dir() 函数会返回这些属性的列表。但是，有时我们只想测试一个或多个属性是否存在。如果对象具有我们正在考虑的属性，那么通常希望只检索该属性。这个任务可以由 hasattr() 和 getattr() 函数来完成。
 * isinstance() 函数测试对象，以确定它是否是某个特定类型或定制类的实例。

### 什么是python猴子补丁python monkey patch？
> 在运行时动态修改已有的代码，而不需要修改原始代码。

在Python中，术语monkey补丁仅指run-time上的类或模块的动态修改
```
class A:
  def func(self):
    print("Hi")
def monkey(self):
  print("Hi, monkey")
A.func = monkey
a = A()
a.func() # Hi, monkey
```


### is 和 == 的区别？

> python中对象包含的三个基本要素，分别是：id(身份标识)、type(数据类型)和value(值) . 身份标识id ，就是在内存中的地址

```python
a = 'hello'
b = 'hello'
print(a is b)  # True

print(a == b) # True
a = 'hello world'
b = 'hello world'
print(a is b) # False
print(a == b) # True
a = [1,2,3]
b = [1,2,3]
print(a is b) # False
print(a == b) # True
a = [1,2,3]
b = a
print(a is b) # True
print(a == b) # True

```

* == 是python标准操作符中的比较操作符，用来比较判断两个对象的value(值)是否相等 
     实际是调用了对象 a 的 __eq()__ 方法，a == b 相当于 a.__eq__(b)。
     
* is 也被叫做同一性运算符（对象标示符），这个运算符比较判断的是对象间的唯一身份标识，
     也就是id（内存中的地址）是否相同  相当于检查 id(a) == id(b)

**为什么 a 和 b 都是 "hello" 的时候，a is b 返回True，而 a 和 b都是 "hello world" 的时候，a is b 返回False呢？**

因为前一种情况下Python的字符串驻留机制起了作用。对于较小的字符串，为了提高系统性能Python会保留其值的一个副本，当创建新的字符串的时候直接指向该副本即可。

所以 "hello" 在内存中只有一个副本，a 和 b 的 id 值相同，而 "hello world" 是长字符串，不驻留内存，Python中各自创建了对象来表示 a 和 b，所以他们的值相同但 id 值不同。

试一下当a=247,b=247时它们的id还是否会相等。事实上Python 为了优化速度，使用了小整数对象池，避免为整数频繁申请和销毁内存空间。而Python 对小整数的定义是 [-5, 257)，只有数字在-5到256之间它们的id才会相等，超过了这个范围就不行了。

```
a = 247
b = 247
print(a is b) # True

a = 258
b = 258
print(a is b) # False
```
 
### 列表和元组有什么不同？
**列表和元组的相同点：**

* 都是序列
* 都可以存储任何数据类型
* 可以通过索引访问

**列表和元组的不同点：**
 * 语法差异
    > 使用方括号[]创建列表，而使用括号()创建元组。
 * 是否可变
    > 列表是可变的，而元组是不可变的，这标志着两者之间的关键差异。
 * 重用与拷贝
    > 元组无法复制。 因为元组是不可变的，所以运行tuple(tuple_name)将返回自己
 * 内存开销
    >Python将低开销的较大的块分配给元组，因为它们是不可变的。
    列表则分配小内存块。与列表相比，元组的内存更小。 
    当你拥有大量元素时，元组比列表快。列表的长度是可变的。
           >
### 什么是负索引？
> Python中的序列索引可以是正也可以是负
如果是正索引，0是序列中的第一个索引，1是第二个索引。
如果是负索引，-1是最后一个索引，-2是倒数第二个索引。

```python
lst=[11,22,33,44,55]
lst[:] # [11, 22, 33, 44, 55]全取列表
lst[:-1] # [11, 22, 33, 44] 码取不到最后一个元素
lst[::-1] # [55, 44, 33, 22, 11] 列表倒序
lst[-1] # 55 取最后一个
```


### 迭代器、可迭代对象、生成器？

1. 什么是迭代
 > 对list、tuple、str等类型的数据使用for...in...的循环语法从其中依次拿到数据进行使用，我们把这样的过程称为遍历，也叫迭代。

假如自己写了一个数据类型，希望这个数据类型里的东西也可以使用for被一个一个的取出来，那我们就必须满足for的要求.

这个要求就叫做 协议 - 可迭代协议。

可迭代协议的定义非常简单，就是内部实现了__iter()__方法

如果某个对象中有_ iter _()方法，这个对象就是可迭代对象 （Iterable） ` if '__iter__' in dir(str) `
 
通俗易懂 ：可以被for循环迭代的对象就是可迭代对象。

从代码上面可以使用isinstance()判断一个对象是否是Iterable对象

```
from collections import Iterable

a = isinstance([], Iterable)
b = isinstance({}, Iterable)
c = isinstance('abc', Iterable)
d = isinstance((x for x in range(10)), Iterable)
e = isinstance(100, Iterable)  # False
``` 
只有最后的数字不是可迭代对象

可迭代对象的本质: 每迭代一次（即在for...in...中每循环一次）都会返回对象中的下一条数据，一直向后读取数据直到迭代了所有数据后结束。
 
能帮助我们进行数据迭代的“人”称为迭代器(Iterator)

可迭代对象通过__iter__方法向我们提供一个迭代器，在迭代一个可迭代对象的时候，实际上就是先获取该对象提供的一个迭代器，然后通过这个迭代器来依次获取对象中的每一个数据。

综上所述，一个具备了__iter__方法的对象，就是一个可迭代对象。

```python
class MyList(object):
    def __init__(self):
        self.container = []
    def add(self, item):
        self.container.append(item)
    def __iter__(self):
        """返回一个迭代器"""
        # 我们暂时忽略如何构造一个迭代器对象
        pass
    
mylist = MyList()
from collections import Iterable
isinstance(mylist, Iterable)
```

**iter()函数与next()函数**
通过iter()函数获取这些可迭代对象的迭代器。
使用next()函数来获取下一条数据。
iter()函数实际上就是调用了可迭代对象的__iter__方法。

i = iter('spam')
next(i) # 's'
next(i) # 'p'
next(i) # 'a'
next(i) # ' m'
next(i) # 当序列遍历完时，将抛出一个StopIteration异常

**迭代器Iterator**
迭代器是用来帮助我们记录每次迭代访问到的位置，当我们对迭代器使用next()函数的时候，迭代器会向我们返回它所记录位置的下一个位置的数据。

实际上，在使用next()函数的时候，调用的就是迭代器对象的__next__方法（Python3中是对象的__next__方法，Python2中是对象的next()方法）。

一个实现了__iter__方法和__next__方法的对象，就是迭代器
```
class MyList(object):
    """自定义的一个可迭代对象"""
    def __init__(self):
        self.items = []
 
    def add(self, val):
        self.items.append(val)
 
    def __iter__(self):
        myiterator = MyIterator(self)
        return myiterator
 
class MyIterator(object):
    """自定义的供上面可迭代对象使用的一个迭代器"""
    def __init__(self, mylist):
        self.mylist = mylist
        # current用来记录当前访问到的位置
        self.current = 0
 
    def __next__(self):
        if self.current < len(self.mylist.items):
            item = self.mylist.items[self.current]
            self.current += 1
            return item
        else:
            raise StopIteration
 
    def __iter__(self):
        return self
 
 
if __name__ == '__main__':
    mylist = MyList()
    mylist.add(1)
    mylist.add(2)
    mylist.add(3)
    mylist.add(4)
    mylist.add(5)
    for num in mylist:
        print(num)

```

[参考](https://blog.csdn.net/weixin_42225318/article/details/81274348)

可迭代对象与迭代器

1. 可迭代对象包含迭代器。
2. 如果一个对象拥有__iter__方法，那么它是可迭代对象；如果一个对象拥有next方法，其是迭代器。
3. 定义可迭代对象，必须实现__iter__方法；定义迭代器，必须实现__iter__和next方法。

生成器

1. 生成器是一种特殊的迭代器，生成器自动实现了“迭代器协议”（即__iter__和next方法），不需要再手动实现两方法。
2. 生成器在迭代的过程中可以改变当前迭代值，而修改普通迭代器的当前迭代值往往会发生异常，影响程序的执行。
3. 具有yield关键字的函数都是生成器，yield可以理解为return，返回后面的值给调用者。不同的是return返回后，函数会释放，而生成器则不会。在直接调用next方法或用for语句进行下一次迭代时，生成器会从yield下一句开始执行，直至遇到下一个yield。

### Python是如何进行内存管理的？

**对象的引用计数机制**: Python内部使用引用计数，来保持追踪内存中的对象，所有对象都有引用计数。

* 引用计数增加的情况：
 * 对象被创建：x='spam'
 * 另外的别人被创建：y=x
 * 被作为参数传递给函数：foo(x)
 * 作为容器对象的一个元素：a=[1,x,'33']

* 引用计数减少情况

 * 一个本地引用离开了它的作用域。比如上面的foo(x)函数结束时，x指向的对象引用减1。
 * 对象的别名被显式的销毁：del x ；或者del y
 * 对象的一个别名被赋值给其他对象：x=789
 * 对象从一个窗口对象中移除：myList.remove(x)
 * 窗口对象本身被销毁：del myList，或者窗口对象本身离开了作用域。

**垃圾回收**

 1. 当内存中有不再使用的部分时，垃圾收集器就会把他们清理掉。它会去检查那些引用计数为0的对象，然后清除其在内存的空间。当然除了引用计数为0的会被清除，还有一种情况也会被垃圾收集器清掉：当两个对象相互引用时，他们本身其他的引用已经为0了。
 2. 循环垃圾回收器, 确保释放循环引用对象(a引用b, b引用a, 导致其引用计数永远不为0)。

在Python中，许多时候申请的内存都是小块的内存，这些小块内存在申请后，很快又会被释放，由于这些内存的申请并不是为了创建对象，所以并没有对象一级的内存池机制。这就意味着Python在运行期间会大量地执行malloc和free的操作，频繁地在用户态和核心态之间进行切换，这将严重影响Python的执行效率。

为了加速Python的执行效率，Python引入了一个内存池机制，用于管理对小块内存的申请和释放。

**内存池机制**

 1. Python提供了对内存的垃圾收集机制，但是它将不用的内存放到内存池而不是返回给操作系统；
 2. Pymalloc机制：为了加速Python的执行效率，Python引入了一个内存池机制，用于管理对小块内存的申请和释放；
 3. 对于Python对象，如整数，浮点数和List，都有其独立的私有内存池，对象间不共享他们的内存池。也就是说如果你分配又释放了大量的整数，用于缓存这些整数的内存就不能再分配给浮点数。

### 继承

类继承，只要通过__class__方法指定类对象就可以了。 

方法对象，为了能让对象实例能被直接调用，需要实现__call__方法

**python多继承的MRO顺序：多继承查找规则**
 
MRO是一个有序列表L，在类被创建时就计算出来。
通用计算公式为：
```
mro(Child(Base1，Base2)) = [ Child ] + merge( mro(Base1), mro(Base2),  [ Base1, Base2] )
（其中Child继承自Base1, Base2）
```

如果继承至多个基类：class B(A1, A2, A3 …)
这时B的mro序列
```
mro(B)  = mro( B(A1, A2, A3 …) )
= [B] + merge( mro(A1), mro(A2), mro(A3) ..., [A1, A2, A3] )
= ...
```
使用 __mro__函数获取搜索列表