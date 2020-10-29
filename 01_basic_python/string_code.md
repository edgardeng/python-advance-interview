## 字符串和编码


## 字符编码

我们已经讲过了，字符串也是一种数据类型，但是，字符串比较特殊的是还有一个编码问题

最早的计算机在设计时采用8个比特（bit）作为一个字节（byte），所以，一个字节能表示的最大的整数就是255（二进制11111111=十进制255），

如果要表示更大的整数，就必须用更多的字节。比如两个字节可以表示的最大整数是65535，

4个字节可以表示的最大整数是4294967295。

**ASCII编码**:  最早只有127个字符被编码到计算机里，也就是大小写英文字母、数字和一些符号

要处理中文显然一个字节是不够的，至少需要两个字节，而且还不能和ASCII编码冲突，所以，中国制定了GB2312编码，用来把中文编进去。

Unicode把所有语言都统一到一套编码里
最常用的是UCS-16编码，用两个字节表示一个字符（如果要用到非常偏僻的字符，就需要4个字节

UTF-8编码把一个Unicode字符根据不同的数字大小编码成1-6个字节，常用的英文字母被编码成1个字节，汉字通常是3个字节，只有很生僻的字符才会被编码成4-6个字节

|字符	|ASCII|	Unicode	|UTF-8|
|:-----|:-----|:-----|:-----|
|A	|01000001	|00000000 01000001|	01000001|
|中	|x	|01001110 00101101|	11100100 10111000 10101101|

## Python的字符串

 * python 2.x默认的字符编码是ASCII，默认的文件编码也是ASCII
    > 如果.py文件本身使用UTF-8编码，并且也申明了# -*- coding: utf-8 -*-，
 * python 3.x默认的字符编码是unicode，默认的文件编码是utf-8
 

单字符的编码
 * ord()函数获取字符的整数表示 `ord('A')  # 65`
 * chr()函数把编码转换为对应的字符：`chr(66)  # 'B'`

如果知道字符的整数编码，还可以用十六进制这么写str： ` a = '\u4e2d\u6587'` 等价于` a= '中文' `

由于Python的字符串类型是str，在内存中以Unicode表示，一个字符对应若干个字节。
如果要在网络上传输，或者保存到磁盘上，就需要把str变为以字节为单位的bytes

bytes类型的数据: `x = b'ABC'`

* str通过encode()方法可以编码为指定的bytes: `x = 'ABC'.encode('ascii')` 或 ` '中文'.encode('utf-8') `
* bytes通过decode转str： `b'\xe4\xb8\xad\xff'.decode('utf-8', errors='ignore')`
* 通过bytes： `x = bytes('ABC', encoding = 'ascii')`

> 含有中文的str无法用ASCII编码，因为中文编码的范围超过了ASCII编码的范围，Python会报错 

关于len函数

* ` len('ABC')` 输出 3
* ` len('中文')` 输出 2
*  `len(b'ABC')`输出 3
*  `len('中文'.encode('utf-8'))`输出 6

> len()函数计算的是str的字符数，如果换成bytes，len()函数就计算字节数

### 格式化

在Python中，采用的格式化方式和C语言是一致的，用%实现，举例如下： ` 'Hello, %s' % 'world' `

  |占位符	 |替换内容 |
  |:-----|:-----|
  |%d	 |整数 |
  |%f	 |浮点数 |
  |%s	 |字符串 |
  |%x	 |十六进制整数 |

你不太确定应该用什么，%s永远起作用 ` 'Age: %s. Gender: %s' % (25, True) `

%是一个普通字符怎么办？这个时候就需要转义   'growth rate: %d %%' % 7

#### format()方法

使用占位符{0}、{1}： ` 'Hello, {0}, 成绩提升了 {1:.1f}%'.format('小明', 17.125) `

#### f-string
> 是Python3.6新引入的一种字符串格式化方法. 格式化字符串常量（formatted string literals）
使用以f开头的字符串，称之为f-string

```python
 r = 2.5
 s = 3.14 * r ** 2
 print(f'The area of a circle with radius {r} is {s:.2f}')

fruits = {"apple":"red","banana":"yellow"}
s = F"The apple is {fruits['apple']},the banana is {fruits['banana']}"	
# f-string内的引号和整体的外部引号不能一致，否则会解析错误
print(s)
# 输出：The apple is red,the banana is yellow

s = "I love U"
print(f"the reverse is '{s[::-1]}'")
# 输出：the reverse is 'U evol I'
# 逆置还可以："".join(reversed(s))

```

> {r}被变量r的值替换，{s:.2f}被变量s的值替换，并且:后面的.2f指定了格式化参数

