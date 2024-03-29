## 面试问题
 
### 一 、with语句的原理
* 上下文管理协议（Context Management Protocol）：包含方法 __enter__()和__exit__()，支持该协议的对象要实现这两个方法。
* 上下文管理器（Context Manager）：支持上下文管理协议的对象，这种对象实现了__enter__()和__exit__()方法。上下文管理器定义执行with语句时要建立的运行时上下文，负责执行with语句块上下文中的进入与退出操作。也可以通过直接调用其方法来使用。

` with EXPR as VAR:  { BLOCK }`  

其中EXPR可以是任意表达式；as VAR是可选的。其一般的执行过程是这样的：

1. 执行EXPR，生成上下文管理器context_manager；
2. 获取上下文管理器的__exit()__方法，并保存起来用于之后的调用；
3. 调用上下文管理器的__enter__()方法；如果使用了as子句，则将__enter__()方法的返回值赋值给as子句中的VAR；
4. 执行BLOCK中的表达式；
5. 不管是否执行过程中是否发生了异常，执行上下文管理器的__exit__()方法，__exit__()方法负责执行“清理”工作，如释放资源等。
   > 如果执行过程中没有出现异常，或者语句体中执行了语句break/continue/return，则以None作为参数调用__exit__(None, None, None)；
   > 如果执行过程中出现异常，则使用sys.exc_info得到的异常信息为参数调用__exit__(exc_type, exc_value, exc_traceback)；
   > 出现异常时，如果__exit__(type, value, traceback)返回False，则会重新抛出异常，让with之外的语句逻辑来处理异常，这也是通用做法；如果返回True，则忽略异常，不再对异常进行处理。

### 二、魔法函数

#### init和new的区别

####

### 三、Python基础

* **python的默认编码？**
 
  python 2.x默认的字符编码是ASCII，默认的文件编码也是ASCII。
  
  python 3.x默认的字符编码是unicode，默认的文件编码是utf-8。
    
* **python中的bytes**
  > bytes 是 Python 3.x 新增的类型，在 Python 2.x 中是不存在的。
  
  字节串（bytes）和字符串（string）的对比：
  * 字符串由若干个字符组成，以字符为单位进行操作；字节串由若干个字节组成，以字节为单位进行操作。
  * 字节串和字符串除了操作的数据单元不同之外，它们支持的所有方法都基本相同。
  * 字节串和字符串都是不可变序列，不能随意增加和删除数据
  
  bytes 类型的数据非常适合在互联网上传输，可以用于网络通信编程；bytes 也可以用来存储图片、音频、视频等二进制格式的文件。

  str和bytes的转换？
  
* **open函数返回什么类型，read返回什么类型**
    
    和文件打开模式有关
       * 普通打开 `file = open (file, mode='r')` 返回 TextIOWrapper对象
           `data = file.read() ` 返回str 字符串
       * 二进制打开  `file = open (file, mode='rb')` 返回 _io.BufferedRandom 对象
                           `data = file.read() ` 返回bytes 字节
    
* **python中的下划线?**

    * 单前导下划线：_var
        > 以单个下划线开头的变量或方法仅供内部使用,类似私有变量/方法。 该约定在PEP 8中有定义 （但并不阻止我们“进入”类并访问该变量的）
        
    * 单末尾下划线：var_
        > 单个末尾下划线（后缀）是一个约定，用来避免与Python关键字产生命名冲突(比如class_)。 PEP 8解释了这个约定
    * 双前导下划线：__var
        > 名称修饰（name mangling）: 双下划线前缀会导致Python解释器重写属性名称，以避免子类中的命名冲突。
          解释器更改变量的名称，以便在类被扩展的时候不容易产生冲突
          `class Test: __baz = 23 ` 类中是没有__baz 但存在_Test__baz
    * 双前导和末尾下划线：__var__
        > 如果一个名字同时以双下划线开始和结束，则不会应用名称修饰。 由双下划线前缀和后缀包围的变量不会被Python解释器修改
        > Python保留了有双前导和双末尾下划线的名称，用于特殊用途。 这样的例子有，__init__对象构造函数，或__call__ 使得一个对象可以被调用。通常被称为魔法方法
    * 单下划线：_
        >  单下划线 _ 是用作一个名字，来表示某个变量是临时的或无关紧要的

* **类()加不加object的区别**
    >  定义一个类时，不加object，称为经典类，加了object，称为新式类
    > 注意，python3.6后，在功能上已经没有经典类和新式类的区分。都是广度优先原则

**类变量与示例变量**


 
**字典中键值的修改**

**list，set,dict在in下的时间复杂度**

**协程，多线程，进程。协程是单线程为什么可以并发**

协程不可以使用异步？

**一条查询语句变慢的原因**

 * 针对偶尔很慢的情况:
    1. 数据库在刷新脏页(我也无奈啊)
        > 当我们要往数据库插入一条数据、或者要更新一条数据的时候，数据库会在内存中把对应字段的数据更新了，但是更新之后，这些更新的字段并不会马上同步持久化到磁盘中去，而是把这些更新的记录写入到 redo log 日记中去，等到空闲的时候，在通过 redo log 里的日记把最新的数据同步到磁盘中去。
        > 不过，redo log 里的容量是有限的，如果数据库一直很忙，更新又很频繁，这个时候 redo log 很快就会被写满了，这个时候就没办法等到空闲的时候再把数据同步到磁盘的，只能暂停其他操作，全身心来把数据同步到磁盘中去的，而这个时候，就会导致我们平时正常的SQL语句突然执行的很慢，所以说，数据库在在同步数据到磁盘的时候，就有可能导致我们的SQL语句执行的很慢了。
 
    2. 拿不到锁(我能怎么办)
        > 我们要执行的这条语句，刚好这条语句涉及到的表，别人在用，并且加锁了，我们拿不到锁，只能慢慢等待别人释放锁了。
        > 或者，表没有加锁，但要使用到的某个一行被加锁了，这个时候，我也没办法啊。
        > 如果要判断是否真的在等待锁，我们可以用 show processlist这个命令来查看当前的状态哦
 
 * 一直执行的很慢，则有如下原因。
    
    1. 没有用上索引：例如该字段没有索引；由于对字段进行运算、函数操作导致无法用索引。
    
    2. 数据库选错了索引  
 
    
