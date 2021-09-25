# Python 高阶学习

## 函数

函数的嵌套

嵌套


## 内存管理

### 引用计数
在python中，任何对象都会放在一个环形双向链表中 refChain
每种类型的对象都有一个ob_refcnt引用计数的值，引用个数+1，-1
当引用计数变成0时，会进行垃圾回收（对象销毁，在refchain中移除）

python 里面每个东西都是对象，核心就是个结构体 PyObject
多个元素组成的对象， PyVarObject

```c
typedef struct_object {
    int ob_refcnt
    struct typeobject * ob_type;
    
} PyObject
```
PyObject 是每个对象必有的内容 
* ob_refcnt 为引用计数 `sys.get_conf`

当一个对象有新的引用时，ob_refcnt会增加，引用的对象被删除时，ob_refcnt减少

引用计数的优点：`

常用的函数：
    * gc.get_count()        当前自动执行垃圾回收的计数器
    * gc.get_threshold      垃圾回收频率
    * gc.set_threshold()    设置频率
    * gc.disable()          关闭垃圾回收
    * gc.collect            手动回收

#### 循环引用

### 标记清除
> 在python的底层，维护一个链表，链表中专门放一些可能存在循环引用的对象（如 List，tuple， dict, set ）
在python内部，某种情况下触发，去扫描可能存在循环引用的对象，检查是否循环引用。如果有则让双方的引用计数-1

### 分代回收

将可能存在循环引用的对象维护成3个链表：
    0 代， 0代对象个数达到700个扫描1次
    1 代， 0代扫描10次，则1次扫描一次
    2 代， 1代扫描10次，则2次扫描一次
    
python在源码内部提出了优化机制
### 缓存

#### 池
  为了避免重复创建和销毁一些常见对象，有个维护池 (int,string)
> 启动解释器是，python内部创建了一个小整数池 [-5,257]  

#### free_list (float,list,tuple,dict)
> 有数量限制
  当一个对象的引用计数器为0，按理应该回收，内部不会直接回收。而是将对象添加到free_list链表中
  以后再创建时，不再重新开辟内存，直接使用free_list

### 源码分析

* float类型


## 异常

异常类
* BaseException
    * KeyBordInterrupt
    * Exception
        * SystaxError 语法错误
        * NameError   访问一个undefined/未申明的变量
        * NumberError 访问一个没有神明
        * ZeroDivisionError 0除错误
        * ValueError   数值错误 ` 1 + 'a' `
        * AttributeError 属性不存在 
        * IndexError  索引错误
        * KeyError   字典关键字不存在
    * SystemExit
    * GeneratorExit
    
## 正则表达式 regular expression

> 正则表达式是对字符串操作的一种逻辑公式。用实现定义好的一些特定字符、及这些特定字符的组合,组成一个规则字符串，对字符串的一种过滤逻辑(检索,截取,替换)

python中通过标准库中的 re 模块 支持正则表达式

### re 模块

#### match 方法
> 字符串的起始位置匹配一个模式。 如果不是其实位置匹配成功的话，返回none

 `re.match(pattern , string, flags=0)` 返回匹配对象
 
 * 调用结果的group方法获取匹配成功的字符串
 * span方法获取匹配的范围
 
 
flags 正则表达式修饰符 - 可选标志

re.I    匹配对大小写不敏感
re.L    做本地化识别locale-aware匹配
re.M    多行匹配 影响 ^ 和 $ 
re.S    使 . 匹配包括换行在内的所有字符
re.U    根据Unicode字符集解析字符。这个标志影响 \w \W \b  \B
re.X    该标志通过给予更灵活的格式，以便将正则表达式写得更易于理解

正则表达式常用的字符

.       匹配任意一个字符（除了\n）
[]      匹配列表中的字符
\w      匹配字母、数字、下划线 （即 a-z，A-Z、0-9，_）
\w      匹配不是字母、数字、下划线
\s      空白字符 \n \t
\S      匹配不是空白字符
\d      匹配数字 0-9
\D      匹配不是数字


表示数量 （匹配多个字符）

常用的限定符号

|符号|描述|
|:----|:----|
|* |匹配零次或多次|
|+ |匹配一次或多次|
|？ |匹配一次或零次|
|{m} |重复m次|
|{m,n}|重复m到n次，其中n可以省略，表示m到任意次
 |{m，} |至少m次| 


原生字符串

正则表达式使用 `\`作为转义字符，可以造成反斜杠困扰

使用 r 原生字符串

边界字符

^   匹配字符串开头
$   匹配字符串结尾
\b  匹配一个单词的边界
\B  匹配非单词的边界


#### search 方法
> 在一个字符串中搜索满足文本模式的字符串

 `re.search(pattern , string, flags=0)` 返回匹配的字符串

search 和 search的区别

* match 从开始匹配。 search 不是

匹配多个字符串

匹配符号 `| `

分组

如果一个模式字符串中用一对圆括号括起来的部分，成为一组

（ab）        将括号中的字符作为一个分组
\num        引用分组num匹配到的字符串 \1 表示第一个分组匹配到的字符串
(?P<name>)  分别起组名
(?P=name)   引用别名为name分组匹配到的字符串

#### sub / subn

实现搜索和替换功能。 将某个字符串所有匹配正则表达式的部分替换成其他字符串
sub函数返回替换后的结果
subn返回一个元组。 （替换后的结果，替换后的总数）

`re.sub(pattern, repl, string, count=0, flags=0)`

* pattern 正则表达式
* repl 替换的字符串
* string 查找的字符串
* count 匹配后替换的最大次数。0表示替换所有的匹配

#### compile
> 用于编译正则表达式， 生成一个正则表达式 pattern对象，供match和search使用
    `re.compile(pattern, flags)` 

#### findall
> 在字符串中找到正则表达式所匹配的所有字串，并返回一个列表如果没有找到则返回空列表

    `re.findall(pattern,string, flags)` 

#### split 函数 
> 根据正则表达式分隔字串
    
    `re.split(pattern,string, maxplit=0,flags=0)


## IO 文件操作

* open 函数用于创建文件对象， 基本的打开方式
    * r  read读模式
    * w  write写模式，不存在则创建
    * a  append加模式
    * b  二进制模式
    * `*`  读写模式

10 Python 函数式编程 BV18E411F7YA

11 Python 正则 BV1N64y1u7Ty

内存管理

## 常用的模块

  builtins 内建函数模块 （默认加载）
  os
  sys
  functools
  json
  logging
  time
  datetime
  calendar
  multiprocessing
  threading
  copy              复制
  hashlib           加密
  re                正则
  socket        
  
## 扩展

 request
 urllib
 scrapy
 beautifulsoup4
 celery
 redis
 pillow
 xlswriter
 xlwt
 xlrd
 elasticsearch
 pymysql
    
python -m heep_server 8888 打开服务器
