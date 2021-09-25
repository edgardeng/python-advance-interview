## 三、Python 的使用

### 1. 请解释一下python的线程锁Lock和Rlock的区别，以及你曾经在项目中是如何使用的？

从原理上来说：在同一线程内，对RLock进行多次acquire()操作，程序不会阻塞。

资源总是有限的，程序运行如果对同一个对象进行操作，则有可能造成资源的争用，甚至导致死锁 也可能导致读写混乱


### 2. 字典、列表查询时的时间复杂度是怎样的？
列表是序列，可以理解为数据结构中的数组，字典可以理解为数据结构中的hashmap，
python中list对象的存储结构采用的是线性表，因此其查询复杂度为O(n)。
而dict对象的存储结构采用的是散列表(hash表)，其在最优情况下查询复杂度为O(1)。

> dict的占用内存稍比list大，会在1.5倍左右

### 3. 是否遇到过python的模块间循环引用的问题，如何避免它?
> 这是代码结构设计的问题，模块依赖和类依赖

如果老是觉得碰到循环引用可能的原因有几点：

 * 可能是模块的分界线划错地方了
 * 可能是把应该在一起的东西硬拆开了
 * 可能是某些职责放错地方了
 * 可能是应该抽象的东西没抽象

总之微观代码规范可能并不能帮到太多，重要的是更宏观的划分模块的经验技巧，推荐uml，脑图，白板等等图形化的工具先梳理清楚整个系统的总体结构和职责分工

采取办法，从设计模式上来规避这个问题，比如:

* 使用 “__all__” 白名单开放接口
* 尽量避免 import

 
### 4. 解释一下python的 and-or 语法
 
 bool and a or b 相当于bool? a: b
 ```
 >>> a = "first"
 >>> b = "second"
 >>> 1 and a or b  # 输出内容为 'first'
 >>> 0 and a or b  # 输出内容为 'second'
```

上述内容你应该可以理解，但是还存在一个问题，请看下面的代码
```
 >>> a = ""
 >>> b = "second"
 >>> 1 and a or b # 输出内容为 'second'
 ```
 
 因为 a 是一个空串，空串在一个布尔环境中被Python看成假值，这个表达式将“失败”，且返回 b 的值。
 
 如果你不将它想象成象 bool ? a : b 一样的语法，而把它看成纯粹的布尔逻辑，这样的话就会得到正确的理解。
 1 是真，a 是假，所以 1 and a 是假。假 or b 是b。
 
 应该将 and-or 技巧封装成一个函数：
 def choose(bool, a, b):
     return (bool and [a] or [b])[0]
 因为 [a] 是一个非空列表，它永远不会为假。甚至 a 是 0 或 ” 或其它假值，列表[a]为真，因为它有一个元素。


### 5 请至少列举5个 PEP8 规范？
 PEP8 规范 官方文档：www.python.org/dev/peps/pe…
 PEP8中文翻译：www.cnblogs.com/ajianbeyour…
 
 * 缩进。4个空格的缩进（编辑器都可以完成此功能），不使用Tap，更不能混合使用Tap和空格。
 * 每行最大长度79，换行可以使用反斜杠，最好使用圆括号。换行点要在操作符的后边敲回车。
 * 类和top-level函数定义之间空两行；类中的方法定义之间空一行；函数内逻辑无关段落之间空一行；其他地方尽量不要再空行。
 * 块注释，在一段代码前增加的注释。在‘#’后加一空格。段落之间以只有‘#’的行间隔
 * 各种右括号前不要加空格。
 * 逗号、冒号、分号前不要加空格。
 * 函数的左括号前不要加空格。
 * 序列的左括号前不要加空格。
 * 操作符左右各加一个空格，不要为了对齐增加空格。
 * 函数默认参数使用的赋值符左右省略空格。
 * 不要将多句语句写在同一行，尽管使用‘；’允许。
 * i- f/for/while语句中，即使执行语句只有一句，也必须另起一行。
 * 类的方法第一个参数必须是self，而静态方法第一个参数必须是cls。


### 在 Python 中，list，tuple，dict，set 有什么区别，主要应用在什么场景？

区别

 * list：链表,有序的数据结构, 通过索引进行查找,使用方括号”[]”;
 * tuple：元组,元组将多样的对象集合到一起,不能修改,通过索引进行查找, 使用括号”()”;
 * dict：字典,字典是一组键(key)和值(value)的组合,通过键(key)进行查找,没有顺序, 使用大括号”{}”;
 * set：集合,无序,元素只出现一次, 自动去重,使用”set([])”

应用场景

 * list：简单的数据集合,可以使用索引;
 * tuple：把一些数据当做一个整体去使用,不能修改;
 * dict：使用键值和值进行关联的数据;
 * set：数据只出现一次,只关心数据是否出现, 不关心其位置。


### python中copy和deepcopy的区别

copy() 函数 浅拷贝 `q=list2.copy()`
 
### Python 程序中中文乱码如何解决？

` #coding:utf-8
  sys.setdefaultencoding('utf-8') `


### Python 列举出一些常用的设计模式？ 
创建型

 * Factory Method（工厂方法）
 * Abstract Factory（抽象工厂）
 * Builder（建造者）
 * Prototype（原型）
 *  * Singleton（单例）

结构型

 * Adapter Class/Object（适配器）
 * Bridge（桥接）
 * Composite（组合）
 * Decorator（装饰）
 * Facade（外观）
 * Flyweight（享元）
 * Proxy（代理）

行为型

 * Interpreter（解释器）
 * Template Method（模板方法）
 * Chain of Responsibility（责任链）
 * Command（命令）
 * Iterator（迭代器）
 * Mediator（中介者）
 * Memento（备忘录）
 * Observer（观察者）
 * State（状态）
 * Strategy（策略）
 * Visitor（访问者）

### Python语言中的模块和包是什么？

**python模块(Module)**

在 Python 中，模块是搭建程序的一种方式。每一个 Python 代码文件都是一个模块，并可以引用其他的模块，比如对象和属性。

表现形式为：写的代码保存为文件。这个文件就是一个模块。abc.py 其中文件名abc为模块名字。
有四种代码类型的模块:

* 使用Python写的程序( .py文件)
* C或C++扩展(已编译为共享库或DLL文件)
* 包(包含多个模块)
* 内建模块(使用C编写并已链接到Python解释器内)

**python包(Package)**
包（Package）就是包含模块文件的目录，目录名称就是包名称，目录中可以包含目录，子目录也是包，但包名称应该包含上一级目录的名称。

Python引入了按目录来组织模块是为了避免模块名冲突，不同包中的模块名可以相同。

注意，每一个包目录下面都会有一个__init__.py的文件，这个文件是必须存在的，否则，Python就把这个目录当成普通目录，而不是一个包。

__init__.py可以是空文件，也可以有Python代码，因为__init__.py本身就是一个模块，而它的模块名就是包名。
 

### docstring是什么？

docstring是一种文档字符串，用于解释构造的作用

在函数、类或方法中将它放在首位来描述其作用。我们用三个单引号或双引号来声明docstring。

获取一个函数的docstring，使用它的_doc_属性

### PYTHONPATH变量是什么？
> Python中一个重要的环境变量,用于在导入模块的时候搜索路径
 
* 路径列表的第一个元素为空字符串,代表的是相对路径下的当前目录
* 由于在导入模块的时候,解释器会按照列表的顺序搜索,直到找到第一个模块,所以优先导入的模块为同一目录下的模块.
* 导入模块时搜索路径的顺序也可以改变.这里分两种情况:
  > 1. 通过sys.path.append(),sys.path.insert()等方法来改变,这种方法当重新启动解释器的时候,原来的设置会失效.
  > 2. 改变PYTHONPATH,这种设置方法永久有效
 
###  Python中的不可变集合（frozenset）是什么？
集合分为两种类型：

* set —— 可变集合。集合中的元素可以动态的增加或删除。
* frozenset —— 不可变集合。集合中的元素不可改变。


###  什么是Python中的连接（concatenation）？
Python中的连接就是将两个序列连在一起，我们使用+运算符完成

###  print input 调用 Python 中底层的什么方法?

**print** 用 sys.stdout.write() 实现

```
import sys
print('hello')     	# hello
sys.stdout.write('hello')  
print('world')  # helloworld 
```

write结尾没有换行，而print()是自动换行的。

**print** 用 sys.stdin.readline()   实现。
```
import sys
a = sys.stdin.readline()  # hello
print(a, len(a))    # hello 6
b = input()         # hello
print(b, len(b))    # hello 5
```

### 三个特殊Python3字符串前缀u、b、r

* 无前缀 & u前缀
 > 字符串默认创建即以Unicode编码存储，可以存储中文。
 > string = 'a'  等效于  string = u'a' Unicode中通常每个字符由2个字节表示

* b前缀 
 > 字符串存储为Ascll码，无法存储中文。

* r 前缀
 > r前缀就相当于三引号，主要解决的是 转义字符，特殊字符 的问题，其中所有字符均视为普通字符。


### 断言方法举例？
    
    assert 语句，在需要确保程序中的某个条件一定为真才能让程序运行的话就非常有用
    
    下面做一些assert用法的语句供参考：
    assert 1==1
    assert 2+2==2*2
    assert len(['my boy',12])<10
    assert range(4)==[0,1,2,3]
    复制代码这里介绍几个常用断言的使用方法，可以一定程度上帮助大家对预期结果进行判断。
    
    assertEqual
    assertNotEqual
    assertTrue
    assertFalse
    assertIsNone
    assertIsNotNone
    
    assertEqual 和 assertNotEqual
    
    assertEqual：如两个值相等，则pass
    assertNotEqual：如两个值不相等，则pass
    
    使用方法:
    assertEqual(first,second,msg)其中first与second进行比较，如果相等则通过；
    msg为失败时打印的信息，选填；
    断言assertNotEqual反着用就可以了。
    assertTrue和assertFalse
    
    assertTrue：判断bool值为True，则pass
    assertFalse：判断bool值为False，则Pass
    
    使用方法:
    assertTrue(expr,msg)其中express输入相应表达式，如果表达式为真，则pass；
    msg选填；
    断言assertFalse如果表达式为假，则pass
    assertIsNone和assertIsNotNone
    
    assertIsNone：不存在，则pass
    assertIsNotNone：存在，则pass
    
    使用方法：
    assertIsNone(obj,msg)检查某个元素是否存在
    
列出python中可变数据类型和不可变数据类型，并简述原理
不可变数据类型：
数值型、字符串型string和元组tuple
不允许变量的值发生变化，如果改变了变量的值，相当于是新建了一个对象，而对于相同的值的对象，在内存中则只有一个对象（一个地址），如下图用id()方法可以打印对象的id.
可变数据类型：
列表list和字典dict
允许变量的值发生变化，即如果对变量进行append、+=等这种操作后，只是改变了变量的值，而不会新建一个对象，变量引用的对象的地址也不会变化。
相同的值在内存中可能会存在不同的对象，即每个对象都有自己的地址，相当于内存中对于同值的对象保存了多份，这里不存在引用计数，是实实在在的对象。

作者：梦想橡皮擦
链接：https://juejin.im/post/6844903838554521608
来源：掘金
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
    
