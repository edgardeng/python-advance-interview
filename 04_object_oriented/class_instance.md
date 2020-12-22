## 类和实例

* 类是抽象的模板，比如Student类，
* 实例是根据类创建出来的一个个具体的“对象”，每个对象都拥有相同的方法，但各自的数据可能不同。

```python
class Student(object):
    def __init__(self, name, score):
        self.name = name
        self.score = score
    def print_score(self):
        print('%s: %s' % (self.name, self.score))
bart = Student() # <__main__.Student object at 0x10a67a590>
Student         # <class '__main__.Student'>
bart.gender = 'girl' # 自由地给一个实例变量绑定属性

```

1. 在Python中，定义类是通过class关键字：
    
2. class后面紧接着是类名，即Student，类名通常是大写开头的单词

3. 紧接着是(object)，表示该类是从哪个类继承下来的

4. 定义好了Student类，就可以根据Student类创建出Student的实例，创建实例是通过类名+()实现的

变量bart指向的就是一个Student的实例，后面的`0x10a67a590`是内存地址，每个object的地址都不一样，

### `_init__`方法
> 通过定义一个特殊的__init__方法，在创建实例的时候，就把name，score等属性绑上去：

注意到`__init__`方法的第一个参数永远是self，表示创建的实例本身

因此，在`__init__`方法内部，就可以把各种属性绑定到self，因为self就指向创建的实例本身。

有了__init__方法，在创建实例的时候，就不能传入空的参数了，必须传入与__init__方法匹配的参数，但self不需要传，Python解释器自己会把实例变量传进去： `bart = Student('Bart Simpson', 59)`

和普通的函数相比，在类中定义的函数只有一点不同，就是第一个参数永远是实例变量self，并且，调用时，不用传递该参数。

除此之外，类的方法和普通函数没有什么区别，所以，你仍然可以用默认参数、可变参数、关键字参数和命名关键字参数。

### 数据封装

面向对象编程的一个重要特点就是数据封装。

封装数据的函数是和Student类本身是关联起来的，我们称之为类的方法:  

`def print_score(self): `
 
### 访问限制 - 私有属性和方法

如果要让内部属性不被外部访问，可以把属性的名称前加上两个下划线`__`

在Python中，实例的变量名如果以`__`开头，就变成了一个私有变量（private），只有内部可以访问，外部不能访问

```python
class Student(object):

    def __init__(self, name, score):
        self.__name = name
        self.__score = score

    def print_score(self):
        print('%s: %s' % (self.__name, self.__score))

bart = Student('Simpson', 59)
bart.__name  # AttributeError: 'Student' object has no attribute '__name'
bart._Student__name # 'Simpson'
bart.__name = 'New Name' # 设置__name变量
print(bart.__name) # 'New Name'
```

外部代码 '成功'地设置了__name变量，但实际上这个__name变量和class内部的__name变量不是一个变量

> 需要注意的是，在Python中，变量名类似__xxx__的，也就是以双下划线开头，并且以双下划线结尾的，是特殊变量，特殊变量是可以直接访问的，不是private变量，所以，不能用__name__、__score__这样的变量名。

> 不能直接访问__name是因为Python解释器对外把__name变量改成了_Student__name，所以，仍然可以通过_Student__name来访问__name变量：

|模式|举例|含义|
|:----|:----|:----|
|单前导下划线| _var|命名约定，仅供内部约定，不用由python解释器强制执行|
|单末尾下划线|var_|避免Python关键字冲突比如：class_|
|双前导下划线|__var|私有属性方法，在类上下文使用时，触发名称修饰。python解释器强制执行|
|双前导末尾下划线|\__var__|表示python定义的特殊方法，避免自己定义|
|单下划线|_|临时变量或没有意义的名称。在python REPL最近的一个表达式的结果|




https://www.cnblogs.com/lyq-biu/p/10310174.html

