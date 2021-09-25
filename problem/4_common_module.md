## 四、常用模块

* os模块
* re模块
* pickle 模块
* datetime模块
* time模块
* math模块


### Python 中的 os 模块常见方法？
os 属于 python内置模块，所以细节在官网有详细的说明，本道面试题考察的是基础能力了，所以把你知道的都告诉面试官吧
官网地址 https://docs.python.org/3/library/os.html
os模块包含了很多操作文件和目录的函数

* os.remove() 删除文件 `如果path是一个目录， 抛出 OSError错误`
* os.removedirs(path) 递归地删除目录。` os.removedirs(“a/b/c”) 将首先删除c目录，然后再删除b和a, 如果他们是空的话，则子目录不能成功删除，将抛出 OSError异常`
* os.rmdir(path) 删除目录 path，`要求path必须是个空目录，否则抛出OSError错误`

* os.walk() 生成目录树下的所有文件名

* os.chdir() 改变目录

* os.getcwd() 返回当前工作目录

* os.listdir(path=".") 列举指定目录中的文件名("."表示当前目录，“..”表示上一级目录)

* os.mkdir(path) 创建建单层目录，如果该目录已存在则抛出异常
* os.rename(old,new)将文件old重命名为new

 


### 如何检查字符串中所有的字符都为字母数字？

 * str.isalnum() 所有字符都是数字或者字母
 * str.isalpha() 所有字符都是字母
 * str.isdigit() 所有字符都是数字
 * str.isspace() 所有字符都是空白字符、t、n、r

### 【datetime】在Python中输入某年某月某日，判断这一天是这一年的第几天？(可以用 Python 标准库）

方法一：

```
import datetime

y = int(input('请输入4位数字的年份：'))  # 获取年份
m = int(input('请输入月份：'))  # 获取月份
d = int(input('请输入是哪一天：'))  # 获取“日”

targetDay = datetime.date(y, m, d)  # 将输入的日期格式化成标准的日期
dayCount = targetDay - datetime.date(targetDay.year - 1, 12, 31)  # 减去上一年最后一天
print('%s是%s年的第%s天。' % (targetDay, y, dayCount.days))
 
```

方法二：

```python
import datetime
dtime = input("请输入求天数的日期(20191111)：")
tnum = datetime.datetime.strptime(dtime,'%Y%m%d').strftime("%j")
print(dtime + "在一年中的天数是: " + tnum + "天。")
```

### 【string】 字符串的拼接–如何高效的拼接两个字符串？

字符串拼接的几种方法


* 加号 `print('Python' + 'Plus')`
* 逗号 `print("Hello", "Python")`
*直接连接 `print("Hello" "Python")`
*格式化    `print('%s %s'%('Python', 'PLUS'))`
*join   `print(['Python', 'Plus'].join(str_list))`
*多行字符串拼接（） `sql = ('select *'
                 'from users'
                 'where id=666')`
 
### 什么是pickling和unpickling？
> 为了让用户在平常的编程和测试时保存复杂的数据类型，python提供了标准模块，称为pickle。
 
* 这个模块可以将几乎任何的python对象(甚至是python的代码)，转换为字符串表示，这个过程称为pickling。
* 从存储的字符串中检索原始Python对象的过程称为unpickling。

###  【re】search()和match()的区别？

* match()函数是在string的开始位置匹配，如果不匹配，则返回None;

* search()会扫描整个string查找匹配;

```
import re
print(re.match('hello','helloworld').span())  # 开头匹配到 (0, 5)
print(re.match('hello','nicehelloworld').span()) # 开头没有匹配到  NoneType
print(re.search('a','abc')) # Match object; span=(0, 1)
print(re.search('a','bac').span()) # (1, 2)
```

###  【random】search()和match()的区别？

```python

import random
random.randint(1,10) # 生成随机整数
random.random() # 0-1 随机小数
``` 

**利用 np.random**

```python
import numpy as np
np.random.randn(5)  生成5个随机小数
```

