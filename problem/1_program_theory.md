## 一、编程理论

### 1. 简述解释型和编译型编程语言
> python 是一门解释型语言

**解释型语言**编写的程序不需要编译，在执行的时候，专门有一个解释器能够将VB语言翻译成机器语言，每个语句都是执行的时候才翻译。
这样解释型语言每执行一次就要翻译一次，效率比较低。

**编译型语言**写的程序执行之前，需要一个专门的编译过程，通过编译系统，把源高级程序编译成为机器语言文件，翻译只做了一次，运行时不需要翻译，所以编译型语言的程序执行效率高，但也不能一概而论，

部分解释型语言的解释器通过在运行时动态优化代码，甚至能够使解释型语言的性能超过编译型语言

### 2. Python解释器种类以及特点？

* Cpython

当从Python官方网站下载并安装好Python2.7后，就直接获得了一个官方版本的解释器：Cpython，这个解释器是用C语言开发的，所以叫 CPython，在命名行下运行python，就是启动CPython解释器，CPython是使用最广的Python解释器。

* IPython

IPython是基于CPython之上的一个交互式解释器，也就是说，IPython只是在交互方式上有所增强，但是执行Python代码的功能和CPython是完全一样的，好比很多国产浏览器虽然外观不同，但内核其实是调用了IE。

* PyPy

PyPy是另一个Python解释器，它的目标是执行速度，PyPy采用JIT技术，对Python代码进行动态编译，所以可以显著提高Python代码的执行速度。

* Jython
 > Jython是运行在Java平台上的Python解释器，可以直接把Python代码编译成Java字节码执行。

* IronPython
> IronPython和Jython类似，只不过IronPython是运行在微软.Net平台上的Python解释器，可以直接把Python代码编译成.Net的字节码。

在Python的解释器中，使用广泛的是CPython，对于Python的编译，除了可以采用以上解释器进行编译外，技术高超的开发者还可以按照自己的需求自行编写Python解释器来执行Python代码

### 3. 位和字节的关系？

* bit就是位，也叫比特位，是计算机表示数据最小的单位
* byte就是字节  (字节就是Byte，也是B)

1byte = 8bit 1byte就是1B 

转换关系如下：

1KB=1024B   1B= 8b

### 4. 字节码和机器码的区别？

* 机器码(machine code)
> 机器码(machine code)，学名机器语言指令，有时也被称为原生码（Native Code），是电脑的CPU可直接解读的数据。
(机器码就是计算机可以直接执行，并且执行速度最快的代码。)

用机器语言编写程序，编程人员要首先熟记所用计算机的全部指令代码和代码的涵义。
手编程序时，程序员得自己处理每条指令和每一数据的存储分配和输入输出，还得记住编程过程中每步所使用的工作单元处在何种状态。
这是一件十分繁琐的工作，编写程序花费的时间往往是实际运行时间的几十倍或几百倍。
而且，编出的程序全是些0和1的指令代码，直观性差，还容易出错。
现在，除了计算机生产厂家的专业人员外，绝大多数的程序员已经不再去学习机器语言了。

机器语言是微处理器理解和使用的，用于控制它的操作二进制代码。
8086到Pentium的机器语言指令长度可以从1字节到13字节。
尽管机器语言好像是很复杂的，然而它是有规律的。
存在着多至100000种机器语言的指令。这意味着不能把这些种类全部列出来。

> 总结：机器码是电脑CPU直接读取运行的机器指令，运行速度最快，但是非常晦涩难懂，也比较难编写，一般从业人员接触不到。

*  字节码（Bytecode）
字节码（Bytecode）是一种包含执行程序、由一序列 op 代码/数据对 组成的二进制文件。字节码是一种中间码，它比机器码更抽象，需要直译器转译后才能成为机器码的中间代码。
通常情况下它是已经经过编译，但与特定机器码无关。字节码通常不像源码一样可以让人阅读，而是编码后的数值常量、引用、指令等构成的序列。
字节码主要为了实现特定软件运行和软件环境、与硬件环境无关。字节码的实现方式是通过编译器和虚拟机器。编译器将源码编译成字节码，特定平台上的虚拟机器将字节码转译为可以直接执行的指令。字节码的典型应用为Java bytecode。
字节码在运行时通过JVM（JAVA虚拟机）做一次转换生成机器指令，因此能够更好的跨平台运行。

> 总结：字节码是一种中间状态（中间码）的二进制代码（文件）。需要直译器转译后才能成为机器码。


### Python的不足之处

Python有以下缺陷：

 * Python的可解释特征会拖累其运行速度。
 * 虽然Python在很多方面都性能良好，但在移动计算和浏览器方面表现不够好。
 * 由于是动态语言，Python使用鸭子类型，即duck-typing，这会增加运行时错误。